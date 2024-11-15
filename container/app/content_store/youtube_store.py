""" save data for youtube videos """

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def save_youtube_data(
    content_id,
    video_title,
    video_id,
    video_url,
    transcript,
    video_description,
    full_text_transcript,
    influencer_id,
    slug,
):
    """save content to database"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "contentId": content_id,
            "videoId": video_id,
            "title": video_title,
            "sourceURL": video_url,
            "mediaType": "youtube_video",
            "videoTranscript": transcript,
            "videoDescription": video_description,
            "fullText": full_text_transcript,
            "contentType": "youtube_video",
            "influencerId": influencer_id,
            "isParsed": True,
            "dateAdded": now.strftime("%Y-%m-%d %H:%M:%S"),
            "slug": slug,
        },
        "query": """
            mutation UpdateContentMutation(
                $contentId: uuid!,
                $videoId: String = "",
                $title: String = "",
                $fullText: String = "", 
                $mediaType: String = "",
                $contentType: String = "",
                $sourceURL: String!,
                $videoTranscript: jsonb = "",
                $videoDescription: String = "",
                $isParsed: Boolean!,
                $dateAdded: timestamptz!,
                $influencerId: uuid!,
                $slug: String!
            ) {
                update_content(where: {id: {_eq: $contentId}}, _set: {
                    title: $title,
                    video_id: $videoId,
                    content_type: $contentType, 
                    media_type: $mediaType,
                    full_text: $fullText, 
                    source_url: $sourceURL,
                    video_transcript: $videoTranscript,
                    video_description: $videoDescription,
                    is_parsed: $isParsed,
                    date_added: $dateAdded,
                    slug: $slug
                }) {
                    affected_rows
                    returning {
                        id
                    }
                }
                insert_influencer_contents_one(
                    object: {
                        influencerId: $influencerId,
                        contentId: $contentId
                    },
                    on_conflict: {
                        constraint: influencer_contents_influencer_id_content_id_key,
                        update_columns: []
                    }
                ) {
                    id
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
        logger.error("save_youtube_data Error making graphql call: %s", e)
        logger.info("result: %s", result)
        return None


def video_exists_in_db(content_id):
    """check if video exists in db"""
    query = {
        "variables": {"contentId": content_id},
        "query": """
        query GetVideoByURLQuery($contentId: uuid!) {
            content(where: {id: {_eq: $contentId}}) {
                id
                date_last_modified
                date_added
                is_parsed
                source_url
                error_message
                canonicalUrl
            }
        }
        """,
    }
    try:
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        exists = len(result["data"]["content"]) > 0
        content = result["data"]["content"][0] if exists else None
        is_exists_and_content = exists and content
        return {
            "exists": exists,
            "source_url": content["source_url"] if is_exists_and_content else "",
            "is_parsed": content["is_parsed"] if is_exists_and_content else False,
            "error_message": content["error_message"] if is_exists_and_content else "",
            "content_id": (
                result["data"]["content"][0]["id"] if is_exists_and_content else None
            ),
            "date_last_modified": (
                result["data"]["content"][0]["date_last_modified"]
                if is_exists_and_content
                else None
            ),
            "date_added": (
                result["data"]["content"][0]["date_added"]
                if is_exists_and_content
                else None
            ),
        }
    except Exception as e:
        logger.error("video_exists_in_db Error making graphql call: %s", e)
        return False
