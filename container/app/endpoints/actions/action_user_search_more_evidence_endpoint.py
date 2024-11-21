""" User add content endpoint """

from ...config.logging import logger
from ...endpoints.assertions import insert_assertions_opposing, get_assertion_content
from ...endpoints.actions.action_update_assertion_score_endpoint import (
    update_assertion_score_by_id,
)
from ...scoring.update import update_content_aggregate_score


def action_user_search_more_evidence_endpoint(assertion_id):
    """Action to update assertion score"""
    return search_more_evidence(assertion_id)


def search_more_evidence(assertion_id):
    """Update assertion score for a given content"""
    try:
        logger.info("Starting search_more_evidence for assertion_id: %s", assertion_id)
        result = insert_assertions_opposing(assertion_id)
        # update assertion score
        update_assertion_score_by_id(assertion_id)
        # update content score
        assertion = get_assertion_content(assertion_id)
        content_id = assertion.get("contentId")
        update_content_aggregate_score(content_id)
        return result

    except Exception as e:
        logger.error("Failed to search_more_evidence: %s", str(e), exc_info=True)
        return {"error": str(e)}
