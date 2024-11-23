""" Module to calculate the evidence score for a given content_id """

from typing import Any, Dict
from ..utils.config import logger
from ..content_store.get_content import get_content_property_by_id


def evidence_score(content_id):
    """Calculate the evidence score for a given content_id"""
    science_paper_classification = get_content_property_by_id(
        content_id, "sciencePaperClassification"
    )
    # #logger.info("science_paper_classification: %s", science_paper_classification)
    if not science_paper_classification:
        logger.error(
            "No sciencePaperClassification found for content_id: %s", content_id
        )
        return {"totalScore": 0, "normalizedScore": 0}

    score = calculate_evidence_score(science_paper_classification)
    # #logger.info("scoring evidence for content_id: %s", content_id)
    # #logger.info("evidence score: %s", score)
    return score


def calculate_evidence_score(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the evidence score based on the provided payload"""
    # Handle case where payload is a list
    if isinstance(payload, list):
        logger.warning("Received list instead of dict for evidence scoring, using first item")
        if not payload:
            return {"totalScore": 0, "normalizedScore": 0}
        payload = payload[0]

    if not payload or not payload.get("studyClassification"):
        return {"totalScore": 0, "normalizedScore": 0}

    methodology = payload["studyClassification"].get("methodology", {})
    sample_size = methodology.get("sampleSize", 0)
    try:
        sample_size = int(sample_size) if sample_size is not None else 0
    except (ValueError, TypeError):
        sample_size = 0

    follow_up_duration = methodology.get("followUpDuration", "") or ""
    confounding_control = methodology.get("confoundingControl", "") or ""
    study_subjects = methodology.get("studySubjects", "").lower()

    # Study subjects multiplier (affects final score)
    subjects_multiplier = 1.0  # Default multiplier
    if "human" in study_subjects:
        subjects_multiplier = 1.0  # Full score for human studies
    elif "animal" in study_subjects:
        subjects_multiplier = 0.8  # 80% score for animal studies
    elif "in vivo" in study_subjects:
        subjects_multiplier = 0.6  # 60% score for in vivo studies

    methodology_scores = {
        "randomization": 20 if methodology.get("randomization") else 0,
        "blinding": 20 if methodology.get("blinding") else 0,
        "controlGroup": 20 if methodology.get("controlGroup") else 0,
        "sampleSize": (20 if sample_size > 200 else 10 if sample_size >= 50 else 0),
        "followUpDuration": (
            20
            if "year" in follow_up_duration
            else 10 if "month" in follow_up_duration else 0
        ),
        "confoundingControl": (
            20
            if "multivariate" in confounding_control
            else 10 if "stratification" in confounding_control else 0
        ),
    }
    methodology_total = sum(methodology_scores.values())

    statistical_analysis = payload["studyClassification"].get("statisticalAnalysis", {})
    statistical_significance = methodology.get("statisticalSignificance")

    # Add bonus for stricter statistical significance
    statistical_significance_bonus = 0
    try:
        if statistical_significance is not None:
            sig_value = float(statistical_significance)
            if sig_value <= 0.01:
                statistical_significance_bonus = 10
            elif sig_value <= 0.05:
                statistical_significance_bonus = 5
    except (ValueError, TypeError):
        logger.warning(
            f"Invalid statistical significance value: {statistical_significance}"
        )
        statistical_significance_bonus = 0

    statistical_analysis_scores = {
        "appropriateTests": 25 if statistical_analysis.get("appropriateTests") else 0,
        "effectSizeReported": (
            25 if statistical_analysis.get("effectSizeReported") else 0
        ),
        "confidenceIntervalsReported": (
            25 if statistical_analysis.get("confidenceIntervalsReported") else 0
        ),
        "pValuesReported": 25 if statistical_analysis.get("pValuesReported") else 0,
    }
    statistical_analysis_total = (
        sum(statistical_analysis_scores.values()) + statistical_significance_bonus
    )

    reporting_transparency = payload["studyClassification"].get(
        "reportingTransparency", {}
    )
    reporting_transparency_scores = {
        "researchQuestionsClear": (
            20 if reporting_transparency.get("researchQuestionsClear") else 0
        ),
        "detailedMethodology": (
            20 if reporting_transparency.get("detailedMethodology") else 0
        ),
        "conflictOfInterestDisclosed": (
            20 if reporting_transparency.get("conflictOfInterestDisclosed") else 0
        ),
        "replicationPossible": (
            20 if reporting_transparency.get("replicationPossible") else 0
        ),
        "dataAvailable": 20 if reporting_transparency.get("dataAvailable") else 0,
    }
    reporting_transparency_total = sum(reporting_transparency_scores.values())

    peer_review_publication = payload["studyClassification"].get(
        "peerReviewPublication", {}
    )
    journal_impact_factor = peer_review_publication.get("journalImpactFactor", "") or ""

    # Convert journal_impact_factor to float, handling string cases with '>' symbol
    if isinstance(journal_impact_factor, str):
        journal_impact_factor = float(
            journal_impact_factor.replace(">", "").strip() or 0
        )
    else:
        journal_impact_factor = float(journal_impact_factor or 0)

    peer_review_publication_scores = {
        "peerReviewedJournal": (
            50 if peer_review_publication.get("peerReviewedJournal") else 0
        ),
        "journalImpactFactor": (
            50
            if journal_impact_factor > 10
            else (
                30
                if journal_impact_factor > 5
                else (
                    20
                    if journal_impact_factor > 2
                    else (10 if journal_impact_factor > 1 else 0)
                )
            )
        ),
    }
    peer_review_publication_total = sum(peer_review_publication_scores.values())

    # Calculate weighted scores
    methodology_weight = 0.35
    statistical_analysis_weight = 0.25
    reporting_transparency_weight = 0.20
    peer_review_publication_weight = 0.20

    weighted_total = (
        methodology_total * methodology_weight
        + statistical_analysis_total * statistical_analysis_weight
        + reporting_transparency_total * reporting_transparency_weight
        + peer_review_publication_total * peer_review_publication_weight
    )

    # Apply study subjects multiplier to the final score
    final_score = weighted_total * subjects_multiplier

    return {
        "totalScore": final_score,
        "normalizedScore": min(100, max(0, final_score)),
        "details": {
            "methodologyScore": methodology_total,
            "statisticalAnalysisScore": statistical_analysis_total,
            "reportingTransparencyScore": reporting_transparency_total,
            "peerReviewPublicationScore": peer_review_publication_total,
            "studySubjectsMultiplier": subjects_multiplier,
            "statisticalSignificanceBonus": statistical_significance_bonus,
        },
    }
