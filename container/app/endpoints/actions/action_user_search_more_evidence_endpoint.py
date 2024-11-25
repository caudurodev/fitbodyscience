""" User add content endpoint """

from ...config.logging import logger
from ...endpoints.assertions import insert_assertions_opposing, get_assertion_content
from ...endpoints.actions.action_update_assertion_score_endpoint import (
    update_assertion_score_by_id,
)
from ...scoring.update import update_content_aggregate_score
from ...store.content_activity import add_content_activity


def action_user_search_more_evidence_endpoint(assertion_id):
    """Action to update assertion score"""
    return search_more_evidence(assertion_id)


def search_more_evidence(assertion_id):
    """Update assertion score for a given content"""
    try:
        logger.info("Starting search_more_evidence for assertion_id: %s", assertion_id)
        assertion = get_assertion_content(assertion_id)
        content_id = assertion.get("contentId")

        add_content_activity(
            name="Searching for more evidence",
            content_id=content_id,
            activity_type="info",
            description="Started Searching for more evidence",
        )

        result = insert_assertions_opposing(assertion_id)
        # update assertion score
        update_assertion_score_by_id(assertion_id)
        # update content score
        assertion = get_assertion_content(assertion_id)
        content_id = assertion.get("contentId")
        add_content_activity(
            name="Searched more evidence",
            content_id=content_id,
            activity_type="info",
            description="Finished Searching for more evidence",
        )
        update_content_aggregate_score(content_id)
        return result

    except Exception as e:
        logger.error("Failed to search_more_evidence: %s", str(e), exc_info=True)
        return {"error": str(e)}
