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
    # logger.info("-------------update_assertion_score assertion_id: %s", assertion_id)
    score_tree = get_assertion_evidence_scores(assertion_id)

    # update evidence scores
    for contents_assertion in score_tree["contents_assertions"]:
        content_id = contents_assertion["content"]["id"]
        result = evidence_score(content_id)
        save_content_score(content_id, result["normalizedScore"])

    # update assertion score
    result = assertion_score(assertion_id)
    logger.info("---->>>assertion_score: %s", result)
    # logger.info(
    #     "assertion_id: %s, pro: %s, against: %s",
    #     assertion_id,
    #     result["pro"],
    #     result["against"],
    # )
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
    for assertion in assertion_tree.get("assertions", []):
        assertion_id = assertion["id"]
        update_assertion_score(assertion_id)
    score = calculate_aggregate_content_score(assertion_tree)
    # save aggregate score
    logger.info("---->>>aggregate_score: %s for content_id %s", score, content_id)
    save_aggregate_content_score(
        content_id, score_pro=score["pro"], score_against=score["against"]
    )
    return True
