"""Web scraping utilities"""

import requests
import re
from urllib.parse import quote
from ..config.logging import logger
from ..config.constants import CROSSREF_API_URL


def get_crossref_data_from_doi(doi_number):
    """Get paper metadata from DOI using Crossref API"""
    # Check if DOI follows the expected format (10.XXXX/XXXXX)
    doi_pattern = r"^10\.\d{4,}/[-._;()/:\w]+$"
    if not re.match(doi_pattern, doi_number):
        logger.info(f"Invalid DOI format: {doi_number}")
        return None

    if not doi_number:
        logger.error("No DOI provided")
        return None

    try:
        encoded_doi = quote(doi_number)
        response = requests.get(f"{CROSSREF_API_URL}{encoded_doi}", timeout=20)
        response.raise_for_status()
        data = response.json()
        # logger.info("Crossref API response: %s", data)
        if data.get("status") != "ok":
            logger.info("Crossref API error: %s", data)
            return None
        return data

    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch paper metadata via Crossref API: %s", e)
        return None
