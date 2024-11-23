
'use client'

import {
    Spinner,
    Button, Chip, Accordion, AccordionItem
} from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { useMutation } from '@apollo/client'
import { EvidenceInfo } from '@/components/VideoPage/EvidenceInfo';
import { USER_SEARCH_MORE_EVIDENCE_MUTATION } from '@/store/action/action'


interface RelatedEvidenceProps {
    assertions_content: any;
    refetch: () => void
}
export const RelatedEvidence = ({
    assertions_content,
    refetch,
}: RelatedEvidenceProps) => {
    const contentAssertions = assertions_content?.assertion?.contents_assertions || [];
    const proEvidence = contentAssertions?.filter((e: any) => e.isProAssertion) || [];
    const conEvidence = contentAssertions?.filter((e: any) => !e.isProAssertion) || [];

    const [userSearchMoreEvidence, { loading: isSearchingMoreEvidence }] = useMutation(USER_SEARCH_MORE_EVIDENCE_MUTATION)
    return (
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
                aria-label="Evidence related to assertion"
                title={
                    <>
                        <h5 className="uppercase text-xs">
                            Evidence related to assertion
                            ({contentAssertions?.length})
                        </h5>
                        <div className="flex gap-2 mt-2">
                            {(() => {
                                return (
                                    <>
                                        {proEvidence.length > 0 && (
                                            <Chip color="success" size="sm" className="text-white">
                                                <Icon icon="mdi:approve" className="inline" />{' '}
                                                {proEvidence.length} supporting ({
                                                    Math.round(
                                                        proEvidence.reduce((acc: any, e: any) => acc + (e.content?.contentScore || 0), 0) / proEvidence.length
                                                    )
                                                }/100)
                                            </Chip>
                                        )}
                                        {conEvidence.length > 0 && (
                                            <Chip color="danger" size="sm" className="text-white">
                                                <Icon icon="ci:stop-sign" className="inline" />{' '}
                                                {conEvidence.length} opposing ({
                                                    Math.round(
                                                        conEvidence.reduce((acc: any, e: any) => acc + (e.content?.contentScore || 0), 0) / conEvidence.length
                                                    )
                                                }/100)
                                            </Chip>
                                        )}
                                    </>
                                );
                            })()}
                        </div>
                    </>
                }
            >
                {!assertions_content?.assertion?.contents_assertions?.length || assertions_content?.assertion?.contents_assertions?.length === 0 &&
                    <Spinner />
                }
                {assertions_content?.assertion?.contents_assertions?.length > 0 ?
                    <>
                        {
                            assertions_content?.assertion?.contents_assertions.map(
                                (o: any, i: number) => (
                                    <Accordion key={i} id={`assertion_${i}`} className="mb-4">
                                        <AccordionItem
                                            key="evidence-details"
                                            aria-label={o?.content?.title || "Evidence details"}
                                            title={
                                                <div className="flex items-top gap-2">
                                                    <Chip
                                                        color={o?.isProAssertion ? 'success' : 'danger'}
                                                        className="text-white"
                                                    >
                                                        <Icon className="inline text-lg" icon={o?.isProAssertion ? "mdi:approve" : "ci:stop-sign"} />{' '}
                                                        {Math.round(o?.content?.contentScore || 0)} / 100
                                                    </Chip>
                                                    <span className="text-sm">{o?.content?.title ?? "Not yet downladed..."}</span>
                                                </div>
                                            }
                                        >
                                            <div className="ml-8 my-2">
                                                <h6 className="text-tiny uppercase">{o?.isCitationFromOriginalContent ? 'From Author' : 'Ai Research'}</h6>
                                                <h6>{o?.whyRelevant}</h6>
                                                <EvidenceInfo refetch={refetch} evidence={o?.content} />
                                            </div>

                                        </AccordionItem>
                                    </Accordion>
                                ))
                        }
                    </> :
                    <div>
                        <h6 className="text-red-500 font-bold">* Evidence not yet found</h6>
                        <Button
                            color="primary"
                            variant="solid"
                            isLoading={isSearchingMoreEvidence}
                            onPress={async () => {
                                console.log('Search for evidence')
                                await userSearchMoreEvidence({ variables: { assertionId: assertions_content?.assertion?.id } })
                                refetch()
                            }}
                            className="my-3"
                            size="sm"
                        >
                            Search for evidence
                        </Button>
                    </div>
                }

            </AccordionItem>
        </Accordion>
    )
}