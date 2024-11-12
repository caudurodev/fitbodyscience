""" Module to calculate the evidence score for a given content_id """

from typing import Any, Dict
from ..utils.config import logger
from ..content_store.get_content import get_content_property_by_id


def evidence_score(content_id):
    """Calculate the evidence score for a given content_id"""
    science_paper_classification = get_content_property_by_id(
        content_id, "science_paper_classification"
    )
    # #logger.info("science_paper_classification: %s", science_paper_classification)
    if not science_paper_classification:
        logger.error(
            "No science_paper_classification found for content_id: %s", content_id
        )
        return {"totalScore": 0, "normalizedScore": 0}

    score = calculate_evidence_score(science_paper_classification)
    # #logger.info("scoring evidence for content_id: %s", content_id)
    # #logger.info("evidence score: %s", score)
    return score


def calculate_evidence_score(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the evidence score based on the provided payload"""
    if not payload.get("studyClassification"):
        return {"totalScore": 0, "normalizedScore": 0}

    methodology = payload["studyClassification"].get("methodology", {})
    sample_size = methodology.get("sampleSize", 0)
    try:
        sample_size = int(sample_size)
    except (ValueError, TypeError):
        sample_size = 0

    follow_up_duration = methodology.get("followUpDuration", "") or ""
    confounding_control = methodology.get("confoundingControl", "") or ""

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
    statistical_analysis_total = sum(statistical_analysis_scores.values())

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
        "dataAvailable": 0,  # Data availability not provided in the payload, assuming 0
    }
    reporting_transparency_total = sum(reporting_transparency_scores.values())

    peer_review_publication = payload["studyClassification"].get(
        "peerReviewPublication", {}
    )
    journal_impact_factor = peer_review_publication.get("journalImpactFactor", "") or ""
    peer_review_publication_scores = {
        "peerReviewedJournal": (
            50 if peer_review_publication.get("peerReviewedJournal") else 0
        ),
        "journalImpactFactor": (
            30
            if journal_impact_factor == "High"
            else (
                20
                if journal_impact_factor == "Moderate"
                else 10 if journal_impact_factor else 0
            )
        ),
        "preRegistration": 20 if peer_review_publication.get("preRegistration") else 0,
    }
    peer_review_publication_total = sum(peer_review_publication_scores.values())

    external_validity = payload["studyClassification"].get("externalValidity", {})
    generalizability = external_validity.get("generalizability", "") or ""
    ecological_validity = external_validity.get("ecologicalValidity", "") or ""
    external_validity_scores = {
        "generalizability": (
            50
            if generalizability == "High"
            else 25 if generalizability == "Moderate" else 0
        ),
        "ecologicalValidity": (
            50
            if ecological_validity == "High"
            else 25 if ecological_validity == "Moderate" else 0
        ),
    }
    external_validity_total = sum(external_validity_scores.values())

    hierarchy_of_evidence_scores = {
        "Systematic Reviews and Meta-Analyses": 100,
        "Randomized Controlled Trials (RCTs)": 90,
        "Cohort Studies": 70,
        "Case-Control Studies": 60,
        "Cross-Sectional Studies": 50,
        "Case Reports and Case Series": 30,
        "Expert Opinion and Editorials": 10,
    }
    hierarchy_of_evidence_score = hierarchy_of_evidence_scores.get(
        payload["studyClassification"].get("hierarchyOfEvidence", ""), 0
    )

    total_score = (
        methodology_total
        + statistical_analysis_total
        + reporting_transparency_total
        + peer_review_publication_total
        + external_validity_total
        + hierarchy_of_evidence_score
    )

    normalized_score = (total_score / 600) * 100

    return {
        "methodologyScores": methodology_scores,
        "statisticalAnalysisScores": statistical_analysis_scores,
        "reportingTransparencyScores": reporting_transparency_scores,
        "peerReviewPublicationScores": peer_review_publication_scores,
        "externalValidityScores": external_validity_scores,
        "hierarchyOfEvidenceScore": hierarchy_of_evidence_score,
        "totalScore": total_score,
        "normalizedScore": normalized_score,
    }
