""" User add content endpoint """

from ...config.logging import logger
from ...meaning.evaluate_content_assertion_relevance import (
    evaluate_content_assertion_relevance,
)
from ...content_store.assertion_store import get_assertion_content
from ...endpoints.assertions import add_evidence_to_assertion
from ...endpoints.actions.action_user_classify_evidence_endpoint import get_url_content
from ...store.content import get_content_by_url


def action_user_append_evidence_to_assertion_endpoint(assertion_id, content_url):
    """Analyze a scientific paper and save the data to the database"""
    logger.info(
        "action_user_append_evidence_to_assertion_endpoint assertion_id: %s, content_url: %s",
        assertion_id,
        content_url,
    )
    # see if content is already in db
    try:
        content = get_content_by_url(content_url)
        logger.info("exists?: %s", content)
        content_id = content.get("id")

        # if content is not None:
        #     return {
        #         "message": f"Error appending evidence to content: {content_url}. Content already exists",
        #         "success": False,
        #     }
    except Exception as e:
        logger.error("Error appending evidence to content: %s", e)
        return {"message": str(e), "success": False}
    try:

        # evaluate if this is scientific evidence related to assertion
        # only science allowed here, no videos or other media
        assertion = get_assertion_content(assertion_id)
        parent_content_id = assertion.get("contentId")
        # logger.warn("parent_content_id: %s", parent_conx§tent_id)
        # logger.warn("content_id: %s", content_id)

        contents_assertions = assertion.get("contents_assertions", [])
        # logger.warn("contents_assertions: %s", contents_assertions)

        if content_id and parent_content_id and len(contents_assertions) > 0:
            for contents_assertion in contents_assertions:
                assertion_content_id = contents_assertion.get("content", {}).get(
                    "id", None
                )
                if assertion_content_id == content_id:
                    logger.warn(
                        "already content_id to assertion: %s", assertion_content_id
                    )
                    return {
                        "message": f"Content already added to assertion",
                        "success": False,
                    }

        assertion_with_context = f"""
            the original assertion was:{assertion["originalSentence"]}
            Which can be summarized as: {assertion["text"]}
            The assertio was made based on {assertion["evidenceType"]}
        """

        logger.info(f"assertion_with_context: {assertion_with_context}")

    except Exception as e:
        logger.error("Error appending evidence to content: %s", e)
        return {"message": str(e), "success": False}

    try:
        logger.info("downloading content url: %s", content_url)
        data = get_url_content(url_to_scrape=content_url)
        if data is False:
            return {
                "message": f"Error appending evidence to content: {content_url}. Could not get URL content",
                "success": False,
            }

        # logger.info(f"website content data: {data}")

        text_content = data.get("fullText", "")
        if not text_content:
            return {
                "message": f"Error appending evidence to content: {content_url}. Could not get URL content",
                "success": False,
            }
    except Exception as e:
        logger.error("Error appending evidence to content: %s", e)
        return {"message": str(e), "success": False}

    try:

        relevance_evaluation = evaluate_content_assertion_relevance(
            text_content, assertion=assertion_with_context
        )
        is_directly_related_to_assertion = relevance_evaluation.get(
            "is_directly_related_to_assertion", False
        )
        is_scientific_factual_content = relevance_evaluation.get(
            "is_scientific_factual_content", False
        )

        if not is_directly_related_to_assertion or not is_scientific_factual_content:
            return {
                "message": f"Error appending evidence to content: {content_url}. Content not related to assertion",
                "success": False,
            }

    except Exception as e:
        logger.error("Error appending evidence to content: %s", e)
        return {"message": str(e), "success": False}

    is_pro_assertion = relevance_evaluation.get("is_pro_assertion", False)
    # is_contradicting_assertion = relevance_evaluation.get(
    #     "is_contradicting_assertion", False
    # )

    logger.info(
        "action_user_append_evidence_to_assertion_endpoint is_scientific_factual_content: %s",
        is_scientific_factual_content,
    )
    logger.info(
        "action_user_append_evidence_to_assertion_endpoint is_pro_assertion: %s",
        is_pro_assertion,
    )

    logger.info(
        "action_user_append_evidence_to_assertion_endpoint relevance_evaluation: %s",
        relevance_evaluation,
    )

    try:
        why_relevant = relevance_evaluation.get("reason_why_related", "")
        why_not_relevant = relevance_evaluation.get("reason_why_not_related", "")
        doi_number = relevance_evaluation.get("doi_number", "")
        content_type = relevance_evaluation.get("content_type", "")
        content_weight_to_assertion = "1" if is_pro_assertion is True else "0"
        add_evidence_to_assertion(
            canonical_url=content_url,
            parent_content_id=parent_content_id,
            media_type="text",
            why_relevant=why_relevant,
            why_not_relevant=why_not_relevant,
            doi_number=doi_number,
            content_type=content_type,
            assertion_id=assertion_id,
            content_weight_to_assertion=content_weight_to_assertion,
            is_pro_assertion=is_pro_assertion,
        )

        # download url

        # if it is, add content to db

        # connect content to assertion

        # update assertion score

        # update contents that use assertion score

        return {
            "message": f"Evidence appended to assertion {assertion_id} url {content_url}",
            "success": True,
        }
    except Exception as e:
        logger.error("Error appending evidence to content: %s", e)
        return {"message": str(e), "success": False}
