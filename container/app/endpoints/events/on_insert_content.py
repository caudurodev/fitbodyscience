""" On insert content endpoint """

from ...config.logging import logger
from ...store.content import get_content_by_id
from ...endpoints.science_paper import analyse_science_paper
from ...scoring.update import update_evidence_score
from ...content_store.error import content_parse_error
from ...endpoints.website_page import analyse_website_page


def on_insert_content_endpoint(content_id):
    """Analyze a scientific paper and save the data to the database"""
    content = get_content_by_id(content_id=content_id)
    if not content:
        logger.error("Content not found for id: %s", content_id)
        return {"message": "Content not found", "success": False}

    logger.info(f"Content ID: {content_id}")
    logger.info(f"content: {content}")

    science_paper_classification = content.get("sciencePaperClassification", None)
    media_type = content.get("mediaType")
    content_type = content.get("contentType")
    is_parsed = content.get("isParsed", False)
    doi_number = content.get("doiNumber")
    canonical_url = content.get("canonicalUrl")

    if science_paper_classification is not None and content_type == "scientific_paper":
        return {"message": "Science paper already classified", "success": True}
    if content_type in ["youtube_video", "youtube_channel"]:
        return {"message": "YT video not added here", "success": True}
    if is_parsed:
        return {"message": "Content already parsed, skipping...", "success": True}

    # Handle scientific papers (with DOI)
    if content_type == "scientific_paper" and doi_number:
        try:
            analyse_science_paper(content_id)

        except Exception as e:
            logger.error("Error analyse_science_paper science paper: %s", str(e))
            content_parse_error(content_id, f"Error: {str(e)}")
            return {"message": f"Error: {str(e)}", "success": False}

        try:
            update_evidence_score(content_id)
            return {
                "message": "Science paper analyzed successfully",
                "content_id": content_id,
                "success": True,
            }
        except Exception as e:
            error_msg = f"Error updating evidence score: {str(e)}"
            logger.error(error_msg)
            content_parse_error(content_id, error_msg)
            return {"message": error_msg, "success": False}

    # Handle website pages
    if media_type == "text" and canonical_url:
        try:
            analyse_website_page(content_id)
            return {
                "message": "Content Parsed.",
                "content_id": content_id,
                "success": True,
            }
        except Exception as e:
            error_msg = f"Error analyzing website page: {str(e)}"
            logger.error(error_msg)
            content_parse_error(content_id, error_msg)
            return {"message": error_msg, "success": False}

    error_msg = f"Unsupported content: type={content_type}, media={media_type}, has_doi={bool(doi_number)}, has_url={bool(canonical_url)}"
    logger.error(error_msg)
    content_parse_error(content_id, error_msg)
    return {
        "message": error_msg,
        "success": False,
    }
