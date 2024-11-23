"""This module contains the function to calculate the 
 aggregate score based on the provided content"""

from typing import Dict, Any, List
from ..utils.config import logger


def calculate_aggregate_content_score(
    assertion_tree: List[Dict[str, Any]]
) -> Dict[str, int]:
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

        # Normalize weight to be between 0.5 and 1.0
        weight = 0.5 + (weight_conclusion / 20)  # This ensures max weight is 1.0

        if pro > 0:
            weighted_score = min(
                100, pro * weight
            )  # Cap individual weighted scores at 100
            total_score_pro += weighted_score
            total_assertions_pro += 1
            additional_points_more_assertions_pro += additional_points

        if against > 0:
            weighted_score = min(
                100, against * weight
            )  # Cap individual weighted scores at 100
            total_score_against += weighted_score
            total_assertions_against += 1
            additional_points_more_assertions_against += additional_points

    final_score_pro = 0
    if total_assertions_pro > 0:
        average_score = total_score_pro / total_assertions_pro
        bonus_points = min(
            10, additional_points_more_assertions_pro
        )  # Cap bonus points at 10
        final_score_pro = min(
            100, average_score + bonus_points
        )  # Ensure final score never exceeds 100

    final_score_against = 0
    if total_assertions_against > 0:
        average_score = total_score_against / total_assertions_against
        bonus_points = min(
            10, additional_points_more_assertions_against
        )  # Cap bonus points at 10
        final_score_against = min(
            100, average_score + bonus_points
        )  # Ensure final score never exceeds 100

    logger.info(
        "Final scores - Pro: %s, Against: %s",
        final_score_pro,
        final_score_against,
    )

    return {
        "pro": round(max(0, final_score_pro)),
        "against": round(max(0, final_score_against)),
    }
