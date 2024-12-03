""" This module contains the functions to save influencer content to database """

from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def get_content_relationship(
    parent_content_id,
):
    """save influencer content to database"""
    query = {
        "variables": {
            "parentContentId": parent_content_id,
        },
        "query": """
            query GetContentRelationship($parentContentId: uuid!) {
                content_relationship(where: {parentContentId: {_eq: $parentContentId}}) {
                    childContentId
                    child_content {
                        title
                        doiNumber
                    }
                }
            }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        return result["data"]["content_relationship"]
    except Exception as e:
        logger.error("get_content_relationship Error making graphql call: %s", e)
        logger.info("result: %s", result)
        return None
