""" Get content from a specific URL """

import requests
from ..config.logging import logger
from ..config.constants import UNPAYWALL_API_URL, EMAIL


def get_unpaywall_download_link(doi_number):
    """Get the full text link using Unpaywall API"""
    try:
        response = requests.get(
            f"{UNPAYWALL_API_URL}{doi_number}", params={"email": EMAIL}, timeout=20
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("is_oa"):
                return data
            else:
                logger.info(f"Not open access: {data}")
                # store response from unpaywall
                return False
        else:
            return False
    except Exception as e:
        logger.error(f"Error getting unpaywall download link: {e}")
        return False
