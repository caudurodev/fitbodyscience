""" This module contains the functions to update the content source URL """

from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def update_content_source_url(content_id: str, source_url: str):
    """Update content source URL"""
    query = {
        "variables": {"contentId": content_id, "sourceUrl": source_url},
        "query": """
        mutation UpdateContentSourceUrlMutation($contentId: uuid!, $sourceUrl: String!) {
            update_content_by_pk(pk_columns: {id: $contentId}, _set: {canonicalUrl: $sourceUrl}) {
                id
            }
        }
        """,
    }

    try:
        response = make_graphql_call(query)
        if response.get("errors"):
            logger.error("GraphQL Error: %s", response["errors"])
            return False
        return True
    except Exception as e:
        logger.error(f"Error updating content source URL: {e}")
        return False
