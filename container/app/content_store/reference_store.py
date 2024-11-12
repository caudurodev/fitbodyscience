""" save data for youtube videos """

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def check_if_related_link_content_exists(source_url):
    """check if related link content exists in the database"""
    query = {
        "variables": {
            "sourceURL": source_url,
        },
        "query": """
        mutation GetRelatedLinkCointentQuery(
            $sourceURL: String!,
        ) {
            content(where: {source_url: {_eq: $sourceURL}}){
                id
            }
        }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # #logger.info("result: %s", result)
        content_id = result["data"]["content"]
        return content_id
    except Exception as e:
        logger.error(
            "check_if_related_link_content_exists Error making graphql call: %s", e
        )
        return None


def save_related_link(full_url, content_type, media_type, doi_number, title=""):
    """create entries in database to be retrieved later"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "sourceURL": full_url,
            "contentType": content_type,
            "mediaType": media_type,
            "doiNumber": doi_number,
            "title": title,
            "dateAdded": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
        mutation InsertContentMutation(
            $title: String = "",
            $sourceURL: String!,
            $contentType: String = "",
            $mediaType: String = "",
            $doiNumber: String = "",
            $dateAdded: timestamptz!
        ) {
            insert_content(objects: {
                title: $title,
                source_url: $sourceURL,
                content_type: $contentType,
                media_type: $mediaType,
                doi_number: $doiNumber,
                is_parsed: false,
                date_added: $dateAdded
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
        # #logger.info("result: %s", result)
        content_id = result["data"]["insert_content"]["returning"][0]["id"]
        return content_id
    except Exception as e:
        logger.error("save_related_link Error making graphql call: %s", e)
        return None

    # connect to original content.
