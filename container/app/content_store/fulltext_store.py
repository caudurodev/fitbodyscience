""" save data for youtube videos """

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def add_fulltext_to_content(content_id, full_text):
    """create entries in database to be retrieved later"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "contentId": content_id,
            "fullText": full_text,
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation UpdateContentMutation(
                $fullText: String = "",
                $contentId: uuid!,
                $dateLastModified: timestamptz!, 
            ) {
                update_content(
                    where: {
                        id: {_eq: $contentId}
                    },
                    _set: {
                        fullText: $fullText,
                        dateLastModified: $dateLastModified
                    }
                ) {
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
        # #logger.info("result: %s", result)
        content_id = result["data"]["update_content"]["returning"][0]["id"]
        return content_id
    except Exception as e:
        logger.error("add_fulltext_to_content Error making graphql call: %s", e)
        return None
