""" This module contains the functions to calculate the assertion score based on the provided evidences. """

from typing import List, Dict, Any
from ..utils.config import logger
from ..content_store.assertion_store import get_assertion_evidence_scores
from .evidence import calculate_evidence_score


def assertion_score(assertion_id: str) -> Dict[str, int]:
    """Calculate the evidence score for a given content_id"""
    assertion_evidence = get_assertion_evidence_scores(assertion_id)
    # #logger.info("assertion_evidence: %s", assertion_evidence)
    score = calculate_assertion_score(assertion_evidence)
    return score


def calculate_from_evidences_score(evidences: List[Dict[str, Any]]) -> float:
    """Calculate the score from a list of evidences"""
    if not evidences:
        # logger.info("No evidences found.")
        return 0

    valid_evidences = [
        evidence
        for evidence in evidences
        if isinstance(evidence, dict)
        and calculate_evidence_score(evidence).get("normalizedScore") is not None
    ]
    highest_score = 0

    for evidence in valid_evidences:
        normalized_score = calculate_evidence_score(evidence).get("normalizedScore", 0)
        if normalized_score > highest_score:
            highest_score = normalized_score

    distinct_evidence_types = len(
        set(
            evidence.get("studyClassification", {}).get("type", "")
            for evidence in valid_evidences
        )
    )
    additional_points = 0
    if distinct_evidence_types > 0:
        additional_points = (distinct_evidence_types - 1) * 5

    # logger.info(
    # "Highest score: %s, Additional points: %s", highest_score, additional_points
    # )
    return highest_score + additional_points


def calculate_assertion_score(assertion: Dict[str, Any]) -> Dict[str, int]:
    """Calculate the assertion score based on the provided evidences"""

    supporting_evidences = []
    contradicting_evidences = []

    for content in assertion[0].get("contents_assertions", []):
        is_pro = content.get("isProAssertion")

        if isinstance(content.get("content"), dict):
            if content["content"].get("sciencePaperClassification") is not None:
                classification = content["content"]["sciencePaperClassification"]

                if is_pro is True:
                    supporting_evidences.append(classification)
                elif is_pro is False:
                    contradicting_evidences.append(classification)
                else:
                    logger.error("isProAssertion is neither True nor False: %s", is_pro)
            else:
                logger.warn(
                    f"No sciencePaperClassification found in content. {content}"
                )
        else:
            logger.error("Content is not a dictionary: %s", content.get("content"))

    supporting_score = calculate_from_evidences_score(supporting_evidences)
    contradicting_score = calculate_from_evidences_score(contradicting_evidences)

    return {
        "pro": round(max(0, min(100, supporting_score))),
        "against": round(max(0, min(100, contradicting_score))),
    }
