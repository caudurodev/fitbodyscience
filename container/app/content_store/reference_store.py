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
        mutation GetRelatedLinkContentQuery(
            $sourceURL: String!,
        ) {
            content(where: {sourceUrl: {_eq: $sourceURL}}){
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


def save_related_link(source_url, content_type, media_type, doi_number=None):
    """save related link content to database"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "sourceURL": source_url,
            "contentType": content_type,
            "mediaType": media_type,
            "doiNumber": doi_number,
            "dateAdded": now.strftime("%Y-%m-%d %H:%M:%S"),
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation InsertRelatedLinkMutation(
                $sourceURL: String!,
                $contentType: String = "",
                $mediaType: String = "",
                $doiNumber: String = "",
                $dateAdded: timestamptz!,
                $dateLastModified: timestamptz!
            ) {
                insert_content_one(
                    object: {
                        sourceUrl: $sourceURL,
                        contentType: $contentType,
                        mediaType: $mediaType,
                        doiNumber: $doiNumber,
                        dateAdded: $dateAdded,
                        dateLastModified: $dateLastModified
                    },
                    on_conflict: {
                        constraint: content_source_url_key,
                        update_columns: [contentType, mediaType, doiNumber, dateLastModified]
                    }
                ) {
                    id
                }
            }
        """,
    }
    try:
        result = make_graphql_call(query)
        return result["data"]["insert_content_one"]["id"]

    except Exception as e:
        logger.error(f"Error saving related link: {str(e)}")
        logger.error(f"Failed result: {result}")
        return None

    # connect to original content.
