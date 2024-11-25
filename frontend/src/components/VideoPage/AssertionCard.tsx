'use client'

import {
    Card, CardBody,
    Button, CardHeader, Accordion, AccordionItem
} from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { motion } from 'framer-motion'
import { useMutation } from '@apollo/client'
import { USER_UPDATE_ASSERTION_SCORE_MUTATION } from '@/store/assertion/mutation'
import { ScoreBar } from "@/components/scoring/ScoreBar";
import { RelatedEvidence } from "@/components/VideoPage/RelatedEvidence";

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
    const [updateAssertionScore, { loading: isUpdatingAssertionScore }] = useMutation(USER_UPDATE_ASSERTION_SCORE_MUTATION)
    const isActive = currentAssertionIndex === assertionIndex
    return (<li className="mb-8 scroll-mt-28" id={`assertion_${assertionIndex}`} >
        <Card shadow="none" radius="sm" className={isActive ? 'border-primary border-4' : ''}>
            <CardHeader className="flex-col items-start gap-2">
                <h4 className="text-xl font-bold text-primary-400">  {assertions_content.assertion.text}</h4>
                <h4 className="text-sm my-2"> {assertions_content.assertionContext}</h4>
                {assertions_content?.assertion &&
                    <>

                        <div className="flex items-center gap-4">
                            <span className="text-xs uppercase">Evidence</span>
                            <div className="flex items-center gap-2">
                                <Icon icon="mdi:approve" className="text-success" />
                                <ScoreBar score={(assertions_content?.assertion?.proEvidenceAggregateScore || 0) / 10} />
                            </div>
                            <div className="flex items-center gap-2">
                                <Icon icon="ci:stop-sign" className="text-danger" />
                                <ScoreBar score={(assertions_content?.assertion?.againstEvidenceAggregateScore || 0) / 10} />
                            </div>

                            <Button
                                color="primary"
                                size="sm"
                                isLoading={isUpdatingAssertionScore}
                                onPress={async () => {
                                    updateAssertionScore({ variables: { assertionId: assertions_content?.assertion?.id } })
                                }}
                            >
                                {!isUpdatingAssertionScore && <Icon icon="mdi:refresh" className="inline" />} update assertionscore
                            </Button>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="text-xs uppercase">Importance</span>
                            <ScoreBar score={assertions_content?.weightConclusion || 0} />
                        </div>
                    </>
                }
            </CardHeader>
            <CardBody className="flex">
                <Accordion
                    showDivider={false}
                    itemClasses={{
                        base: "py-0",
                        title: "font-normal text-small",
                        trigger: "px-0 py-0 data-[hover=true]:bg-default-100",
                        content: "text-small px-2"
                    }}
                >
                    <AccordionItem
                        key="evidence"
                        title={
                            <h5 className="text-xs uppercase">
                                Was said (time: {assertions_content?.videoTimestamp}):
                            </h5>
                        }
                    >
                        <p className="italic">
                            &quot;{assertions_content?.assertion.originalSentence}&quot;
                        </p>
                    </AccordionItem>
                </Accordion>

                <RelatedEvidence
                    refetch={refetch}
                    assertions_content={assertions_content}
                />
            </CardBody>
        </Card>
    </li>)
}