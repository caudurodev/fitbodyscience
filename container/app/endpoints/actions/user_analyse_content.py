""" User add content endpoint """

from ...config.logging import logger
from ...meaning.summarize import summarise_text_and_add_to_content
from ...content_store.youtube_store import video_exists_in_db
from ...content_store.assertion_store import parse_assertions_long_text
from ...store.content import update_content_is_parsed
from ...store.content_relationship import get_content_relationship
from ...store.assertions_content import get_content_assertions
from ...store.content_activity import add_content_activity
from ...scoring.update import update_content_aggregate_score
from ...endpoints.actions.action_user_classify_evidence_endpoint import (
    classify_evidence,
)
from ...endpoints.actions.action_update_assertion_score_endpoint import (
    update_assertion_score_by_id,
)
from ...endpoints.assertions import insert_assertions_opposing
from ...content_get.related_links import retrieve_video_description_links_and_save

# from ...utils.run_async import run_method_async

# from ...endpoints.actions.action_user_classify_evidence_endpoint import (
#     connect_evidence_content_to_assertions,
# )


def user_analyse_content_endpoint(content_id):
    """
    Analyze content and connect it to assertions
    """
    try:
        if not content_id:
            return {
                "success": False,
                "message": "Content ID is required",
                "error": "Missing content ID",
            }

        content = video_exists_in_db(content_id)
        if not content:
            return {
                "success": False,
                "message": "Content not found",
                "error": f"No content found with ID {content_id}",
            }

        video_transcript = content.get("videoTranscript", None)

        if not video_transcript:
            return {
                "success": False,
                "message": "No video transcript found",
                "error": f"No video transcript found for content {content_id}",
            }

        video_description = content.get("videoDescription", None)

        update_content_is_parsed(content_id=content_id, is_parsed=False)

        add_content_activity(
            name="Summarising video content",
            content_id=content_id,
            activity_type="info",
            description="Summarising video content into main points",
        )

        summarise_text_and_add_to_content(
            video_content_id=content_id,
            long_text=video_transcript,
            video_description=video_description,
        )

        add_content_activity(
            name="Summarising done",
            content_id=content_id,
            activity_type="info",
            description="Summarising video content done",
        )

        related_content = retrieve_video_description_links_and_save(
            parent_content_id=content_id, video_description=video_description
        )

        related_contents = get_content_relationship(parent_content_id=content_id)
        for related_content in related_contents:
            child_content_id = related_content.get("childContentId", None)
            if child_content_id is None:
                continue
            title = related_content.get("child_content", {}).get("title", "")
            doi = related_content.get("child_content", {}).get("doiNumber", "")

            add_content_activity(
                name=f"Classifying evidence provided by author: {title} - {doi}",
                content_id=content_id,
                activity_type="info",
                description=f"Classifying evidence provided by author: {title} - {doi}",
            )
            classify_evidence(content_id=child_content_id)

            add_content_activity(
                name=f"Summarising: {title} - {doi}",
                content_id=content_id,
                activity_type="info",
                description=f"Summarising: {title} - {doi}",
            )
            summarise_text_and_add_to_content(
                video_content_id=child_content_id,
                long_text=video_transcript,
                video_description=video_description,
            )

            # connect_evidence_content_to_assertions(
            #     main_content_id=content_id, evidence_content_id=child_content_id
            # )

        add_content_activity(
            name="Extracting assertions started",
            content_id=content_id,
            activity_type="info",
            description="Extracting assertions from video content",
        )

        parse_assertions_long_text(
            content_id=content_id,
            long_text=video_transcript,
            additional_information=video_description,
        )

        add_content_activity(
            name="Extracting assertions done",
            content_id=content_id,
            activity_type="info",
            description="Extracting assertions from video content done",
        )
        update_content_aggregate_score(content_id)

        update_content_is_parsed(content_id=content_id, is_parsed=True)

        return {
            "success": True,
            "message": "Content analyzed successfully",
            "error": None,
        }

    except Exception as e:
        logger.error("Error in user_analyse_content_endpoint: %s", str(e))
        return {
            "success": False,
            "message": "Failed to analyze content",
            "error": str(e),
        }


def add_pro_against_assertions(content_id):
    """Add pro against assertions"""
    logger.warning(f"add_pro_against_assertions content_id: {content_id}")
    content_assertions = get_content_assertions(content_id=content_id)

    logger.info(f"content_assertions: {content_assertions}")

    for content_assertion in content_assertions:
        content_assertion_id = content_assertion["assertion"]["id"]
        title = content_assertion["assertion"]["text"]
        # logger.warning(f"content_assertion_id: {content_assertion_id}")
        add_content_activity(
            name=f"Searching for evidence for: {title}",
            content_id=content_id,
            activity_type="info",
            description=f"Searching for evidence for: {title}",
        )
        insert_assertions_opposing(assertion_id=content_assertion_id)
        update_assertion_score_by_id(content_assertion_id)
        update_content_aggregate_score(content_id)
        # break

    return "done"
