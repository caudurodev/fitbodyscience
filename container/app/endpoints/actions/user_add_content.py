""" User add content endpoint """

from ...config.logging import logger
from ...endpoints.get_channel_data import upsert_influencer_endpoint
from ...video.get_yt_channel_data import get_channel_url_from_video
from ...video.youtube import get_clean_youtube_url
from ...store.content import upsert_content
from ...store.slug import generate_unique_slug
from ...store.influencer_contents import add_influencer_content_relationship
from ...store.content import get_content_by_url
from ...store.content_activity import add_content_activity
from ...content_get.youtube_video import get_youtube_video_data
from ...meaning.evaluate_content_for_science import (
    evaluate_transcript_for_science_based,
)


def user_add_content_endpoint(content_url, content_type):
    """Analyze a scientific paper and save the data to the database"""

    existing_content = get_content_by_url(content_url)
    if (
        existing_content is not None
        and "slug" in existing_content
        and "influencer_contents" in existing_content
    ):
        slug = existing_content["slug"]
        influencer_slug = existing_content["influencer_contents"][0]["influencer"][
            "slug"
        ]
        full_slug = f"{influencer_slug}/{slug}"
        return {
            "message": "Content already exists",
            "slug": full_slug,
            "success": True,
        }

    cleaned_url = get_clean_youtube_url(content_url)
    if cleaned_url is None:
        return {
            "message": "error getting cleaned url",
            "success": False,
            "slug": "",
        }

    content_saved = get_content_by_url(cleaned_url)
    if content_saved is not None:
        influencer_slug = content_saved["influencer_contents"][0]["influencer"]["slug"]
        full_slug = f"{influencer_slug}/{content_saved['slug']}"
        return {
            "message": "Content already exists",
            "slug": full_slug,
            "success": True,
        }

    influencer_info = None
    channel_url = get_channel_url_from_video(cleaned_url)
    if channel_url:
        influencer_info = upsert_influencer_endpoint(channel_url)

    if influencer_info is None:
        logger.error("Error getting influencer")
        return {
            "message": "Error getting influencer",
            "success": False,
            "slug": "",
        }
    influencer_slug = influencer_info["slug"]

    video_data = get_youtube_video_data(cleaned_url)
    if video_data is None:
        return {
            "message": "Error getting video data from youtube",
            "success": False,
            "slug": "",
        }

    video_info = video_data.get("video_info", {})
    video_title = video_info.get("title")
    logger.info("video_title: %s", video_title)

    if not video_title:
        logger.error("No video title found in data: %s", video_data)
        return {
            "message": "Error: Could not get video title",
            "success": False,
            "slug": "",
        }

    slug = generate_unique_slug(video_title, table_name="content")
    logger.info("slug: %s", slug)
    video_transcript = video_data.get("transcript", "")
    if video_transcript is None:
        logger.error("No transcript found in data: %s", video_data)
        return {
            "message": "Error: Could not get transcript",
            "success": False,
            "slug": "",
        }

    science_based_evaluation = evaluate_transcript_for_science_based(
        text_content=video_transcript,
    )

    is_science_based = (
        science_based_evaluation is not None
        and science_based_evaluation.get("evaluation") == "true"
    )

    content_id = upsert_content(
        video_title=video_title,
        video_id=video_info.get("display_id", ""),
        video_url=content_url,
        content_type=content_type,
        canonical_url=cleaned_url,
        transcript=video_transcript,
        video_description=video_info.get("description", ""),
        full_text_transcript=video_data.get("full_text_transcript", ""),
        is_parsed=False,
        is_science_based=is_science_based,
        science_based_evaluation=science_based_evaluation,
        slug=slug,
    )
    if content_id is None:
        return {"message": "Error saving content", "success": False}

    logger.info("content_id: %s", content_id)
    add_content_activity(
        name="Retrieved video content",
        content_id=content_id,
        activity_type="info",
        description="Transcript and metadata have been retrieved",
    )

    add_influencer_content_relationship(influencer_info["id"], content_id)

    add_content_activity(
        name="Video Description Processed",
        content_id=content_id,
        activity_type="info",
        description="Content description has been processed and evidence has been retrieved",
    )

    if is_science_based is False:
        add_content_activity(
            name="Video is Not Science Based",
            content_id=content_id,
            activity_type="info",
            description="Video is Not Science Based",
        )
        return {
            "message": f"Video is not science based {science_based_evaluation}",
            "success": False,
            "slug": "",
        }

    full_slug = f"{influencer_info['slug']}/{slug}"
    return {
        "message": "success",
        "slug": full_slug,
        "success": True,
        "content_id": content_id,
    }
