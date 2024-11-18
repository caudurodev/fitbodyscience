""" Module to extract the visible text content and important tags from HTML. """

from urllib.parse import urljoin  # Add this import
from bs4 import BeautifulSoup, Comment


def extract_content_links(
    html_content, link_path_extract, base_url
):  # Add base_url parameter
    """Extracts the title and a list of text and corresponding links from HTML, ignoring non-content links."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title = soup.title.string if soup.title else None

    # Remove unwanted elements
    for element in soup(["script", "style", "noscript", "iframe", "head", "meta"]):
        element.decompose()

    # Remove comments
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    results = []

    # Find all <a> tags
    for link in soup.find_all("a"):
        href = link.get("href")
        text = link.get_text(strip=True)
        if text and is_valid_article_link(href) and link_path_extract in href:
            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(base_url, href)
            results.append({"text": text, "url": absolute_url})

    return {"html_title": title, "all_urls": results}


def is_valid_article_link(href):
    """Check if the link is likely to be a valid article link."""
    if not href:
        return False

    # Ignore anchor links, javascript, and other non-article URLs
    if href.startswith(("#", "javascript:", "mailto:", "//")):
        return False

    # Ignore links to the homepage or section pages
    if href == "/":
        return False

    return True
