"""This module contains the logic for analyzing a scientific paper and saving the data to the database"""

from ..utils.config import logger
from ..content_store.reference_store import (
    save_related_link,
    check_if_related_link_content_exists,
)
from ..content_store.assertion_store import (
    add_content_relation_to_assertion,
)
from ..agents.more_pro_against_evidence import get_opposing_viewpoints
from ..content_store.content_relation_store import create_content_relation
from ..content_store.assertion_store import get_assertion_content
from ..endpoints.actions.action_user_classify_evidence_endpoint import (
    classify_evidence,
)


def insert_assertions_opposing(assertion_id):
    """insert assertions and related content for opposing viewpoints"""
    try:
        assertion = get_assertion_content(assertion_id)
        parent_content_id = assertion.get("contentId")
    except Exception as e:
        logger.error(
            "Error insert_assertions_opposing getting assertion content: %s", e
        )
        return False

    try:
        result = get_opposing_viewpoints(assertion_id)
        logger.info("get_opposing_viewpoints result: %s", result)

    except Exception as e:
        logger.error(
            "Error insert_assertions_opposing getting opposing viewpoints: %s", e
        )
        return False

    evidence_supports = result.get("evidence_supports", [])
    evidence_disprove = result.get("evidence_disprove", [])

    if len(evidence_supports) > 0:
        for evidence in evidence_supports:
            # Try both canonical_url and source_url
            canonical_url = evidence.get("canonical_url") or evidence.get("source_url")
            if not canonical_url:
                logger.error("Missing URL in evidence: %s", evidence)
                continue
            add_evidence_to_assertion(
                canonical_url=canonical_url,
                parent_content_id=parent_content_id,
                media_type="text",
                why_relevant=evidence.get("proof_assertion_is_true", ""),
                why_not_relevant="",
                doi_number=evidence.get("doi_number", ""),
                content_type=evidence.get("evidence_type", ""),
                assertion_id=assertion_id,
                content_weight_to_assertion="1",
                is_pro_assertion=True,
            )

            # # 1. add content from evidence
            # new_content_id = check_if_related_link_content_exists(canonical_url)
            # if new_content_id is None:
            #     new_content_id = save_related_link(
            #         source_url=canonical_url,
            #         canonical_url=canonical_url,
            #         content_type=evidence.get("evidence_type", ""),
            #         media_type="text",
            #         doi_number=evidence.get("doi_number", ""),
            #     )

            # if new_content_id is not None:
            #     create_content_relation(
            #         parent_content_id=parent_content_id,
            #         child_content_id=new_content_id,
            #     )
            #     # 2. connect content to assertion
            #     add_content_relation_to_assertion(
            #         assertion_id=assertion_id,
            #         content_weight_to_assertion="1",
            #         content_id=new_content_id,
            #         why_relevant=evidence.get("proof_assertion_is_true", ""),
            #         why_not_relevant="",
            #         is_pro_assertion=True,
            #         is_citation_from_original_content=False,
            #     )
            #     classify_evidence(content_id=new_content_id)

    if len(evidence_disprove) > 0:
        for evidence in evidence_disprove:
            # Try both canonical_url and source_url
            canonical_url = evidence.get("canonical_url") or evidence.get("source_url")
            if not canonical_url:
                logger.error("Missing URL in evidence: %s", evidence)
                continue
            add_evidence_to_assertion(
                canonical_url=canonical_url,
                parent_content_id=parent_content_id,
                media_type="text",
                why_relevant=evidence.get("proof_assertion_is_false", ""),
                why_not_relevant="",
                doi_number=evidence.get("doi_number", ""),
                content_type=evidence.get("evidence_type", ""),
                assertion_id=assertion_id,
                content_weight_to_assertion="0",
                is_pro_assertion=False,
            )
            # canonical_url = evidence.get("canonical_url") or evidence.get("source_url")
            # if not canonical_url:
            #     logger.error("Missing URL in evidence: %s", evidence)
            #     continue

            # # 1. add content from evidence
            # new_content_id = check_if_related_link_content_exists(canonical_url)
            # if new_content_id is None:
            #     new_content_id = save_related_link(
            #         source_url=canonical_url,
            #         canonical_url=canonical_url,
            #         content_type=evidence.get("evidence_type", ""),
            #         media_type="text",
            #         doi_number=evidence.get("doi_number", ""),
            #     )

            # if new_content_id is not None:
            #     # 2. connect content to assertion
            #     add_content_relation_to_assertion(
            #         assertion_id=assertion_id,
            #         content_id=new_content_id,
            #         content_weight_to_assertion=0,
            #         why_relevant=evidence.get("proof_assertion_is_false", ""),
            #         why_not_relevant="",
            #         is_pro_assertion=False,
            #         is_citation_from_original_content=False,
            #     )

    return True


def add_evidence_to_assertion(
    canonical_url,
    parent_content_id,
    media_type="text",
    why_relevant="",
    why_not_relevant="",
    doi_number="",
    content_type="",
    assertion_id="",
    content_weight_to_assertion="0",
    is_pro_assertion=True,
):
    """Analyze a scientific paper and save the data to the database"""
    new_content_id = check_if_related_link_content_exists(canonical_url)
    if new_content_id is None:
        new_content_id = save_related_link(
            source_url=canonical_url,
            canonical_url=canonical_url,
            content_type=content_type,
            media_type=media_type,
            doi_number=doi_number,
        )

    if new_content_id is not None:
        create_content_relation(
            parent_content_id=parent_content_id,
            child_content_id=new_content_id,
        )
        # 2. connect content to assertion
        add_content_relation_to_assertion(
            assertion_id=assertion_id,
            content_weight_to_assertion=content_weight_to_assertion,
            content_id=new_content_id,
            why_relevant=why_relevant,
            why_not_relevant=why_not_relevant,
            is_pro_assertion=is_pro_assertion,
            is_citation_from_original_content=False,
        )
        classify_evidence(content_id=new_content_id)
