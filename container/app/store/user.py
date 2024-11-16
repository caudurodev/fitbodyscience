""" This module contains the functions to get the user from the database """

from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def get_user_by_id(user_id: str):
    """Get the articles for the weekly newsletter"""
    query = {
        "variables": {
            "userId": user_id,
        },
        "query": """
           query GetUserByIdQuery($userId: uuid!) {
                users(where: {id: {_eq: $userId}}) {
                    displayName
                    email
                    id
                    emailVerified
                    avatarUrl
                }
            }

        """,
    }
    try:
        response = make_graphql_call(query)
        if not response or "data" not in response or not response["data"]["users"]:
            logger.error(f"No user data found for user_id: {user_id}")
            return None
        return response["data"]["users"][0]
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        logger.info(f"Response: {response}")
        return None  # Changed from False to None for consistency
