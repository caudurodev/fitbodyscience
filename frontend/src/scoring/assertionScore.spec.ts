import { calculateAggregateScore } from '@/scoring/assertionScore'; // Adjust the import path as necessary
import { calculateEvidenceScore } from '@/scoring/score';

// Mock the calculateEvidenceScore function
jest.mock('@/scoring/score', () => ({
    calculateEvidenceScore: jest.fn()
}));

describe('calculateAggregateScore', () => {
    beforeAll(() => {
        // Mock the implementation of calculateEvidenceScore
        (require('@/scoring/score').calculateEvidenceScore as jest.Mock).mockImplementation((content) => {
            switch (content.science_paper_classification) {
                case 'supporting1': return { totalScore: 30 };
                case 'supporting2': return { totalScore: 50 };
                case 'contradicting1': return { totalScore: 20 };
                default: return { totalScore: 0 };
            }
        });
    });

    it('should calculate the correct aggregate score', () => {
        const mainContent = {
            assertions_contents: [
                {
                    assertion: {
                        text: "Assertion 1",
                        contents_assertions: [
                            { is_pro_assertion: true, content: { science_paper_classification: 'supporting1' } },
                            { is_pro_assertion: true, content: { science_paper_classification: 'supporting2' } }
                        ]
                    },
                    weight: 1
                },
                {
                    assertion: {
                        text: "Assertion 2",
                        contents_assertions: [
                            { is_pro_assertion: true, content: { science_paper_classification: 'supporting2' } }
                        ]
                    },
                    weight: 2
                },
                {
                    assertion: {
                        text: "Assertion 3",
                        contents_assertions: [
                            { is_pro_assertion: true, content: { science_paper_classification: 'supporting2' } },
                            { is_pro_assertion: false, content: { science_paper_classification: 'contradicting1' } }
                        ]
                    },
                    weight: 1
                },
                {
                    assertion: {
                        text: "Assertion 4",
                        contents_assertions: []
                    },
                    weight: 1
                }
            ]
        };

        const maxImportanceWeight = 2;
        const aggregateScore = calculateAggregateScore(mainContent, maxImportanceWeight);

        // Calculate expected aggregate score manually
        const expectedWeightedScores = [20, 100, 7.5, 0]; // Corrected weights * scores
        const expectedTotalWeight = 1 + 2 + 1 + 1;
        const expectedAggregateScore = expectedWeightedScores.reduce((sum, score) => sum + score, 0) / expectedTotalWeight;
        const expectedNormalizedScore = Math.min(expectedAggregateScore, 100); // Normalize if necessary

        expect(aggregateScore).toBeCloseTo(expectedNormalizedScore, 1); // Using toBeCloseTo for potential floating-point precision issues
    });
});
