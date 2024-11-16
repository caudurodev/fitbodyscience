""" save data for youtube videos """

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call


def update_science_paper_content(source_url, full_text):
    """create entries in database to be retrieved later"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "sourceURL": source_url,
            "mediaType": "text",
            "fullText": full_text,
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation UpdateContentMutation(
                $sourceURL: String!,
                $mediaType: String = "", 
                $fullText: String = "", 
                $dateLastModified: timestamptz!, 
            ) {
                update_content(
                    where: {
                        sourceUrl: {_eq: $sourceURL}
                    },
                    _set: {
                        mediaType: $mediaType,
                        isParsed: true, 
                        fullText: $fullText, 
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
        logger.error("Error making graphql call: %s", e)
        return None


def update_science_paper_crossref_content(source_url, crossref_jsonb):
    """create entries in database to be retrieved later"""
    now = datetime.datetime.now()
    title_list = crossref_jsonb.get("message", {}).get("title", [])
    first_title = title_list[0] if title_list else ""

    abstract = crossref_jsonb.get("message", {}).get("abstract", "")

    query = {
        "variables": {
            "crossrefInfo": crossref_jsonb,
            "sourceURL": source_url,
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
            "title": first_title,
            "abstract": abstract,
        },
        "query": """
            mutation UpdateContentCrossrefMutation(
                $sourceURL: String!, 
                $crossrefInfo: jsonb!, 
                $dateLastModified: timestamptz!
                $title: String = "",
                $abstract: String = ""
            ) {
            update_content(where: {
                sourceUrl: {_eq: $sourceURL}
                },
                  _set: {
                    title: $title,
                    abstract: $abstract,
                    crossrefInfo: $crossrefInfo, 
                    dateLastModified: $dateLastModified
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
        content_id = result["data"]["update_content"]["returning"][0]["id"]
        return content_id
    except Exception as e:
        logger.error("Error making graphql call: %s", e)
        return None


def update_science_paper_classification_content(content_id, classification_jsonb):
    """create entries in database to be retrieved later"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "classificationJsonb": classification_jsonb,
            "contentId": content_id,
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation updateContentPaperClassifications(
                $contentId: uuid = "", 
                $dateLastModified: timestamptz = "", 
                $classificationJsonb: jsonb = ""
            ) {
                update_content(
                    where: {id: {_eq: $contentId}}, 
                    _set: {
                        sciencePaperClassification: $classificationJsonb
                        dateLastModified: $dateLastModified, 
                        isParsed: true
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
        content_id = result["data"]["update_content"]["returning"][0]["id"]
        return content_id
    except Exception as e:
        logger.error("Error making graphql call: %s", e)
        return None


def update_science_paper_direct_download_content(source_url, direct_download_url):
    """create entries in database to be retrieved later"""
    now = datetime.datetime.now()
    query = {
        "variables": {
            "directDownloadUrl": direct_download_url,
            "sourceURL": source_url,
            "dateLastModified": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "query": """
            mutation UpdateContentCrossrefMutation(
                $sourceURL: String!, 
                $directDownloadUrl: String!, 
                $dateLastModified: timestamptz!
            ) {
            update_content(
                where: {sourceUrl: {_eq: $sourceURL}},
                  _set: {
                    directDownloadUrl: $directDownloadUrl, 
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
        logger.error("Error making graphql call: %s", e)
        return None
