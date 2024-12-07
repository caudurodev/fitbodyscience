"""This module contains functions to add assertions to content"""

import datetime
import uuid
from ..utils.config import logger
from ..utils.graphql import make_graphql_call
from ..meaning.assertions import extract_assertions_from_long_text
from ..store.slug import generate_unique_slug


def parse_assertions_long_text(content_id, long_text, additional_information=""):
    """parse assertions from long text"""

    # save related links and connect to assertions if they match
    logger.info(f"parse_assertions_long_text content_id: {content_id}")
    related_content = []
    try:
        related_content = get_content_related_links(content_id)
    except Exception as e:
        logger.error("Error get_content_related_links related links: %s", e)

    assertions = get_assertion_content_ids(content_id)
    if assertions and len(assertions) > 0:
        logger.info("assertions already exist for content")
        return None

    # extract
    extraction = extract_assertions_from_long_text(
        long_text=long_text,
        additional_information=additional_information,
        related_content=related_content,
    )

    if extraction is None or len(extraction) == 0:
        logger.error("Error extracting assertions from long text")
        return None

    try:
        # logger.info(f"parse_assertions_long_text extraction: {extraction}")
        assertions = extraction["assertions"]
        if assertions is not None or len(assertions) > 0:
            for assertion in assertions:
                try:
                    assertion_id = add_assertion_to_content(content_id, assertion)
                    if assertion_id is None:
                        logger.error(
                            "Error adding assertion to content: assertion_id is None"
                        )
                        continue
                except Exception as e:
                    logger.error("Error adding assertion to content: %s", e)
                    continue
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
                        original_sentence=assertion.get(
                            "part_of_text_assertion_made", ""
                        ),
                        timestamp=assertion.get(
                            "part_of_transcript_assertion_timestamp", ""
                        ),
                    )
                if len(assertion.get("citations", [])):
                    for citation in assertion.get("citations"):
                        citation_content_id = citation.get("contentId", "")
                        if not citation_content_id:  # Skip empty content IDs
                            logger
                            continue
                        logger.info("add_assertion_relation_to_content AGAINST")
                        # evidence that supports assertion extracted from long text, not original content id
                        logger.info(f"citation: {citation}")
                        add_content_relation_to_assertion(
                            assertion_id=assertion_id,
                            content_id=citation_content_id,
                            content_weight_to_assertion=citation.get(
                                "content_weight_to_assertion"
                            ),
                            why_relevant=citation.get("why_relevant"),
                            why_not_relevant="",
                            is_pro_assertion=True,
                            is_citation_from_original_content=True,
                        )
    except Exception as e:
        logger.error("Error adding assertions to content: %s", e)


def add_assertion_to_content(content_id, assertion):
    """add assertions to content"""
    # Validate main content_id first
    check_content_query = {
        "variables": {"contentId": content_id},
        "query": """
            query CheckContent($contentId: uuid!) {
                content_by_pk(id: $contentId) {
                    id
                }
            }
        """,
    }
    try:
        result = make_graphql_call(check_content_query)
        if not result.get("data", {}).get("content_by_pk"):
            logger.error(f"Main content ID {content_id} not found in content table")
            return None
    except Exception as e:
        logger.error(f"Error checking main content: {e}")
        return None

    now = datetime.datetime.now()
    citations = assertion.get("citations", [])

    # Process citations and validate UUIDs
    if isinstance(citations, list):
        for citation in citations:
            if citation.get("contentId") == "uuid" or not citation.get("contentId"):
                citation["contentId"] = str(uuid.uuid4())
        citation_content_ids = [citation.get("contentId", "") for citation in citations]
    else:
        if citations.get("contentId") == "uuid" or not citations.get("contentId"):
            citations["contentId"] = str(uuid.uuid4())
        citation_content_ids = [citations.get("contentId", "")]

    # Validate citation_content_id
    citation_content_id = None
    if citation_content_ids and citation_content_ids[0]:
        # Check if the content exists in the content table
        check_query = {
            "variables": {"contentId": citation_content_ids[0]},
            "query": """
                query CheckContent($contentId: uuid!) {
                    content_by_pk(id: $contentId) {
                        id
                    }
                }
            """,
        }
        try:
            result = make_graphql_call(check_query)
            if result.get("data", {}).get("content_by_pk"):
                citation_content_id = citation_content_ids[0]
            else:
                logger.warning(
                    f"Citation content ID {citation_content_ids[0]} not found in content table"
                )
        except Exception as e:
            logger.error(f"Error checking citation content: {e}")

    assertion_text = assertion.get("assertion", "")

    is_fallacy = assertion.get("is_fallacy", False)
    evidence_type = assertion.get("evidence_type", "")
    assertion_search_verify = assertion.get("assertion_search_verify", "")
    original_sentence = assertion.get("part_of_text_assertion_made", "")
    timestamp = assertion.get("part_of_transcript_assertion_timestamp", "")
    standalone_assertion_reliability = str(
        assertion.get("standalone_assertion_reliability", "0")
    )

    slug = generate_unique_slug(title=assertion_text, table_name="assertions")
    try:
        variables = {
            "contentId": content_id,
            "text": assertion_text,
            "isFallacy": is_fallacy,
            "evidenceType": evidence_type,
            "citations": citations,
            "citationContentId": citation_content_id,
            "assertionSearchVerify": assertion_search_verify,
            "originalSentence": original_sentence,
            "timestamp": timestamp,
            "dateCreated": now.strftime("%Y-%m-%d %H:%M:%S"),
            "standaloneAssertionReliability": standalone_assertion_reliability,
            "slug": slug,
        }
        # logger.info("add_assertion_to_content variables: %s", variables)
    except Exception as e:
        logger.error("Error adding assertions to content: %s", e)
        return None

    try:
        query = {
            "variables": variables,
            "query": """
                mutation UpsertContentAssertionMutation(
                    $contentId: uuid!, 
                    $citations: jsonb!, 
                    $evidenceType: String!, 
                    $isFallacy: Boolean!, 
                    $text: String!,
                    $originalSentence: String!,
                    $timestamp: String!,
                    $citationContentId: uuid,
                    $assertionSearchVerify: String!,
                    $dateCreated: timestamptz!,
                    $standaloneAssertionReliability: String!,
                    $slug: String!
                ) {
                    insert_assertions(
                        objects: {
                            citations: $citations,
                            contentId: $contentId, 
                            evidenceType: $evidenceType, 
                            isFallacy: $isFallacy, 
                            assertionSearchVerify: $assertionSearchVerify,
                            text: $text,
                            originalSentence: $originalSentence,
                            timestamp: $timestamp,
                            dateCreated: $dateCreated,
                            citationContentId: $citationContentId,
                            standaloneAssertionReliability: $standaloneAssertionReliability,
                            slug: $slug
                        },
                        on_conflict: {
                            constraint: assertions_pkey,
                            update_columns: [
                                citations,
                                evidenceType,
                                isFallacy,
                                assertionSearchVerify,
                                originalSentence,
                                timestamp,
                                citationContentId,
                                standaloneAssertionReliability,
                                slug
                            ]
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
        result = make_graphql_call(query, user_id=None, user_role=None, is_admin=True)
        return result["data"]["insert_assertions"]["returning"][0]["id"]
    except Exception as e:
        logger.error("Error adding assertions to content: %s", e)
        logger.info("result: %s", result)
        return None


def add_content_relation_to_assertion(
    assertion_id,
    content_id,
    content_weight_to_assertion=0,
    why_relevant="",
    why_not_relevant="",
    is_pro_assertion=True,
    is_citation_from_original_content=False,
):
    """add assertions to content"""
    # logger.info(
    #     "params: 1 %s  2 %s 3 %s 4 %s 5 %s 6 %s 7 %s",
    #     assertion_id,
    #     content_id,
    #     content_weight_to_assertion,
    #     why_relevant,
    #     why_not_relevant,
    #     is_pro_assertion,
    #     is_citation_from_original_content,
    # )

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
                "weightConclusion": int(
                    content_weight_to_assertion
                    if content_weight_to_assertion is not None
                    else 0
                ),
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
                    $weightConclusion: numeric,
                    $whyRelevant: String = "",
                    $whyNotRelevant: String = "",
                    $dateCreated: timestamptz!,
                    $isProAssertion: Boolean,
                    $isCitationFromOriginalContent: Boolean
                ) {
                    insert_contents_assertion(objects: {
                        assertionId: $assertionId, 
                        contentId: $contentId, 
                        weightConclusion: $weightConclusion,
                        dateCreated: $dateCreated
                        whyRelevant: $whyRelevant,
                        whyNotRelevant: $whyNotRelevant,
                        isProAssertion: $isProAssertion,
                        isCitationFromOriginalContent: $isCitationFromOriginalContent
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
            "InsertContentAssertionMutation insert_contents_assertion result: %s",
            result,
        )
        return result["data"]["insert_contents_assertion"]["returning"][0]["id"]
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
    # logger.info(
    #     "params: 1 %s  2 %s 3 %s 4 %s 5 %s 6 %s 7 %s 8 %s",
    #     assertion_id,
    #     content_id,
    #     assertion_weight,
    #     why_relevant,
    #     assertion_context,
    #     is_pro_content,
    #     original_sentence,
    #     timestamp,
    # )
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
                "weightConclusion": int(
                    assertion_weight if assertion_weight is not None else 0
                ),
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
                        assertionId: $assertionId, 
                        contentId: $contentId, 
                        weightConclusion: $weightConclusion,
                        dateCreated: $dateCreated
                        whyRelevant: $whyRelevant,
                        assertionContext: $assertionContext,
                        isProContent: $isProContent,
                        originalSentence: $originalSentence,
                        videoTimestamp: $videoTimestamp
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
                    content_relationship(where: {parentContentId: {_eq: $contentId}}) {
                        child_content {
                            id
                            title
                            summaryJsonb
                            sourceUrl
                            doiNumber
                            contentType
                            mediaType
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
                    contents_assertion(where: {contentId: {_eq: $contentId}}) {
                        contentId
                        assertionId
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
                query GetAssertionContentQuery($assertionId: uuid!) {
                    assertions(where: {id: {_eq: $assertionId}}) {
                        assertionSearchVerify
                        citationContentId
                        citations
                        contentContext
                        contentId
                        dateCreated
                        dateLastModified
                        evidenceType
                        isFallacy
                        id
                        originalSentence
                        source
                        standaloneAssertionReliability
                        text
                        timestamp
                        contents_assertions{
                            content {
                                id
                                title
                                doiNumber
                                sourceUrl
                            }
                        }
                        content {
                            id
                            title
                            summary
                            sourceUrl
                            canonicalUrl
                            doiNumber
                        }
                    }
                }
            """,
        }
        result = make_graphql_call(query)
        return result["data"]["assertions"][0]

    except Exception as e:
        logger.error("Error getting assertion content : %s", e)
        logger.info(f"result: {result}")
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
                        contentId
                        contents_assertions {
                            isProAssertion
                            content {
                                id
                                contentScore
                                sciencePaperClassification
                            }
                        }
                    }
                }
            """,
        }
        result = make_graphql_call(query)
        return result["data"]["assertions"]

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
                        contentId
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
                    assertions_content(where: {assertionId: {_eq: $assertionId}}) {
                        assertionId
                        contentId
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
