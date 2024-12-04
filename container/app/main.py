"""Main file for the Flask app."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from .config.logging import logger
from .endpoints.get_channel_data import upsert_influencer_endpoint
from .utils.auth.user import require_auth, require_role
from .utils.validators import validate_input
from .endpoints.actions.user_analyse_content import (
    user_analyse_content_endpoint,
    add_pro_against_assertions,
)
from .endpoints.actions.user_add_content import user_add_content_endpoint
from .endpoints.actions.action_user_classify_evidence_endpoint import (
    action_user_classify_evidence_endpoint,
)
from .endpoints.actions.action_update_assertion_score_endpoint import (
    action_update_assertion_score_endpoint,
)
from .endpoints.actions.action_update_evidence_score_endpoint import (
    action_update_evidence_score_endpoint,
)
from .endpoints.actions.action_user_search_more_evidence_endpoint import (
    action_user_search_more_evidence_endpoint,
)
from .endpoints.actions.action_user_append_evidence_to_assertion_endpoint import (
    action_user_append_evidence_to_assertion_endpoint,
)
from .utils.run_async import run_method_async
from .scoring.update import update_content_aggregate_score
from .store.assertions_content import get_content_assertions
from .store.content import remove_content_and_relations_by_id

app = Flask(__name__)
CORS(app)


@app.route("/action_user_add_content", methods=["POST"])
@require_auth
@require_role("pro")
@validate_input(
    required_fields=["url"],
    optional_fields=["mediaType", "contentType"],
    payload_key="input",
)
def action_user_add_content_method(input_data):
    """Action to add user content"""
    try:
        response = user_add_content_endpoint(
            content_url=input_data["url"], content_type=input_data["contentType"]
        )
        logger.info("response: %s", response)
        new_content_id = response.get("content_id", None)

        run_method_async(user_analyse_content_endpoint, new_content_id)
        return (
            jsonify(
                {
                    "message": response["message"],
                    "slug": response["slug"],
                    "success": response["success"],
                }
            ),
            200,
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify({"message": f"Error adding content {str(e)}", "success": False}),
            500,
        )


@app.route("/action_user_remove_content", methods=["POST"])
@require_auth
@require_role("pro")
@validate_input(
    required_fields=["contentId"],
    payload_key="input",
)
def action_user_remove_content_method(input_data):
    """Action to add user content"""
    try:
        # logger.info(f"action_user_remove_content_method user_role: {user_role}")
        logger.info(f"action_user_remove_content_method input_data: {input_data}")
        response = remove_content_and_relations_by_id(
            content_id=input_data["contentId"]
        )
        logger.info("response: %s", response)
        return (
            jsonify(
                {
                    "message": "Content removed",
                    "success": True,
                }
            ),
            200,
        )
    except Exception as e:
        logger.error("Error removing content %s", e)
        return (
            jsonify({"message": f"Error removing content {str(e)}", "success": False}),
            500,
        )


@app.route("/action_user_analyse_content", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["contentId"],
    payload_key="input",
)
def action_analyse_content_method(input_data):
    """Action to add user content"""
    try:
        result = user_analyse_content_endpoint(content_id=input_data["contentId"])
        return jsonify(result), 200
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify({"message": f"Error adding content {str(e)}", "success": False}),
            500,
        )


@app.route("/action_user_classify_evidence", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["contentId"],
    payload_key="input",
)
def action_user_classify_evidence_method(input_data):
    """Action to add user content"""
    try:
        return action_user_classify_evidence_endpoint(
            content_id=input_data["contentId"]
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify({"message": f"Error adding content {str(e)}", "success": False}),
            500,
        )


@app.route("/action_user_append_evidence_to_assertion", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["assertionId", "contentUrl"],
    payload_key="input",
)
def action_user_append_evidence_to_assertion_method(input_data):
    """Action to add user content"""
    try:
        return action_user_append_evidence_to_assertion_endpoint(
            assertion_id=input_data["assertionId"],
            content_url=input_data["contentUrl"],
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify({"message": f"Error adding content {str(e)}", "success": False}),
            500,
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify({"message": f"Error adding content {str(e)}", "success": False}),
            500,
        )


@app.route("/action_update_evidence_score", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["contentId"],
    payload_key="input",
)
def action_update_evidence_score_method(input_data):
    """Action to add user content"""
    try:
        action_update_evidence_score_endpoint(content_id=input_data["contentId"])
        return (
            jsonify({"message": "Content score updated", "success": True}),
            200,
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify({"message": f"Error adding content {str(e)}", "success": False}),
            500,
        )


@app.route("/action_user_search_more_evidence", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["assertionId"],
    payload_key="input",
)
def action_user_search_more_evidence_method(input_data):
    """Action to add user content"""
    try:
        action_user_search_more_evidence_endpoint(
            assertion_id=input_data["assertionId"]
        )
        return (
            jsonify({"message": "Assertion evidence searched", "success": True}),
            200,
        )
    except Exception as e:
        logger.error("Error searching for more evidence %s", e)
        return (
            jsonify(
                {
                    "message": f"Error searching for more evidence {str(e)}",
                    "success": False,
                }
            ),
            500,
        )


@app.route("/action_update_assertion_score", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["assertionId"],
    payload_key="input",
)
def action_update_assertion_score_method(input_data):
    """Action to add user content"""
    try:
        return action_update_assertion_score_endpoint(
            assertion_id=input_data["assertionId"]
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify({"message": f"Error adding content {str(e)}", "success": False}),
            500,
        )


@app.route("/action_update_assertions_score", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["contentId"],
    payload_key="input",
)
def action_update_assertions_score_method(input_data):
    """Action to add user content"""
    try:
        result = add_pro_against_assertions(content_id=input_data["contentId"])
        logger.info("action_update_assertions_score_method result: %s", result)
        return (
            jsonify({"message": "Content score updated", "success": True}),
            200,
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        return (
            jsonify(
                {
                    "message": f"Error action_update_assertion_score_method {str(e)}",
                    "success": False,
                }
            ),
            500,
        )


@app.route("/on_update_content", methods=["POST"])
def on_update_content_endpoint():
    """When content is updated, recalculate scores"""
    try:
        data = request.get_json()
        event_data = data.get("event", {}).get("data", {})
        new_data = event_data.get("new", None)
        old_data = event_data.get("old", None)

        content_id = new_data.get("id") if new_data else None
        new_score = new_data.get("contentScore") if new_data else None
        old_score = old_data.get("contentScore") if old_data else None

        logger.info("content_id: %s", content_id)
        logger.info("new_score: %s", new_score)
        logger.info("old_score: %s", old_score)

        if content_id is None:
            return (
                jsonify({"message": "Error: no content_id provided", "success": False}),
                400,
            )

        if new_score is None:
            return jsonify({"message": "No score update needed", "success": True}), 200

        if new_score == old_score:
            return jsonify({"message": "No change in score", "success": True}), 200

        # Recalculate scores
        try:
            assertions = get_content_assertions(content_id)
            if assertions:
                for assertion in assertions:
                    assertion_id = assertion.get("assertion", {}).get("id")
                    if assertion_id:
                        add_pro_against_assertions(assertion_id)
            return jsonify({"message": "Content scores updated", "success": True}), 200
        except Exception as e:
            logger.error("Error updating scores: %s", str(e))
            return (
                jsonify(
                    {"message": f"Error updating scores: {str(e)}", "success": False}
                ),
                500,
            )

    except Exception as e:
        logger.error("Error in on_update_content: %s", str(e))
        return jsonify({"message": f"Error: {str(e)}", "success": False}), 500


@app.route("/recalculate_aggregate_score", methods=["POST"])
def recalculate_aggregate_score_endpoint():
    """Test method for recalculate_aggregate_score hasura action"""
    data = request.get_json()
    logger.info("recalculate_aggregate_score data %s", data)
    content_id = data.get("input", {}).get("contentId", None)
    logger.info("content_id: %s", content_id)
    if content_id is None:
        return (
            jsonify(
                {
                    "success": False,
                }
            ),
            400,
        )
    update_content_aggregate_score(content_id)
    return (
        jsonify(
            {
                "success": True,
            }
        ),
        200,
    )


@app.route("/get_yt_channel", methods=["POST"])
@validate_input(
    required_fields=["url"],
    payload_key="",
)
def get_yt_channel_endpoint(input_data):
    """Test method for get_yt_channel"""
    channel_url = input_data.get("url", None)
    logger.info("channel_url: %s", channel_url)

    result = upsert_influencer_endpoint(channel_url)

    return jsonify(result)


@app.route("/", methods=["GET", "POST"])
def hello():
    """Test method for the server"""
    return "sup"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
