interface PaperDetails {
    doi: string;
    title: string;
    authors: string[];
    journal: string;
    publicationDate: string;
}

interface Methodology {
    blinding?: boolean;
    sampleSize?: number;
    controlGroup?: boolean;
    randomization?: boolean;
    followUpDuration?: string;
    confoundingControl?: string;
}

interface ExternalValidity {
    generalizability?: string;
    ecologicalValidity?: string;
}

interface StatisticalAnalysis {
    pValuesReported?: boolean;
    appropriateTests?: boolean;
    effectSizeReported?: boolean;
    pValueSignificance?: number;
    confidenceIntervalsReported?: boolean;
}

interface PeerReviewPublication {
    preRegistration?: boolean;
    journalImpactFactor?: string;
    peerReviewedJournal?: boolean;
}

interface ReportingTransparency {
    detailedMethodology?: boolean;
    replicationPossible?: boolean;
    researchQuestionsClear?: boolean;
    conflictOfInterestDisclosed?: boolean;
}

type HierarchyOfEvidence =
    | "Systematic Reviews and Meta-Analyses"
    | "Randomized Controlled Trials (RCTs)"
    | "Cohort Studies"
    | "Case-Control Studies"
    | "Cross-Sectional Studies"
    | "Case Reports and Case Series"
    | "Expert Opinion and Editorials";

interface StudyClassification {
    type?: string;
    methodology?: Methodology;
    externalValidity?: ExternalValidity;
    hierarchyOfEvidence?: HierarchyOfEvidence;
    statisticalAnalysis?: StatisticalAnalysis;
    peerReviewPublication?: PeerReviewPublication;
    reportingTransparency?: ReportingTransparency;
}

interface Payload {
    paperDetails: PaperDetails;
    studyClassification?: StudyClassification;
}

export function calculateEvidenceScore(payload: Payload): any {
    if (!payload?.studyClassification) {
        return 0
    };
    const methodologyScores = {
        randomization: payload.studyClassification?.methodology?.randomization ? 20 : 0,
        blinding: payload.studyClassification?.methodology?.blinding ? 20 : 0,
        controlGroup: payload.studyClassification?.methodology?.controlGroup ? 20 : 0,
        sampleSize: payload.studyClassification?.methodology?.sampleSize && payload.studyClassification.methodology.sampleSize > 200 ? 20 :
            (payload.studyClassification?.methodology?.sampleSize && payload.studyClassification.methodology.sampleSize >= 50 ? 10 : 0),
        followUpDuration: payload.studyClassification?.methodology?.followUpDuration && payload.studyClassification.methodology.followUpDuration.includes("year") ? 20 :
            (payload.studyClassification?.methodology?.followUpDuration && payload.studyClassification.methodology.followUpDuration.includes("month") ? 10 : 0),
        confoundingControl: payload.studyClassification?.methodology?.confoundingControl && payload.studyClassification.methodology.confoundingControl.includes("multivariate") ? 20 :
            (payload.studyClassification?.methodology?.confoundingControl && payload.studyClassification.methodology.confoundingControl.includes("stratification") ? 10 : 0)
    };
    const methodologyTotal = Object.values(methodologyScores).reduce((a, b) => a + b, 0);

    const statisticalAnalysisScores = {
        appropriateTests: payload.studyClassification?.statisticalAnalysis?.appropriateTests ? 25 : 0,
        effectSizeReported: payload.studyClassification?.statisticalAnalysis?.effectSizeReported ? 25 : 0,
        confidenceIntervalsReported: payload.studyClassification?.statisticalAnalysis?.confidenceIntervalsReported ? 25 : 0,
        pValuesReported: payload.studyClassification?.statisticalAnalysis?.pValuesReported ? 25 : 0
    };
    const statisticalAnalysisTotal = Object.values(statisticalAnalysisScores).reduce((a, b) => a + b, 0);

    const reportingTransparencyScores = {
        researchQuestionsClear: payload.studyClassification?.reportingTransparency?.researchQuestionsClear ? 20 : 0,
        detailedMethodology: payload.studyClassification?.reportingTransparency?.detailedMethodology ? 20 : 0,
        conflictOfInterestDisclosed: payload.studyClassification?.reportingTransparency?.conflictOfInterestDisclosed ? 20 : 0,
        replicationPossible: payload.studyClassification?.reportingTransparency?.replicationPossible ? 20 : 0,
        dataAvailable: 0  // Data availability not provided in the payload, assuming 0
    };
    const reportingTransparencyTotal = Object.values(reportingTransparencyScores).reduce((a, b) => a + b, 0);

    const peerReviewPublicationScores = {
        peerReviewedJournal: payload.studyClassification?.peerReviewPublication?.peerReviewedJournal ? 50 : 0,
        journalImpactFactor: payload.studyClassification?.peerReviewPublication?.journalImpactFactor === "High" ? 30 :
            (payload.studyClassification?.peerReviewPublication?.journalImpactFactor === "Moderate" ? 20 : 10),
        preRegistration: payload.studyClassification?.peerReviewPublication?.preRegistration ? 20 : 0
    };
    const peerReviewPublicationTotal = Object.values(peerReviewPublicationScores).reduce((a, b) => a + b, 0);

    const externalValidityScores = {
        generalizability: payload.studyClassification?.externalValidity?.generalizability === "High" ? 50 :
            (payload.studyClassification?.externalValidity?.generalizability === "Moderate" ? 25 : 0),
        ecologicalValidity: payload.studyClassification?.externalValidity?.ecologicalValidity === "High" ? 50 :
            (payload.studyClassification?.externalValidity?.ecologicalValidity === "Moderate" ? 25 : 0)
    };
    const externalValidityTotal = Object.values(externalValidityScores).reduce((a, b) => a + b, 0);

    const hierarchyOfEvidenceScores: Record<HierarchyOfEvidence, number> = {
        "Systematic Reviews and Meta-Analyses": 100,
        "Randomized Controlled Trials (RCTs)": 90,
        "Cohort Studies": 70,
        "Case-Control Studies": 60,
        "Cross-Sectional Studies": 50,
        "Case Reports and Case Series": 30,
        "Expert Opinion and Editorials": 10
    };
    const hierarchyOfEvidenceScore = (payload.studyClassification?.hierarchyOfEvidence &&
        hierarchyOfEvidenceScores[payload.studyClassification.hierarchyOfEvidence]) || 0;

    const totalScore = methodologyTotal + statisticalAnalysisTotal + reportingTransparencyTotal + peerReviewPublicationTotal + externalValidityTotal + hierarchyOfEvidenceScore;

    const normalizedScore = (totalScore / 600) * 100;

    return {
        methodologyScores,
        statisticalAnalysisScores,
        reportingTransparencyScores,
        peerReviewPublicationScores,
        externalValidityScores,
        hierarchyOfEvidenceScore,
        totalScore,
        normalizedScore
    };
}
