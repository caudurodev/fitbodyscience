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
            Given a science paper with crossref json data like this:
            
            {crossref_data}

            and full text like this:

            {study_fulltext}

            Return a JSON with important classification information following the instructions below:

            To classify a scientific paper based on its rigor, quality, and reliability, follow these detailed instructions:
            Input Information

            Crossref Information: Use the provided metadata such as journal name, publication date, DOI, author affiliations, and citation count.
            Summary and Abstract: Utilize the abstract and summary of the paper to understand the study's objectives, methods, and conclusions.

            Steps to Classify the Paper

                Identify the Type of Study:
                    Systematic Review and Meta-Analysis: Look for indications that the paper synthesizes results from multiple studies.
                    Randomized Controlled Trial (RCT): Check for terms like "randomized", "control group", and "trial".
                    Cohort Study: Identify if the study follows a group of people over time.
                    Case-Control Study: Determine if the study compares individuals with and without a condition.
                    Cross-Sectional Study: Look for data collected at a single point in time.
                    Case Report/Series: Look for detailed descriptions of individual or grouped cases.
                    Expert Opinion/Editorial: Identify if the paper is based on expert consensus or clinical experience.

                Assess Study Design and Methodology:
                    Randomization: Check if the subjects were randomly assigned to groups.
                    Blinding: Look for terms indicating whether the study was single-blind, double-blind, or not blinded.
                    Control Groups: Determine if there is a comparison against a baseline or control group.
                    Sample Size: Note the number of participants; larger sizes typically increase reliability.
                    Follow-Up Duration: Check how long the subjects were followed.
                    Confounding Control: Look for statistical methods used to control confounding variables.

                Evaluate Statistical Analysis:
                    Statistical Tests: Ensure appropriate statistical tests were used for the data type.
                    Effect Size and Confidence Intervals: Check if these measures are reported.
                    P-Values and Significance Levels: Note the p-values and whether the results are statistically significant.

                Review Reporting and Transparency:
                    Research Questions and Objectives: Ensure the study has clear aims and hypotheses.
                    Methodology Details: Verify that the study design, procedures, and analysis methods are described thoroughly.
                    Conflict of Interest Disclosures: Look for disclosures about funding sources and conflicts of interest.
                    Replication and Reproducibility: Assess if the study can be replicated with the provided information.

                Check Peer Review and Publication:
                    Peer-Reviewed Journal: Confirm if the paper is published in a reputable, peer-reviewed journal.
                    Impact Factor: Consider the journal's impact factor as an additional quality indicator.
                    Pre-Registration: Check if the study was pre-registered in a clinical trial database or registry.

                Assess External Validity:
                    Generalizability: Determine if the findings can be applied to broader populations.
                    Ecological Validity: Assess if the study conditions reflect real-world settings.

            Output Classification

            Based on the analysis, classify the scientific paper into one of the following categories:

                High Quality and Reliable: Papers that rank high in the hierarchy of evidence, have rigorous study designs, appropriate statistical analysis, transparent reporting, and are published in reputable journals.
                Moderate Quality and Reliability: Papers that are generally sound but may have some limitations in methodology or reporting.
                Low Quality and Reliability: Papers with significant methodological flaws, poor reporting, or published in less reputable journals.

            Example Classification Process

                Study Type: Determine if the study is a Randomized Controlled Trial.
                Design and Methodology: Check for randomization and blinding methods.
                Statistical Analysis: Ensure appropriate statistical tests were used and results are significant.
                Reporting and Transparency: Verify detailed methodology and conflict of interest disclosures.
                Peer Review and Publication: Confirm publication in a peer-reviewed journal with a high impact factor.
                External Validity: Assess if the results are generalizable and ecologically valid.

            By following these steps, you can classify scientific papers effectively, determining their rigor, quality, and reliability.

            Return valid JSON response like this:
           {{
                "paperDetails": {{
                    "title": "",
                    "authors": ["John Doe", "Jane Smith"],
                    "journal": "Journal of Medical Research",
                    "publicationDate": "2024-05-01",
                    "doi": "10.1234/jmr.2024.5678",
                }},
                "studyClassification": {{
                    "type": "Randomized Controlled Trial",
                    "hierarchyOfEvidence": "High",
                    "methodology": {{
                        "randomization": true,
                        "blinding": "Double-blind",
                        "controlGroup": true,
                        "sampleSize": 500,
                        "followUpDuration": "12 months",
                        "confoundingControl": "Multivariate analysis"
                    }},
                    "statisticalAnalysis": {{
                        "appropriateTests": true,
                        "effectSizeReported": true,
                        "confidenceIntervalsReported": true,
                        "pValuesReported": true,
                        "pValueSignificance": 0.001
                    }},
                    "reportingTransparency": {{
                        "researchQuestionsClear": true,
                        "detailedMethodology": true,
                        "conflictOfInterestDisclosed": true,
                        "replicationPossible": true
                    }},
                    "peerReviewPublication": {{
                        "peerReviewedJournal": true,
                        "journalImpactFactor": 8.5,
                        "preRegistration": true
                    }},
                    "externalValidity": {{
                        "generalizability": "High",
                        "ecologicalValidity": "Moderate"
                    }}
                }}
            }}

        """
        )
        # #logger.info("classify result : %s", classify)
        try:
            classify_json = json.loads(classify)
            return classify_json
        except Exception as e:
            logger.error("Error classify_evidence_content assertions1: %s", e)
            logger.info("classify: %s", classify)
            return None
    except Exception as e:
        logger.error("Error classify_evidence_content2: %s", e)
        return None
