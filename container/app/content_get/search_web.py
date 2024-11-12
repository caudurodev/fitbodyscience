""" This module is used to search the web for the query provided by the user. """

import json
import requests
from ..utils.config import logger, settings


def search_web(query):
    """Search the web for the query provided by the user."""
    # logger.info("Searching the web for: %s", query)
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=120)
    # logger.info("search_web response: %s", response.text)
    return response.text
