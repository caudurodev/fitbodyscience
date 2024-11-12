""" get related content """

import re
import json
from ..utils.llm import get_llm_completion
from ..content_store.reference_store import save_related_link
from ..content_store.content_relation_store import create_content_relation
from ..utils.config import logger


def retrieve_video_description_links_and_save(parent_content_id, video_description):
    """gets links from description"""
    # logger.info(
    # "retrieve_video_description_links_and_save parent_content_id %s",
    # parent_content_id,
    # )
    # #logger.info("Getting evidence links from video description: %s", video_description)

    has_links = contains_link(video_description)
    if not has_links:
        logger.error(
            "No links found in video description, don't parse for evidence links."
        )
        return ""

    evidence_links_json = []
    try:
        evidence_links = get_llm_completion(
            f"""
            Given this youtube video description: 
            
            {video_description}

            Return a JSON with all of the links mentioned and categorize them as likely evidence links such as
            links to scientific papers, news articles, or blog posts, or likely non-evidence links such as
            links to social media, entertainment websites, or shopping websites.

            in the "media_type" json property: add the most likely type of media the link points to, such as text, video, or image.
            in the "content_type" json property: add the type of content the link points to, such as scientific paper, news article, 
            blog post, social media, video, audio, podcast etc.
            If the extracted link URL seems like it is a direct link to a scientific paper, try to extract the DOI number
            from the URL and add it to the JSON response.

            Return valid JSON response like this:
            {{
                "evidence_links": [
                    {{
                        "full_url":"https://www.scientificpaper.com/full/path/",
                        "content_type": "scientific paper",
                        "doi":"10.1186/1550-2783-10-39",
                        "media_type": "text"
                    }}
                ]
            }}
        """
        )
        # #logger.info("parent_content_id %s", parent_content_id)
        # #logger.info("video_description %s", video_description)
        # #logger.info("Evidence links found: %s", evidence_links)
        evidence_links_json = json.loads(evidence_links)
        new_links_saved = []
        if len(evidence_links_json.get("evidence_links")) > 0:
            for link in evidence_links_json.get("evidence_links"):
                # #logger.info("Evidence link found: %s", link)
                full_url = link.get("full_url")
                content_type = link.get("content_type")
                media_type = link.get("media_type")
                doi_number = link.get("doi")
                try:
                    link_content_id = save_related_link(
                        full_url, content_type, media_type, doi_number
                    )
                    if link_content_id is None or parent_content_id is None:
                        logger.error("Error saving related link: %s", link)
                        continue
                    new_links_saved.append(
                        {
                            "link_content_id": link_content_id,
                            "full_url": full_url,
                            "content_type": content_type,
                            "media_type": media_type,
                            "doi": doi_number,
                        }
                    )
                    try:
                        relation_id = create_content_relation(
                            parent_content_id, link_content_id
                        )

                        if relation_id is None:
                            logger.error("Error creating content relation: %s", link)
                            continue
                        # logger.info("Content relation created: %s", relation_id)
                    except Exception as e:
                        logger.error("Error creating content relation: %s", e)
                        continue

                except Exception as e:
                    logger.error("Error saving related link: %s", e)
                    continue
            return new_links_saved
        # idea: check if sponsors are conflict of interest
        # if len(evidence_links_json.get("non_evidence_links")) > 0:
        #     for link in evidence_links_json.get("non_evidence_links"):
        #         #logger.info("Non-evidence link found: %s", link)
    except Exception as e:
        logger.error("Error getting evidence links: %s", e)
    return evidence_links_json


def contains_link(text: str) -> bool:
    """Regular expression pattern for detecting URLs"""
    url_pattern = re.compile(r"https?://")
    return bool(url_pattern.search(text))
