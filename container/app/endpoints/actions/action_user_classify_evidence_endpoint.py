""" User add content endpoint """

import json
from ...config.logging import logger
from ...store.content import get_content_by_id
from ...content_get.classify_study import classify_evidence_content
from ...data_sources.crossref import get_crossref_data_from_doi
from ...vendors.web_scraping import download_website
from ...utils.html.visible_text import get_main_content
from ...store.content import update_content
from ...content_store.science_paper import update_science_paper_classification_content
from ...scoring.evidence import calculate_evidence_score
from ...store.slug import generate_unique_slug
from ...vendors.llm.get_response import get_response
from ...content_store.assertion_store import add_content_relation_to_assertion


def connect_content_to_assertions(content_id):
    """
    Connect a content_id to an assertion_id
    """
    content = get_content_by_id(content_id)
    content_assertions = content.get("assertions_contents", "")
    science_paper_classification = content.get("sciencePaperClassification", "")
    if not content_assertions:
        logger.error(f"No assertions found for content_id {content_id}")

        return

    response = get_response(
        f"""
        Given the following content: {content['title']}

        Which has the content ID: {content_id}

        And has been classified as: {science_paper_classification}

        and the following assertions: {content_assertions}

        Connect the assertions, if any, to the content, if the conent directly supports
        or goes against the assertion.

        If the assertions are not related to the content, return an empty array. 

        Explanation of json properties:
        - assertion_id: The ID of the assertion that is connected to the content.
        - why_relevant: Why the assertion might beelevant to the content.
        - why_not_relevant: Why the assertion might not be relevant to the content.
        - content_weight_to_assertion: The weight of the content to the assertion, or how much the content supports or opposes the assertion from 1 to 10.
        - is_pro_assertion: Whether the assertion is a pro assertion - true or false.

        only return connected assertions, ignore the rest of the assertions

        Return valid JSON response like this:
        {{
            "connected_assertions":[
                {{  
                    "content_id": "<content_id>",
                    "assertion_id": "<assertion_id>",
                    "why_relevant": "<why_relevant>",
                    "why_not_relevant": "<why_not_relevant>",
                    "content_weight_to_assertion": "<content_weight_to_assertion>",
                    "is_pro_assertion": "<is_pro_assertion>",
                }}
            ]
        }}
        """
    )
    logger.info("connect_content_to_assertions Response from LLM: %s", response)

    if not response:
        logger.error("No response from LLM")
        return

    connections = json.loads(response)
    if len(connections.get("connected_assertions", [])) > 0:
        # connect assertions to content
        for connection in connections.get("connected_assertions", []):
            assertion_id = connection.get("assertion_id", None)
            evidence_content_id = connection.get("content_id", None)
            why_relevant = connection.get("why_relevant", "")
            why_not_relevant = connection.get("why_not_relevant", "")
            content_weight_to_assertion = connection.get(
                "content_weight_to_assertion", ""
            )
            is_pro_assertion = connection.get("is_pro_assertion", "")
            add_content_relation_to_assertion(
                assertion_id=assertion_id,
                content_id=evidence_content_id,
                content_weight_to_assertion=content_weight_to_assertion,
                why_relevant=why_relevant,
                why_not_relevant=why_not_relevant,
                is_pro_assertion=is_pro_assertion,
                is_citation_from_original_content=True,
            )


# Todo: Move this to a separate module
def classify_evidence(content_id):
    """
    Classify the evidence for a given content_id
    """
    content = get_content_by_id(content_id)
    if not content:
        logger.error(f"No content found for id {content_id}")
        return {"message": "No content found", "success": False}

    doi_number = content.get("doiNumber", None)
    url_to_scrape = content.get("canonicalUrl", None)
    crossref_info = content.get("crossrefInfo", None)
    url = content.get("url", None)

    logger.info(f"Content ID: {content_id}")
    logger.info(f"DOI: {doi_number}")
    logger.info(f"URL: {url_to_scrape}")

    if doi_number is None or url_to_scrape is None:
        return {
            "message": "No DOI or URL found, cannot continue",
            "success": False,
        }

    # Try to get crossref data if not already present
    if crossref_info is None and doi_number is not None:
        cross_ref_info_data = get_crossref_data_from_doi(doi_number)
        if cross_ref_info_data:
            # Extract URL from crossref data if available
            if (
                "message" in cross_ref_info_data
                and "URL" in cross_ref_info_data["message"]
            ):
                paper_url = cross_ref_info_data["message"]["URL"]
                if paper_url and paper_url != url_to_scrape:
                    update_content(content_id, {"canonicalUrl": paper_url})
                    url_to_scrape = paper_url

            # Extract title from Crossref data, handling array case
            title = cross_ref_info_data.get("message", {}).get("title", "")
            if isinstance(title, list):
                title = title[0] if title else ""
            slug = generate_unique_slug(title=title, table_name="content")
            update_content(
                content_id,
                {"crossrefInfo": cross_ref_info_data, "title": title, "slug": slug},
            )
            logger.info(f"Updated content with Crossref data for DOI: {doi_number}")

    # download full text if not present
    if content.get("fullText") is None:
        if url:
            logger.info(f"Downloading content from {url}")
            content_text = download_website(url)

            if not content_text:
                logger.error(f"No content returned from {url}")
                return {"message": "No content returned", "success": False}

            content = content_text.get("content", "")
            if not content:
                logger.error(f"No text content extracted from {url}")
                return {"message": "No text content extracted", "success": False}

            content_length = len(content)
            if content_length < 100:  # Too short to be meaningful
                logger.error(
                    f"Extracted content too short ({content_length} chars) from {url}"
                )
                if content_length > 0:
                    logger.error(f"Content preview: {content}")
                return {"message": "Extracted content too short", "success": False}

            update_content(content_id, {"content": content})
            logger.info(
                f"Content updated successfully with {content_length} characters of text"
            )
        else:
            logger.info(f"Downloading content from {url_to_scrape}")

            # Update content with extracted data
            data = get_url_content(url_to_scrape=url_to_scrape)
            slug = generate_unique_slug(title=data["title"], table_name="content")
            update_content(
                content_id,
                {
                    "fullText": data["fullText"],
                    "title": data["title"],
                    "htmlJsonb": data["htmlJsonb"],
                    "isParsed": True,
                    "slug": slug,
                },
            )

            logger.info(
                f"Content updated successfully with {len(data['fullText'])} characters of text"
            )

    # classify evidence using available information
    logger.info(f"Classifying content {content_id}")
    try:
        classify = classify_evidence_content(content_id=content_id)
        if not classify:
            logger.warning(
                f"Failed to classify content - no classification returned {classify}"
            )
            return {"message": "Failed to classify content", "success": False}

        update_science_paper_classification_content(
            content_id=content_id, classification_jsonb=classify
        )

        logger.info(f"Content {content_id} classified")

        # update score
        try:
            full_score = calculate_evidence_score(classify)
            score = float(full_score.get("normalizedScore", 0.0))
        except (ValueError, TypeError, AttributeError) as e:
            logger.error(f"Error calculating evidence score: {e}")
            if isinstance(full_score, dict):
                logger.info(f"Full score data: {full_score}")
            else:
                logger.info(f"Invalid full_score type: {type(full_score)}")
            score = 0.0

        logger.info(f"Content score: {score}")

        update_content(
            content_id,
            {
                "contentScore": score,
            },
        )

        return {"message": "Content classified successfully", "success": True}
    except Exception as e:
        logger.error(f"Error in classification process: {e}")
        return {"message": "Error in classification process", "success": False}


def action_user_classify_evidence_endpoint(content_id):
    """Analyze a scientific paper and save the data to the database"""
    try:
        classify_evidence(content_id)
        return {"message": "Content classified successfully", "success": True}
    except Exception as e:
        logger.error("Error classifying content: %s", e)
        return {"message": str(e), "success": False}


def get_url_content(url_to_scrape):
    """Download website content and extract main content"""
    raw_html = download_website(url_to_scrape)
    if not raw_html:
        logger.error(f"Error scrape_content_url empty result or error: {url_to_scrape}")
        # Try alternative URL if available
        if url_to_scrape != url and url:
            logger.info(f"Trying alternative URL: {url}")
            raw_html = download_website(url)
            if not raw_html:
                logger.error(f"Failed to download from alternative URL: {url}")
                return False
        else:
            return False

    # Process the HTML to extract main content
    html_content = get_main_content(raw_html)

    if not html_content:
        logger.error(f"Failed to extract main content from {url_to_scrape}")
        return False

    if (
        not isinstance(html_content, dict)
        or "title" not in html_content
        or "text" not in html_content
    ):
        logger.error(f"Invalid content structure from {url_to_scrape}: {html_content}")
        return False

    return {
        "fullText": html_content["text"],
        "title": html_content["title"],
        "htmlJsonb": html_content,
    }
