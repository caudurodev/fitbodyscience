'use client'

import {
    Card, Spinner, CardBody, ScrollShadow,
    Button, Link, Chip, CardHeader, Accordion, AccordionItem
} from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { motion } from 'framer-motion'
import { useSubscription, useMutation, useQuery } from '@apollo/client'
import { GET_CONTENT_SUBSCRIPTION, GET_CONTENT_QUERY } from '@/store/content/query'
import {
    RECALCULATE_AGGREGATE_SCORES_MUTATION,
    USER_ANALYSE_CONTENT_MUTATION,
    DELETE_CONTENT_MUTATION,
    CLASSIFY_CONTENT_MUTATION,
    USER_UPDATE_EVIDENCE_SCORE_MUTATION,
    USER_UPDATE_ASSERTIONS_SCORE_MUTATION
} from '@/store/content/mutation'
import { USER_UPDATE_ASSERTION_SCORE_MUTATION } from '@/store/assertion/mutation'
import { USER_SEARCH_MORE_EVIDENCE_MUTATION } from '@/store/action/action'
import { useHydration } from '@/hooks/useHydration'
import StudyClassification from "@/components/StudyClassification";
import { useState } from 'react'
import toast from "react-hot-toast";
import { useRouter } from 'next/navigation';
import YouTubePlayer from '@/components/YouTubePlayer';
import { SummarySkeleton, AssertionsSkeleton } from '@/components/ContentSkeletons';
import { ScoreBar } from "@/components/scoring/ScoreBar";

const convertTimestampToSeconds = (timestamp: string) => {
    if (!timestamp) return 0;
    if (timestamp.includes('-')) {
        const startTime = timestamp.split('-')[0];
        return parseInt(startTime.replace('s', ''));
    }
    if (timestamp.includes(':')) {
        const [minutes, seconds] = timestamp.split(':').map(Number);
        return minutes * 60 + seconds;
    }
    return parseInt(timestamp.replace('s', ''));
};

const VideoPage = ({ params }: { params: { influencer_slug: string, content_slug: string } }) => {
    const router = useRouter()
    const { data: contentData, refetch } = useQuery(GET_CONTENT_QUERY, {
        variables: {
            contentSlug: params?.content_slug,
            influencerSlug: params?.influencer_slug
        },
        skip: !params.content_slug || !params.influencer_slug,
        fetchPolicy: 'network-only'
    })
    const isParsed = contentData?.content?.[0]?.isParsed === true
    const { data: subscriptionData } = useSubscription(
        GET_CONTENT_SUBSCRIPTION,
        {
            variables: {
                contentSlug: params?.content_slug,
                influencerSlug: params?.influencer_slug
            },
            skip: !params.content_slug || !params.influencer_slug || isParsed === true
        },
    )
    const [recalculateAggregateScores, { loading: isRecalculating }] = useMutation(RECALCULATE_AGGREGATE_SCORES_MUTATION)
    const [userAnalyseContent, { loading: isAnalysingContent }] = useMutation(USER_ANALYSE_CONTENT_MUTATION)
    const [deleteContent, { loading: isDeletingContent }] = useMutation(DELETE_CONTENT_MUTATION)
    const [classifyContent, { loading: isClassifyingContent }] = useMutation(CLASSIFY_CONTENT_MUTATION)
    const [updateEvidenceScore, { loading: isUpdatingEvidenceScore }] = useMutation(USER_UPDATE_EVIDENCE_SCORE_MUTATION)
    const [updateAssertionScore, { loading: isUpdatingAssertionScore }] = useMutation(USER_UPDATE_ASSERTION_SCORE_MUTATION)
    const [updateAssertionsScore, { loading: isUpdatingAssertionsScore }] = useMutation(USER_UPDATE_ASSERTIONS_SCORE_MUTATION)
    const [userSearchMoreEvidence, { loading: isSearchingMoreEvidence }] = useMutation(USER_SEARCH_MORE_EVIDENCE_MUTATION)

    const mainContent = subscriptionData?.content?.[0] || contentData?.content?.[0]
    const assertions_contents = mainContent?.assertions_contents
    const isHydrated = useHydration()
    const [currentTimestamp, setCurrentTimestamp] = useState(0)
    const [currentAssertionIndex, setCurrentAssertionIndex] = useState(0);
    const [player, setPlayer] = useState<any>(null);
    const [highlightedAssertion, setHighlightedAssertion] = useState<number | null>(null);

    if (!isHydrated) { return null }
    return (
        <main className="h-[calc(100vh-180px)] overflow-hidden">
            <div className="h-full flex flex-col lg:flex-row">
                {/* Video Column */}
                <aside className="w-full lg:w-[400px] shrink-0 p-4">
                    <div className="space-y-4">
                        {/* Video player section */}
                        <div className="w-full">
                            <YouTubePlayer
                                videoId={mainContent?.videoId}
                                currentTimestamp={currentTimestamp}
                                onPlayerReady={setPlayer}
                                className="w-full aspect-video"
                            />
                        </div>
                        {!mainContent?.title ?
                            <Spinner /> :
                            <motion.h1
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.2, ease: "easeInOut" }}
                                className="text-xl font-bold my-2">
                                {mainContent?.title}
                            </motion.h1>
                        }
                        <h4 className="uppercase text-tiny my-2">Overall Score</h4>
                        <div className="mb-2">
                            <Chip color="success" size="lg" className="mr-2">
                                <Icon icon="mdi:approve" className="inline mr-2" />
                                {mainContent?.proAggregateContentScore} / 100
                            </Chip>
                            <Chip color="danger" size="lg" className="mr-2">
                                <Icon icon="ci:stop-sign" className="inline mr-2" />
                                {mainContent?.againstAggregateContentScore} / 100
                            </Chip>
                        </div>
                        <Button
                            size="sm"
                            className="my-4"
                            variant="solid"
                            color="primary"
                            isLoading={isRecalculating}
                            isDisabled={!mainContent?.id}
                            onPress={() => {
                                recalculateAggregateScores({ variables: { contentId: mainContent?.id } })
                            }}
                        >
                            {!isRecalculating && <Icon icon="mdi:refresh" className="inline" />} score
                        </Button>

                        {/* Navigation Buttons */}
                        {assertions_contents?.length > 0 && (
                            <div className="flex gap-2 mt-4">
                                <Button
                                    size="sm"
                                    variant="flat"
                                    isDisabled={currentAssertionIndex === 0}
                                    onPress={() => {
                                        if (currentAssertionIndex > 0) {
                                            const newIndex = currentAssertionIndex - 1;
                                            setCurrentAssertionIndex(newIndex);
                                            setHighlightedAssertion(newIndex);
                                            const element = document.getElementById(`assertion_${newIndex}`);
                                            element?.scrollIntoView({ behavior: 'smooth' });
                                            if (player && assertions_contents[newIndex]) {
                                                const seconds = convertTimestampToSeconds(assertions_contents[newIndex]?.videoTimestamp);
                                                player.seekTo(seconds);
                                            }
                                            // Reset highlight after animation
                                            setTimeout(() => setHighlightedAssertion(null), 1500);
                                        }
                                    }}
                                >
                                    <Icon icon="mdi:chevron-left" className="inline" /> Previous
                                </Button>
                                <Button
                                    size="sm"
                                    variant="flat"
                                    isDisabled={currentAssertionIndex >= assertions_contents.length - 1}
                                    onPress={() => {
                                        if (currentAssertionIndex < assertions_contents.length - 1) {
                                            const newIndex = currentAssertionIndex + 1;
                                            setCurrentAssertionIndex(newIndex);
                                            setHighlightedAssertion(newIndex);
                                            const element = document.getElementById(`assertion_${newIndex}`);
                                            element?.scrollIntoView({ behavior: 'smooth' });
                                            if (player && assertions_contents[newIndex]) {
                                                const seconds = convertTimestampToSeconds(assertions_contents[newIndex]?.videoTimestamp);
                                                player.seekTo(seconds);
                                            }
                                            // Reset highlight after animation
                                            setTimeout(() => setHighlightedAssertion(null), 1500);
                                        }
                                    }}
                                >
                                    Next <Icon icon="mdi:chevron-right" className="inline" />
                                </Button>
                            </div>
                        )}
                        <div className="flex flex-row items-center justify-start gap-2 mt-16">
                            {isParsed === false ? <h6 className="text-xs"><Spinner /> Parsing</h6> : <h6 className="text-xs">Parsed.</h6>}
                            {/* <h6>{isParsed === true ? 'is Parsed true' : 'is not parsed'} {mainContent?.id}</h6> */}
                            <Button
                                className="my-2"
                                color="primary"
                                size="sm"
                                isLoading={isAnalysingContent}
                                onPress={() => {
                                    userAnalyseContent({ variables: { contentId: mainContent?.id } })
                                }}
                            >
                                Analyse
                            </Button>
                            <Button
                                className="my-2 mx-4"
                                size="sm"
                                color="danger"
                                isLoading={isDeletingContent}
                                onPress={async () => {
                                    deleteContent({ variables: { contentId: mainContent?.id } })
                                    router.push(`/`)
                                }}
                            >
                                Delete
                            </Button>
                        </div>
                    </div>
                </aside>

                {/* Content Column */}
                <section className="flex-1 h-full overflow-hidden p-4">
                    <ScrollShadow className="h-full overflow-y-auto px-6">
                        <div className="space-y-6 pb-8">
                            <h2 className="uppercase text-xs font-bold text-primary">Main point</h2>
                            {!mainContent?.summaryJsonb?.conclusion ? (
                                <SummarySkeleton />
                            ) : (
                                <h2 className="text-2xl">{mainContent?.summaryJsonb?.conclusion}</h2>
                            )}
                            <div className="w-3/4 mx-auto">
                                {mainContent?.summaryJsonb?.eli5 &&
                                    <div className="my-4">
                                        <h2 className="uppercase font-bold text-primary my-4">Tl;Dw:</h2>
                                        <ul className="list-disc list-inside  ">
                                            {mainContent?.summaryJsonb?.eli5?.map((e: string, i: number) =>
                                                <li key={i}>{e}</li>)
                                            }
                                        </ul>
                                    </div>
                                }
                            </div>
                            <div className=" ">
                                <h2 className="uppercase  my-4 font-bold text-primary">Summary</h2>
                                {!mainContent?.summaryJsonb?.summary ? (
                                    <SummarySkeleton />
                                ) : (
                                    <h2 className=" my-4">{mainContent?.summaryJsonb?.summary}</h2>
                                )}
                            </div>
                        </div>

                        <Button
                            color="primary"
                            size="sm"
                            className="mb-4"
                            isLoading={isUpdatingAssertionsScore}
                            onPress={async () => {
                                await updateAssertionsScore({
                                    variables: {
                                        contentId: mainContent?.id
                                    }
                                })
                            }}>
                            {!isUpdatingAssertionsScore && <Icon icon="mdi:refresh" className="inline" />} score
                        </Button>
                        {!assertions_contents?.length ? (
                            <AssertionsSkeleton />
                        ) : (
                            <>
                                <h2 className="uppercase text-xs my-2">The main Assertions ({assertions_contents?.length})</h2>
                                <ul className="my-2">
                                    {assertions_contents.map((assertions_content: any, index: number) => {
                                        return (
                                            <li key={index} className="mb-8 scroll-mt-28" id={`assertion_${index}`}>
                                                <motion.div
                                                    animate={{
                                                        backgroundColor: highlightedAssertion === index ?
                                                            ['rgba(var(--color-primary-200), 0.2)', 'rgba(var(--color-primary-200), 0)'] :
                                                            'rgba(var(--color-primary-200), 0)',
                                                    }}
                                                    transition={{
                                                        duration: 1.5,
                                                        ease: "easeOut",
                                                    }}
                                                    className="rounded-lg"
                                                >
                                                    <Card shadow="none" radius="sm">
                                                        <CardHeader className="flex-col items-start gap-2">
                                                            <h4 className="text-xl font-bold text-primary-400">{index + 1}. {assertions_content.assertion.text}</h4>
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
                                                                        {isUpdatingAssertionScore &&
                                                                            <Button
                                                                                color="primary"
                                                                                size="sm"
                                                                                isLoading={isUpdatingAssertionScore}
                                                                                onPress={async () => {
                                                                                    updateAssertionScore({ variables: { assertionId: assertions_content?.assertion?.id } })
                                                                                }}
                                                                            >
                                                                                {!isUpdatingAssertionScore && <Icon icon="mdi:refresh" className="inline" />} score
                                                                            </Button>
                                                                        }
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
                                                                                ({assertions_content?.assertion?.contents_assertions?.length})
                                                                            </h5>
                                                                            <div className="flex gap-2 mt-2">
                                                                                {(() => {
                                                                                    const proEvidence = assertions_content?.assertion?.contents_assertions?.filter((e: any) => e.isProAssertion) || [];
                                                                                    const conEvidence = assertions_content?.assertion?.contents_assertions?.filter((e: any) => !e.isProAssertion) || [];

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
                                                                                                    <div className="flex items-center gap-2">
                                                                                                        <Chip
                                                                                                            color={o?.isProAssertion ? 'success' : 'danger'}
                                                                                                            className="text-white"
                                                                                                        >
                                                                                                            <Icon className="inline text-lg" icon={o?.isProAssertion ? "mdi:approve" : "ci:stop-sign"} />{' '}
                                                                                                            {Math.round(o?.content?.contentScore || 0)} / 100
                                                                                                        </Chip>
                                                                                                        <span className="text-sm">{o?.content?.title}</span>
                                                                                                    </div>
                                                                                                }
                                                                                            >
                                                                                                <div className="ml-8 my-2">
                                                                                                    <h6 className="text-tiny uppercase">{o?.isCitationFromOriginalContent ? 'From Author' : 'Ai Research'}</h6>
                                                                                                    <Link href={o?.content?.sourceUrl}>{o?.content?.title}</Link>
                                                                                                    <h6 className="text-tiny my-3">DOI: {o?.content?.doiNumber}</h6>

                                                                                                    <h6>{o?.whyRelevant}</h6>
                                                                                                    <div className="my-3">
                                                                                                        <Chip color="warning" className="text-white">{o?.content?.contentType}</Chip>
                                                                                                    </div>
                                                                                                    {o?.content?.sciencePaperClassification ?
                                                                                                        <>
                                                                                                            <StudyClassification paperClassification={o?.content?.sciencePaperClassification} />
                                                                                                            <Button
                                                                                                                className="mt-2"
                                                                                                                color="primary"
                                                                                                                size="sm"
                                                                                                                isLoading={isUpdatingEvidenceScore}
                                                                                                                isDisabled={isUpdatingEvidenceScore}
                                                                                                                onPress={async () => {
                                                                                                                    try {
                                                                                                                        await updateEvidenceScore({ variables: { contentId: o?.content?.id } })
                                                                                                                        await refetch()
                                                                                                                    } catch (e) {
                                                                                                                        toast.error('Error updating evidence score')
                                                                                                                        console.error(e)
                                                                                                                    }
                                                                                                                }}
                                                                                                            >
                                                                                                                Update Score
                                                                                                            </Button>
                                                                                                        </> :
                                                                                                        <div>
                                                                                                            <h6 className="text-red-500 font-bold">* Evidence not yet classified</h6>
                                                                                                            <Button
                                                                                                                className="mt-2"
                                                                                                                size="sm"
                                                                                                                isLoading={isClassifyingContent}
                                                                                                                isDisabled={!!o?.content?.sciencePaperClassification || isClassifyingContent}
                                                                                                                onPress={async () => {
                                                                                                                    try {
                                                                                                                        await classifyContent({ variables: { contentId: o?.content?.id } })
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

                                                        </CardBody>
                                                    </Card>
                                                </motion.div>
                                            </li>
                                        )
                                    })}
                                </ul>
                            </>
                        )}

                    </ScrollShadow>
                </section>
            </div>
        </main>
    );
}

export default VideoPage