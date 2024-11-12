"""This module contains the function to calculate the
 aggregate score based on the provided content"""

from typing import Dict, Any
from ..utils.config import logger


def calculate_aggregate_content_score(main_content: Dict[str, Any]) -> Dict[str, int]:
    """Calculate the aggregate score based on the provided content"""
    additional_points = 1

    total_score_pro = 0
    total_assertions_pro = 0
    additional_points_more_assertions_pro = 0

    total_score_against = 0
    total_assertions_against = 0
    additional_points_more_assertions_against = 0

    for assertion in main_content.get("assertions", []):
        weight_conclusion = assertion.get("assertions_contents", [{}])[0].get(
            "weight_conclusion", 0
        )

        pro = assertion.get("pro_evidence_aggregate_score", 0) or 0
        against = assertion.get("against_evidence_aggregate_score", 0) or 0

        # logger.info("calculate_aggregate_content_score:  against: %s", against)

        max_weight = 10
        multiplier = 1 + (max_weight - weight_conclusion) / max_weight
        weigh_assertion_to_main_argument = ((multiplier - 1) / 2) + 1

        # logger.info("calculate_aggregate_content_score: weigh_assertion_to_main_argument: %s", weigh_assertion_to_main_argument)

        if pro > 0:
            total_score_pro += pro * weigh_assertion_to_main_argument
            total_assertions_pro += 1
            additional_points_more_assertions_pro += additional_points

        if against > 0:
            # logger.info("calculate_aggregate_content_score: add against: %s", against)
            total_score_against += against * weigh_assertion_to_main_argument
            total_assertions_against += 1
            additional_points_more_assertions_against += additional_points
            # logger.info(
            #     "calculate_aggregate_content_score: add total_assertions_against: %s",
            #     total_assertions_against,
            # )

    # logger.info(
    #     "calculate_aggregate_content_score: total_score_pro: %s, total_assertions_pro: %s, additional_points_more_assertions_pro: %s",
    #     total_score_pro,
    #     total_assertions_pro,
    #     additional_points_more_assertions_pro,
    # )

    # logger.info(
    #     "calculate_aggregate_content_score: total_score_against: %s, total_assertions_against: %s, additional_points_more_assertions_against: %s",
    #     total_score_against,
    #     total_assertions_against,
    #     additional_points_more_assertions_against,
    # )

    aggregate_score_pro = (
        (total_score_pro / total_assertions_pro + additional_points_more_assertions_pro)
        if total_assertions_pro > 0
        else 0
    )
    aggregate_score_against = (
        (
            total_score_against / total_assertions_against
            + additional_points_more_assertions_against
        )
        if total_assertions_against > 0
        else 0
    )

    return {
        "pro": round(max(0, min(100, aggregate_score_pro))),
        "against": round(max(0, min(100, aggregate_score_against))),
    }
