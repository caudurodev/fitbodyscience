"""Update the assertion score for a given assertion_id"""

from ..utils.config import logger
from ..content_store.assertion_store import get_assertion_evidence_scores
from ..content_store.get_content import get_content_assertion_tree
from ..content_store.score_store import (
    save_aggregate_assertion_score,
    save_content_score,
    save_aggregate_content_score,
)
from .evidence import evidence_score
from .assertion import assertion_score
from .aggregate import calculate_aggregate_content_score


def update_evidence_score(content_id):
    """Update the evidence score for a given content_id"""
    # logger.info("-------------update_evidence_score content_id: %s", content_id)
    result = evidence_score(content_id)
    # logger.info("---->>>evidence_score: %s", result)
    save_content_score(content_id, result["normalizedScore"])
    return True


def update_assertion_score(assertion_id):
    """Update the assertion score for a given assertion_id"""
    logger.info("Starting update_assertion_score for assertion_id: %s", assertion_id)
    score_tree = get_assertion_evidence_scores(assertion_id)

    if not score_tree or not isinstance(score_tree, list) or len(score_tree) == 0:
        logger.error("Invalid score_tree: %s", score_tree)
        return False

    # update evidence scores
    for contents_assertion in score_tree[0].get("contents_assertions", []):
        content = contents_assertion.get("content")
        if not content or not isinstance(content, dict):
            logger.error(
                "Invalid content in contents_assertion: %s", contents_assertion
            )
            continue

        content_id = content.get("id")
        if not content_id:
            logger.error("No content id found in: %s", content)
            continue

        logger.info("Updating evidence score for content_id: %s", content_id)
        result = evidence_score(content_id)
        save_content_score(content_id, result["normalizedScore"])

    # update assertion score
    result = assertion_score(assertion_id)
    logger.info("Assertion score result: %s", result)

    save_aggregate_assertion_score(
        assertion_id, score_pro=result["pro"], score_against=result["against"]
    )
    return True


def update_content_aggregate_score(content_id):
    """
    Update the aggregate score for a given content_id
    updates down the tree
    """
    logger.info("-------------Updating aggregate score for content_id: %s", content_id)
    assertion_tree = get_content_assertion_tree(content_id)
    logger.info("---->>>assertion_tree: %s", assertion_tree)

    if not assertion_tree or not isinstance(assertion_tree, list):
        logger.error("Invalid assertion tree structure: %s", assertion_tree)
        return False

    for assertion_content in assertion_tree:
        if not isinstance(assertion_content, dict):
            logger.error("Invalid assertion content structure: %s", assertion_content)
            continue

        assertion = assertion_content.get("assertion")
        if not assertion or not isinstance(assertion, dict):
            logger.error("Invalid assertion structure: %s", assertion_content)
            continue

        assertion_id = assertion.get("id")
        if not assertion_id:
            logger.error("No assertion id found in: %s", assertion)
            continue

        logger.info("Updating assertion score for assertion_id: %s", assertion_id)
        update_assertion_score(assertion_id)

    score = calculate_aggregate_content_score(assertion_tree)
    # save aggregate score
    logger.info("---->>>aggregate_score: %s for content_id %s", score, content_id)
    save_aggregate_content_score(
        content_id, score_pro=score["pro"], score_against=score["against"]
    )
