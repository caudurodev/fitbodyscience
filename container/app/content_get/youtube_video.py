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
    result = {}
    
    # Try to get video info
    try:
        video_info = get_youtube_video_info(video_url)
        if video_info:
            result["video_info"] = video_info
    except Exception as e:
        logger.error("Failed to get video info: %s", e)
    
    # Try to get transcript
    try:
        transcript = get_youtube_transcript(video_url)
        if transcript:
            result["transcript"] = transcript
            result["full_text_transcript"] = transcript
            try:
                result["count_tokens_response"] = count_tokens(transcript)
            except Exception as e:
                logger.error("Failed to count tokens: %s", e)
    except Exception as e:
        logger.error("Failed to get transcript: %s", e)
    
    # Return None only if we got no data at all
    if not result:
        logger.error("Failed to get any YouTube video data")
        return None
        
    return result
