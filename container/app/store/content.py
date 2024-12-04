""" This module contains the functions to update the content source URL """

import datetime
from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def upsert_content(
    video_title,
    video_id,
    video_url,
    content_type,
    canonical_url,
    transcript,
    video_description,
    full_text_transcript,
    is_parsed,
    is_science_based,
    science_based_evaluation,
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
            "isParsed": is_parsed,
            "isScienceBased": is_science_based,
            "scienceBasedEvaluation": science_based_evaluation,
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
                $isScienceBased: Boolean,
                $scienceBasedEvaluation: jsonb,
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
                    isScienceBased: $isScienceBased,
                    scienceBasedEvaluation: $scienceBasedEvaluation,
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
                        isScienceBased, scienceBasedEvaluation, dateLastModified, slug, 
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
            content(where: {_or: [
                {canonicalUrl: {_eq: $url}},
                {sourceUrl: {_eq: $url}}
            ]}) {
                id
                slug
                mediaType
                contentType
                isParsed
                canonicalUrl
                influencer_contents {
                    influencer {
                        slug
                    }
                }
            }
        }
        """,
    }
    try:
        response = make_graphql_call(query)
        return response["data"]["content"][0]
    except Exception:
        # logger.error(f"Error getting content by URL: {e}")
        # logger.info("response: %s", response)
        return None


def get_content_by_id(content_id: str):
    """Get content by ID"""
    query = {
        "variables": {"contentId": content_id},
        "query": """
          query GetContentById($contentId: uuid!) {
            content(where: {id: {_eq: $contentId}}) {
                id
                slug
                mediaType
                contentType
                isParsed
                doiNumber
                canonicalUrl
                title
                summaryJsonb
                sciencePaperClassification
                assertions_contents {
                    assertionContext
                    whyRelevant
                    whyNotRelevant
                    isProContent
                    assertion {
                        citations
                        originalSentence
                        assertionSearchVerify
                        text
                        id
                    }
                }
                influencer_contents {
                    influencer {
                        slug
                    }
                }
                parent_content{
                    id
                    content{
                        id
                        title
                    }
                }
                }
            }
        """,
    }
    try:
        response = make_graphql_call(query)
        return response["data"]["content"][0]
    except Exception as e:
        logger.error(f"Error getting content by id: {e}")
        logger.info("response: %s", response)
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


def update_content_is_parsed(content_id: str, is_parsed: bool):
    """Update content is parsed"""
    query = {
        "variables": {"contentId": content_id, "isParsed": is_parsed},
        "query": """
            mutation UpdateContentIsParsedMutation($contentId: uuid!, $isParsed: Boolean!) {
                update_content_by_pk(pk_columns: {id: $contentId}, _set: {isParsed: $isParsed}) {
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
        logger.error(f"Error updating content is parsed: {e}")
        return False


def update_content_crossref(content_id: str, cross_ref_info: dict):
    """Update content crossref info"""
    query = {
        "variables": {"contentId": content_id, "crossrefInfo": cross_ref_info},
        "query": """
            mutation UpdateContentIsParsedMutation($contentId: uuid!, $crossrefInfo: jsonb!) {
                update_content_by_pk(pk_columns: {id: $contentId}, _set: {crossrefInfo: $crossrefInfo}) {
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
        logger.error(f"Error updating content is parsed: {e}")
        return False


def _infer_graphql_type(value):
    """Helper function to infer GraphQL type from Python value"""
    if isinstance(value, bool):
        return "Boolean!"
    elif isinstance(value, int):
        return "Int!"
    elif isinstance(value, float):
        return "numeric!"
    elif isinstance(value, dict):
        return "jsonb!"
    elif value is None:
        return "String"
    else:
        return "String!"  # Default to string for unknown types


def update_content(content_id: str, updates: dict):
    """Generic method to update content properties

    Args:
        content_id (str): The content ID to update
        updates (dict): Dictionary of field names and values to update

    Returns:
        bool: True if successful, False otherwise

    Example:
        update_content(content_id, {
            "full_text": text,
            "title": title,
            "is_parsed": True
        })
    """
    # Convert Python snake_case to GraphQL camelCase and handle arrays
    graphql_updates = {}
    for k, v in updates.items():
        key = "".join(
            word.capitalize() if i > 0 else word for i, word in enumerate(k.split("_"))
        )
        if isinstance(v, (list, tuple)):
            graphql_updates[key] = str(v[0]) if v else ""  # Take first element if array
        else:
            graphql_updates[key] = v

    # Build dynamic GraphQL variables
    variables = {"contentId": content_id}
    variables.update(graphql_updates)

    # Build dynamic GraphQL input fields
    set_fields = ", ".join(f"{k}: ${k}" for k in graphql_updates.keys())

    # Build dynamic variable definitions
    var_defs = ", ".join(
        f"${k}: {_infer_graphql_type(v)}" for k, v in graphql_updates.items()
    )

    query = {
        "variables": variables,
        "query": f"""
            mutation UpdateContentMutation($contentId: uuid!, {var_defs}) {{
                update_content_by_pk(
                    pk_columns: {{id: $contentId}}, 
                    _set: {{{set_fields}}}
                ) {{
                    id
                }}
            }}
        """,
    }

    try:
        response = make_graphql_call(query)
        if response.get("errors"):
            logger.error("GraphQL Error: %s", response["errors"])
            logger.error("Response: %s", response)
            logger.info("query: %s", query)
            return False
        return True
    except Exception as e:
        logger.error(f"Error updating content: {e}")
        logger.info("Response: %s", response)
        return False


def update_content_score(content_id: str, score: float):
    """Update content score"""
    query = {
        "variables": {
            "contentId": content_id,
            "contentScore": score,
        },
        "query": """
            mutation UpdateContentMutation($contentId: uuid!, $contentScore: numeric!) {
                update_content_by_pk(
                    pk_columns: {id: $contentId}, 
                    _set: {contentScore: $contentScore}
                ) {
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
        logger.error(f"Error updating content score: {e}")
        return False


def remove_content_and_relations_by_id(content_id: str):
    """Remove content and relations by ID"""
    query = {
        "variables": {"contentId": content_id},
        "query": """
                mutation DeleteContentMutation($contentId: uuid!) {
                    delete_content_activity(where: {contentId: {_eq: $contentId}}) {
                        affected_rows
                    }
                    delete_influencer_contents(where: {contentId: {_eq: $contentId}}) {
                        affected_rows
                    }
                    delete_assertions_content(where: {contentId: {_eq: $contentId}}) {
                        affected_rows
                    }
                    delete_contents_assertion(where: {_or: [{contentId: {_eq: $contentId}}, {assertion: {contentId: {_eq: $contentId}}}]}) {
                        affected_rows
                    }
                    delete_assertions(where: {_or: [{contentId: {_eq: $contentId}}, {citationContentId: {_eq: $contentId}}]}) {
                        affected_rows
                    }
                }
        """,
    }
    try:
        response = make_graphql_call(query)
        logger.info(f"DeleteContentMutation result: {response}")
    except Exception as e:
        logger.error(f"Error removing content and relations by ID: {e}")

    query = {
        "variables": {"contentId": content_id},
        "query": """
            mutation DeleteRelatedContentAndRelationshipsMutation($contentId: uuid!) {
                delete_content_relationship(where: {parentContentId: {_eq: $contentId}}) {
                    affected_rows
                }
                delete_content(where: {_or: [{content_relationships: {parentContentId: {_eq: $contentId}}}, {id: {_eq: $contentId}}]}) {
                    affected_rows
                    returning {
                        id
                    }
                }
            }
        """,
    }
    try:
        response = make_graphql_call(query)
        logger.info(f"DeleteRelatedContentAndRelationshipsMutation result: {response}")
        return True
    except Exception as e:
        logger.error(f"Error removing content relationship and relations by ID: {e}")
        logger.info(f"DeleteRelatedContentAndRelationshipsMutation result: {response}")
        return False
