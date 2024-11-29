
'use client'

import { Spinner, Badge, Button, Chip, Input } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { useMutation } from '@apollo/client'
import { EvidenceInfo } from '@/components/VideoPage/EvidenceInfo';
import { USER_APPEND_EVIDENCE_TO_ASSERTION_MUTATION, USER_SEARCH_MORE_EVIDENCE_MUTATION } from '@/store/action/action'
import { useState, useRef } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { toast } from 'react-hot-toast'
import { motion } from 'framer-motion'
import { ProWarningModal, ProWarningModalHandle, useIsProUser } from "@/components/subscription/ProWarningModal";


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
    const { isPro } = useIsProUser()
    const proModalRef = useRef<ProWarningModalHandle>(null);

    return (
        <>
            <ProWarningModal ref={proModalRef} />
            <h6 className="text-tiny uppercase my-2">Evidence ({contentAssertions?.length})</h6>
            <>
                <div className="flex gap-2 mb-3">
                    {(() => {
                        return (
                            <>
                                {proEvidence.length > 0 && (
                                    <Chip color="success" size="sm" className="text-white">
                                        <Icon icon="mdi:success-bold" className="inline" />{' '}
                                        {proEvidence.length} supporting ({
                                            Math.round(
                                                proEvidence.reduce((acc: any, e: any) => acc + (e.content?.contentScore || 0), 0) / proEvidence.length
                                            )
                                        }/100)
                                    </Chip>
                                )}
                                {conEvidence.length > 0 && (
                                    <Chip color="danger" size="sm" className="text-white">
                                        <Icon icon="bx:error" className="inline" />{' '}
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
            {!contentAssertions?.length || contentAssertions?.length === 0 &&
                <Spinner />
            }
            {contentAssertions?.length > 0 ?
                <>
                    {
                        contentAssertions.map(
                            (o: any, i: number) => (
                                <div key={i} id={`assertion_${i}`} className="mb-4">
                                    <div className="flex gap-2 ">
                                        <Chip
                                            color={o?.isProAssertion ? 'success' : 'danger'}
                                            className="text-white"
                                            size="sm"
                                        >
                                            <Icon className="inline" icon={o?.isProAssertion ? "mdi:success-bold" : "ci:stop-sign"} />{' '}
                                            {Math.round(o?.content?.contentScore || 0)} / 100
                                        </Chip>
                                        <span className="text-sm">{o?.content?.title ?? "Not yet evaluated"}</span>
                                    </div>
                                    <div className="ml-8 my-2">
                                        <h6 className="text-tiny uppercase my-2">{o?.isCitationFromOriginalContent ? 'From Author' : 'AI Research'}</h6>
                                        <h6><b>Relevance:</b> {o?.whyRelevant}</h6>
                                        <EvidenceInfo refetch={refetch} evidence={o?.content} />
                                    </div>
                                </div>
                            )
                        )
                    }
                </> :
                <div>
                    <h6 className="text-red-500 font-bold">* No Evidence</h6>
                </div>
            }
            <div className="my-4 flex gap-2">
                <Badge content="PRO" color="default" size="sm" >
                    <Button
                        color="secondary"
                        variant="solid"
                        isLoading={isSearchingMoreEvidence}
                        onPress={async () => {
                            if (!isPro) {
                                proModalRef.current?.open();
                                return
                            }
                            console.log('Search for evidence')
                            await userSearchMoreEvidence({ variables: { assertionId: assertions_content?.assertion?.id } })
                            refetch()
                        }}
                        size="sm"
                        fullWidth={false}
                    >
                        AI Search
                    </Button>
                </Badge>
                <UserAddMoreEvidenceToAssertion assertionId={assertions_content?.assertion?.id} onAddEvidence={refetch} />
            </div>
        </>
    )
}

export const UserAddMoreEvidenceToAssertion = ({ assertionId, onAddEvidence }: { assertionId: string, onAddEvidence: () => void }) => {

    const [isShowAddEvidence, setIsShowAddEvidence] = useState(false)
    const [addMoreEvidence, { loading }] = useMutation(USER_APPEND_EVIDENCE_TO_ASSERTION_MUTATION)
    const {
        handleSubmit,
        control,
        formState: { errors },
        reset,
    } = useForm()

    const onSubmit = async (data: any) => {
        try {
            const result = await addMoreEvidence({ variables: { assertionId: assertionId, contentUrl: data.contentUrl } })
            setIsShowAddEvidence(false)
            reset()
            onAddEvidence()
            if (!result?.data?.userAppendEvidenceToAssertion?.success) {
                toast.error(`Error adding evidence: ${result?.data?.userAppendEvidenceToAssertion?.message}`)
            }
            console.log({ result })
        } catch (e) {
            console.log(e)
            toast.error(`Error adding evidence: ${e}`)
        }
    }
    return (
        <>
            <div>
                <Badge content="PRO" color="default" size="sm">
                    <Button
                        color="secondary"
                        variant="solid"
                        onPress={() => {
                            setIsShowAddEvidence(!isShowAddEvidence)
                        }}
                        size="sm"
                    >
                        {isShowAddEvidence ? 'Close' : 'Add'}
                    </Button>
                </Badge>
            </div>
            {isShowAddEvidence &&
                <motion.div
                    className="my-4"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <form onSubmit={handleSubmit(onSubmit)} className="w-full">
                        <Controller
                            name="contentUrl"
                            control={control}
                            rules={{
                                required: true,
                                pattern: /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/
                            }}
                            render={({ field }) => (
                                <Input
                                    {...field}
                                    isDisabled={loading}
                                    label="Evidence URL"
                                    variant="bordered"
                                    size="lg"
                                    color="primary"
                                    startContent={
                                        <div className="pointer-events-none flex items-center">
                                            <Icon icon="material-symbols:link" />
                                        </div>
                                    }
                                    onChange={(e) => field.onChange(e.target.value)}
                                    errorMessage={
                                        !errors.contentUrl
                                            ? ''
                                            : 'Invalid URL'
                                    }
                                    isInvalid={!errors.contentUrl ? false : true}
                                />
                            )}
                        />
                        <div className="my-4 flex justify-end">
                            <Button
                                isDisabled={loading}
                                isLoading={loading}
                                color="primary"
                                onPress={() => {
                                    handleSubmit(onSubmit)()
                                }}
                            >
                                Send
                            </Button>
                        </div>
                    </form>
                </motion.div>
            }
        </>
    )
}