""" save data for youtube videos """

from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def save_content_score(content_id, score):
    """check if related link content exists in the database"""
    query = {
        "variables": {
            "contentId": content_id,
            "score": score,
        },
        "query": """
        mutation UpdateContentScoreMutation($score: numeric!, $contentId: uuid!) {
            update_content(where: {id: {_eq: $contentId}}, _set: {content_score: $score}) {
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
        updated_content_id = result["data"]["update_content"]["returning"][0]["id"]
        # logger.info(
        # "update_content score success: %s for content id %s",
        # score,
        #     updated_content_id,
        # )
        return updated_content_id
    except Exception as e:
        logger.error("save_content_score Error making graphql call: %s", e)
        return None


def save_aggregate_content_score(content_id, score_pro, score_against):
    """check if related link content exists in the database"""
    # logger.info(
    #     "save_aggregate_content_score content_id: %s, score_pro: %s, score_against: %s",
    #     content_id,
    #     score_pro,
    #     score_against,
    # )
    query = {
        "variables": {
            "contentId": content_id,
            "scorePro": score_pro,
            "scoreAgainst": score_against,
        },
        "query": """
        mutation UpdateAggregateContentScoreMutation(
            $scorePro: numeric!,
            $scoreAgainst: numeric!,
            $contentId: uuid!
        ) {
              update_content(
                where: {id: {_eq: $contentId}},
                _set: {
                    against_aggregate_content_score: $scoreAgainst
                    pro_aggregate_content_score: $scorePro
                }) {
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
        content_id = result["data"]["update_content"]
        return content_id
    except Exception as e:
        logger.error("save_aggregate_content_score Error making graphql call: %s", e)
        return None


def save_aggregate_assertion_score(assertion_id, score_pro, score_against):
    """check if related link content exists in the database"""
    query = {
        "variables": {
            "contentId": assertion_id,
            "scorePro": score_pro,
            "scoreAgainst": score_against,
        },
        "query": """
        mutation UpdateAggregateAssertionScore(
            $contentId: uuid!, 
            $scoreAgainst: numeric!, 
            $scorePro: numeric!
        ) {
            update_assertions(
                where: {
                    id: {_eq: $contentId}
                },
                _set: {
                against_evidence_aggregate_score: $scoreAgainst, 
                pro_evidence_aggregate_score: $scorePro
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
        content_id = result["data"]["update_assertions"]
        return content_id
    except Exception as e:
        logger.error("save_aggregate_assertion_score Error making graphql call: %s", e)
        return None
