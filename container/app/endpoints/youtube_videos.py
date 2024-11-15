""" YouTube video endpoint """

from ..utils.config import logger
from ..utils.run_async import run_method_async
from ..content_get.youtube_video import get_youtube_video_data
from ..content_store.youtube_store import save_youtube_data, video_exists_in_db
from ..content_store.assertion_store import parse_assertions_long_text
from ..meaning.summarize import summarise_text_and_add_to_content
from ..store.slug import generate_slug


def analyze_youtube_video(content_id, influencer_id):
    """Analyze a YouTube video and save the data to the database"""
    response = {
        "message": "Success",
        "server_response": 200,
    }
    if content_id is None:
        response["message"] = "Error: no content_id provided"
        response["server_response"] = 400
        return response

    # logger.info("content_id: %s", content_id)
    exists_result = video_exists_in_db(content_id)
    logger.info("exists_result: %s", exists_result)
    canonical_url = exists_result["canonicalUrl"]
    is_parsed = exists_result["is_parsed"]
    error_message = exists_result["error_message"]
    # logger.info("exists_result: %s", exists_result)
    is_skip = exists_result["exists"] and not error_message and is_parsed is True
    if canonical_url is None:
        response["message"] = "Error: content does not exist in the database"
        response["server_response"] = 400
        return response
    if error_message:
        response["message"] = "Error: content exists in the database but has an error"
        response["server_response"] = 400
        return response
    if is_skip:
        # logger.info("Content already exists in the database, skipping...")
        response["message"] = "Video already exists in the database, skipping..."
        response["server_response"] = 400
        return response

    # logger.info("Video does not exist in the database, processing...")

    try:
        # logger.info("Getting YouTube video data...")
        video_data = get_youtube_video_data(canonical_url)
    except Exception as e:
        logger.error("Error getting YouTube video data: %s", e)
        response["message"] = "Error getting YouTube video data"
        response["server_response"] = 500
        return response

    try:
        # #logger.info("video_data: ")
        video_transcript = video_data["transcript"]
        # #logger.info("video_transcript: %s", video_transcript)
        full_text_transcript = video_data["full_text_transcript"]
        # #logger.info("full_text_transcript: %s", full_text_transcript)
        video_description = video_data["video_info"]["description"]
        # #logger.info("video_description: %s", video_description)
        video_title = video_data["video_info"]["title"]
        # #logger.info("video_title: %s", video_title)
        video_id = video_data["video_info"]["display_id"]
        # #logger.info("video_id: %s", video_id)

    except Exception as e:
        logger.error("Exception Error parsing YouTube video data: %s", e)
        response["message"] = "Error parsing YouTube video data"
        response["server_response"] = 500
        return response

    slug = generate_slug(video_title)

    try:
        # #logger.info("Saving YouTube data...")
        video_content_id = save_youtube_data(
            content_id=content_id,
            video_title=video_title,
            video_id=video_id,
            video_url=canonical_url,
            transcript=video_transcript,
            video_description=video_description,
            full_text_transcript=full_text_transcript,
            influencer_id=influencer_id,
            slug=slug,
        )

        logger.info("video_content_id: %s", video_content_id)

        if full_text_transcript is not None:
            simplified_transcript = []
            for entry in video_transcript:
                timestamp = round(entry["start"])
                sentence = entry["text"]
                simplified_transcript.append(f"{timestamp}s {sentence}")
            simplified_transcription = "\n".join(simplified_transcript)

            # #logger.info("parse_assertions_long_text starts")
            # run_method_async(
            #     parse_assertions_long_text,
            #     video_content_id,
            #     simplified_transcription,
            #     video_description,
            # )

            # #logger.info("summarise_text_and_add_to_content starts")
            # run_method_async(
            #     summarise_text_and_add_to_content,
            #     video_content_id,
            #     full_text_transcript,
            #     video_description,
            # )
            response["message"] = "Success"
            response["server_response"] = 200
            return response

    except Exception as e:
        logger.error("Error saving YouTube data: %s", e)
        response["message"] = "Error saving YouTube data"
        response["server_response"] = 500
        return response
