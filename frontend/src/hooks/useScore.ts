import { calculateFromEvidencesScore, calculateAggregateScore, calculateAssertionScore } from '@/scoring/assertionScore'
import { calculateEvidenceScore } from '@/scoring/score'

export const useScore = () => {

    const getAggregateScore = (mainContent: any) => {
        if (!mainContent) return 0;
        const aggregateScore = calculateAggregateScore(mainContent);
        return aggregateScore
    }

    const getAssertionScore = (assertion: any) => {
        return calculateAssertionScore(assertion)
    }

    const getEvidenceScore = (paperClassification: any) => {
        if (!paperClassification) return 0
        const { normalizedScore } = calculateEvidenceScore(paperClassification)
        return Math.round(normalizedScore)

    }
    return { getAggregateScore, getAssertionScore, getEvidenceScore }
}