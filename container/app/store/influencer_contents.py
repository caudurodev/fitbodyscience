""" This module contains the functions to save influencer content to database """

from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def add_influencer_content_relationship(
    influencer_id,
    content_id,
):
    """save influencer content to database"""
    query = {
        "variables": {
            "influencerId": influencer_id,
            "contentId": content_id,
        },
        "query": """
            mutation AddInfluencerContentRelationshipMutation($influencerId: uuid!, $contentId: uuid!) {
                insert_influencer_contents(objects: {contentId: $contentId, influencerId: $influencerId}) {
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
        influencer_content_id = result["data"]["insert_influencer_contents"][
            "returning"
        ][0]["id"]
        return influencer_content_id
    except Exception as e:
        logger.error("save_youtube_data Error making graphql call: %s", e)
        logger.info("result: %s", result)
        return None
