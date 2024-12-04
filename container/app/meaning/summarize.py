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
        if existing_summary is not None:
            logger.info("Summary already exists for content")
            return existing_summary
    except Exception as e:
        logger.error("Error getting existing summary: %s", e)

    try:
        summary_jsonb = summarise_text(
            long_text=long_text, additional_information=video_description
        )
        summary = summary_jsonb.get("summary", "")
        conclusion = summary_jsonb.get("conclusion", "")
        if summary:
            add_summary_to_content(
                content_id=video_content_id,
                summary=summary,
                conclusion=conclusion,
                summary_jsonb=summary_jsonb,
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
            **Task**: Summarize the given text by focusing on the main factual points and assertions, and return a JSON object with the specified structure.

            **Input**:

            - **Long Text**:
            {long_text}

            - **Additional Information** (possibly links to evidence, etc.):
            {additional_information}

            **Instructions**:

            1. **Summary**:

                - Provide a concise summary of the text in one paragraph.
                - Focus on the main factual points and assertions.
                - Include the conclusion of the text within the summary.
                - Use simple words and avoid referring to the text as "the text".

            2. **Conclusion**:

                - Write a standalone sentence that encapsulates the main point of the text.
                - Ensure it can be understood without needing to read the original text.

            3. **ELI5 Explanation**:

                - Explain the conclusion as if to a five-year-old (ELI5).
                - Use simple terms and break down the explanation into a list of strings.
                - Do not include any additional text or formatting; just the list of explanation points.

            **Output Format**:

            Return a valid JSON object with the following structure:

            ```json
            {{
                "summary": "<Your summary here>",
                "conclusion": "<Your conclusion here>",
                "eli5": [
                    "Explanation point 1", 
                    "Explanation point 2", 
                    "..."
                ]
            }}
            ```

            **Important Notes**:

            - **Do Not Include** any promotional content or references to sponsors.
            - Ensure all field names and JSON structure match exactly.
            - Do not include any text outside of the JSON object.
            - All string values should be enclosed in double quotes.
            - For any data not available or applicable, use an empty string `""` or an empty list `[]` as appropriate.
            - The tone should be friendly and accessible, using simple language.
            - Do not add bullet points or numbering inside the strings; formatting will be handled via CSS.

            """,
            quality="Best",
        )

        try:
            result = json.loads(summary)

            return result
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error parsing summary: {str(e)}")
            # Try to extract fields from raw text if JSON parsing fails
            if isinstance(summary, str):
                # Simple extraction based on field markers
                summary = extract_between(summary, '"summary":', ',"')
                conclusion = extract_between(summary, '"conclusion":', ',"')

                if summary and conclusion:
                    result = {
                        "summary": summary.strip('" '),
                        "conclusion": conclusion.strip('" '),
                        "eli5": [],  # Default empty for failed parsing
                    }
                else:
                    return None
            else:
                return None

            return result
    except Exception as e:
        logger.error("Error extracting summary: %s", e)
        return None


def extract_between(text, start_marker, end_marker):
    """Helper function to extract text between markers"""
    try:
        start = text.find(start_marker)
        if start >= 0:
            start += len(start_marker)
            end = text.find(end_marker, start)
            if end >= 0:
                return text[start:end]
    except:
        pass
    return None
