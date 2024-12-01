""" This module extracts assertions from long text and adds them to the content store """

import json
from ..vendors.llm.get_response import get_response
from ..utils.config import logger


def extract_assertions_from_long_text(
    long_text, additional_information, related_content
):
    """extract assertions from long text"""
    try:
        assertions = get_response(
            f"""
            Given the following:

            1. **Long Text:**

            {long_text}

            2. **Additional Information about the Long Text (possibly links to evidence, etc.):**

            {additional_information}

            3. **Saved Links Related to the Text in JSON Format:**

            {related_content}

            ---

            **Instructions:**

            Extract all important assertions from the long text that make up the core of the argument. 
            For each assertion, provide detailed information as specified below, and return a valid JSON object.

            ---

            **JSON Structure:**

            {{
            "main_conclusion": "The main conclusion of the text for which most assertions are relevant.",
            "assertions": [
                {{
                "assertion": "The specific assertion from the text as a standalone sentence that explains the assertion.",
                "assertion_weight": "An integer from 0 to 10 indicating how important the assertion is to the main point (0 = irrelevant, 10 = critical).",
                "standalone_assertion_reliability": "An integer from 0 to 10 evaluating the reliability of the assertion by itself without larger context (0 = completely unreliable, 10 = completely reliable).",
                "why_relevant_main_point": "A short explanation of why the assertion is relevant to the main conclusion.",
                "assertion_context": "Context to help readers understand the topics the assertion refers to.",
                "assertion_search_verify": "A precise sentence encapsulating the assertion for verification via a search engine.",
                "part_of_text_assertion_made": "The exact sentence from the original text where the assertion was made.",
                "part_of_transcript_assertion_timestamp": "The timestamp from the video transcript where the assertion appears, if available.",
                "assertion_type": "The most likely type of assertion (e.g., 'true', 'false').",
                "fallacy": "Type of fallacy if the assertion is likely false; otherwise, 'none'.",
                "evidence_type": "Evidence supporting the assertion if mentioned in the text.",
                "conflict_of_interest": "Any conflicts of interest related to the assertion, if mentioned.",
                "citations": [
                    {{
                    "url": "URL of the source provided in the text or additional information.",
                    "contentId": "The UUID from related_content if applicable.",
                    "why_relevant": "Explanation of why the evidence is relevant to the assertion.",
                    "content_weight_to_assertion": "An integer from 0 to 10 indicating how critical the evidence is to support the assertion (0 = irrelevant, 10 = critical)."
                    }}
                ],
                "tags": ["concepts from the assertion (e.g., astronomy, geology, science)"]
                }}
            ]
            }}

            ---

            **Additional Guidelines:**

            - **Source Integrity:** Only include assertions and evidence present in the provided text or additional information. Do not add any content not found in these sources.
            - **Promotional Content:** Ignore any promotional or sponsored content. If sponsored content presents a conflict of interest, note it in the "conflict_of_interest" property.
            - **Assertion Clarity:** Ensure each assertion is clear and accurately reflects the original text.
            - **Evidence Accuracy:** Only include evidence that is directly mentioned in the text. Do not infer or add external evidence.
            - **JSON Validity:** Return a well-formatted JSON without syntax errors, such as unnecessary trailing commas.
            - **Exclusions:** Do not include any assertions or evidence not found in the provided text.

            ---

            **Example JSON Response:**

            {{
            "main_conclusion": "The main point most of the assertions are trying to make.",
            "assertions": [
                {{
                "assertion": "The earth is round.",
                "assertion_weight": "10",
                "standalone_assertion_reliability": "10",
                "why_relevant_main_point": "This assertion supports the main conclusion about the earth's shape.",
                "assertion_context": "Discussion about the shape of the Earth in a geographical context.",
                "assertion_search_verify": "Is there scientific evidence that the Earth is round?",
                "part_of_text_assertion_made": "Scientists have proven that the Earth is round through satellite imagery.",
                "part_of_transcript_assertion_timestamp": "3:12",
                "assertion_type": "true",
                "fallacy": "none",
                "evidence_type": "Satellite images and space missions confirm the Earth's roundness.",
                "conflict_of_interest": "",
                "citations": [
                    {{
                    "url": "https://www.nasa.gov/mission_pages/satellites/main/index.html",
                    "contentId": "uuid-1234",
                    "why_relevant": "Provides satellite evidence supporting the Earth's shape.",
                    "content_weight_to_assertion": "9"
                    }}
                ],
                "tags": ["astronomy", "geography", "science", "Earth"]
                }}
            ]
            }}

            ---

            **Final Notes:**

            - Focus on extracting assertions that are significant to the text's main argument.
            - Provide comprehensive details for each assertion to facilitate verification through primary scientific studies.
            - Ensure all information is accurate and derived solely from the provided text and additional information.
            - Avoid adding any content not found in the provided text or additional information.

            ---
            """
        )
        # #logger.info("Assertions found: %s", assertions)
        try:
            assertions_json = json.loads(assertions)
            return assertions_json
        except Exception as e:
            logger.error("Error parsing assertions: %s", e)
            logger.info("assertions %s", assertions)
            return None
    except Exception as e:
        logger.error("Error extracting assertions: %s", e)
        return None
