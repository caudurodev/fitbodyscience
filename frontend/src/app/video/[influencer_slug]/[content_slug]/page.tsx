'use client'

import { Spinner, ScrollShadow, Button, Chip } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { motion } from 'framer-motion'
import { useSubscription, useMutation, useQuery } from '@apollo/client'
import { useState } from 'react'
import { useRouter } from 'next/navigation';
import { GET_CONTENT_SUBSCRIPTION, GET_CONTENT_QUERY } from '@/store/content/query'
import {
    RECALCULATE_AGGREGATE_SCORES_MUTATION,
    USER_ANALYSE_CONTENT_MUTATION,
    DELETE_CONTENT_MUTATION,
    DELETE_RELATED_CONTENT_AND_RELATIONSHIPS_MUTATION,
    USER_UPDATE_ASSERTIONS_SCORE_MUTATION
} from '@/store/content/mutation'
import { useHydration } from '@/hooks/useHydration'
import { YouTubePlayer } from '@/components/YouTubePlayer';
import { SummarySkeleton, AssertionsSkeleton } from '@/components/ContentSkeletons';
import { ContentActivityFeed } from "@/components/notifications/ContentActivityFeed";
import { AssertionCard } from '@/components/VideoPage/AssertionCard';
import { convertTimestampToSeconds } from '@/utils/time'

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

    const { data: subscriptionData } = useSubscription(
        GET_CONTENT_SUBSCRIPTION,
        {
            variables: {
                contentSlug: params?.content_slug,
                influencerSlug: params?.influencer_slug
            },
            skip: !params.content_slug || !params.influencer_slug || !contentData
        },
    )

    // Use query data for initial load, then switch to subscription data when available
    const mainContent = subscriptionData?.content?.[0] || contentData?.content?.[0]

    const isParsed = mainContent?.isParsed === true
    const [recalculateAggregateScores, { loading: isRecalculating }] = useMutation(RECALCULATE_AGGREGATE_SCORES_MUTATION)
    const [userAnalyseContent, { loading: isAnalysingContent }] = useMutation(USER_ANALYSE_CONTENT_MUTATION)
    const [deleteContent, { loading: isDeletingContent }] = useMutation(DELETE_CONTENT_MUTATION)
    const [deleteRelatedContentAndRelationships, { loading: isDeletingRelatedContentAndRelationships }] = useMutation(DELETE_RELATED_CONTENT_AND_RELATIONSHIPS_MUTATION)
    const [updateAssertionsScore, { loading: isUpdatingAssertionsScore }] = useMutation(USER_UPDATE_ASSERTIONS_SCORE_MUTATION)

    const assertions_contents = mainContent?.assertions_contents
    const isHydrated = useHydration()
    const [currentTimestamp, setCurrentTimestamp] = useState(0)
    const [currentAssertionIndex, setCurrentAssertionIndex] = useState(-1);
    const [player, setPlayer] = useState<any>(null);
    const [highlightedAssertion, setHighlightedAssertion] = useState<number | null>(null);

    const influencerInfo = mainContent?.influencer_contents?.[0]?.influencer

    if (!isHydrated) { return null }
    return (
        <>
            <main className="h-[calc(100vh-180px)] overflow-hidden">
                <div className="h-full flex flex-col lg:flex-row">
                    <ScrollShadow className="w-full lg:w-[400px] shrink-0 p-4">
                        <div className="space-y-4">
                            <ContentActivityFeed contentId={mainContent?.id} />

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
                            <Button
                                variant="light"
                                color="secondary"
                                size="sm"
                                onPress={() => {
                                    router.push(`/video/${influencerInfo?.slug}`)
                                }}
                            >
                                By {influencerInfo?.name}
                            </Button>
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
                            <h6 className="text-xs">{mainContent?.id}</h6>
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
                                {!isRecalculating && <Icon icon="mdi:refresh" className="inline" />} recaulculate aggregate score
                            </Button>
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
                                                console.log(`assertion_${newIndex}`, element)
                                                element?.scrollIntoView({ behavior: 'smooth' });
                                                if (player && assertions_contents[newIndex]) {
                                                    const seconds = convertTimestampToSeconds(assertions_contents[newIndex]?.videoTimestamp);
                                                    player.seekTo(seconds);
                                                }
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
                                    isLoading={isDeletingContent || isDeletingRelatedContentAndRelationships}
                                    onPress={async () => {
                                        const contentId = mainContent?.id
                                        await deleteContent({ variables: { contentId } })
                                        await deleteRelatedContentAndRelationships({ variables: { contentId } })
                                        router.push(`/`)
                                    }}
                                >
                                    Delete
                                </Button>
                            </div>
                        </div>
                    </ScrollShadow>
                    <ScrollShadow className=" flex-1 h-full overflow-y-auto px-6">
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
                            {!isUpdatingAssertionsScore && <Icon icon="mdi:refresh" className="inline" />} score updateAssertionsScore
                        </Button>
                        {!assertions_contents?.length ? (
                            <AssertionsSkeleton />
                        ) : (
                            <>
                                <h2 className="uppercase text-xs my-2">The main Assertions by importance ({assertions_contents?.length})</h2>
                                <ul className="my-2">
                                    {assertions_contents.map((assertions_content: any, index: number) => {
                                        return (
                                            <AssertionCard
                                                highlightedAssertion={highlightedAssertion}
                                                assertions_content={assertions_content}
                                                key={index}
                                                assertionIndex={index}
                                                refetch={refetch}
                                            />
                                        )
                                    })}
                                </ul>
                            </>
                        )}
                    </ScrollShadow>
                </div>
            </main>
        </>

    );
}

export default VideoPage