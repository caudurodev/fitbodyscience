""" User add content endpoint """

import json
from flask import jsonify
from ...config.logging import logger
from ...store.content import get_content_by_id, update_content_score
from ...scoring.evidence import calculate_evidence_score


def action_update_evidence_score_endpoint(content_id):
    """Update evidence score for a given content"""
    content = get_content_by_id(content_id)
    if not content:
        return jsonify({"message": "Content not found", "success": False}), 404

    full_score = calculate_evidence_score(content["sciencePaperClassification"])
    try:
        score = int(float(full_score["normalizedScore"]))
    except (ValueError, TypeError):
        score = 0
    logger.info(f"Content score: {score}")

    try:
        success = update_content_score(content_id, score)
        if not success:
            return jsonify({"message": "Error updating score", "success": False}), 500
            
        return jsonify({
            "message": "Content score updated successfully", 
            "success": True,
            "score": score
        }), 200
            
    except Exception as e:
        logger.error("Error updating content: %s", e)
        return jsonify({"message": f"Error updating content {str(e)}"}), 500
