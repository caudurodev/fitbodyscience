""" save data for youtube videos """

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def add_summary_to_content(content_id, summary, summary_jsonb, conclusion):
    """create entries in database to be retrieved later"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "contentId": content_id,
            "summary": summary,
            "summaryJsonb": summary_jsonb,
            "conclusion": conclusion,
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation UpdateContentMutation(
                $conclusion: String = "",
                $contentId: uuid!,
                $summary: String = "", 
                $summaryJsonb: jsonb = "", 
                $dateLastModified: timestamptz!, 
            ) {
                update_content(
                    where: {
                        id: {_eq: $contentId}
                    },
                    _set: {
                        conclusion: $conclusion,
                        summary: $summary,
                        summaryJsonb: $summaryJsonb,
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
        logger.error("add_summary_to_content Error making graphql call: %s", e)
        logger.info("result: %s", result)
        return None


def get_content_summary_by_id(content_id):
    """get the summary for a content"""
    query = {
        "variables": {"contentId": content_id},
        "query": """
            query GetContentSummary($contentId: uuid!) {
                content(where: {id: {_eq: $contentId}}) {
                    summary
                }
            }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        return result["data"]["content"][0]["summary"]
    except Exception as e:
        logger.error("get_summary_for_content Error making graphql call: %s", e)
        return None
