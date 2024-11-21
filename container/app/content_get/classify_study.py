""" This module extracts assertions from long text and adds them to the content store """

import json
from ..vendors.llm.get_response import get_response
from ..utils.config import logger
from ..content_store.get_content import get_content_by_id


def classify_evidence_content(content_id):
    """extract assertions from long text"""

    try:
        result = get_content_by_id(content_id)

        content = result[0]
        # #logger.info("content: %s", content)
        crossref_data = content["crossrefInfo"]
        # #logger.info("crossref_data: %s", crossref_data)
        study_fulltext = content["fullText"]
        # #logger.info("study_fulltext: %s", study_fulltext)
    except Exception as e:
        logger.error("Error getting content: %s", e)
        return None

    try:
        classify = get_response(
            f"""
            Given a scientific paper with Crossref JSON data as follows:

            {crossref_data}

            and the full text of the paper as follows:

            {study_fulltext}

            **Task**: Classify the scientific paper based on its rigor, quality, and reliability, and return a JSON object with the specified structure.

            **Instructions**:

            **1. Analyze the Paper**

            - Use the provided Crossref metadata (e.g., journal name, publication date, DOI, author affiliations, citation count).
            - Utilize the abstract and summary from the full text to understand the study's objectives, methods, and conclusions.

            **2. Classification Steps**

            **a. Identify the Type of Study**

            Choose one of the following for `"type"`:

            - "Systematic Review and Meta-Analysis"
            - "Randomized Controlled Trial"
            - "Cohort Study"
            - "Case-Control Study"
            - "Cross-Sectional Study"
            - "Case Report/Series"
            - "Expert Opinion/Editorial"

            **b. Assess Study Design and Methodology**

            - `"randomization"`: `true` or `false`
            - `"blinding"`: One of "None", "Single-blind", "Double-blind", "Triple-blind"
            - `"controlGroup"`: `true` or `false`
            - `"sampleSize"`: Integer (number of participants)
            - `"model"`: One of "Observational", "Experimental", "Quasi-experimental"
            - `"conclusionType"`: One of "Causal", "Correlational", "Descriptive"
            - `"statisticalSignificance"`: Numeric value (e.g., 0.05)
            - `"studySubjects"`: One of "Human", "Animal", "In Vitro", "Other"
            - `"followUpDuration"`: String (e.g., "12 months")
            - `"confoundingControl"`: One of "None", "Multivariate analysis", "Randomization", "Matching", "Stratification", "Statistical adjustment"

            **c. Evaluate Statistical Analysis**

            - `"appropriateTests"`: `true` or `false`
            - `"effectSizeReported"`: `true` or `false`
            - `"confidenceIntervalsReported"`: `true` or `false`
            - `"pValuesReported"`: `true` or `false`
            - `"pValueSignificance"`: Numeric value (e.g., 0.001)

            **d. Review Reporting and Transparency**

            - `"researchQuestionsClear"`: `true` or `false`
            - `"detailedMethodology"`: `true` or `false`
            - `"conflictOfInterestDisclosed"`: `true` or `false`
            - `"replicationPossible"`: `true` or `false`

            **e. Check Peer Review and Publication**

            - `"peerReviewedJournal"`: `true` or `false`
            - `"journalImpactFactor"`: Numeric value (e.g., 8.5)
            - `"preRegistration"`: `true` or `false`

            **f. Assess External Validity**

            - `"generalizability"`: One of "High", "Moderate", "Low"
            - `"ecologicalValidity"`: One of "High", "Moderate", "Low"

            **3. Output Classification**

            Based on your analysis, set `"hierarchyOfEvidence"` to one of:

            - "High"
            - "Moderate"
            - "Low"

            **4. Return a Valid JSON Object**

            Structure your JSON response exactly like this:

            {{
                "paperDetails": {{
                    "title": "<Title of the paper>",
                    "authors": ["Author One", "Author Two"],
                    "journal": "<Journal Name>",
                    "publicationDate": "YYYY-MM-DD",
                    "doi": "<DOI>"
                }},
                "studyClassification": {{
                    "type": "<Type of Study from the list above>",
                    "hierarchyOfEvidence": "<High|Moderate|Low>",
                    "methodology": {{
                        "randomization": true,
                        "blinding": "<None|Single-blind|Double-blind|Triple-blind>",
                        "controlGroup": true,
                        "sampleSize": <Integer>,
                        "model": "<Observational|Experimental|Quasi-experimental>",
                        "conclusionType": "<Causal|Correlational|Descriptive>",
                        "statisticalSignificance": <Numeric value>,
                        "studySubjects": "<Human|Animal|In Vitro|Other>",
                        "followUpDuration": "<Duration (e.g., '12 months')>",
                        "confoundingControl": "<Option from the list above>"
                    }},
                    "statisticalAnalysis": {{
                        "appropriateTests": true,
                        "effectSizeReported": true,
                        "confidenceIntervalsReported": true,
                        "pValuesReported": true,
                        "pValueSignificance": <Numeric value>
                    }},
                    "reportingTransparency": {{
                        "researchQuestionsClear": true,
                        "detailedMethodology": true,
                        "conflictOfInterestDisclosed": true,
                        "replicationPossible": true
                    }},
                    "peerReviewPublication": {{
                        "peerReviewedJournal": true,
                        "journalImpactFactor": <Numeric value>,
                        "preRegistration": true
                    }},
                    "externalValidity": {{
                        "generalizability": "<High|Moderate|Low>",
                        "ecologicalValidity": "<High|Moderate|Low>"
                    }}
                }}
            }}
            
        """,
            quality="best",
        )
        # Log the raw response for debugging
        logger.debug(f"Raw classification response: {classify}")
        
        if not classify:
            logger.error("Empty response from classification")
            return None
        
        # Remove any trailing whitespace or newlines that might affect JSON parsing
        classify = classify.strip()
        
        # Try to parse the JSON
        try:
            classify_json = json.loads(classify)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Failed JSON content: {classify}")
            return None
        
        # Validate required fields are present
        required_fields = ["paperDetails", "studyClassification"]
        for field in required_fields:
            if field not in classify_json:
                logger.error(f"Missing required field '{field}' in classification response")
                return None
        
        # Validate study classification fields
        study_class = classify_json.get("studyClassification", {})
        required_study_fields = ["methodology", "statisticalAnalysis", "reportingTransparency", "peerReviewPublication", "externalValidity"]
        for field in required_study_fields:
            if field not in study_class:
                logger.error(f"Missing required study classification field '{field}'")
                return None
        
        return classify_json
        
    except Exception as e:
        logger.error(f"Unexpected error in classify_evidence_content: {str(e)}")
        return None
