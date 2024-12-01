'use client'

import { Card, CardBody, Button, CardHeader } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { useMutation } from '@apollo/client'
import { USER_UPDATE_ASSERTION_SCORE_MUTATION } from '@/store/assertion/mutation'
import { ScoreBar } from "@/components/scoring/ScoreBar";
import { RelatedEvidence } from "@/components/VideoPage/RelatedEvidence";
import { useResponsive } from "@/hooks/useResponsive";

interface AssertionCardProps {
    assertions_content: any;
    currentAssertionIndex: number;
    refetch: () => void
    assertionIndex: number
}
export const AssertionCard = ({
    refetch,
    assertionIndex,
    currentAssertionIndex,
    assertions_content,
}: AssertionCardProps) => {
    const { isMobile } = useResponsive()
    const [updateAssertionScore, { loading: isUpdatingAssertionScore }] = useMutation(USER_UPDATE_ASSERTION_SCORE_MUTATION)
    const isActive = currentAssertionIndex === assertionIndex
    return (<li className="mb-8 scroll-mt-28" id={`assertion_${assertionIndex}`} >
        <Card shadow="none" radius="sm" className={isActive ? 'border-primary border-4' : ''}>
            <CardHeader className="flex-col items-start gap-2">
                <h4 className="text-xl font-bold text-primary-500">{assertions_content.assertion.text}</h4>
                <h4 className="text-sm my-2"><b className="text-xs uppercase">Context:</b> {assertions_content.assertionContext}</h4>
                {assertions_content?.assertion &&
                    <>
                        <div className="flex items-center gap-4">
                            <span className="text-xs uppercase">Score</span>
                            <div className="flex items-center gap-2">
                                <Icon icon="mdi:success-bold" className="text-success" />
                                <ScoreBar score={(assertions_content?.assertion?.proEvidenceAggregateScore || 0) / 10} />
                            </div>
                            <div className="flex items-center gap-2">
                                <Icon icon="maki:cross" className="text-danger" />
                                <ScoreBar score={(assertions_content?.assertion?.againstEvidenceAggregateScore || 0) / 10} />
                            </div>

                            {
                                !isMobile && <Button
                                    color="primary"
                                    size="sm"
                                    isLoading={isUpdatingAssertionScore}
                                    onPress={async () => {
                                        updateAssertionScore({ variables: { assertionId: assertions_content?.assertion?.id } })
                                    }}
                                >
                                    {!isUpdatingAssertionScore && <Icon icon="mdi:refresh" className="inline" />} Recalculate
                                </Button>
                            }
                        </div>
                        {/* <div className="flex items-center gap-2">
                            <span className="text-xs uppercase">Importance to video</span>
                            <ScoreBar score={assertions_content?.weightConclusion || 0} />
                        </div> */}
                    </>
                }
            </CardHeader>
            <CardBody className="flex">
                <div className="bg-secondary/10 px-2  py-1 rounded-md my-2">
                    <h5 className="text-xs uppercase my-2">
                        At: {assertions_content?.videoTimestamp}:
                    </h5>
                    <p className="italic my-2">
                        &quot;{assertions_content?.assertion.originalSentence}&quot;
                    </p>
                </div>
                <RelatedEvidence
                    refetch={refetch}
                    assertions_content={assertions_content}
                />
            </CardBody>
        </Card>
    </li >)
}