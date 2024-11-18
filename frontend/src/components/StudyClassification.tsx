import { useEffect, useState } from 'react'
import { calculateEvidenceScore } from '@/scoring/score'
import { Chip } from "@nextui-org/react";

export const StudyClassification = ({ paperClassification }: { paperClassification: any }) => {
    const [scores, setScores] = useState(null)
    useEffect(() => {
        if (!!paperClassification) {
            const scoresCalculated = calculateEvidenceScore(paperClassification)
            setScores(scoresCalculated)
        }
    }, [paperClassification])
    const paperDetails = paperClassification?.paperDetails
    const studyType = paperClassification?.studyClassification?.type
    return (
        <div>
            {/* {!!scores && <>
                <ScoresDisplay scores={scores} />
            </>} */}
            {!!paperDetails &&
                <div className="my-4">
                    {/* <h6 className="text-tiny uppercase">{paperDetails?.doi}</h6> */}
                    <Chip color="warning" className="text-white">{studyType}</Chip>
                </div>
            }
        </div>
    )
}

export default StudyClassification



interface Scores {
    methodologyScores: Record<string, number>;
    statisticalAnalysisScores: Record<string, number>;
    reportingTransparencyScores: Record<string, number>;
    peerReviewPublicationScores: Record<string, number>;
    externalValidityScores: Record<string, number>;
    hierarchyOfEvidenceScore: number;
    totalScore: number;
    normalizedScore: number;
}

interface Props {
    scores: Scores;
}

const ScoresDisplay: React.FC<Props> = ({ scores }) => {
    return (
        <div>
            {/* <h5>Methodology</h5>
            <ul>
                {Object.entries(scores.methodologyScores).map(([key, value]) => (
                    <li key={key}>{key}: {value}</li>
                ))}
            </ul>
            <h5>External Validity</h5>
            <ul>
                {Object.entries(scores.externalValidityScores).map(([key, value]) => (
                    <li key={key}>{key}: {value}</li>
                ))}
            </ul>
            <h5>Statistical Analysis</h5>
            <ul>
                {Object.entries(scores.statisticalAnalysisScores).map(([key, value]) => (
                    <li key={key}>{key}: {value}</li>
                ))}
            </ul>
            <h5>Peer Review Publication</h5>
            <ul>
                {Object.entries(scores.peerReviewPublicationScores).map(([key, value]) => (
                    <li key={key}>{key}: {value}</li>
                ))}
            </ul>
            <h5>Reporting Transparency</h5>
            <ul>
                {Object.entries(scores.reportingTransparencyScores).map(([key, value]) => (
                    <li key={key}>{key}: {value}</li>
                ))}
            </ul>
            <h5>Hierarchy of Evidence</h5>
            <ul>
                <li>Score: {scores.hierarchyOfEvidenceScore}</li>
            </ul>
            <h5 >Total Score</h5>
            <ul>
                <li >Score: {scores.totalScore}</li>
            </ul> */}
            {/* <h5 className="text-xl font-bold">Normalized Score</h5> */}
            {/* <ul>
                <li className="text-xl font-bold text-green-500">Score: {Math.round(Number(scores?.normalizedScore))}/100</li>
            </ul> */}
            <Chip color="success" className="text-white font-bold">{Math.round(Number(scores?.normalizedScore))} / 100</Chip>
        </div>
    );
};