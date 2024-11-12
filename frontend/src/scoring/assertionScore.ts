import { calculateEvidenceScore } from '@/scoring/score'
interface Evidence {
    totalScore: number;
    type: string; // Add a type property to differentiate evidence types
}

interface Classification {
    science_paper_classification: Evidence;
}

interface AssertionContent {
    is_pro_assertion: boolean;
    content: Classification;
}

interface Assertion {
    text: string;
    contents_assertions: AssertionContent[];
}

interface SimplifiedAssertion {
    assertion: Assertion;
}

interface MainContent {
    assertions_contents: SimplifiedAssertion[];
}


interface Evidence {
    totalScore: number;
    type: string; // Add a type property to differentiate evidence types
}

interface Classification {
    science_paper_classification: Evidence;
}

interface AssertionContent {
    is_pro_assertion: boolean;
    content: Classification;
}

interface Assertion {
    text: string;
    contents_assertions: AssertionContent[];
}

interface SimplifiedAssertion {
    assertion: Assertion;
}

interface MainContent {
    assertions_contents: SimplifiedAssertion[];
}

// Helper function to calculate the evidence score
export function calculateFromEvidencesScore(evidences: Evidence[]): number {
    if (evidences.length === 0) return 0;
    const validEvidences = evidences.filter(evidence => !!calculateEvidenceScore(evidence)?.normalizedScore);
    let highestScore = 0;
    validEvidences.forEach(evidence => {
        let { normalizedScore } = calculateEvidenceScore(evidence);
        if (normalizedScore > highestScore) {
            highestScore = normalizedScore;
        }
    });
    const distinctEvidenceTypes = new Set(validEvidences.map(evidence => {
        return evidence.studyClassification.type
    })).size;
    const additionalPoints = (distinctEvidenceTypes - 1) * 5; // Add points for each additional distinct evidence type of ranked evidence
    return highestScore + additionalPoints;
}

// Calculate assertion score based on the provided evidences
export function calculateAssertionScore(assertion: Assertion) {
    const supportingEvidences = assertion.contents_assertions
        .filter(content => content.is_pro_assertion)
        .map(content => content.content.science_paper_classification)
        .filter(evidence => evidence !== null); // Filter out null evidences

    const contradictingEvidences = assertion.contents_assertions
        .filter(content => !content.is_pro_assertion)
        .map(content => content.content.science_paper_classification)
        .filter(evidence => evidence !== null); // Filter out null evidences

    const supportingScore = calculateFromEvidencesScore(supportingEvidences);
    const contradictingScore = calculateFromEvidencesScore(contradictingEvidences);

    const result = {
        'pro': Math.round(Math.max(0, Math.min(100, supportingScore))),
        'against': Math.round(Math.max(0, Math.min(100, contradictingScore)))
    }
    return result;
}

// Calculate the aggregate score for the main content
export function calculateAggregateScore(mainContent: MainContent) {

    const additionalPoints = 1;

    let totalScorePro = 0;
    let totalAssertionsPro = 0;
    let additionaPointsMoreAssertionsPro = 0;

    let totalScoreAgainst = 0;
    let totalAssertionsAgainst = 0;
    let additionaPointsMoreAssertionsAgainst = 0;

    mainContent.assertions_contents.forEach(({ assertion, weight_conclusion }) => {
        const { pro, against } = calculateAssertionScore(assertion);
        const maxWeight = 10
        const multiplier = (1 + (maxWeight - weight_conclusion) / maxWeight)
        const weighDown = ((multiplier - 1) / 2) + 1
        if (pro > 0) {
            totalScorePro += pro * weighDown
            totalAssertionsPro++;
            additionaPointsMoreAssertionsPro = additionaPointsMoreAssertionsPro + additionalPoints
        }
        if (against > 0) {
            totalScoreAgainst += against * weighDown
            totalAssertionsAgainst++;
            additionaPointsMoreAssertionsAgainst = additionaPointsMoreAssertionsAgainst + additionalPoints
        }
    });
    const aggregateScorePro = totalAssertionsPro > 0 ? (totalScorePro / totalAssertionsPro) + additionaPointsMoreAssertionsPro : 0;
    const aggregateScoreAgainst = totalAssertionsAgainst > 0 ? (totalScoreAgainst / totalAssertionsAgainst) + additionaPointsMoreAssertionsAgainst : 0;
    return {
        pro: Math.round(Math.max(0, Math.min(100, aggregateScorePro))),
        against: Math.round(Math.max(0, Math.min(100, aggregateScoreAgainst)))
    }
}

