
'use client'

import {
    Spinner,
    Button, Chip, Accordion, AccordionItem,
    Input,
} from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { useMutation } from '@apollo/client'
import { EvidenceInfo } from '@/components/VideoPage/EvidenceInfo';
import { USER_APPEND_EVIDENCE_TO_ASSERTION_MUTATION, USER_SEARCH_MORE_EVIDENCE_MUTATION } from '@/store/action/action'
import { useState } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { toast } from 'react-hot-toast'


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
        <>
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
                    {!contentAssertions?.length || contentAssertions?.length === 0 &&
                        <Spinner />
                    }
                    {contentAssertions?.length > 0 ?
                        <>
                            {
                                contentAssertions.map(
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
                        </div>
                    }

                </AccordionItem>
            </Accordion>
            <div className="flex gap-2">
                <Button
                    color="primary"
                    variant="solid"
                    isLoading={isSearchingMoreEvidence}
                    onPress={async () => {
                        console.log('Search for evidence')
                        await userSearchMoreEvidence({ variables: { assertionId: assertions_content?.assertion?.id } })
                        refetch()
                    }}
                    className="my-3 "
                    size="sm"
                    fullWidth={false}
                >
                    Find more evidence
                </Button>
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
        <div className="flex flex-col">
            <div>
                <Button
                    color="primary"
                    variant="solid"
                    onPress={() => {
                        setIsShowAddEvidence(!isShowAddEvidence)
                    }}
                    className="my-3 "
                    size="sm"
                    fullWidth={false}
                >
                    Add more evidence
                </Button>
            </div>
            {isShowAddEvidence &&
                <div>
                    <form onSubmit={handleSubmit(onSubmit)} className="">
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
                        <div className="my-4 flex self-end w-full">
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
                </div>
            }
        </div>
    )
}