"""This module contains the function to calculate the 
 aggregate score based on the provided content"""

from typing import Dict, Any, List
from ..utils.config import logger


def calculate_aggregate_content_score(assertion_tree: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate the aggregate score based on the provided content"""
    additional_points = 1

    total_score_pro = 0
    total_assertions_pro = 0
    additional_points_more_assertions_pro = 0

    total_score_against = 0
    total_assertions_against = 0
    additional_points_more_assertions_against = 0

    for assertion_content in assertion_tree:
        assertion = assertion_content.get("assertion", {})
        weight_conclusion = assertion.get("assertions_contents", [{}])[0].get(
            "weightConclusion", 0
        )

        pro = assertion.get("proEvidenceAggregateScore", 0) or 0
        against = assertion.get("againstEvidenceAggregateScore", 0) or 0

        max_weight = 10
        multiplier = 1 + (max_weight - weight_conclusion) / max_weight
        weigh_assertion_to_main_argument = ((multiplier - 1) / 2) + 1

        if pro > 0:
            total_score_pro += pro * weigh_assertion_to_main_argument
            total_assertions_pro += 1
            additional_points_more_assertions_pro += additional_points

        if against > 0:
            total_score_against += against * weigh_assertion_to_main_argument
            total_assertions_against += 1
            additional_points_more_assertions_against += additional_points

    final_score_pro = 0
    if total_assertions_pro > 0:
        final_score_pro = (
            total_score_pro / total_assertions_pro
        ) + additional_points_more_assertions_pro

    final_score_against = 0
    if total_assertions_against > 0:
        final_score_against = (
            total_score_against / total_assertions_against
        ) + additional_points_more_assertions_against

    logger.info(
        "Final scores - Pro: %s, Against: %s",
        final_score_pro,
        final_score_against,
    )

    return {
        "pro": round(max(0, min(100, final_score_pro))),
        "against": round(max(0, min(100, final_score_against))),
    }
