"""Get content by content ID"""

from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def get_content_by_id(content_id):
    """Get content by content ID"""

    query = {
        "variables": {
            "contentId": content_id,
        },
        "query": """
            query GetContentByIdQuery($contentId: uuid!) {
                content(where: {id: {_eq: $contentId}}) {
                    contentType
                    dateAdded
                    dateLastModified
                    summary
                    fullText
                    isParsed
                    mediaType
                    sourceUrl
                    videoDescription
                    videoTranscript
                    doiNumber
                    crossrefInfo
                    sciencePaperClassification
                    id
                }
            }
        """,
    }
    try:
        full_content = make_graphql_call(
            query, user_id=None, user_role=None, is_admin=True
        )
        # #logger.info("full_content: %s", full_content)
        content = full_content["data"]["content"]
        return content
    except Exception as e:
        logger.error("get_content_by_id Error making graphql call: %s", e)
        return None


def get_content_property_by_id(content_id, property_name):
    """Get content by content ID"""

    query = {
        "variables": {
            "contentId": content_id,
        },
        "query": f"""
            query GetContentPropertyByIdQuery($contentId: uuid!) {{
                content(
                    where: {{
                        id: {{
                            _eq: $contentId
                        }}
                    }}
                ) {{
                    id
                    {property_name}
                }}
            }}
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # #logger.info("result: %s", result)
        value = result["data"]["content"][0][property_name]
        return value
    except Exception as e:
        logger.error("get_content_property_by_id Error making graphql call: %s", e)
        return None


def get_content_assertion_tree(content_id):
    """get assertion content"""
    try:
        query = {
            "variables": {
                "contentId": content_id,
            },
            "query": """
                query GetAssertionEvidenceScoresQuery($contentId: uuid!) {
                    content(where: {id: {_eq: $contentId}}) {
                        assertions {
                        id
                        againstEvidenceAggregateScore
                        proEvidenceAggregateScore
                            assertions_contents {
                                weightConclusion
                            }
                        }
                    }
                }
            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)

        assertion = result.get("data", {}).get("content", [{}])[0]
        return assertion

    except Exception as e:
        logger.error("Error getting assertion content : %s", e)
        return None
