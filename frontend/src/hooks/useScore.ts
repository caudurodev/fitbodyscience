import { calculateFromEvidencesScore, calculateAggregateScore, calculateAssertionScore } from '@/scoring/assertionScore'
import { calculateEvidenceScore } from '@/scoring/score'

export const useScore = () => {

    const getAggregateScore = (mainContent) => {
        if (!mainContent) return 0;
        const aggregateScore = calculateAggregateScore(mainContent);
        return aggregateScore
    }

    const getAssertionScore = (assertion) => {
        return calculateAssertionScore(assertion)
    }

    const getEvidenceScore = (paperClassification) => {
        if (!paperClassification) return 0
        const { normalizedScore } = calculateEvidenceScore(paperClassification)
        return Math.round(normalizedScore)

    }
    return { getAggregateScore, getAssertionScore, getEvidenceScore }
}