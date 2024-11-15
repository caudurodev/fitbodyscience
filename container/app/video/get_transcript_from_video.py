import yt_dlp
import tiktoken
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from ..config.logging import logger


def get_youtube_transcript(video_url: str) -> str:
    """Get the transcript of a YouTube video given its URL"""
    video_id = video_url.split("youtube.com/watch?v=")[-1]
    transcript = None

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except NoTranscriptFound:
        print(
            f"No English transcript found for video: {video_id}. Trying other languages."
        )
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for transcript_obj in transcript_list:
                if transcript_obj.language_code != "en":
                    transcript = transcript_obj.fetch()
                    break
        except Exception as e:
            print(f"Error retrieving transcript: {e}")

    if not transcript:
        return "No transcript available in any available language."

    return transcript


def store_segments(segments):
    """Store the text, start times of each segment and the full text of the video transcript"""
    text_segments = []
    start_times = []
    end_times = []
    full_text = ""
    for segment in segments:
        text_segments.append(segment["text"])
        start_times.append(segment["start"])
        end_times.append(segment["end"])
        full_text += f' {segment["text"]} '

    return full_text, text_segments, start_times


def get_youtube_video_description(video_url: str) -> str:
    """Get the description of a YouTube video given its URL"""
    video_info = get_youtube_video_info(video_url)
    return video_info.get("description", None)  # Get video title


def get_youtube_video_info(video_url: str) -> str:
    """Get the description of a YouTube video given its URL"""
    ydl_opts = {
        # "format": "best",
        "outtmpl": "video/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        # #logger.info("video_info: %s", video_info)
        return video_info


def count_tokens(text, model_name="text-davinci-003"):
    """Count the number of tokens in a given text"""
    encoder = tiktoken.encoding_for_model(model_name)

    # Encode the text to get the tokens
    tokens = encoder.encode(text)

    # Return the number of tokens
    return len(tokens)
