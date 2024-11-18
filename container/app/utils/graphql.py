import requests
from ..config.constants import HASURA_ADMIN_SECRET, GRAPHQL_URL, VERIFY_SSL_LOCAL_DEV
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def make_graphql_call(query, user_id=None, user_role=None, is_admin=False):
    """Make a call to the Hasura GraphQL endpoint."""
    try:
        # Start with mandatory header
        headers = {
            "content-type": "application/json",
        }

        if user_id is not None:
            headers["x-hasura-user-id"] = user_id
        if user_role is not None:
            headers["x-hasura-role"] = user_role
        # elif is_admin:
        headers["X-Hasura-Admin-Secret"] = HASURA_ADMIN_SECRET

        graphql_url = f"{GRAPHQL_URL}"

        response = requests.post(
            graphql_url,
            headers=headers,
            json=query,
            timeout=10,
            verify=VERIFY_SSL_LOCAL_DEV,
        )

        if response.status_code != 200:
            logger.error(
                "make_graphql_call error: status code %s", response.status_code
            )
            return None

        # print("smake_graphql_call success: 200 status code")
        return response.json()

    except Exception as e:
        logger.error("make_graphql_call error: %s", e)
        return None
