""" extract data from youtube videos """

from typing import Dict, Any
from ..utils.config import logger


from ..video.get_transcript_from_video import (
    get_youtube_transcript,
    get_youtube_video_info,
    count_tokens,
)


def get_youtube_video_data(video_url: str) -> Dict[str, Any]:
    """Fetch all possible content from a YouTube video in text format.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        Dict[str, Any]: A dictionary containing the transcript, full text transcript,
                        video description, and token count response.
    """
    try:
        # Get video info first to ensure it's available even if transcript fails
        video_info = get_youtube_video_info(video_url)

        # Get transcript
        transcript = get_youtube_transcript(video_url)

        # The transcript is already a string from get_youtube_transcript
        full_text_transcript = transcript

        count_tokens_response = count_tokens(full_text_transcript)

        return {
            "transcript": transcript,
            "full_text_transcript": full_text_transcript,
            "count_tokens_response": count_tokens_response,
            "video_info": video_info,
        }
    except Exception as e:
        # Handle the exception (e.g., log it, raise a custom error, etc.)
        logger.error("Failed to get YouTube video data: %s", e)
        # Don't try to log video_info here as it might not exist
        return None
