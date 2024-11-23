""" User add content endpoint """

import json
from flask import jsonify
from ...config.logging import logger
from ...store.content import get_content_by_id, update_content_score
from ...scoring.evidence import calculate_evidence_score
from ...content_store.science_paper import update_science_paper_classification_content
from ...content_get.classify_study import classify_evidence_content
from ...store.content_activity import add_content_activity


def action_update_evidence_score_endpoint(content_id):
    """Update evidence score for a given content"""
    content = get_content_by_id(content_id)
    if not content:
        return jsonify({"message": "Content not found", "success": False}), 404

    science_paper_classification = content.get("sciencePaperClassification")
    if not science_paper_classification:
        science_paper_classification = classify_evidence_content(content_id=content_id)
    try:
        add_content_activity(
            content_id=content_id,
            name="Update evidence score",
            description="Updating evidence score",
        )
        update_science_paper_classification_content(
            content_id=content_id, classification_jsonb=science_paper_classification
        )
    except Exception as e:
        logger.error("Error updating content: %s", e)
        return jsonify({"message": f"Error updating content {str(e)}"}), 500

    full_score = calculate_evidence_score(science_paper_classification)
    try:
        score = int(float(full_score["normalizedScore"]))
    except (ValueError, TypeError):
        score = 0
    logger.info(f"Content score: {score}")

    try:
        success = update_content_score(content_id, score)
        if not success:
            return jsonify({"message": "Error updating score", "success": False}), 500

        return (
            jsonify(
                {
                    "message": "Content score updated successfully",
                    "success": True,
                    "score": score,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Error updating content: %s", e)
        return jsonify({"message": f"Error updating content {str(e)}"}), 500
