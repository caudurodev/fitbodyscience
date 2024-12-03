""" This module contains the functions to save influencer content to database """

from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def get_content_assertions(
    content_id,
):
    """save influencer content to database"""
    query = {
        "variables": {
            "contentId": content_id,
        },
        "query": """
            query GetAssertionsContentQuery($contentId: uuid!) {
                assertions_content(where: {contentId: {_eq: $contentId}}) {
                    assertion{
                        id
                        text
                    }
                }
            }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        return result["data"]["assertions_content"]
    except Exception as e:
        logger.error("assertions_content Error making graphql call: %s", e)
        logger.info("result: %s", result)
        return None
