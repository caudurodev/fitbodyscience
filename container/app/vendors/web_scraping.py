"""Web scraping utilities"""

import requests
import time
from requests.exceptions import RequestException

from ..content_get.website_content import get_visible_text
from ..utils.config import settings, logger


def download_website(url_to_scrape, return_format="html"):
    """
    Download website content using multiple vendors with fallback
    """
    errors = []
    vendors = ["oxylabs", "use_scraper", "scrapingbee", "brightdata"]

    for vendor in vendors:
        try:
            logger.info(
                f"Attempting to download content from {url_to_scrape} using {vendor}"
            )
            content = None

            if vendor == "oxylabs":
                content = download_url_with_oxylabs(url_to_scrape, return_format)
            elif vendor == "use_scraper":
                content = get_website_with_use_scraper(url_to_scrape, return_format)
            elif vendor == "scrapingbee":
                content = get_website_with_scrapingbee(url_to_scrape, return_format)
            elif vendor == "brightdata":
                content = get_website_with_brightdata(url_to_scrape, return_format)
            else:
                logger.error(f"Unsupported vendor: {vendor}")
                continue

            if content:
                content_length = len(content) if content else 0
                logger.info(
                    f"Successfully downloaded content using {vendor} (length: {content_length} chars)"
                )
                if content_length > 0:
                    logger.info(f"First 100 chars: {content[:100]}")
                else:
                    logger.warning("Downloaded content is empty")
                    continue

                if return_format == "text":
                    try:
                        text_content = get_visible_text(content)
                        if not text_content:
                            logger.warning(
                                f"Failed to extract visible text with {vendor}"
                            )
                            continue

                        text = text_content.get("content", "")
                        if not text:
                            logger.warning(f"No text content extracted with {vendor}")
                            continue

                        text_length = len(text)
                        logger.info(f"Extracted text length: {text_length} chars")
                        if text_length > 0:
                            logger.info(
                                f"First 100 chars of extracted text: {text[:100]}"
                            )
                            return text_content
                        else:
                            logger.warning(f"Empty text content from {vendor}")
                            continue
                    except Exception as e:
                        logger.error(f"Error extracting text with {vendor}: {str(e)}")
                        continue

                return content
            else:
                logger.warning(f"No content returned from {vendor}")
                errors.append(f"{vendor}: No content returned")

        except Exception as e:
            error_msg = f"Unexpected error with {vendor}: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            continue

    # If we get here, all attempts failed
    logger.error("All download attempts failed:")
    for error in errors:
        logger.error(f"- {error}")
    return None


def download_url_with_oxylabs(
    url_to_scrape, return_format="html", max_retries=3, retry_delay=5
):
    """Extract visible text from HTML content with retry logic

    Args:
        url_to_scrape (str): URL to scrape
        return_format (str): Format to return ('html' or 'text')
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay in seconds between retries
    """
    api_url = "https://realtime.oxylabs.io/v1/queries"
    payload = {
        "source": "universal",
        "url": url_to_scrape,
        "geo_location": "United States",
        "render": "html",
    }
    headers = {"Content-Type": "application/json"}
    auth = (settings.OXYLABS_USER, settings.OXYLABS_PASS)

    for attempt in range(max_retries):
        try:
            logger.info(
                f"Attempt {attempt + 1}/{max_retries} to fetch content from {url_to_scrape}"
            )
            response = requests.post(
                api_url, json=payload, headers=headers, auth=auth, timeout=120
            )
            response.raise_for_status()
            oxylabs_response = response.json()
            downloaded = oxylabs_response.get("results", [{}])[0].get("content", "")

            if downloaded:
                logger.info(f"Successfully downloaded content on attempt {attempt + 1}")
                return downloaded
            else:
                logger.warning(
                    f"Attempt {attempt + 1}: No content found in Oxylabs response"
                )
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    time.sleep(retry_delay)
                continue

        except RequestException as e:
            logger.error(
                f"Attempt {attempt + 1} failed with RequestException: {str(e)}"
            )
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            continue
        except ValueError as e:
            logger.error(f"Attempt {attempt + 1} failed with ValueError: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            continue
        except Exception as e:
            logger.error(
                f"Attempt {attempt + 1} failed with unexpected error: {str(e)}"
            )
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            continue

    logger.error(f"All {max_retries} attempts to download content failed")
    return None


# https://docs.usescraper.com/api-reference/scraper/scrape
def get_website_with_use_scraper(url_to_scrape, return_format="html"):
    """Extract visible text from HTML content"""
    api_url = "https://api.usescraper.com/scraper/scrape"

    payload = {"url": url_to_scrape, "format": return_format}
    headers = {
        "Authorization": f"Bearer {settings.USE_SCRAPER_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        # logger.info("Fetching article from UseScraper API: %s", url_to_scrape)
        response = requests.request(
            "POST", api_url, json=payload, headers=headers, timeout=120
        )
        downloaded = response.json().get(return_format)
        # logger.info("downloaded: %s", downloaded)
        return downloaded
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch article via UseScraper API: %s", e)
        return None


def get_website_with_scrapingbee(url_to_scrape, return_format):
    """Extract visible text from HTML content"""
    try:
        response = requests.get(
            url="https://app.scrapingbee.com/api/v1/",
            params={
                "api_key": "YDDRE9M8ND00OKRSDDI6NETY5P7L7X74BBCND1NZNJQ3BRI231U06PZXBHX73Y3S1AAID955E05D4CCM",
                "url": url_to_scrape,
            },
            timeout=120,
        )
        # logger.info("Fetching article from ScrapingBee API: %s", url_to_scrape)
        # print('Response HTTP Status Code: ', response.status_code)

        # print('Response HTTP Response Body: ', response.content)
        if return_format == "text":
            text = get_visible_text(response.content)
            # logger.info("ScrapingBee text response: %s", text)
            return text
        if return_format == "pdf":
            response = response.json()
            return response.content

        # logger.info("ScrapingBee Response HTTP Response Body: %s", response.content)
        return response.content
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch article via ScrapingBee API: %s", e)
        return None


def get_website_with_brightdata(url_to_scrape, return_format):
    """Extract visible text from HTML content"""
    api_url = "https://api.brightdata.com/webscraper"
    payload = {
        "url": url_to_scrape,
        "format": return_format,
    }
    headers = {
        "Authorization": f"Bearer {settings.BRIGHT_DATA_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        # logger.info("Fetching article from BrightData API: %s", url_to_scrape)
        response = requests.post(api_url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        brightdata_response = response.json()
        if return_format == "pdf":
            pdf_url = brightdata_response.get("pdfUrl")
            pdf_response = requests.get(pdf_url, headers=headers, timeout=120)
            pdf_response.raise_for_status()
            return pdf_response.content
        else:
            return brightdata_response.get("content", "")
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch article via BrightData API: %s", e)
        return None
