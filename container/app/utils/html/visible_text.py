""" Module to extract the visible text content and important tags from HTML. """

import json
import trafilatura

# from ...config.logging import logger
from bs4 import BeautifulSoup, Comment
import re


def get_visible_text(html_content):
    """Extracts all visible text from HTML content, ignoring JavaScript, CSS, and comments."""
    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.title.string if soup.title else None

    # Remove all script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    # Remove comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Extract all visible text
    visible_text = soup.get_text(separator=" ", strip=True)
    return {"content": visible_text, "title": title}


def get_main_content(html_content):
    """
    Extracts the main content from HTML, including the DOI if present.
    Returns the content as JSON.
    """
    # First try trafilatura
    try:
        extracted_content = trafilatura.extract(
            html_content,
            include_links=True,
            include_images=False,
            output_format="json",
            with_metadata=True,
            favor_precision=True,  # More precise but slower extraction
            include_formatting=False,
            include_tables=False,
            no_fallback=False,  # Allow fallback methods
        )
        
        if extracted_content:
            try:
                content_json = json.loads(extracted_content)
                # Remove unnecessary fields
                content_json.pop("excerpt", None)
                content_json.pop("raw_text", None)
                return content_json
            except json.JSONDecodeError:
                pass  # Fall through to basic parsing
    except Exception:
        pass  # Fall through to basic parsing

    # Fallback to basic HTML parsing
    basic_content = get_visible_text(html_content)
    return {
        "title": basic_content["title"] or "",
        "text": basic_content["content"],
        "author": "",
        "date": "",
        "url": "",
        "description": "",
        "categories": [],
        "tags": [],
        "id": "",
        "source": "basic_parser"
    }
