""" User add content endpoint """

from flask import jsonify
from ...config.logging import logger

# from ..get_channel_data import upsert_influencer_endpoint
# from ...video.get_yt_channel_data import get_channel_url_from_video
# from ...store.content import upsert_content
# from ...content_get.youtube_video import get_youtube_video_data
# from ...store.slug import generate_slug
# from ...store.influencer_contents import add_influencer_content_relationship
# from ...video.youtube import get_clean_youtube_url
# from ...store.content import get_content_by_url
from ...content_store.youtube_store import video_exists_in_db
from ...meaning.summarize import summarise_text_and_add_to_content

from ...content_store.assertion_store import parse_assertions_long_text
from ...store.content import update_content_is_parsed

# from ...utils.run_async import run_method_async


def user_analyse_content_endpoint(content_id):
    """Analyze a scientific paper and save the data to the database"""
    content = video_exists_in_db(content_id)
    if not content:
        return jsonify({"message": "Content not found", "success": False}), 404

    video_transcript = content.get("videoTranscript")
    video_description = content.get("videoDescription")

    if not video_transcript:
        logger.error(f"No video transcript found for content {content_id}")
        return jsonify({"message": "No video transcript found", "success": False}), 400

    summarise_text_and_add_to_content(
        video_content_id=content_id,
        long_text=video_transcript,
        video_description=video_description,
    )
    parse_assertions_long_text(
        content_id=content_id,
        long_text=video_transcript,
        additional_information=video_description,
    )

    update_content_is_parsed(content_id=content_id, is_parsed=True)

    logger.info(f"Started analyzing content {content_id}")
    return jsonify({"message": "Analysis started", "success": True}), 200
