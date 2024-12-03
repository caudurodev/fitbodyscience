""" save data for youtube videos """

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call
from ..store.slug import generate_unique_slug


def check_if_related_link_content_exists(canonical_url):
    """check if related link content exists in the database"""
    if not canonical_url:
        logger.error("canonical_url is required")
        return None

    query = {
        "variables": {
            "canonicalUrl": canonical_url,
        },
        "query": """
        query GetRelatedLinkContentQuery(
            $canonicalUrl: String!
        ) {
            content(where: {canonicalUrl: {_eq: $canonicalUrl}}) {
                id
            }
        }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        contents = result.get("data", {}).get("content", [])
        return contents[0]["id"] if contents else None
    except Exception as e:
        logger.error(
            "check_if_related_link_content_exists Error making graphql call: %s", e
        )
        return None


def save_related_link(
    title, source_url, canonical_url, content_type, media_type, doi_number=None
):
    """save related link content to database"""
    if not source_url:
        logger.error("source_url is required")
        return None

    now = datetime.datetime.now()
    slug = generate_unique_slug(title=title, table_name="content")
    query = {
        "variables": {
            "title": title or "",
            "slug": slug,
            "sourceURL": source_url,
            "canonicalUrl": canonical_url,
            "contentType": content_type,
            "mediaType": media_type,
            "doiNumber": doi_number,
            "dateAdded": now.strftime("%Y-%m-%d %H:%M:%S"),
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation InsertRelatedLinkMutation(
                $title: String!,
                $slug: String!,
                $sourceURL: String!,
                $canonicalUrl: String!,
                $contentType: String!,
                $mediaType: String!,
                $doiNumber: String!,
                $dateAdded: timestamptz!,
                $dateLastModified: timestamptz!
            ) {
                insert_content_one(
                    object: {
                        title: $title,
                        slug: $slug,
                        sourceUrl: $sourceURL,
                        canonicalUrl: $canonicalUrl,
                        contentType: $contentType,
                        mediaType: $mediaType,
                        doiNumber: $doiNumber,
                        dateAdded: $dateAdded,
                        dateLastModified: $dateLastModified
                    },
                    on_conflict: {
                        constraint: content_source_url_key,
                        update_columns: [title,slug,contentType, mediaType, doiNumber, canonicalUrl, dateLastModified]
                    }
                ) {
                    id
                }
            }
        """,
    }
    try:
        result = make_graphql_call(query)
        if not result.get("data"):
            logger.error("No data returned from mutation")
            logger.info("Failed result: %s", result)
            return None

        return result["data"]["insert_content_one"]["id"]

    except Exception as e:
        logger.error("Error saving related link: %s", e)
        return None

    # connect to original content.
