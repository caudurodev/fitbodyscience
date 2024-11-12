"""Functions to extract the main text of a scientific study from its URL using Oxylabs API."""

import re
import json
import requests
from bs4 import BeautifulSoup, Comment

from newspaper import Article
from newspaper.article import ArticleException
from ..utils.config import logger, settings

# from ..utils.save_file import save_to_file

OXYLABS_API_URL = "https://realtime.oxylabs.io/v1/queries"


def get_website_main_text(url):
    """Get the main text of a scientific study from its URL using Oxylabs API"""
    api_url = "https://realtime.oxylabs.io/v1/queries"
    payload = {
        "source": "universal",
        "url": url,
        "geo_location": "United States",
        "render": "html",
    }
    headers = {"Content-Type": "application/json"}
    auth = ("deconstruct_n3Z5d", settings.OXYLABS_PASS)

    try:
        # logger.info("Fetching article from Oxylabs API: %s", url)
        response = requests.post(
            api_url, json=payload, headers=headers, auth=auth, timeout=120
        )
        # #logger.info("response: %s", response)
        response.raise_for_status()
        oxylabs_response = response.json()

        # Extract the main content from the response
        html_content = oxylabs_response.get("results", [{}])[0].get("content", "")
        # save_to_file(html_content, "html_content.txt")

        if not html_content:
            raise ValueError("No content found in Oxylabs response")

        # dois = extract_dois(html_content)
        # #logger.info("dois1: %s", dois)
        # save_to_file(dois, "dois.txt")
        # visible_html = extract_visible_html(html_content)
        # save_to_file(visible_html, "visible_html.txt")

        visible_text = get_visible_text(html_content)
        # save_to_file(visible_text, "visible_text.txt")

        dois2 = extract_dois(visible_text)
        # logger.info("----dois: %s", dois2)

    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch article via Oxylabs API: %s", e)
        return None, None
    except ValueError as e:
        logger.error("Error processing Oxylabs response: %s", e)
        return None, None

    article = Article(url)
    article.set_html(html_content)
    try:
        article.parse()
    except ArticleException as e:
        logger.error("Failed to parse article: %s", e)
        return None, None

    title = article.title
    # logger.info("title: %s", title)
    authors = article.authors
    # logger.info("authors: %s", authors)
    publish_date = article.publish_date
    # logger.info("publish_date: %s", publish_date)
    # text = article.text
    # #logger.info("text: %s", text)

    # text = fulltext(html_content)
    # #logger.info("html_content fulltext: %s", text)
    full_text = f"""
        DOI: {json.dumps(dois2)}
        title: {title}
        authors: {authors}
        publish_date: {publish_date}

        {article.text}
    """
    # full_html = article.html
    # #logger.info("full_text: %s", full_text)

    # save_to_file(full_text, "full_text.txt")
    return full_text


def extract_dois(html_content):
    """Extract all DOI numbers or links from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Regex pattern to match DOI links and numbers
    doi_pattern = re.compile(r"\b10.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)

    # Find all links and text that match the DOI pattern
    doi_links = set()

    # Search for DOIs in anchor tags
    for a in soup.find_all("a", href=True):
        if "doi.org" in a["href"]:
            doi_links.add(a["href"])
        elif doi_pattern.search(a["href"]):
            doi_links.add(a["href"])

    # Search for DOIs in the text
    for text in soup.stripped_strings:
        match = doi_pattern.search(text)
        if match:
            doi_links.add(match.group(0))

    return list(doi_links)


def extract_visible_html(html_content):
    """Extracts the visible HTML content, ignoring JavaScript, CSS, and comments."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove all script, style, and comments
    for element in soup(["script", "style"]):
        element.decompose()

    # Remove comments
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Return the cleaned HTML
    visible_html = soup.prettify()
    return visible_html


def get_visible_text(html_content):
    """Extracts all visible text from HTML content, ignoring JavaScript, CSS, and comments."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove all script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    # Remove comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Extract all visible text
    visible_text = soup.get_text(separator=" ", strip=True)
    return visible_text
