""" User add content endpoint """

from flask import jsonify
from ...config.logging import logger


def action_user_append_evidence_to_assertion_endpoint(assertion_id, content_url):
    """Analyze a scientific paper and save the data to the database"""
    try:
        logger.infor(
            "action_user_append_evidence_to_assertion_endpoint assertion_id: %s, content_url: %s",
            assertion_id,
            content_url,
        )

        return jsonify(
            {
                "message": f"Evidence appended to assertion {assertion_id} url {content_url}",
                "success": True,
            }
        )
    except Exception as e:
        logger.error("Error appending evidence to content: %s", e)
        return jsonify({"message": str(e), "success": False}), 500
