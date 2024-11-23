""" User add content endpoint """

from ...config.logging import logger
from ...scoring.assertion import calculate_assertion_score
from ...scoring.assertion import get_assertion_evidence_scores
from ...scoring.update import update_assertion_score
from ...store.content_activity import add_content_activity


def action_update_assertion_score_endpoint(assertion_id):
    """Action to update assertion score"""
    return update_assertion_score_by_id(assertion_id)


def update_assertion_score_by_id(assertion_id):
    """Update assertion score for a given content"""
    try:
        logger.info("Starting score update for assertion_id: %s", assertion_id)

        assertion_evidence = get_assertion_evidence_scores(assertion_id)
        # logger.info("Raw assertion evidence data: %s", assertion_evidence)

        if not assertion_evidence:
            logger.error("No assertion evidence found for id: %s", assertion_id)
            return {"error": "No assertion evidence found"}

        if not isinstance(assertion_evidence, list):
            logger.error(
                "Expected list but got %s: %s",
                type(assertion_evidence),
                assertion_evidence,
            )
            return {"error": "Invalid assertion evidence format"}

        content_id = assertion_evidence[0]["contentId"]
        logger.info("assertion_evidence Content id: %s", content_id)

        score = calculate_assertion_score(assertion_evidence)
        logger.info("Calculated score: %s", score)

        update_assertion_score(assertion_id=assertion_id)
        logger.info("Successfully updated assertion score")

        notification_text = f"Update Assertion score to Pro score: {score['pro']} against score: {score['against']}"
        add_content_activity(
            content_id=content_id,
            name=notification_text,
            description=notification_text,
        )

        return score

    except Exception as e:
        logger.error("Failed to update assertion score: %s", str(e), exc_info=True)
        return {"error": str(e)}
