"""update database entries with errors for users to see"""

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def content_parse_error(content_id, error_message):
    """update database entries with errors for users to see"""
    now = datetime.datetime.now()
    # logger.info("content_parse_error: %s %s", content_id, error_message)
    query = {
        "variables": {
            "errorMessage": error_message,
            "contentId": content_id,
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation updateContentPaperClassifications(
                $contentId: uuid = "", 
                $dateLastModified: timestamptz = "", 
                $errorMessage: String = ""
            ) {
                update_content(
                    where: {id: {_eq: $contentId}}, 
                    _set: {
                        error_message: $errorMessage
                        date_last_modified: $dateLastModified, 
                    }) {
                        affected_rows
                        returning {
                            id
                        }
                }
            }

        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # logger.info("content_parse_error added : %s", result)
        content_id = result["data"]["update_content"]["returning"][0]["id"]
        return content_id
    except Exception as e:
        logger.error("content_parse_error Error making graphql call: %s", e)
        logger.info("content_parse_error Error making graphql call result: %s", result)
        return None
