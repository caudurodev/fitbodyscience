'use client'

import { Spinner, ScrollShadow, Button, Chip } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { motion } from 'framer-motion'
import { useSubscription, useMutation, useQuery } from '@apollo/client'
import { useCallback, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation';
import { GET_CONTENT_SUBSCRIPTION, GET_CONTENT_QUERY } from '@/store/content/query'
import {
    RECALCULATE_AGGREGATE_SCORES_MUTATION,
    USER_ANALYSE_CONTENT_MUTATION,
    DELETE_CONTENT_MUTATION,
} from '@/store/content/mutation'
import { useHydration } from '@/hooks/useHydration'
import { YouTubePlayer } from '@/components/YouTubePlayer';
import { SummarySkeleton, AssertionsSkeleton } from '@/components/ContentSkeletons';
import { ContentActivityFeed } from "@/components/notifications/ContentActivityFeed";
import { AssertionCard } from '@/components/VideoPage/AssertionCard';
import { convertTimestampToSeconds } from '@/utils/time'
import { useResponsive } from '@/hooks/useResponsive'
import toast from "react-hot-toast";

export default function Page({ params }: { params: { influencer_slug: string, content_slug: string } }) {
    const router = useRouter()
    const { isMobile } = useResponsive()
    const [currentAssertionIndex, setCurrentAssertionIndex] = useState(-1);
    const [currentTimestamp, setCurrentTimestamp] = useState(0)
    const [player, setPlayer] = useState<any>(null);

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

    const mainContent = subscriptionData?.content?.[0] || contentData?.content?.[0]

    const isParsed = mainContent?.isParsed === true
    const [recalculateAggregateScores, { loading: isRecalculating }] = useMutation(RECALCULATE_AGGREGATE_SCORES_MUTATION)
    const [userAnalyseContent, { loading: isAnalysingContent }] = useMutation(USER_ANALYSE_CONTENT_MUTATION)
    const [deleteContent, { loading: isDeletingContent }] = useMutation(DELETE_CONTENT_MUTATION)
    // const [deleteRelatedContentAndRelationships, { loading: isDeletingRelatedContentAndRelationships }] = useMutation(DELETE_RELATED_CONTENT_AND_RELATIONSHIPS_MUTATION)
    // const [updateAssertionsScore, { loading: isUpdatingAssertionsScore }] = useMutation(USER_UPDATE_ASSERTIONS_SCORE_MUTATION)

    const assertions_contents = mainContent?.assertions_contents
    const isHydrated = useHydration()


    const influencerInfo = mainContent?.influencer_contents?.[0]?.influencer

    const goToAssertionTimeStampInVideo = useCallback((assertionIndex: number) => {
        const seconds = convertTimestampToSeconds(assertions_contents[assertionIndex]?.videoTimestamp);
        player.seekTo(seconds);
    }, [player, assertions_contents])

    if (!isHydrated) { return null }
    return (
        <>
            <main className="sm:h-[calc(100vh-180px)] overflow-hidden">
                <div className="h-full flex flex-col lg:flex-row gap-4">
                    <ScrollShadow className="w-full lg:w-[400px] shrink-0 flex flex-col gap-4">

                        <h6 className="uppercase text-xs text-gray-500 ml-2"><b>Scoring</b> v0.1 - <b>AI</b> v0.1</h6>
                        {!isMobile && <ContentActivityFeed contentId={mainContent?.id} />}
                        <div className="sm:space-y-4">
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
                                className="pl-0 ml-1 my-2"
                                size="sm"
                                onPress={() => {
                                    router.push(`/video/${influencerInfo?.slug}`)
                                }}
                            >
                                By {influencerInfo?.name}
                            </Button>
                            <div className="flex gap-2 bg-primary-100 rounded-2xl p-4">
                                <h4 className="uppercase font-bold text-primary-500 text-xs my-2">Our Score</h4>
                                <div className="mb-2">
                                    <Chip color="success" size="lg" className="mr-2">
                                        <Icon icon="mdi:success-bold" className="inline mr-2" />
                                        {mainContent?.proAggregateContentScore} / 100
                                    </Chip>
                                    <Chip color="danger" size="lg" className="mr-2">
                                        <Icon icon="maki:cross" className="inline mr-2" />
                                        {mainContent?.againstAggregateContentScore} / 100
                                    </Chip>
                                </div>
                            </div>
                            {!isMobile &&
                                <div className="p-4 bg-danger-100 rounded-lg">
                                    <h6 className="text-xs uppercase font-bold text-primary-500 my-2">Admin</h6>
                                    <h6 className="text-xs">
                                        {mainContent?.id}
                                        {isParsed === false ?
                                            <span className="text-xs"><Spinner /> Parsing</span> :
                                            <span className="text-xs">Parsed.</span>
                                        }
                                    </h6>

                                    <div className="flex flex-row items-center justify-start gap-2 ">
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
                                            {!isRecalculating && <Icon icon="mdi:refresh" className="inline" />} Recalculate
                                        </Button>
                                        <Button
                                            className="my-2"
                                            color="primary"
                                            size="sm"
                                            isLoading={isAnalysingContent}
                                            onPress={async () => {
                                                try {
                                                    await userAnalyseContent({ variables: { contentId: mainContent?.id } })
                                                } catch (e) {
                                                    toast.error('error analysing content')
                                                    console.error(e)
                                                }
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
                                                const contentId = mainContent?.id
                                                try {
                                                    await deleteContent({ variables: { contentId } })
                                                    router.push(`/`)
                                                } catch (e) {
                                                    toast.error('error deleting content')
                                                    console.error(e)
                                                }
                                            }}
                                        >
                                            Delete
                                        </Button>
                                    </div>
                                </div>
                            }
                        </div>
                    </ScrollShadow>
                    <ScrollShadow className="flex-1 h-full overflow-y-auto sm:px-6 px-2">
                        <div className="sm:space-y-6 sm:pb-8">
                            <h2 className="uppercase text-xs font-bold text-primary">Main point</h2>
                            {!mainContent?.summaryJsonb?.conclusion ? (
                                <SummarySkeleton />
                            ) : (
                                <h2 className="text-2xl">{mainContent?.summaryJsonb?.conclusion}</h2>
                            )}
                            <div className="sm:w-3/4 px-6 sm:px-0 mx-auto">
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
                        {!assertions_contents?.length ? (
                            <AssertionsSkeleton />
                        ) : (
                            <>
                                <h2 className="uppercase text-xs my-2">The main Assertions by importance ({assertions_contents?.length})</h2>
                                <ul className="my-2">
                                    {assertions_contents.map((assertions_content: any, index: number) => {
                                        return (
                                            <AssertionCard
                                                assertions_content={assertions_content}
                                                key={index}
                                                currentAssertionIndex={currentAssertionIndex}
                                                assertionIndex={index}
                                                refetch={refetch}

                                            />
                                        )
                                    })}
                                </ul>
                            </>
                        )}
                    </ScrollShadow>
                    <NavigateAssertions
                        assertions={assertions_contents}
                        currentAssertionIndex={currentAssertionIndex}
                        onSetCurrentAssertionIndex={(i) => {
                            setCurrentAssertionIndex(i)
                        }}
                    />
                </div>
            </main>
        </>

    );
}

function NavigateAssertions({ assertions, currentAssertionIndex, onSetCurrentAssertionIndex }: { assertions: any, currentAssertionIndex: number, onSetCurrentAssertionIndex: React.Dispatch<React.SetStateAction<number>> }) {
    const scrollToAssertion = useCallback((index: number) => {
        onSetCurrentAssertionIndex(index);
    }, [onSetCurrentAssertionIndex]);

    useEffect(() => {
        if (currentAssertionIndex >= 0) {
            const element = document.getElementById(`assertion_${currentAssertionIndex}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
    }, [currentAssertionIndex]);

    const handleKeyDown = useCallback((event: KeyboardEvent) => {
        if (event.key === 'ArrowUp') {
            event.preventDefault();
            if (currentAssertionIndex > 0) {
                scrollToAssertion(currentAssertionIndex - 1);
            }
        } else if (event.key === 'ArrowDown') {
            event.preventDefault();
            if (currentAssertionIndex < assertions.length - 1) {
                scrollToAssertion(currentAssertionIndex + 1);
            }
        }
    }, [currentAssertionIndex, scrollToAssertion, assertions?.length]);

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [handleKeyDown])

    return (
        <>
            {assertions?.length > 0 && (
                <div className="z-10 fixed bottom-8 right-4 flex flex-col gap-2 mt-4 bg-white p-2   rounded-2xl shadow-xl">
                    <h6 className="text-xs uppercase text-center"> {currentAssertionIndex > -1 ? `(${currentAssertionIndex + 1}/${assertions.length})` : `(${assertions.length})`}</h6>
                    <Button
                        size="sm"
                        variant="solid"
                        color="success"
                        isDisabled={currentAssertionIndex <= 0}
                        onPress={() => {
                            if (currentAssertionIndex > 0) {
                                scrollToAssertion(currentAssertionIndex - 1);
                            }
                        }}
                    >
                        <Icon icon="mdi:chevron-up" className="inline" />
                    </Button>
                    <Button
                        size="sm"
                        variant="solid"
                        color="success"
                        isDisabled={currentAssertionIndex >= assertions.length - 1}
                        onPress={() => {
                            if (currentAssertionIndex < assertions.length - 1) {
                                scrollToAssertion(currentAssertionIndex + 1);
                            }
                        }}
                    >
                        <Icon icon="mdi:chevron-down" className="inline" />
                    </Button>
                </div >
            )}
        </>
    )
}
