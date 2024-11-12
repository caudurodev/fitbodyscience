"""Web scraping utilities"""

import requests


from ..content_get.website_content import get_visible_text
from ..utils.config import settings, logger


def download_website(url_to_scrape, return_format="text", vendor="oxylabs"):
    """Extract visible text from HTML content"""
    try:
        if vendor == "oxylabs":
            # logger.info("Using Oxylabs to fetch website content")
            data = download_url_with_oxylabs(url_to_scrape, return_format)
        elif vendor == "use_scraper":
            # logger.info("Using Use Scraper to fetch website content")
            data = get_website_with_use_scraper(url_to_scrape, return_format)
        elif vendor == "scrapingbee":
            # logger.info("Using ScrapingBee to fetch website content")
            data = get_website_with_scrapingbee(url_to_scrape, return_format)
        elif vendor == "brightdata":
            # logger.info("Using BrightData to fetch website content")
            data = get_website_with_brightdata(url_to_scrape, return_format)
        else:
            logger.error("Unsupported vendor: %s", vendor)
            return None

        # #logger.info("download_website return data from vendor %s: %s", vendor, data)
        if data is None or data == "":
            logger.error("No content found in response")
            return None
        # #logger.info("get_visible_data return data: %s", data)
        if return_format == "text":
            return get_visible_text(data)

        return data
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch article via %s API: %s", vendor, e)
        return None


def download_url_with_oxylabs(url_to_scrape, return_format="text"):
    """Extract visible text from HTML content"""
    api_url = "https://realtime.oxylabs.io/v1/queries"
    payload = {
        "source": "universal",
        "url": url_to_scrape,
        "geo_location": "United States",
        "render": "html",
    }
    headers = {"Content-Type": "application/json"}
    auth = (settings.OXYLABS_USER, settings.OXYLABS_PASS)

    try:
        # #logger.info(
        #     "download_url_with_oxylabs Fetching article from Oxylabs API: %s",
        #     url_to_scrape,
        # )
        response = requests.post(
            api_url, json=payload, headers=headers, auth=auth, timeout=120
        )
        # #logger.info("download_url_with_oxylabs response : %s", response)

        response.raise_for_status()
        oxylabs_response = response.json()
        # #logger.info(
        #     "download_url_with_oxylabs oxylabs_response: %s",
        #     oxylabs_response,
        # )
        downloaded = oxylabs_response.get("results", [{}])[0].get("content", "")
        # #logger.info(
        #     "download_url_with_oxylabs downloaded: %s",
        #     downloaded,
        # )

        if not downloaded:
            logger.error(
                "download_url_with_oxylabs Error No content found in Oxylabs response"
            )
            # #logger.info(
            #     "download_url_with_oxylabs Error Oxylabs response: %s", oxylabs_response
            # )
            # #logger.info(
            #     "download_url_with_oxylabs vError Oxylabs downloaded: %s", downloaded
            # )

        # #logger.info(
        #     "download_url_with_oxylabs success Oxylabs downloaded: %s", downloaded
        # )

        return downloaded
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch article via Oxylabs API: %s", e)
        return None
    except ValueError as e:
        logger.error("Error processing Oxylabs response: %s", e)
        return None


# https://docs.usescraper.com/api-reference/scraper/scrape
def get_website_with_use_scraper(url_to_scrape, return_format="text"):
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
