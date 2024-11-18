"""Summarize text using llm"""

import json
from ..vendors.llm.get_response import get_response
from ..utils.config import logger
from ..content_store.summary_store import (
    add_summary_to_content,
    get_content_summary_by_id,
)


def summarise_text_and_add_to_content(video_content_id, long_text, video_description):
    """extract assertions from long text"""

    try:
        existing_summary = get_content_summary_by_id(video_content_id)
        if existing_summary:
            return existing_summary
    except Exception as e:
        logger.error("Error getting existing summary: %s", e)

    try:
        result = summarise_text(
            long_text=long_text, additional_information=video_description
        )
        summary = result.get("summary", "")
        conclusion = result.get("conclusion", "")
        if summary:
            add_summary_to_content(
                content_id=video_content_id, summary=summary, conclusion=conclusion
            )
            return summary
        else:
            logger.error("Error summarising text")
            return None

    except Exception as e:
        logger.error("Error summarising text: %s", e)
        return None


def summarise_text(long_text, additional_information):
    """summarise text"""
    try:
        summary = get_response(
            f"""
            Given this long text: 
            
            {long_text}

            and additional infortmation about the long text (possibly links to evidence, etc.):
            {additional_information}

            summarise the text focuising on the main factual points and assertions. What are the main assertions?
            what are the facts and evidence that support the assertions? You can ignore any promotional content
            or sponsors.

            The summary should be concise and focus on the main points of the text and one paraghraph long.

            Don't call the text "the text". Just summarise the text. Make sure to include the conclusion of the text in the summary.

            The tone of the summary should be to use simple words and hope to create instructions about what the text
            is proposing.

            The conclusion should be a standalone sentence that does not require the reader to read the text to understand, 
            but encapsulates the main point of the text.

            Return valid JSON response like this:
            {{  
                "summary": "",
                "conclusion":""
            }}
        """
        )
        try:
            summary = json.loads(summary)

            return summary
        except Exception as e:
            logger.error("Error parsing summary: %s", e)
            return None
    except Exception as e:
        logger.error("Error extracting summary: %s", e)
        return None
