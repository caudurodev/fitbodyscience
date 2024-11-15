""" User add content endpoint """

from ...config.logging import logger
from ...endpoints.get_channel_data import upsert_influencer_endpoint
from ...video.get_yt_channel_data import get_channel_url_from_video
from ...store.content import upsert_content
from ...content_get.youtube_video import get_youtube_video_data
from ...store.slug import generate_slug
from ...store.influencer_contents import add_influencer_content_relationship
from ...video.youtube import get_clean_youtube_url
from ...store.content import get_content_by_url


def user_add_content_endpoint(content_url, content_type):
    """Analyze a scientific paper and save the data to the database"""

    try:
        content_saved_input_url = get_content_by_url(content_url)
        if content_saved_input_url is not None:
            try:
                slug = content_saved_input_url["slug"]
                influencer_slug = content_saved_input_url["influencer_contents"][0][
                    "influencer"
                ]["slug"]
                full_slug = f"{influencer_slug}/{slug}"
                return {
                    "message": "Content already exists",
                    "slug": full_slug,
                    "success": True,
                }
            except (KeyError, IndexError) as e:
                logger.error(
                    "Error accessing content data structure: %s. Content data: %s",
                    str(e),
                    content_saved_input_url,
                )
                return {
                    "message": "Error processing existing content",
                    "success": False,
                }
    except Exception as e:
        logger.error(
            "Error checking existing content: %s. URL: %s", str(e), content_url
        )

    try:
        cleaned_url = get_clean_youtube_url(content_url)
        if cleaned_url is None:
            return {
                "message": "error getting cleaned url",
                "success": False,
            }

        try:
            content_saved = get_content_by_url(cleaned_url)
            if content_saved is not None:
                influencer_slug = content_saved["influencer_contents"][0]["influencer"][
                    "slug"
                ]
                full_slug = f"{influencer_slug}/{content_saved['slug']}"
                logger.info("content alreadysaved: %s", content_saved)
                logger.info("full_slug: %s", full_slug)
                return {
                    "message": "Content already exists",
                    "slug": full_slug,
                    "success": True,
                }
        except Exception:
            logger.info("Content not found, adding content")

        influencer_info = None
        channel_url = get_channel_url_from_video(cleaned_url)
        if channel_url:
            influencer_info = upsert_influencer_endpoint(channel_url)

        if influencer_info is None:
            logger.error("Error getting influencer")
            return {
                "message": "Error getting influencer",
                "success": False,
            }

        logger.info("influencer_info: %s", influencer_info)
        influencer_slug = influencer_info["slug"]
        logger.info("influencer_slug: %s", influencer_slug)

        video_data = get_youtube_video_data(cleaned_url)
        if video_data is None:
            return {
                "message": "Error getting video data from youtube",
                "success": False,
            }

        try:
            video_title = video_data["video_info"]["title"]
            logger.info("video_title: %s", video_title)
        except (KeyError, TypeError) as e:
            logger.error(
                "Error accessing video data structure: %s. Video data: %s",
                str(e),
                video_data,
            )
            return {"message": "Error processing video data", "success": False}

        slug = generate_slug(video_title)
        logger.info("slug: %s", slug)

        content_id = upsert_content(
            video_title=video_data["video_info"]["title"],
            video_id=video_data["video_info"]["display_id"],
            video_url=content_url,
            content_type=content_type,
            canonical_url=cleaned_url,
            transcript=video_data["transcript"],
            video_description=video_data["video_info"]["description"],
            full_text_transcript=video_data["full_text_transcript"],
            slug=slug,
        )

        add_influencer_content_relationship(influencer_info["id"], content_id)
        # result = analyze_youtube_video(video_data, influencer_id)
        full_slug = f"{influencer_info['slug']}/{slug}"
        logger.info("full_slug: %s", full_slug)
        return {
            "message": "success",
            "slug": full_slug,
            "success": True,
        }
    except Exception as e:
        logger.error("Error adding content: %s. Traceback: ", str(e), exc_info=True)
        return {"message": f"Error adding content: {str(e)}", "success": False}
