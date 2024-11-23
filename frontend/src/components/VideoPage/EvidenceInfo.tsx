

'use client'

import {
    Button, Link, Chip
} from "@nextui-org/react";
import { useMutation } from '@apollo/client'
import {
    CLASSIFY_CONTENT_MUTATION,
    USER_UPDATE_EVIDENCE_SCORE_MUTATION,
} from '@/store/content/mutation'
import StudyClassification from "@/components/StudyClassification";
import toast from "react-hot-toast";


export const EvidenceInfo = ({ evidence, refetch }: { evidence: any, refetch: () => void }) => {
    const [classifyContent, { loading: isClassifyingContent }] = useMutation(CLASSIFY_CONTENT_MUTATION)
    const [updateEvidenceScore, { loading: isUpdatingEvidenceScore }] = useMutation(USER_UPDATE_EVIDENCE_SCORE_MUTATION)
    return (
        <>
            <Link href={evidence?.sourceUrl}>{evidence?.title ?? "Not yet downladed..."}</Link>
            <h6 className="text-tiny my-3">DOI: {evidence?.doiNumber}</h6>
            <div className="my-3">
                <Chip color="warning" className="text-white">{evidence?.contentType}</Chip>
            </div>
            {evidence?.sciencePaperClassification ?
                <>
                    <StudyClassification paperClassification={evidence?.sciencePaperClassification} />
                    <Button
                        className="mt-2"
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
                        Update Score
                    </Button>
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