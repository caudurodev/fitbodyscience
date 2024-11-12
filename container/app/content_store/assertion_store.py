"""This module contains functions to add assertions to content"""

import datetime
from ..utils.config import logger
from ..utils.graphql import make_graphql_call
from ..meaning.assertions import extract_assertions_from_long_text
from ..content_get.related_links import retrieve_video_description_links_and_save


def parse_assertions_long_text(content_id, long_text, additional_information):
    """parse assertions from long text"""

    # save related links and connect to assertions if they match
    related_content = []
    try:
        related_content = get_content_related_links(content_id)
    except Exception as e:
        logger.error("Error get_content_related_links related links: %s", e)

    if related_content is None or len(related_content) == 0:
        # logger.info("links not yet extracted, trying to extract now")
        related_content = retrieve_video_description_links_and_save(
            content_id, additional_information
        )
    else:
        logger.error("links already extracted")

    extraction = extract_assertions_from_long_text(
        long_text=long_text,
        additional_information=additional_information,
        related_content=related_content,
    )

    if extraction is None or len(extraction) == 0:
        logger.error("Error extracting assertions from long text")
        return None

    assertions = extraction["assertions"]
    if assertions is not None or len(assertions) > 0:
        for assertion in assertions:
            assertion_id = add_assertion_to_content(content_id, assertion)
            logger.info("add_assertion_to_content content_id: %s", content_id)
            logger.info("add_assertion_to_content assertion_id: %s", assertion_id)
            assertion_weight = assertion.get("assertion_weight", "0")
            why_relevant = assertion.get("why_relevant_main_point", "")
            assertion_context = assertion.get("assertion_context", "")
            logger.info("parse_assertions_long_text assertion_id: %s", assertion_id)
            if assertion_id is not None:
                logger.info("add_assertion_relation_to_content PRO")
                add_assertion_relation_to_content(
                    assertion_id,
                    content_id,
                    assertion_weight,
                    why_relevant,
                    assertion_context,
                    is_pro_content=True,
                    original_sentence=assertion.get("part_of_text_assertion_made", ""),
                    timestamp=assertion.get(
                        "part_of_transcript_assertion_timestamp", ""
                    ),
                )
            if len(assertion.get("citations", [])):
                for citation in assertion.get("citations"):
                    logger.info("add_assertion_relation_to_content AGAINST")
                    # evidence that supports assertion extracted from long text, not original content id
                    add_content_relation_to_assertion(
                        assertion_id=assertion_id,
                        content_id=citation.get("contentId"),
                        content_weight_to_assertion=citation.get(
                            "content_weight_to_assertion"
                        ),
                        why_relevant=citation.get("why_relevant"),
                        why_not_relevant="",
                        is_pro_assertion=True,
                        is_citation_from_original_content=True,
                    )


def add_assertion_to_content(content_id, assertion):
    """add assertions to content"""
    now = datetime.datetime.now()
    citations = assertion.get("citations", [])

    citation_content_id = ""
    if isinstance(citations, list):
        # Assuming you need to handle multiple citations
        citation_content_ids = [citation.get("contentId", "") for citation in citations]
    else:
        # If citations is not a list, handle it as a single citation
        citation_content_ids = [citations.get("contentId", "")]
    if len(citation_content_ids) > 0:
        citation_content_id = citation_content_ids[0]

    # Convert empty UUID to None
    if citation_content_id == "":
        citation_content_id = None

    try:
        query = {
            "variables": {
                "contentId": content_id,
                "text": assertion.get("assertion", ""),
                "isFallacy": assertion.get("is_fallacy", False),
                "evidenceType": assertion.get("evidence_type", ""),
                "citations": citations,
                "citationContentId": citation_content_id,
                "assertionSearchVerify": assertion.get("assertion_search_verify", ""),
                "originalSentence": assertion.get("part_of_text_assertion_made", ""),
                "timestamp": assertion.get(
                    "part_of_transcript_assertion_timestamp", ""
                ),
                "dateCreated": now.strftime("%Y-%m-%d %H:%M:%S"),
                "standaloneAssertionReliability": str(
                    assertion.get("standalone_assertion_reliability", "0")
                ),
            },
            "query": """
            mutation InsertContentAssertionMutation(
                $contentId: uuid = "", 
                $citations: jsonb = "[]",
                $evidenceType: String = "", 
                $isFallacy: Boolean = false, 
                $text: String = "",
                $originalSentence: String = "",
                $timestamp: String = "",
                $citationContentId: uuid = "",
                $assertionSearchVerify: String = "",
                $dateCreated: timestamptz = "",
                $standaloneAssertionReliability: String = 0,
            ) {
                insert_assertions(objects: {
                    citations: $citations,
                    content_id: $contentId, 
                    evidence_type: $evidenceType, 
                    is_fallacy: $isFallacy, 
                    assertion_search_verify: $assertionSearchVerify,
                    text: $text,
                    original_sentence: $originalSentence,
                    timestamp: $timestamp,
                    date_created: $dateCreated, 
                    citation_content_id: $citationContentId,
                    standalone_assertion_reliability: $standaloneAssertionReliability,
                }) {
                    affected_rows
                    returning {
                        id
                    }
                }
            }
            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # logger.info("add_assertion_to_content result: %s", result)
        assertion_id = (
            result.get("data", {})
            .get("insert_assertions", {})
            .get("returning", [{}])[0]
            .get("id", None)
        )
        return assertion_id
    except Exception as e:
        logger.error("Error adding assertions to content: %s", e)
        return None


def add_content_relation_to_assertion(
    assertion_id,
    content_id,
    content_weight_to_assertion="0",
    why_relevant="",
    why_not_relevant="",
    is_pro_assertion=True,
    is_citation_from_original_content=False,
):
    """add assertions to content"""
    if not assertion_id or not content_id:
        logger.error(
            "assertion_id or content_id is None %s %s",
            assertion_id,
            content_id,
        )
        return None

    now = datetime.datetime.now()
    try:
        query = {
            "variables": {
                "assertionId": assertion_id,
                "contentId": content_id,
                "weightConclusion": int(content_weight_to_assertion),
                "whyRelevant": why_relevant,
                "whyNotRelevant": why_not_relevant,
                "dateCreated": now.strftime("%Y-%m-%d %H:%M:%S"),
                "isProAssertion": is_pro_assertion,
                "isCitationFromOriginalContent": is_citation_from_original_content,
            },
            "query": """
            mutation InsertContentAssertionRelationMutation(
                $assertionId: uuid!, 
                $contentId: uuid!, 
                $weightConclusion: numeric!,
                $whyRelevant: String = "",
                $whyNotRelevant: String = "",
                $dateCreated: timestamptz!,
                $isProAssertion: Boolean = true,
                $isCitationFromOriginalContent: Boolean = true
            ) {
                insert_contents_assertion(objects: {
                    assertion_id: $assertionId, 
                    content_id: $contentId, 
                    weight_conclusion: $weightConclusion,
                    date_created: $dateCreated
                    why_relevant: $whyRelevant,
                    why_not_relevant: $whyNotRelevant,
                    is_pro_assertion: $isProAssertion,
                    is_citation_from_original_content: $isCitationFromOriginalContent
                }) {
                    affected_rows
                    returning {
                        id
                    }
                }
            }
            """,
        }

        # logger.info("InsertContentAssertionMutation query: %s", query)
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # logger.info(
        #     "InsertContentAssertionMutation insert_contents_assertion result: %s",
        #     result,
        # )
        assertion_id = (
            result.get("data", {})
            .get("insert_contents_assertion", {})
            .get("returning", [{}])[0]
            .get("id", None)
        )
        return assertion_id
    except Exception as e:
        logger.error("Error adding add_assertion_relation_to_content : %s", e)
        return None


def add_assertion_relation_to_content(
    assertion_id,
    content_id,
    assertion_weight="0",
    why_relevant="",
    assertion_context="",
    is_pro_content=True,
    original_sentence="",
    timestamp="",
):
    """add assertions to content"""
    # logger.info("add_assertion_relation_to_content called")
    logger.info(
        "params: 1 %s  2 %s 3 %s 4 %s 5 %s 6 %s 7 %s 8 %s",
        assertion_id,
        content_id,
        assertion_weight,
        why_relevant,
        assertion_context,
        is_pro_content,
        original_sentence,
        timestamp,
    )
    if not assertion_id or not content_id or not assertion_weight:
        logger.error(
            "assertion_id or content_id is None %s %s %s",
            assertion_id,
            content_id,
            assertion_weight,
        )
        return None

    now = datetime.datetime.now()
    try:
        query = {
            "variables": {
                "assertionId": assertion_id,
                "contentId": content_id,
                "weightConclusion": int(assertion_weight),
                "whyRelevant": why_relevant,
                "assertionContext": assertion_context,
                "dateCreated": now.strftime("%Y-%m-%d %H:%M:%S"),
                "isProContent": is_pro_content,
                "originalSentence": original_sentence,
                "videoTimestamp": timestamp,
            },
            "query": """
            mutation InsertAssertionContentMutation(
                $assertionId: uuid!, 
                $contentId: uuid!, 
                $weightConclusion: numeric!,
                $whyRelevant: String = "",
                $assertionContext: String = "",
                $dateCreated: timestamptz!,
                $isProContent: Boolean = true,
                $originalSentence: String = "",
                $videoTimestamp: String = ""
            ) {
                insert_assertions_content(objects: {
                    assertion_id: $assertionId, 
                    content_id: $contentId, 
                    weight_conclusion: $weightConclusion,
                    date_created: $dateCreated
                    why_relevant: $whyRelevant,
                    assertion_context: $assertionContext,
                    is_pro_content: $isProContent,
                    original_sentence: $originalSentence,
                    video_timestamp: $videoTimestamp
                }) {
                    affected_rows
                    returning {
                        id
                    }
                }
            }
            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        logger.info(
            "asdasdasdasdasdasd ====== add_assertion_relation_to_content result: %s",
            result,
        )
        assertion_id = (
            result.get("data", {})
            .get("insert_assertions", {})
            .get("returning", [{}])[0]
            .get("id", None)
        )
        return assertion_id
    except Exception as e:
        logger.error("Error adding add_assertion_relation_to_content : %s", e)
        return None


def get_content_related_links(content_id):
    """get related links for content"""
    try:
        query = {
            "variables": {
                "contentId": content_id,
            },
            "query": """
            query GetRelatedContentQuery($contentId: uuid!) {
                content_relationship(where: {parent_content_id: {_eq: $contentId}}) {
                    child_content {
                        id
                        source_url
                        doi_number
                        content_type
                        media_type
                    }
                }
            }
            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)

        related_contents = result.get("data", {}).get("content_relationship", [])
        return_related = []
        for related_content in related_contents:
            child_content = related_content.get("child_content", {})
            source_url = child_content.get("source_url", "")
            doi_number = child_content.get("doi_number", "")
            content_type = child_content.get("content_type", "")
            media_type = child_content.get("media_type", "")
            child_content_id = child_content.get("id", "")
            return_related.append(
                {
                    "source_url": source_url,
                    "doi_number": doi_number,
                    "content_type": content_type,
                    "media_type": media_type,
                    "child_content_id": child_content_id,
                }
            )
        if return_related:
            return return_related

    except Exception as e:
        logger.error("Error adding add_assertion_relation_to_content : %s", e)
        return None


def get_content_assertion_ids(content_id):
    """get content assertion ids"""
    try:
        query = {
            "variables": {
                "contentId": content_id,
            },
            "query": """
            query GetContentAssertionIdsQuery($contentId: uuid!) {
                contents_assertion(where: {content_id: {_eq: $contentId}}) {
                    content_id
                    assertion_id
                }
            }

            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        # logger.info("get_content_assertion_ids result: %s", result)

        return result["data"]["contents_assertion"]

    except Exception as e:
        logger.error("Error adding add_assertion_relation_to_content : %s", e)
        return None


def get_assertion_content(assertion_id):
    """get assertion content"""
    try:
        query = {
            "variables": {
                "assertionId": assertion_id,
            },
            "query": """
            query GetAssertionContentQuery($assertionId: uuid = "") {
                assertions(where: {id: {_eq: $assertionId}}) {
                    assertion_search_verify
                    citation_content_id
                    citations
                    content_context
                    content_id
                    date_created
                    date_last_modified
                    evidence_type
                    is_fallacy
                    id
                    original_sentence
                    source
                    standalone_assertion_reliability
                    text
                    timestamp
                    contents_assertions{
                        content {
                            title
                            doi_number
                            source_url
                        }
                    }
                    content {
                        id
                        title
                        summary
                        source_url
                        doi_number
                    }
                }
            }
            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)

        assertion = result.get("data", {}).get("assertions", [{}])[0]
        return assertion

    except Exception as e:
        logger.error("Error getting assertion content : %s", e)
        return None


def get_assertion_evidence_scores(assertion_id):
    """get assertion content"""
    try:
        query = {
            "variables": {
                "assertionId": assertion_id,
            },
            "query": """
            query GetAssertionEvidenceScoresQuery($assertionId: uuid!) {
                assertions(where: {id: {_eq: $assertionId}}) {
                    id
                    contents_assertions {
                        is_pro_assertion
                        content {
                            id
                            content_score
                            science_paper_classification
                        }
                    }
                }
            }
            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)

        assertion = result.get("data", {}).get("assertions", [{}])[0]
        return assertion

    except Exception as e:
        logger.error("Error getting assertion content : %s", e)
        return None


def get_assertion_content_ids(assertion_id):
    """get assertion content"""
    try:
        query = {
            "variables": {
                "assertionId": assertion_id,
            },
            "query": """
            query GetAssertionContentQuery($assertionId: uuid!) {
                assertions(where: {id: {_eq: $assertionId}}) {
                    content_id
                }
            }
            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)

        contents = result.get("data", {}).get("assertions", [{}])
        return contents

    except Exception as e:
        logger.error("Error getting assertion content : %s", e)
        return None


def get_assertion_parent_content_ids(assertion_id):
    """get assertion content"""
    try:
        query = {
            "variables": {
                "assertionId": assertion_id,
            },
            "query": """
            query GetAssertionParentContentIds($assertionId: uuid!) {
                assertions_content(where: {assertion_id: {_eq: $assertionId}}) {
                    assertion_id
                    content_id
                }
            }

            """,
        }
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)

        contents = result.get("data", {}).get("assertions_content", [{}])
        return contents

    except Exception as e:
        logger.error("Error getting assertion content : %s", e)
        return None
