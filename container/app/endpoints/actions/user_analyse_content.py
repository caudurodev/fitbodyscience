""" User add content endpoint """

from ...config.logging import logger
from ...content_store.youtube_store import video_exists_in_db
from ...meaning.summarize import summarise_text_and_add_to_content
from ...content_store.assertion_store import parse_assertions_long_text
from ...store.content import update_content_is_parsed
from ...store.content_relationship import get_content_relationship
from ...store.assertions_content import get_content_assertions
from ...endpoints.actions.action_user_classify_evidence_endpoint import (
    classify_evidence,
)
from ...scoring.update import update_content_aggregate_score
from ...endpoints.actions.action_update_assertion_score_endpoint import (
    update_assertion_score_by_id,
)
from ...endpoints.assertions import insert_assertions_opposing
from ...utils.run_async import run_method_async


def user_analyse_content_endpoint(content_id):
    """Analyze a scientific paper and save the data to the database"""
    try:
        content = video_exists_in_db(content_id)
        if not content:
            logger.error(f"Content not found for id {content_id}")
            return

        video_transcript = content.get("videoTranscript")
        video_description = content.get("videoDescription")

        if not video_transcript:
            logger.error(f"No video transcript found for content {content_id}")
            return

        update_content_is_parsed(content_id=content_id, is_parsed=False)

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

        # evaluate evidence
        # get all related content
        related_contents = get_content_relationship(parent_content_id=content_id)
        logger.info(f"related_contents: {related_contents}")
        for related_content in related_contents:
            child_content_id = related_content["childContentId"]
            logger.info(f"classify_evidence for related content {child_content_id}")
            classify_evidence(content_id=child_content_id)

        # get opposing viewpoints
        run_method_async(add_pro_against_assertions, content_id)

        # get opposing viewpoints

        update_content_is_parsed(content_id=content_id, is_parsed=True)

        logger.info(f"Finished analyzing content {content_id}")
    except Exception as e:
        logger.error(f"Error analyzing content {content_id}: {str(e)}")


def add_pro_against_assertions(content_id):
    """Add pro against assertions"""
    logger.warning(f"add_pro_against_assertions content_id: {content_id}")
    content_assertions = get_content_assertions(content_id=content_id)

    logger.info(f"content_assertions: {content_assertions}")

    for content_assertion in content_assertions:
        content_assertion_id = content_assertion["assertion"]["id"]
        logger.warning(f"content_assertion_id: {content_assertion_id}")
        insert_assertions_opposing(assertion_id=content_assertion_id)
        update_assertion_score_by_id(content_assertion_id)
        update_content_aggregate_score(content_id)
        break

    return "done"
