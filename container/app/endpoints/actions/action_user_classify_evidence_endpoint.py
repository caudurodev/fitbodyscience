""" User add content endpoint """

from flask import jsonify
from ...config.logging import logger
from ...store.content import get_content_by_id
from ...content_get.classify_study import classify_evidence_content
from ...data_sources.crossref import get_crossref_data_from_doi
from ...vendors.web_scraping import download_website
from ...utils.html.visible_text import get_main_content
from ...store.content import update_content
from ...content_store.science_paper import update_science_paper_classification_content
from ...scoring.evidence import calculate_evidence_score


# Todo: Move this to a separate module
def classify_evidence(content_id):
    """
    Classify the evidence for a given content_id
    """
    content = get_content_by_id(content_id)
    if not content:
        raise Exception("Content not found")

    doi_number = content.get("doiNumber", None)
    url_to_scrape = content.get("canonicalUrl", None)
    crossref_info = content.get("crossrefInfo", None)

    logger.info(f"Content ID: {content_id}")
    logger.info(f"DOI: {doi_number}")
    logger.info(f"URL: {url_to_scrape}")

    if doi_number is None or url_to_scrape is None:
        return (
            jsonify(
                {"message": "No DOI or URL found, cannot continue", "success": False}
            ),
            400,
        )

    # Get crossref data if not present
    if crossref_info is None and doi_number is not None:
        cross_ref_info_data = get_crossref_data_from_doi(doi_number)
        if cross_ref_info_data:
            update_content(
                content_id,
                {
                    "crossrefInfo": cross_ref_info_data,
                },
            )

    # download full text
    if content.get("fullText") is None:
        logger.info(f"Downloading content from {url_to_scrape}")

        # Get raw HTML first
        raw_html = download_website(url_to_scrape=url_to_scrape, return_format="html")

        # logger.info(f"Raw HTML downloaded, length: {len(raw_html) if raw_html else 0}")

        if not raw_html:
            logger.info(
                f"Error scrape_content_url empty result or error: {url_to_scrape}"
            )
            raise Exception(
                f"Error scrape_content_url empty result or error: {url_to_scrape}"
            )

        # Process the HTML to extract main content
        html_content = get_main_content(raw_html)

        # logger.info(f"Main content extracted, length: {len(html_content) if html_content else 0}")

        if not html_content:
            logger.error(f"Failed to extract main content from {url_to_scrape}")
            return True

        if (
            not isinstance(html_content, dict)
            or "title" not in html_content
            or "text" not in html_content
        ):
            logger.error(
                f"Invalid content structure from {url_to_scrape}: {html_content}"
            )
            raise Exception(
                f"Invalid content structure from {url_to_scrape}: {html_content}"
            )
        # Update content with extracted data
        update_content(
            content_id,
            {
                "fullText": html_content["text"],
                "title": html_content["title"],
                "htmlJsonb": html_content,
                "isParsed": True,
            },
        )

        logger.info(
            f"Content updated successfully with {len(html_content['text'])} characters of text"
        )

    # classify evidence using available information
    logger.info(f"Classifying content {content_id}")
    try:
        classify = classify_evidence_content(content_id=content_id)
        if not classify:
            logger.error("Failed to classify content - no classification returned")
            return False

        update_science_paper_classification_content(
            content_id=content_id, classification_jsonb=classify
        )

        logger.info(f"Content {content_id} classified")

        # update score
        try:
            full_score = calculate_evidence_score(classify)
            score = float(full_score["normalizedScore"])
        except (ValueError, TypeError, AttributeError) as e:
            logger.error(f"Error calculating evidence score: {e}")
            score = 0.0
        logger.info(f"Content score: {score}")

        update_content(
            content_id,
            {
                "contentScore": score,
            },
        )

        return True
    except Exception as e:
        logger.error(f"Error in classification process: {e}")
        return False


def action_user_classify_evidence_endpoint(content_id):
    """Analyze a scientific paper and save the data to the database"""
    try:
        classify_evidence(content_id)
        return jsonify({"message": "Content classified successfully", "success": True})
    except Exception as e:
        logger.error("Error classifying content: %s", e)
        return jsonify({"message": str(e), "success": False}), 500
