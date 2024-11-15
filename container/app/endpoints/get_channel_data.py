"""
Get channel data
"""

import os
import tempfile
import requests
from ..video.get_yt_channel_data import get_youtube_channel_info
from ..store.influencer import upsert_influencer, get_influencer_by_url
from ..config.logging import logger
from ..utils.nhost.upload import upload_files_to_nhost
from ..store.slug import generate_slug


def upsert_influencer_endpoint(url: str):
    """Upserts influencer data to the database"""

    # check if duplicate
    if influencer_info := get_influencer_by_url(url):
        logger.info("Influencer already exists: %s", influencer_info)
        return influencer_info

    channel_data = get_youtube_channel_info(url)
    # logger.info("channel_data: %s", channel_data)

    # Handle profile image upload
    profile_img_id = ""
    if thumbnail_url := channel_data.get("thumbnail"):
        try:
            # Download image to temp file
            response = requests.get(thumbnail_url, timeout=10)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(
                    suffix=".jpg", delete=False
                ) as temp_file:
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name

                # Upload to storage and get UUID
                uploaded_files = upload_files_to_nhost(
                    bucket_id=None, file_paths=[temp_file_path]
                )
                if uploaded_files and len(uploaded_files) > 0:
                    profile_img_id = uploaded_files[0].get("id", "")
                    logger.info("Uploaded profile image with ID: %s", profile_img_id)

                # Cleanup temp file
                os.remove(temp_file_path)
        except Exception as e:
            logger.error("Error uploading profile image: %s", e)
            # Continue without profile image if upload fails

    logger.info("Generating slug for influencer: %s", channel_data["name"])
    slug = generate_slug(channel_data["name"])
    logger.info("Generated slug: %s", slug)

    influencer_info = upsert_influencer(
        name=channel_data["name"],
        profile_img=profile_img_id,
        yt_channel_info_jsonb=channel_data,
        yt_description=channel_data["description"],
        yt_url=url,
        slug=slug,
    )

    if influencer_info is None:
        logger.error("Failed to upsert influencer")
        return {"error": "Failed to upsert influencer"}

    return influencer_info
