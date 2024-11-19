""" get related content """

import re
import json
from ..vendors.llm.get_response import get_response
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
        evidence_links = get_response(
            f"""
                Given the following YouTube video description:

                {video_description}

                Perform the following tasks:

                1. **Extract all URLs** mentioned in the video description.

                2. **For each URL**, determine:
                - **Evidence Type**: Categorize the link as either an "evidence" link or a "non-evidence" link.
                    - *Evidence links* include those to scientific papers, science news articles, or blog posts.
                    - *Non_evidence links* include those to social media, generic blog posts, entertainment websites, or shopping websites.
                - **Media Type**: Identify the most likely type of media the link points to (e.g., text, video, image).
                - **Content Type**: Specify the type of content the link points to (e.g., scientific_paper, news_article, blog_post, social_media, video, audio, podcast, etc).
                - **DOI**: If the URL is a direct link to a scientific paper and contains a DOI number, extract it and include it. If not, set this field to an empty string.
                    - *Note*: Do not include identifiers like PubMed IDs in the "doi" field. Identifiers from urls like pubmed.ncbi.nlm.nih.gov and pubmed.ncbi.nlm.nih.gov are not valid DOIs.


                3. **Return a valid JSON** object containing an array of all the links with their associated properties.

                4. **Source** specify where to find more information about the sciencetific evicence.
                Source examples are: "doi", "pubmed",  "arxiv", list sources that typically provide an API that can be used to lookup the identifier in more details

                The JSON should be structured as follows:

                {{
                    "links": [
                        {{
                            "full_url": "https://www.example.com/full/path/",
                            "evidence_type": "evidence",
                            "source":"pubmed",
                            "media_type": "text",
                            "content_type": "scientific_paper",
                            "doi": "10.1186/1550-2783-10-39"
                        }},
                    ]
                }}
            """
        )
        # logger.info("parent_content_id %s", parent_content_id)
        # logger.info("video_description %s", video_description)
        # logger.info("Evidence links found: %s", evidence_links)
        evidence_links_json = json.loads(evidence_links)
        new_links_saved = []

        if len(evidence_links_json.get("links", [])) > 0:
            for link in evidence_links_json.get("links"):
                # Only process evidence links
                if link.get("evidence_type") != "evidence":
                    continue

                full_url = link.get("full_url")
                canonical_url = full_url
                content_type = link.get("content_type")
                media_type = link.get("media_type")
                doi_number = link.get("doi")

                try:
                    link_content_id = save_related_link(
                        full_url, canonical_url, content_type, media_type, doi_number
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
