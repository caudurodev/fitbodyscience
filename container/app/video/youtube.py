"""
Clean and resolve a YouTube URL to its canonical form.
Removes tracking parameters and resolves shortened URLs.
Returns None if the URL is invalid or not from YouTube.
"""

from ..utils.config import logger
from yt_dlp import YoutubeDL


def get_clean_youtube_url(url):
    """
    Clean and resolve a YouTube URL to its canonical form.
    Removes tracking parameters and resolves shortened URLs.
    Returns None if the URL is invalid or not from YouTube.
    """
    try:
        with YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return f"https://www.youtube.com/watch?v={info['id']}"
    except Exception as e:
        logger.error(f"Error cleaning YouTube URL: {e}")
        return None
