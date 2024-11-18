"""This module contains the logic for analyzing a scientific paper and saving the data to the database"""

from ..utils.config import logger
from ..content_store.get_content import get_content_by_id
from ..vendors.web_scraping import download_website
from ..content_store.fulltext_store import add_fulltext_to_content


def analyse_website_page(content_id):
    """Analyze a scientific paper and save the data to the database"""

    result = get_content_by_id(content_id)

    if not result:
        logger.error("Error analyse_website_page No content found")
        return None
    if len(result) > 0:
        content = result[0]
    else:
        content = result

    # #logger.info("analyse_science_paper content %s", content)
    canonical_url = content["canonicalUrl"]

    if not canonical_url:
        logger.error("Error analyse_website_page No canonical_url provided")
        return None

    try:
        text = download_website(url_to_scrape=canonical_url, return_format="text")
        if text is None:
            logger.error("Error analyse_website_page No text found")
            return None
        add_fulltext_to_content(content_id, text)
        return True
    except Exception as e:
        logger.error("Error analyse_website_page: %s", e)
        return None
