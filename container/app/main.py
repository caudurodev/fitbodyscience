"""Main file for the Flask app."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from .config.logging import logger
from .endpoints.get_channel_data import upsert_influencer_endpoint
from .content_store.error import content_parse_error
from .content_store.assertion_store import get_assertion_parent_content_ids
from .scoring.update import update_assertion_score, update_content_aggregate_score
from .endpoints.science_paper import analyse_science_paper
from .endpoints.youtube_videos import analyze_youtube_video
from .endpoints.website_page import analyse_website_page
from .endpoints.assertions import insert_assertions_opposing
from .video.get_yt_channel_data import get_channel_url_from_video
from .store.content import upsert_content
from .content_get.youtube_video import get_youtube_video_data
from .store.slug import generate_slug

from .utils.auth.user import require_auth
from .utils.validators import validate_input
from .content_store.assertion_store import (
    get_content_assertion_ids,
    get_assertion_content_ids,
)
from .scoring.update import update_evidence_score
from .video.youtube import get_clean_youtube_url
from .store.content import update_content_source_url, get_content_by_url

# from .graphdb.main import create_dummy_data, read_data


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def hello():
    """Test method for the server"""
    return "Hello World3!"


@app.route("/action_user_add_content", methods=["POST"])
@require_auth
@validate_input(
    required_fields=["url"],
    optional_fields=["mediaType", "contentType"],
    payload_key="input",
)
@validate_input(
    required_fields=["x-hasura-user-id", "x-hasura-role"],
    payload_key="session_variables",
)
def action_user_add_content_method(input_data, session_variables_data):
    """Action to add user content"""
    logger.info("action_user_add_content_method")
    logger.info("input_data: %s", input_data)
    logger.info("session_variables_data: %s", session_variables_data)
    try:
        cleaned_url = get_clean_youtube_url(input_data["url"])
        if cleaned_url is None:
            return (
                jsonify(
                    {
                        "message": "error",
                        "success": False,
                    }
                ),
                200,
            )
        try:
            content_saved = get_content_by_url(cleaned_url)
            if content_saved is not None:
                return (
                    jsonify(
                        {
                            "message": "Content already exists",
                            "slug": content_saved["slug"],
                            "success": True,
                        }
                    ),
                    200,
                )
        except Exception:
            logger.info("Content not found, adding content")

        influencer_id = None
        channel_url = get_channel_url_from_video(cleaned_url)
        if channel_url:
            influencer_id = upsert_influencer_endpoint(channel_url)

        if influencer_id is None:
            logger.error("Error upserting influencer")
            return (
                jsonify(
                    {
                        "message": "Error getting influencer id",
                        "success": False,
                    }
                ),
                500,
            )

        video_data = get_youtube_video_data(cleaned_url)
        if video_data is not None:
            return (
                jsonify(
                    {
                        "message": "Error getting video data",
                        "success": False,
                    }
                ),
                500,
            )
        slug = generate_slug(video_data["video_info"]["title"])
        logger.info("slug: %s", slug)

        upsert_content(
            video_title=video_data["video_info"]["title"],
            video_id=video_data["video_info"]["display_id"],
            video_url=input_data["url"],
            content_type=input_data["contentType"],
            canonical_url=cleaned_url,
            transcript=video_data["transcript"],
            video_description=video_data["video_info"]["description"],
            full_text_transcript=video_data["full_text_transcript"],
            slug=slug,
        )
        # result = analyze_youtube_video(video_data, influencer_id)

        return (
            jsonify(
                {
                    "message": "success",
                    "slug": slug,
                    "success": True,
                }
            ),
            200,
        )
    except Exception as e:
        logger.error("Error adding content %s", e)
        logger.info("input_data: %s", input_data)
        return jsonify({"message": f"Error adding content {str(e)}"}), 500


# @app.route("/on_insert_content", methods=["POST"])
# def on_insert_content_endpoint():
#     """When content is added, get extra information and classify when possible"""
#     data = request.get_json()
#     # #logger.info("on_insert_content data %s", data)
#     if data is None:
#         logger.error("No data provided")
#         return (
#             jsonify(
#                 {
#                     "message": "Error: no data provided",
#                 }
#             ),
#             400,
#         )
#     else:
#         new_data = data["event"]["data"]["new"]
#         content_id = new_data["id"]
#         media_type = new_data["media_type"]
#         content_type = new_data["content_type"]
#         is_parsed = new_data["is_parsed"]
#         if is_parsed:
#             # #logger.info("Content already parsed, skipping...")
#             return (
#                 jsonify(
#                     {
#                         "message": "Content already parsed, skipping...",
#                     }
#                 ),
#                 200,
#             )
#         # #logger.info("Content not parsed, processing...")

#         if content_type == "youtube_video":
#             # #logger.info("media_type: youtube_video")
#             logger.info("new_data.get('source_url'): %s", new_data.get("source_url"))
#             cleaned_url = get_clean_youtube_url(new_data.get("source_url"))
#             logger.info("cleaned_url: %s", cleaned_url)

#             if cleaned_url is None:
#                 logger.error("Error cleaning YouTube URL")
#                 return (
#                     jsonify(
#                         {
#                             "message": "Error cleaning YouTube URL",
#                         }
#                     ),
#                     500,
#                 )
#             if cleaned_url != new_data.get("source_url"):
#                 update_content_source_url(content_id, cleaned_url)
#             # add influencer if not in db
#             influencer_id = None
#             channel_url = get_channel_url_from_video(cleaned_url)
#             if channel_url:
#                 influencer_id = upsert_influencer_endpoint(channel_url)

#             if influencer_id is None:
#                 logger.error("Error upserting influencer")
#                 return (
#                     jsonify(
#                         {
#                             "message": "Error getting influencer id",
#                         }
#                     ),
#                     500,
#                 )
#             result = analyze_youtube_video(content_id, influencer_id)
#             if result["server_response"] != 200:
#                 content_parse_error(content_id, result["message"])
#             return (
#                 jsonify(
#                     {
#                         "message": str(result["message"]),
#                     }
#                 ),
#                 result["server_response"],
#             )
#         if new_data.get("doi_number") is not None:
#             content_id = analyse_science_paper(content_id)
#             update_evidence_score(content_id)
#             if content_id is None:
#                 content_parse_error(content_id, "Error parsing content")
#                 return (
#                     jsonify(
#                         {
#                             "message": "Error parsing content",
#                         }
#                     ),
#                     500,
#                 )
#         if new_data.get("source_url") is not None:
#             if media_type == "text":
#                 # logger.info("media_type: text")
#                 analyse_website_page(content_id)
#                 return (
#                     jsonify(
#                         {
#                             "message": "Content Parsed.",
#                             "content_id": content_id,
#                         }
#                     ),
#                     200,
#                 )
#         return (
#             jsonify(
#                 {
#                     "message": "Unknown media type",
#                 }
#             ),
#             400,
#         )


@app.route("/on_insert_assertion", methods=["POST"])
def get_opposing_viewpoints_endpoint():
    """Test method for extract_content_data_endpoint"""
    data = request.get_json()
    new_data = data["event"]["data"]["new"]
    assertion_id = new_data["id"]

    # logger.info("assertion_id: %s", assertion_id)
    if assertion_id is None:
        return (
            jsonify(
                {
                    "message": "Error: no assertion_id provided",
                }
            ),
            400,
        )

    try:
        result = insert_assertions_opposing(assertion_id)
        # result = "skip"
        return jsonify(
            {
                "message": "assertion.",
                "assertion_id": assertion_id,
                "result": result,
            }
        )
    except Exception as e:
        logger.error("Error insert_assertions_opposing result: %s", e)
        return (
            jsonify(
                {
                    "message": "Error insert_assertions_opposing result",
                }
            ),
            500,
        )


@app.route("/on_update_content", methods=["POST"])
def on_update_content_endpoint():
    """Test method for extract_content_data_endpoint"""
    logger.info("-------------on_update_content_endpoint...")
    data = request.get_json()

    # Ensure the data structure is as expected
    event_data = data.get("event", {}).get("data", {})
    new_data = event_data.get("new", None)
    old_data = event_data.get("old", None)

    # Extract values with defaulting to None if they do not exist
    content_id = new_data.get("id") if new_data else None
    new_score = new_data.get("content_score") if new_data else None
    old_score = old_data.get("content_score") if old_data else None

    logger.info("content_id: %s", content_id)
    logger.info("new_score: %s", new_score)
    logger.info("old_score: %s", old_score)

    # Log warnings if critical data is missing
    if content_id is None:
        logger.warning("content_id is missing")

    # logger.info("updating content aggregate score")
    # update_content_aggregate_score(content_id)

    if new_score is None:
        logger.warning("new_score is missing")
    if old_score is None:
        logger.warning("old_score is missing")

    if content_id is None or new_score is None:
        return (
            jsonify(
                {
                    "message": "Error: on_update_content_endpoint no content_id provided",
                }
            ),
            400,
        )

    if new_score == old_score:
        return (
            jsonify(
                {
                    "message": "on_update_content_endpoint No change in score or no score.",
                }
            ),
            200,
        )

    try:
        # logger.info("getting assertionis for content_id %s", content_id)
        assertions = get_content_assertion_ids(content_id)
        # logger.info("assertions: %s", assertions)
        if len(assertions) == 0 or assertions is None:
            return (
                jsonify(
                    {
                        "message": "No assertion_ids found for content_id",
                    }
                ),
                404,
            )
        for assertion in assertions:
            # logger.info("update assertion id %s", assertion)
            update_assertion_score(assertion["assertion_id"])
            # logger.info("content updated")

        for assertion in assertions:
            # get parent content_ids to assertion
            parent_content_ids = get_assertion_parent_content_ids(
                assertion["assertion_id"]
            )
            for parent_content_id in parent_content_ids:
                parent_content_id = parent_content_id["content_id"]
                logger.info("parent_content_id: %s", parent_content_id)
                update_content_aggregate_score(parent_content_id)

        return jsonify(
            {
                "message": "assertion scores updated.",
            }
        )
    except Exception as e:
        logger.error("Error on_update_content_endpoint result: %s", e)
        return (
            jsonify(
                {
                    "message": "Error on_update_content_endpoint result",
                }
            ),
            500,
        )


@app.route("/on_update_assertion", methods=["POST"])
def on_update_assertion_endpoint():
    """Test method for extract_content_data_endpoint"""
    # logger.info("on_update_assertion")
    data = request.get_json()
    try:
        new_data = data["event"]["data"]["new"]
        assertion_id = new_data["id"]
        new_score_pro = new_data["pro_evidence_aggregate_score"]
        new_score_against = new_data["against_evidence_aggregate_score"]

        old_data = data["event"]["data"]["old"]
        old_score_pro = old_data["pro_evidence_aggregate_score"]
        old_score_against = old_data["against_evidence_aggregate_score"]
    except Exception as e:
        logger.error(
            "Error on_update_content_endpoint could not get vars result: %s", e
        )
        return (
            jsonify(
                {
                    "message": "Error: on_update_content_endpoint no data provided",
                }
            ),
            400,
        )
    if assertion_id is None:
        return (
            jsonify(
                {
                    "message": "Error: on_update_content_endpoint no content_id provided",
                }
            ),
            400,
        )
    if new_score_pro == old_score_pro and new_score_against == old_score_against:
        return (
            jsonify(
                {
                    "message": "on_update_content_endpoint No change in score or no score.",
                }
            ),
            200,
        )
    content_ids = get_assertion_content_ids(assertion_id)
    if content_ids is None or len(content_ids) == 0:
        return (
            jsonify(
                {
                    "message": "No content_ids found for assertion_id",
                }
            ),
            404,
        )
    for content_id in content_ids:
        update_content_aggregate_score(content_id)

    return (
        jsonify(
            {
                "message": "content scores updated.",
            }
        ),
    )


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


# @app.route("/init_grapqhdb", methods=["POST"])
# def init_grapqhdb_endpoint():
#     """Test method for graphql_endpoint"""
#     # data = request.get_json()
#     create_dummy_data()
#     # logger.info("graphql_endpoint data %s", data)
#     return (
#         jsonify(
#             {
#                 "message": "create_dummy_data",
#             }
#         ),
#         200,
#     )


# @app.route("/query_grapqhdb", methods=["POST"])
# def query_grapqhdb_endpoint():
#     """Test method for graphql_endpoint"""
#     # data = request.get_json()
#     result = read_data()
#     # logger.info("graphql_endpoint data %s", data)
#     logger.info("graphql_endpoint data %s", result)
#     return (
#         jsonify(
#             {
#                 "message": "query_grapqhdb",
#                 "result": result,
#             }
#         ),
#         200,
#     )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
