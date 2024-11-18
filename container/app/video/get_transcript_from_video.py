""" get transcript from youtube video """

import os
from pathlib import Path
import time
import yt_dlp
import tiktoken
import together
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from ..config.logging import logger
from ..config.constants import TOGETHER_API_KEY


def download_audio(video_url: str, output_path: str = "temp_audio.mp3") -> str:
    """Download audio from YouTube video"""
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return output_path
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return None


def transcribe_with_together(audio_path: str) -> str:
    """Transcribe audio file using Together.ai's Whisper API"""
    try:
        # Set your API key
        together.api_key = TOGETHER_API_KEY

        # Read the audio file as bytes
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # Call Together's Whisper API
        response = together.Audio.transcribe(
            model="togethercomputer/whisper-large-v3",  # or "togethercomputer/whisper-large-v2"
            file=audio_data,
        )

        return response["text"]
    except Exception as e:
        logger.error(f"Error transcribing with Together.ai: {e}")
        return None
    finally:
        # Clean up the temporary audio file
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                logger.debug(f"Cleaned up temporary audio file: {audio_path}")
        except Exception as e:
            logger.error(f"Error cleaning up audio file {audio_path}: {e}")


def get_youtube_transcript(video_url: str) -> str:
    """Get the transcript of a YouTube video given its URL"""
    video_id = video_url.split("youtube.com/watch?v=")[-1]
    transcript = None
    temp_audio_path = None
    result = "No transcript available through any method."

    try:
        # Try getting transcript through YouTube API first
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            # Process transcript only if it's a list of dictionaries
            if isinstance(transcript, list) and transcript:
                logger.info(
                    f"Successfully retrieved English transcript from YouTube API for video: {video_id}"
                )
                result = " ".join([segment["text"] for segment in transcript])
                return result
        except NoTranscriptFound:
            logger.info(
                f"No English transcript found for video: {video_id}. Trying other languages."
            )
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                for transcript_obj in transcript_list:
                    if transcript_obj.language_code != "en":
                        transcript = transcript_obj.fetch()
                        if isinstance(transcript, list) and transcript:
                            logger.info(
                                f"Successfully retrieved {transcript_obj.language_code} transcript from YouTube API for video: {video_id}"
                            )
                            result = " ".join([segment["text"] for segment in transcript])
                            return result
                        break
            except Exception as e:
                logger.info(f"Error retrieving transcript from YouTube API: {e}")
                # Continue to Whisper fallback
        except Exception as e:
            logger.info(f"Error retrieving transcript from YouTube API: {e}")
            # Continue to Whisper fallback

        # If we get here, no transcript was found through YouTube API, try Whisper
        logger.info(
            "No transcript available from YouTube API. Falling back to Together.ai Whisper transcription."
        )
        temp_audio_path = f"temp_audio_{video_id}.mp3"
        audio_path = download_audio(video_url, temp_audio_path)

        if audio_path:
            whisper_transcript = transcribe_with_together(audio_path)
            if whisper_transcript:
                logger.info(
                    f"Successfully generated transcript using Together.ai Whisper for video: {video_id}"
                )
                result = whisper_transcript
                return result

        logger.warning(
            f"Failed to obtain transcript through any method for video: {video_id}"
        )
        
    except Exception as e:
        logger.error(f"Error in transcript generation process: {e}")
        
    finally:
        # Additional cleanup in case the audio file wasn't cleaned up
        try:
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                logger.debug(
                    f"Cleaned up temporary audio file in finally block: {temp_audio_path}"
                )
        except Exception as e:
            logger.error(f"Error in final cleanup of audio file {temp_audio_path}: {e}")
    
    return result


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


def get_temp_directory():
    """Create and return a temporary directory for audio files"""
    temp_dir = Path("temp_audio_files")
    temp_dir.mkdir(exist_ok=True)
    return temp_dir


def cleanup_temp_directory():
    """Remove all files in the temporary directory"""
    temp_dir = Path("temp_audio_files")
    if temp_dir.exists():
        for file in temp_dir.glob("*.mp3"):
            try:
                file.unlink()
            except Exception as e:
                logger.error(f"Error deleting {file}: {e}")


def cleanup_old_files(max_age_hours=24):
    """Remove temporary files older than max_age_hours"""
    temp_dir = Path("temp_audio_files")
    if temp_dir.exists():
        current_time = time.time()
        for file in temp_dir.glob("*.mp3"):
            try:
                file_age = current_time - file.stat().st_mtime
                if file_age > (max_age_hours * 3600):
                    file.unlink()
                    logger.debug(f"Removed old temporary file: {file}")
            except Exception as e:
                logger.error(f"Error cleaning up old file {file}: {e}")
