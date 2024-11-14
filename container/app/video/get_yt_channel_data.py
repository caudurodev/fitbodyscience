import yt_dlp
from ..config.logging import logger
from .get_transcript_from_video import get_youtube_video_info


def get_youtube_channel_info(channel_url: str) -> dict:
    """Get information about a YouTube channel given its URL"""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "playlist_items": "0",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            channel_info = ydl.extract_info(channel_url, download=False)

            # Get avatar thumbnail
            thumbnail = None
            banner = None
            if thumbnails := channel_info.get("thumbnails"):
                for thumb in thumbnails:
                    if thumb.get("id") == "avatar_uncropped":
                        thumbnail = thumb.get("url")
                    elif thumb.get("id") == "banner_uncropped":
                        banner = thumb.get("url")

            channel_data = {
                # Basic Info
                "id": channel_info.get(
                    "id", None
                ),  # Channel handle (e.g., @ThomasDeLauerOfficial)
                "title": channel_info.get("title", None),  # Channel title
                "name": channel_info.get("uploader", channel_info.get("channel", None)),
                "channel_id": channel_info.get("channel_id", None),
                "description": channel_info.get("description", None),
                # URLs
                "channel_url": channel_info.get("channel_url", None),
                "webpage_url": channel_info.get(
                    "webpage_url", None
                ),  # Full URL to channel page
                "uploader_url": channel_info.get("uploader_url", None),  # Handle URL
                # Stats
                "subscriber_count": channel_info.get(
                    "subscriber_count", channel_info.get("channel_follower_count", None)
                ),
                "view_count": channel_info.get("view_count", None),
                "playlist_count": channel_info.get(
                    "playlist_count", None
                ),  # Number of playlists/videos
                # Media
                "thumbnail": thumbnail,  # Avatar
                "banner": banner,  # Channel banner
                # Metadata
                "tags": channel_info.get("tags", []),
                "availability": channel_info.get("availability", None),
                "modified_date": channel_info.get("modified_date", None),
                "upload_date": channel_info.get("upload_date", None),
                "release_year": channel_info.get("release_year", None),
                "epoch": channel_info.get(
                    "epoch", None
                ),  # Unix timestamp of data fetch
                # Technical details
                "extractor": channel_info.get("extractor", None),  # youtube:tab
                "extractor_key": channel_info.get("extractor_key", None),  # YoutubeTab
                "webpage_url_domain": channel_info.get(
                    "webpage_url_domain", None
                ),  # youtube.com
            }
            return channel_data

        except Exception as e:
            logger.error("Error extracting channel info: %s", e)
            return {}


def get_channel_url_from_video(video_url: str) -> str:
    """Extract channel URL from a YouTube video URL"""
    video_info = get_youtube_video_info(video_url)
    return video_info.get("channel_url", None)
