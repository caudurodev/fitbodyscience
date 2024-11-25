

'use client'

import {
    Button, Link, Chip
} from "@nextui-org/react";
import { useMutation } from '@apollo/client'
import {
    CLASSIFY_CONTENT_MUTATION,
    USER_UPDATE_EVIDENCE_SCORE_MUTATION,
} from '@/store/content/mutation'
import { DELETE_CONTENT_RELATIONSHIP_MUTATION } from '@/store/content_relationship/mutation'
import StudyClassification from "@/components/StudyClassification";
import toast from "react-hot-toast";
import { Icon } from '@iconify/react'


export const EvidenceInfo = ({ evidence, refetch }: { evidence: any, refetch: () => void }) => {
    const [classifyContent, { loading: isClassifyingContent }] = useMutation(CLASSIFY_CONTENT_MUTATION)
    const [updateEvidenceScore, { loading: isUpdatingEvidenceScore }] = useMutation(USER_UPDATE_EVIDENCE_SCORE_MUTATION)
    const [deleteContentRelationship, { loading: isDeletingContentRelationship }] = useMutation(DELETE_CONTENT_RELATIONSHIP_MUTATION)
    return (
        <>
            <Link href={evidence?.sourceUrl}>{evidence?.title ?? "Not yet downladed..."}</Link>
            <h6 className="text-tiny my-3">DOI: {evidence?.doiNumber ? evidence?.doiNumber : "N/a"}</h6>
            {evidence?.id}
            <div className="my-3">
                <Chip color="warning" className="text-white">{evidence?.contentType}</Chip>
            </div>
            {evidence?.sciencePaperClassification ?
                <>
                    <StudyClassification paperClassification={evidence?.sciencePaperClassification} />
                    <div className="my-3 bg-warning-100/30 p-2 rounded">
                        <h6 className="text-tiny uppercase text-danger">Admin only</h6>
                        <div className="flex gap-2 my-2">
                            <Button
                                color="primary"
                                size="sm"
                                isLoading={isUpdatingEvidenceScore}
                                isDisabled={isUpdatingEvidenceScore}
                                onPress={async () => {
                                    try {
                                        await updateEvidenceScore({ variables: { contentId: evidence?.id } })
                                        await refetch()
                                    } catch (e) {
                                        toast.error('Error updating evidence score')
                                        console.error(e)
                                    }
                                }}
                            >
                                <Icon icon="mdi:refresh" className="inline text-lg" /> Score
                            </Button>
                            <Button
                                size="sm"
                                color="danger"
                                isLoading={isClassifyingContent}
                                isDisabled={isClassifyingContent}
                                onPress={async () => {
                                    try {
                                        await classifyContent({ variables: { contentId: evidence?.id } })
                                        await refetch()
                                    } catch (e) {
                                        toast.error('Error classifying content')
                                        console.error(e)
                                    }
                                }}
                            >
                                <Icon icon="mdi:refresh" className="inline text-lg" /> Reclassify
                            </Button>
                            <Button
                                size="sm"
                                color="danger"
                                isLoading={isDeletingContentRelationship}
                                isDisabled={isDeletingContentRelationship}
                                onPress={async () => {
                                    try {
                                        await deleteContentRelationship({ variables: { childContentId: evidence?.id } })
                                        await refetch()
                                    } catch (e) {
                                        toast.error('Error disconnecting evidence from assertion')
                                        console.error(e)
                                    }
                                }}
                            >
                                <Icon icon="hugeicons:unlink-01" className="inline ml-2 text-lg" />
                                Disconnect Evidence
                            </Button>
                        </div>
                    </div>
                </>
                :
                <div>
                    <h6 className="text-red-500 font-bold">* Evidence not yet classified</h6>
                    <Button
                        className="mt-2"
                        size="sm"
                        isLoading={isClassifyingContent}
                        isDisabled={!!evidence?.sciencePaperClassification || isClassifyingContent}
                        onPress={async () => {
                            try {
                                await classifyContent({ variables: { contentId: evidence?.id } })
                                await refetch()
                            } catch (e) {
                                toast.error('Error classifying content')
                                console.error(e)
                            }
                        }}
                    >
                        Classify Now
                    </Button>

                </div>
            }
        </>
    )
}