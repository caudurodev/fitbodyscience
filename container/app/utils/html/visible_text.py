""" Module to extract the visible text content and important tags from HTML. """

import json
import re
import trafilatura
from ...config.logging import logger
from bs4 import BeautifulSoup, Comment


def get_visible_text(html_content):
    """Extracts all visible text from HTML content, ignoring JavaScript, CSS, and comments."""
    if not html_content or not isinstance(html_content, str):
        return {"content": "", "title": None}

    soup = BeautifulSoup(html_content, "html.parser")
    if not soup.body:
        return {"content": "", "title": None}

    title = soup.title.string if soup.title else None

    # Remove all script and style elements
    for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
        element.decompose()

    # Remove comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Extract all visible text
    visible_text = " ".join(
        text.strip() for text in soup.stripped_strings if text.strip()
    )

    # Basic content validation
    if len(visible_text) < 100:  # Too short to be meaningful
        return {"content": "", "title": None}

    return {"content": visible_text, "title": title}


def get_main_content(html_content):
    """
    Extracts the main content from HTML, including the DOI if present.
    Returns the content as JSON.
    """
    if not html_content:
        logger.error("Empty HTML content provided")
        return None
        
    if not isinstance(html_content, str):
        try:
            html_content = str(html_content)
            logger.warning("Had to convert HTML content to string")
        except:
            logger.error("Failed to convert HTML content to string")
            return None
            
    # Remove null bytes that can cause parsing issues
    html_content = html_content.replace('\x00', '')
    
    if len(html_content.strip()) < 50:  # Too short to be valid HTML
        logger.error(f"HTML content too short ({len(html_content)} chars)")
        return None

    # First try trafilatura with different configurations
    for extraction_config in [
        {"include_tables": True, "favor_precision": True},
        {"include_tables": False, "favor_precision": True},
        {"include_tables": True, "favor_precision": False},
        {"include_tables": False, "favor_precision": False}
    ]:
        try:
            logger.info(f"Trying trafilatura with config: {extraction_config}")
            extracted_content = trafilatura.extract(
                html_content,
                include_links=True,
                include_images=False,
                output_format="json",
                with_metadata=True,
                include_formatting=False,
                no_fallback=False,
                **extraction_config
            )
            
            if extracted_content:
                try:
                    content_json = json.loads(extracted_content)
                    if not content_json.get("text"):
                        logger.warning("No text content in trafilatura output")
                        continue
                        
                    # Remove unnecessary fields
                    content_json.pop("excerpt", None)
                    content_json.pop("raw_text", None)
                    
                    text_length = len(content_json["text"])
                    logger.info(f"Successfully extracted {text_length} chars with trafilatura")
                    return content_json
                except (json.JSONDecodeError, ValueError) as e:
                    logger.warning(f"Failed to parse trafilatura JSON: {e}")
                    continue
        except Exception as e:
            logger.warning(f"Trafilatura extraction failed: {str(e)}")
            continue

    logger.info("Falling back to basic HTML parsing")
    # Fallback to basic HTML parsing
    basic_content = get_visible_text(html_content)
    if not basic_content or not basic_content["content"]:
        logger.error("Failed to extract any content with basic parsing")
        return None
        
    text_length = len(basic_content["content"])
    if text_length < 100:
        logger.error(f"Extracted content too short ({text_length} chars)")
        return None
        
    logger.info(f"Successfully extracted {text_length} chars with basic parsing")
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
