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
import json


def insert_assertions_opposing(assertion_id):
    """insert assertions and related content for opposing viewpoints"""
    try:
        assertion = get_assertion_content(assertion_id)
        parent_content_id = assertion.get("contentId")
    except Exception as e:
        logger.error(
            "Error insert_assertions_opposing getting assertion content: %s", e
        )
        logger.info(f"assertion_id: {assertion_id}")
        return False

    try:
        result = get_opposing_viewpoints(assertion_id)
        if result is None:
            logger.error("Received None result from get_opposing_viewpoints")
            raise ValueError("Invalid response from LLM call - None or empty.")

        logger.info(f"Raw result from get_opposing_viewpoints: {result}")

        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse result as JSON: {e}")
                logger.error(f"Raw result was: {result}")
                raise ValueError(f"Invalid JSON response: {e}")

        logger.info("get_opposing_viewpoints result: %s", result)

    except Exception as e:
        logger.error(
            "Error insert_assertions_opposing getting opposing viewpoints: %s", e
        )
        logger.info(f"assertion_id: {assertion_id}")
        logger.info(f"assertion: {assertion}")
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
                assertion_id=assertion_id,
                evidence=evidence,
            )

    if len(evidence_disprove) > 0:
        for evidence in evidence_disprove:
            # Try both canonical_url and source_url
            canonical_url = evidence.get("canonical_url") or evidence.get("source_url")
            if not canonical_url:
                logger.error("Missing URL in evidence: %s", evidence)
                continue
            add_evidence_to_assertion(
                assertion_id=assertion_id,
                evidence=evidence,
            )

    return True


def add_evidence_to_assertion(assertion_id, evidence):
    """Add a single piece of evidence to an assertion"""
    try:
        # First check if evidence has the expected structure
        if not isinstance(evidence, dict):
            logger.error(f"Evidence is not a dictionary: {type(evidence)}")
            return False

        # Log the structure of the evidence for debugging
        logger.info(f"Evidence structure: {json.dumps(evidence, indent=2)}")

        # Extract required fields with safe gets
        title = evidence.get("title", "")
        url = evidence.get("canonical_url", "")
        doi = evidence.get("doi_number", "")

        if not (title and url):
            logger.warning(f"Missing required fields in evidence: {evidence}")
            return False

        # Create content entry
        new_content_id = create_content(
            title=title,
            url=url,
            doi_number=doi,
            content_type="SCIENCE_PAPER",
        )

        if not new_content_id:
            logger.error("Failed to create content")
            return False

        logger.info(f"Created content with ID: {new_content_id}")

        # Classify the evidence
        classify_result = classify_evidence(content_id=new_content_id)
        if not classify_result:
            logger.error(f"Failed to classify evidence for content {new_content_id}")
            return False

        logger.info(f"Successfully classified evidence for content {new_content_id}")

        # Connect content to assertion
        add_content_relation_to_assertion(
            assertion_id=assertion_id,
            content_id=new_content_id,
            content_weight_to_assertion="1",  # Since this is supporting evidence
            why_relevant=evidence.get("proof_assertion_is_true", ""),
            why_not_relevant="",
            is_pro_assertion=True,  # Since this is supporting evidence
            is_citation_from_original_content=False,
        )

        return True

    except Exception as e:
        logger.error(f"Error in add_evidence_to_assertion: {e}")
        return False


def create_content(title, url, doi_number, content_type):
    """Create a new content entry in the database"""
    new_content_id = check_if_related_link_content_exists(url)
    if new_content_id is None:
        new_content_id = save_related_link(
            source_url=url,
            canonical_url=url,
            content_type=content_type,
            media_type="text",
            doi_number=doi_number,
        )

    # if new_content_id is not None:
    #     create_content_relation(
    #         parent_content_id=None,
    #         child_content_id=new_content_id,
    #     )

    return new_content_id
