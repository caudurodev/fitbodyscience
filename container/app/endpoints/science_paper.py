"""This module contains the logic for analyzing a scientific paper and saving the data to the database"""

from ..utils.config import logger
from ..content_store.get_content import get_content_by_id
from ..content_get.classify_study import classify_evidence_content
from ..content_get.doi_paper import get_paper_main
from ..content_store.science_paper import update_science_paper_classification_content
from ..vendors.web_scraping import download_website
from ..content_store.fulltext_store import add_fulltext_to_content


def analyse_science_paper(content_id):
    """Analyze a scientific paper and save the data to the database"""
    result = get_content_by_id(content_id)

    if not result:
        logger.error("Error analyze_science_paper No content found")
        return None
    if len(result) > 0:
        content = result[0]
    else:
        content = result

    # #logger.info("analyse_science_paper content %s", content)
    content_doi_number = content["doi_number"]
    source_url = content["source_url"]

    if not source_url:
        logger.error("Error analyze_science_paper No source URL provided")
        return None
    if content_doi_number is None:
        logger.error("No DOI provided is article?")

        try:
            text = download_website(url_to_scrape=source_url, return_format="text")
            if text is None:
                logger.error("Error download_website No text found")
                return None
            add_fulltext_to_content(content_id, text)
            # classify_evidence_content(content_id)

        except Exception as e:
            logger.error("Error download_website: %s", e)
            return None

    try:
        # logger.info("analyze_science_paper Getting paper data... %s", source_url)
        scrape_success = get_paper_main(content_doi_number, source_url)
        if scrape_success:
            # logger.info("analyze_science_paper Paper data gotten %s", source_url)
            try:
                # logger.info(
                # "analyze_science_paper Classifying evidence content... %s",
                # source_url,
                # )
                classify = classify_evidence_content(content_id)
                # logger.info(
                # "analyze_science_paper Classified evidence content %s", source_url
                # )
                try:
                    update_science_paper_classification_content(
                        content_id=content_id, classification_jsonb=classify
                    )
                    # logger.info(
                    # "-------------------------------------analyze_science_paper DONE media_type: scientific paper %s",
                    # source_url,
                    # )
                    return content_id
                except Exception as e:
                    logger.error("Error updating science paper classification: %s", e)
            except Exception as e:
                logger.error("Error classifying evidence content: %s", e)
        else:
            logger.error("Error get_paper_main getting paper data")
    except Exception as e:
        logger.error("Error getting paper data: %s", e)

    # logger.info("Error analyze_science_paper")
    return None
