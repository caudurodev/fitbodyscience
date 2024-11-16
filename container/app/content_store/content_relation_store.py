""" This module contains the functions to create content relation"""

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def create_content_relation(parent_content_id, child_content_id):
    """save content to database"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "parentContentId": parent_content_id,
            "childContentId": child_content_id,
            "dateAdded": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation InsertRelationshipMutation(
                $parentContentId: uuid!, 
                $childContentId: uuid!,
                $dateAdded: timestamptz!
            ) {
                insert_content_relationship(objects: {
                    parentContentId: $parentContentId
                    childContentId: $childContentId, 
                    dateAdded: $dateAdded
                }) {
                    returning {
                        id
                    }
                    affected_rows
                }
            }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # logger.info("insert_content_relationship result: %s", result)
        return result["data"]["insert_content_relationship"]["returning"][0]["id"]
    except Exception as e:
        logger.error("create_content_relation Error making graphql call: %s", e)
        logger.info("Failed result: %s", result)
        return None

    # connect to original content.
