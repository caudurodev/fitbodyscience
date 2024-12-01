"""Functions to fetch paper metadata and content from PubMed using their API"""

import re
import json
import requests
from typing import Optional, Dict, Any
from ..utils.config import logger, settings
from ..content_store.science_paper import (
    update_science_paper_crossref_content,
    update_science_paper_direct_download_content,
    update_science_paper_content,
)
from ..vendors.web_scraping import download_website

# PubMed API endpoints
PUBMED_API_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
PUBMED_SEARCH_URL = f"{PUBMED_API_BASE}esearch.fcgi"
PUBMED_FETCH_URL = f"{PUBMED_API_BASE}efetch.fcgi"
PUBMED_SUMMARY_URL = f"{PUBMED_API_BASE}esummary.fcgi"

# Your API key if you have one (recommended for higher rate limits)
PUBMED_API_KEY = settings.PUBMED_API_KEY if hasattr(settings, 'PUBMED_API_KEY') else None


def get_paper_main(pubmed_id: str, content_url: Optional[str] = None) -> Optional[bool]:
    """Get the main content of a paper from a PubMed ID and URL"""
    
    if not pubmed_id:
        logger.error("get_paper_main: No PubMed ID provided")
        return None

    # Validate PubMed ID format (typically 1-8 digits)
    if not re.match(r'^\d{1,8}$', pubmed_id):
        logger.error(f"Invalid PubMed ID format: {pubmed_id}")
        return None

    try:
        # Get detailed metadata from PubMed
        paper_metadata = get_pubmed_metadata(pubmed_id)
        if paper_metadata:
            update_science_paper_crossref_content(
                source_url=content_url,
                crossref_jsonb=paper_metadata
            )
        else:
            logger.error("Error getting PubMed metadata")
            return None

        # Try to get full text content
        full_text = get_pubmed_full_text(pubmed_id)
        if full_text:
            update_science_paper_content(
                source_url=content_url,
                full_text=full_text
            )
            return True

        # If direct PubMed content retrieval fails, try scraping the URL
        if content_url:
            logger.info("Attempting to get full text from URL...")
            text = download_website(url_to_scrape=content_url, return_format="text")
            if text:
                update_science_paper_content(
                    source_url=content_url,
                    full_text=text
                )
                return True

        logger.error("Failed to retrieve paper content through all available methods")
        return None

    except Exception as e:
        logger.error(f"Error in get_paper_main: {str(e)}")
        return None


def get_pubmed_metadata(pubmed_id: str) -> Optional[Dict[str, Any]]:
    """Fetch and parse metadata for a PubMed article"""
    try:
        params = {
            'db': 'pubmed',
            'id': pubmed_id,
            'retmode': 'json',
            'rettype': 'abstract'
        }
        
        if PUBMED_API_KEY:
            params['api_key'] = PUBMED_API_KEY

        response = requests.get(
            PUBMED_FETCH_URL,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            return parse_pubmed_response(data)
        else:
            logger.error(f"Failed to fetch PubMed metadata. Status code: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Error fetching PubMed metadata: {str(e)}")
        return None


def parse_pubmed_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the PubMed API response into a structured format"""
    try:
        result = {
            'title': '',
            'authors': [],
            'abstract': '',
            'publication_date': '',
            'journal': '',
            'doi': '',
            'pmid': '',
            'keywords': []
        }

        if 'PubmedArticleSet' in response_data:
            article = response_data['PubmedArticleSet']['PubmedArticle'][0]
            article_data = article['MedlineCitation']['Article']
            
            # Extract basic metadata
            result['title'] = article_data.get('ArticleTitle', '')
            result['abstract'] = article_data.get('Abstract', {}).get('AbstractText', [''])[0]
            result['journal'] = article_data.get('Journal', {}).get('Title', '')

            # Extract authors
            if 'AuthorList' in article_data:
                for author in article_data['AuthorList']:
                    if isinstance(author, dict):
                        name_parts = []
                        if 'LastName' in author:
                            name_parts.append(author['LastName'])
                        if 'ForeName' in author:
                            name_parts.append(author['ForeName'])
                        if name_parts:
                            result['authors'].append(' '.join(name_parts))

            # Extract publication date
            pub_date = article_data.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})
            date_parts = []
            for part in ['Year', 'Month', 'Day']:
                if part in pub_date:
                    date_parts.append(pub_date[part])
            result['publication_date'] = '-'.join(date_parts)

            # Extract identifiers
            result['pmid'] = str(article['MedlineCitation']['PMID'])
            
            # Extract DOI if available
            article_ids = article.get('PubmedData', {}).get('ArticleIdList', [])
            for id_item in article_ids:
                if isinstance(id_item, dict) and id_item.get('@IdType') == 'doi':
                    result['doi'] = str(id_item['#text'])

            # Extract keywords
            if 'KeywordList' in article['MedlineCitation']:
                result['keywords'] = [
                    str(keyword) 
                    for keyword in article['MedlineCitation']['KeywordList'][0]
                ]

        return result

    except Exception as e:
        logger.error(f"Error parsing PubMed response: {str(e)}")
        return None


def get_pubmed_full_text(pubmed_id: str) -> Optional[str]:
    """Attempt to retrieve full text content from PubMed Central if available"""
    try:
        # First, check if article is available in PubMed Central
        params = {
            'db': 'pmc',
            'id': pubmed_id,
            'retmode': 'json',
            'rettype': 'full'
        }
        
        if PUBMED_API_KEY:
            params['api_key'] = PUBMED_API_KEY

        response = requests.get(
            PUBMED_FETCH_URL,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            # Extract full text if available
            if 'body' in data:
                return data['body']
            else:
                logger.info(f"Full text not available in PubMed Central for ID: {pubmed_id}")
                return None
        else:
            logger.error(f"Failed to fetch full text. Status code: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Error fetching full text from PubMed: {str(e)}")
        return None
