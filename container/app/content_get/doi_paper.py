"""Functions to fetch paper metadata from DOI using Crossref API"""

# import os
import re
import base64
import requests
import fitz
from ..utils.config import logger, settings
from ..content_store.science_paper import (
    update_science_paper_crossref_content,
    update_science_paper_direct_download_content,
    update_science_paper_content,
)
from ..vendors.web_scraping import download_website


CROSSREF_API_URL = "https://api.crossref.org/works/"

# OXYLABS
USERNAME = "deconstruct_n3Z5d"
PASSWORD = settings.OXYLABS_PASS
OXYLABS_API_URL = f"http://{USERNAME}:{PASSWORD}@realtime.oxylabs.io/v1/queries"

# UNPAYWALL
UNPAYWALL_API_URL = "https://api.unpaywall.org/v2/"
EMAIL = "rod@cauduro.dev"


def get_paper_main(content_doi_number, content_url):
    """Get the main content of a paper from a DOI number and URL"""

    # TODO: if no DOI, open website to try and extract it

    if content_doi_number is None:
        logger.error("get_paper_main No DOI number provided")
        return None

    doi_pattern = r"^10\.\d{4,}/[-._;()/:\w]+$"
    if not re.match(doi_pattern, content_doi_number):
        logger.info(f"Invalid DOI format: {content_doi_number}")
        return None

    try:
        # logger.info("Getting Crossref data for DOI: %s", content_doi_number)
        # TODO check if crossref data already exists
        cross_ref_info = get_crossref_data_from_doi(content_doi_number)
        if cross_ref_info is None:
            logger.error("Error getting Crossref data")
        else:
            update_science_paper_crossref_content(
                source_url=content_url, crossref_jsonb=cross_ref_info
            )
    except Exception as e:
        logger.error("Error getting Crossref data: %s", e)

    try:
        unpaywall_link = get_unpaywall_download_link(content_doi_number)
        # logger.info("unpaywall_link: %s", unpaywall_link)
        if is_url(unpaywall_link) is not None:
            try:
                update_science_paper_direct_download_content(
                    source_url=content_url, direct_download_url=unpaywall_link
                )
            except Exception as e:
                logger.error("Error updating direct download content: %s", e)
                return None

            try:
                full_text = download_pdf_extract_full_text(
                    unpaywall_link, f'{content_doi_number.replace("/", "_")}.pdf'
                )

                if full_text is not None:
                    # #logger.info("full_text from pdf: %s", full_text)
                    try:
                        update_science_paper_content(
                            source_url=content_url, full_text=full_text
                        )
                        return True
                    except Exception as e:
                        logger.error("Error updating science paper content: %s", e)
                else:
                    logger.error("Error extracting text from PDF")
            except Exception as e:
                logger.error("Error downloading PDF: %s", e)
        else:
            logger.error("No unpaywall link , trying to get website full text...")
    except Exception as e:
        logger.error("Error downloading PDF: %s", e)

    # TODO: alternative download methods
    # logger.info("All failed , trying to get website full text...")
    text = download_website(url_to_scrape=content_url, return_format="text")
    if text is not None:
        try:
            update_science_paper_content(source_url=content_url, full_text=text)
            return True
        except Exception as e:
            logger.error("Error updating science paper content: %s", e)
    logger.error("Error getting paper main content, all failed")
    return None


def get_crossref_data_from_doi(doi):
    """Get paper metadata from DOI using Crossref API"""
    if not doi:
        logger.error("No DOI provided")
        return None

    try:
        response = requests.get(f"{CROSSREF_API_URL}{doi}", timeout=10)
        response.raise_for_status()
        data = response.json()
        # #logger.info("Crossref API response: %s", data)
        if data.get("status") != "ok":
            logger.error("Crossref API error: %s", data)
            return None
        return data
        # parsed_data = parse_crossref_response(data["message"])

        # #logger.info("title: %s", parsed_data.get("title"))
        # #logger.info("abstract: %s", parsed_data.get("abstract"))
        # #logger.info("study type: %s", parsed_data.get("type"))

        # return parsed_data
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch paper metadata via Crossref API: %s", e)
        return None


def extract_text_from_pdf(filename: str):
    """Extract all text content from a PDF file"""
    try:
        document = fitz.open(filename)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        # #logger.info("Extracted text from PDF: %s", text)
        return text
    except Exception as e:
        logger.error("Failed to extract text from PDF: %s", e)
        return None


def parse_crossref_response(response):
    """Parse the Crossref API response into a structured format"""
    paper_metadata = {
        "status": response.get("status"),
        "message_type": response.get("message-type"),
        "message_version": response.get("message-version"),
        "doi": response.get("DOI"),
        "title": response.get("title", [None])[0],
        "authors": [
            {
                "given": author.get("given"),
                "family": author.get("family"),
                "affiliation": [
                    aff.get("name") for aff in author.get("affiliation", [])
                ],
            }
            for author in response.get("author", [])
        ],
        "journal": response.get("container-title", [None])[0],
        "publisher": response.get("publisher"),
        "published_date": response.get("published-print", {}).get(
            "date-parts", [[None]]
        )[0],
        "reference_count": response.get("reference-count"),
        "license": [
            {
                "url": lic.get("URL"),
                "start_date": lic.get("start", {}).get("date-parts", [[None]])[0],
                "content_version": lic.get("content-version"),
                "delay_in_days": lic.get("delay-in-days"),
            }
            for lic in response.get("license", [])
        ],
        "content_domain": response.get("content-domain"),
        "short_container_title": response.get("short-container-title", []),
        "published_online": response.get("published-online", {}).get(
            "date-parts", [[None]]
        )[0],
        "type": response.get("type"),
        "created_date": response.get("created", {}).get("date-parts", [[None]])[0],
        "source": response.get("source"),
        "is_referenced_by_count": response.get("is-referenced-by-count"),
        "prefix": response.get("prefix"),
        "volume": response.get("volume"),
        "issue": response.get("issue"),
        "page": response.get("page"),
        "link": response.get("link", []),
        "deposited": response.get("deposited", {}).get("date-parts", [[None]])[0],
        "score": response.get("score"),
        "resource": response.get("resource"),
        "subtitle": response.get("subtitle", []),
        "short_title": response.get("short-title", []),
        "issued": response.get("issued", {}).get("date-parts", [[None]])[0],
        "references_count": response.get("references-count"),
        "journal_issue": response.get("journal-issue"),
        "alternative_id": response.get("alternative-id", []),
        "url": response.get("URL"),
        "relation": response.get("relation", {}),
        "issn": response.get("ISSN", []),
        "issn_type": response.get("issn-type", []),
        "subject": response.get("subject", []),
        "published": response.get("published", {}).get("date-parts", [[None]])[0],
        "abstract": response.get("abstract"),
    }

    return paper_metadata


def get_unpaywall_download_link(doi):
    """Get the full text link using Unpaywall API"""
    response = requests.get(
        f"{UNPAYWALL_API_URL}{doi}", params={"email": EMAIL}, timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        if data.get("is_oa"):
            return data.get("best_oa_location", {}).get("url_for_pdf")
        else:
            return "No open access version available."
    else:
        return "Failed to retrieve data from Unpaywall."


def dump_to_file(filename: str, data: bytes):
    """Save the content to a file"""
    with open(filename, "wb") as file:
        file.write(data)


def download_pdf_extract_full_text(url: str, filename: str):
    """Download a PDF from a URL and save it to a file"""
    # logger.info("Downloading PDF from URL: %s", url)
    parameters = {
        "source": "universal",
        "url": url,
        "geo_location": "United States",
        "content_encoding": "base64",
    }
    auth = (settings.OXYLABS_USER, settings.OXYLABS_PASS)
    response = requests.post(OXYLABS_API_URL, json=parameters, auth=auth, timeout=120)

    # #logger.info("response: %s", response)
    if response.ok:
        data = response.json()
        # #logger.info("data: %s", data)
        if (
            "results" in data
            and len(data["results"]) > 0
            and "content" in data["results"][0]
        ):
            pdf_base64 = data["results"][0]["content"]
            try:
                # Decode the base64 content
                pdf_bytes = base64.b64decode(pdf_base64)
                dump_to_file(filename, pdf_bytes)
                text = extract_text_from_pdf(filename)
                # uploaded_files = upload_files_to_nhost("default", [filename])

                # if uploaded_files:
                #     print("Files uploaded successfully:", uploaded_files)
                #     # Clean up the local file after uploading
                #     os.remove(filename)
                # else:
                #     print("Failed to upload files to Nhost.")
                print(f"PDF downloaded successfully and saved as {filename}")
                return text
            except Exception as e:
                print(f"Failed to handle PDF content: {e}")
                return None
        else:
            print("No content found in the API response.")
            return None
    else:
        logger.error(
            "Failed to retrieve the PDF. Status code: %s", response.status_code
        )
        return None

    return None


def is_url(string):
    """Regex pattern for URL validation"""
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, string) is not None
