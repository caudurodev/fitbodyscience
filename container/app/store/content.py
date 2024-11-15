""" This module contains the functions to update the content source URL """

from ..config.logging import logger
from ..utils.graphql import make_graphql_call
import datetime


def upsert_content(
    video_title,
    video_id,
    video_url,
    content_type,
    canonical_url,
    transcript,
    video_description,
    full_text_transcript,
    slug,
):
    """save content to database"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "title": video_title,
            "sourceUrl": video_url,
            "canonicalUrl": canonical_url,
            "mediaType": "youtube_video",
            "videoId": video_id,
            "videoTranscript": transcript,
            "videoDescription": video_description,
            "fullText": full_text_transcript,
            "contentType": content_type,
            "isParsed": True,
            "dateAdded": now.strftime("%Y-%m-%d %H:%M:%S"),
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
            "slug": slug,
        },
        "query": """
            mutation UpsertContentMutation(
                $canonicalUrl: String!,
                $videoId: String,
                $title: String,
                $fullText: String, 
                $mediaType: String,
                $contentType: String,
                $sourceUrl: String!,
                $videoTranscript: jsonb,
                $videoDescription: String,
                $isParsed: Boolean,
                $dateAdded: timestamptz,
                $dateLastModified: timestamptz,
                $slug: String!
            ) {
                insert_content_one(object: {
                    canonicalUrl: $canonicalUrl,
                    title: $title,
                    videoId: $videoId,
                    contentType: $contentType,
                    mediaType: $mediaType,
                    fullText: $fullText,
                    sourceUrl: $sourceUrl,
                    videoTranscript: $videoTranscript,
                    videoDescription: $videoDescription,
                    isParsed: $isParsed,
                    dateAdded: $dateAdded,
                    dateLastModified: $dateLastModified,
                    slug: $slug
                },
                on_conflict: {
                    constraint: content_canonical_url_key,
                    update_columns: [
                        title, videoId, contentType, mediaType, fullText,
                        sourceUrl, videoTranscript, videoDescription, isParsed,
                        dateLastModified, slug
                    ]
                }) {
                    id
                }
            }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # #logger.info("result: %s", result)
        content_id = result["data"]["insert_content_one"]["id"]
        return content_id
    except Exception as e:
        logger.error("save_youtube_data Error making graphql call: %s", e)
        logger.info("result: %s", result)
        return None


def get_content_by_url(url: str):
    """Get content by URL"""
    query = {
        "variables": {"url": url},
        "query": """
            query GetContentByUrl($url: String!) {
                content(where: {canonicalUrl: {_eq: $url}}) {
                    id
                    slug
                }
            }
        """,
    }
    try:
        response = make_graphql_call(query)
        return response["data"]["content"][0]
    except Exception as e:
        logger.error(f"Error getting content by URL: {e}")
        return None


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
