import uuid
import datetime
from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def add_content_activity(
    name, content_id, activity_type="info", expires_at=None, description=""
):
    """create entries in database to be retrieved later"""
    logger.info(
        "add_content_activity: %s %s %s",
        name,
        content_id,
        activity_type,
    )
    now = datetime.datetime.now()

    # Convert dates to YYYY-MM-DD HH:MM:SS format
    formatted_created_at = now.strftime("%Y-%m-%d %H:%M:%S")
    formatted_expires_at = None
    if expires_at:
        try:
            if isinstance(expires_at, str):
                formatted_expires_at = datetime.datetime.fromisoformat(
                    expires_at
                ).strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(expires_at, datetime.datetime):
                formatted_expires_at = expires_at.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            logger.warning(f"Invalid expires_at format: {expires_at}, setting to None")
            formatted_expires_at = None

    query = {
        "variables": {
            "name": name,
            "contentId": content_id,
            "createdAt": formatted_created_at,
            "type": activity_type,
            "expiresAt": formatted_expires_at,
            "description": description or "",
        },
        "query": """
            mutation AddContentActivityMutation(
                $name: String!
                $contentId: uuid!
                $createdAt: timestamptz!
                $type: String!
                $expiresAt: timestamptz
                $description: String!
            ) {
                insert_content_activity(
                    objects: {
                        name: $name
                        contentId: $contentId
                        createdAt: $createdAt
                        type: $type
                        expiresAt: $expiresAt
                        description: $description
                    }
                ) {
                    returning {
                        id
                    }
                }
            }
        """,
    }

    try:
        response = make_graphql_call(query)
        if response.get("errors"):
            logger.error("add_content_activity GraphQL Error: %s", response["errors"])
            return False
        return response["data"]["insert_content_activity"]["returning"][0]["id"]
    except Exception as e:
        logger.error(f"add_content_activity Error adding content activity: {e}")
        logger.info(f"add_content_activity Response: {response}")
        return False
