'use client'

import { Card, Spinner, Slider, CardBody, CardFooter, Divider, Button, Link, Chip } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { motion } from 'framer-motion'
import { useSubscription, useMutation, useQuery } from '@apollo/client'
import { GET_CONTENT_SUBSCRIPTION, GET_CONTENT_QUERY } from '@/store/content/query'
import {
    RECALCULATE_AGGREGATE_SCORES_MUTATION,
    USER_ANALYSE_CONTENT_MUTATION,
    DELETE_CONTENT_MUTATION,
    CLASSIFY_CONTENT_MUTATION,
    USER_UPDATE_EVIDENCE_SCORE_MUTATION
} from '@/store/content/mutation'
import { useHydration } from '@/hooks/useHydration'
import StudyClassification from "@/components/StudyClassification";
import { AnimatedNumber } from "@/components/AnimatedNumber";
import { useState } from 'react'
import toast from "react-hot-toast";
import { useRouter } from 'next/navigation';
import YouTubePlayer from '@/components/YouTubePlayer';

const VideoPage = ({ params }: { params: { influencer_slug: string, content_slug: string } }) => {
    const router = useRouter()
    const { data: contentData, refetch } = useQuery(GET_CONTENT_QUERY, {
        variables: {
            contentSlug: params?.content_slug,
            influencerSlug: params?.influencer_slug
        },
        skip: !params.content_slug || !params.influencer_slug
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
    const [recalculateAggregateScores] = useMutation(RECALCULATE_AGGREGATE_SCORES_MUTATION)
    const [userAnalyseContent, { loading: isAnalysingContent }] = useMutation(USER_ANALYSE_CONTENT_MUTATION)
    const [deleteContent, { loading: isDeletingContent }] = useMutation(DELETE_CONTENT_MUTATION)
    const [classifyContent, { loading: isClassifyingContent }] = useMutation(CLASSIFY_CONTENT_MUTATION)
    const [updateEvidenceScore, { loading: isUpdatingEvidenceScore }] = useMutation(USER_UPDATE_EVIDENCE_SCORE_MUTATION)

    const mainContent = subscriptionData?.content?.[0] || contentData?.content?.[0]
    const assertions_contents = mainContent?.assertions_contents
    const isHydrated = useHydration()
    const [currentTimestamp, setCurrentTimestamp] = useState(0)
    const [player, setPlayer] = useState<any>(null);
    const convertTimestampToSeconds = (timestamp: string) => {
        if (!timestamp) return 0;

        // Handle formats like "15s-18s"
        if (timestamp.includes('-')) {
            // Take the first number before the dash
            const startTime = timestamp.split('-')[0];
            // Remove the 's' and convert to number
            return parseInt(startTime.replace('s', ''));
        }

        // Handle original MM:SS format
        if (timestamp.includes(':')) {
            const [minutes, seconds] = timestamp.split(':').map(Number);
            return minutes * 60 + seconds;
        }

        // Handle single number with 's' format
        return parseInt(timestamp.replace('s', ''));
    };
    if (!isHydrated) { return null }
    return (
        <>

            <h6>{isParsed === true ? 'is Parsed true' : 'is not parsed'} {mainContent?.id}</h6>
            <Button
                className="my-2"
                color="primary"
                isLoading={isAnalysingContent}
                onPress={() => {
                    userAnalyseContent({ variables: { contentId: mainContent?.id } })
                }}
            >
                Analyse content
            </Button>
            <Button
                className="my-2 mx-4"
                color="danger"
                isLoading={isDeletingContent}
                onPress={async () => {
                    deleteContent({ variables: { contentId: mainContent?.id } })
                    router.push(`/`)
                }}
            >
                Delete content
            </Button>
            <Card>
                <CardBody className="flex sm:flex-row sm:gap-x-8">
                    <div className="sm:w-1/3">
                        <YouTubePlayer
                            videoId={mainContent?.videoId}
                            currentTimestamp={currentTimestamp}
                            onPlayerReady={setPlayer}
                            className="w-full aspect-video"
                        />
                        {!mainContent?.title ?
                            <Spinner /> :
                            <motion.h1
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.2, ease: "easeInOut" }}
                                className="text-3xl font-bold my-8">{mainContent?.title}
                            </motion.h1>
                        }
                        <h4 className="uppercase text-tiny my-3">Overall Score</h4>
                        <div className="mb-5">
                            <Chip color="danger" size="lg" className="mr-2 text-white">
                                <Icon icon="ci:stop-sign" className="inline mr-2" />
                                {mainContent?.againstAggregateContentScore} / 100
                            </Chip>
                            <Chip color="success" size="lg" className="mr-2 text-white">
                                <Icon icon="mdi:approve" className="inline mr-2" />
                                {mainContent?.proAggregateContentScore} / 100
                            </Chip>
                            <Button
                                size="sm"
                                className="ml-4"
                                variant="flat"
                                color="primary"
                                isDisabled={!mainContent?.id}
                                onPress={() => {
                                    recalculateAggregateScores({ variables: { contentId: mainContent?.id } })
                                }}
                            >
                                Refresh Score
                            </Button>
                        </div>
                        {assertions_contents?.length > 0 &&
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.2, ease: "easeInOut" }}
                            >
                                <h4 className="uppercase text-tiny my-3">Breakdown of argument</h4>
                                {
                                    assertions_contents?.length > 0 && assertions_contents.map((assertions_content: any, index: number) => (
                                        <Card className="mb-4" key={`assertion_content_${index}`}>
                                            <CardBody >
                                                <Link
                                                    onPress={() => {
                                                        if (!player) return;
                                                        const seconds = convertTimestampToSeconds(assertions_content?.videoTimestamp);
                                                        try {
                                                            player.seekTo(seconds);
                                                        } catch (error) {
                                                            console.error('Error seeking video:', error);
                                                        }

                                                        const element = document.getElementById(`assertion_${index}`);
                                                        element?.scrollIntoView({ behavior: 'smooth' });
                                                    }}
                                                    size="sm"
                                                    className="cursor-pointer"
                                                >
                                                    {index + 1}) (time: {assertions_content?.videoTimestamp}): {assertions_content?.assertion.text}
                                                </Link>
                                                <Slider
                                                    step={1}
                                                    isDisabled
                                                    size="sm"
                                                    hideThumb={true}
                                                    hideValue={true}
                                                    color="success"
                                                    showSteps={false}
                                                    maxValue={10}
                                                    minValue={0}
                                                    defaultValue={Number(assertions_content?.weightConclusion)}
                                                    className="max-w-md mb-2"
                                                />
                                                <div>
                                                    <Chip color="success" className="text-white mr-2 ">
                                                        <Icon icon="mdi:approve" className="inline" />{' '}
                                                        <AnimatedNumber targetNumber={assertions_content?.assertion?.proEvidenceAggregateScore || 0} /> / 100
                                                    </Chip>
                                                    <Chip color="danger" className="text-white">
                                                        <Icon icon="ci:stop-sign" className="inline" />{' '}
                                                        <AnimatedNumber targetNumber={assertions_content?.assertion?.againstEvidenceAggregateScore || 0} /> / 100
                                                    </Chip>
                                                </div>
                                                <div className="block mt-3">
                                                    {
                                                        assertions_content?.assertion?.contents_assertions.map((o: any, i: number) => (
                                                            <Chip
                                                                key={i}
                                                                color={o?.isProAssertion === true ? 'success' : 'danger'}
                                                                className="text-white mr-2"
                                                            // className={`${o?.is_pro_assertion === true ? 'bg-green-500' : 'bg-red-500'} px-4 text-tiny  inline-block mr-2 p-1 text-white rounded-full`}
                                                            >
                                                                {/* {o?.is_pro_assertion === true ? <Icon icon="mdi:approve" className="inline" /> : <Icon icon="ci:stop-sign" className="inline" />} */}
                                                                {/* {Math.round(o?.content?.content_score) || 0} */}
                                                                <AnimatedNumber targetNumber={Math.round(o?.content?.contentScore) || 0} /> / 100
                                                            </Chip>
                                                        ))
                                                    }
                                                </div>
                                            </CardBody>
                                        </Card >
                                    ))
                                }
                            </motion.div>
                        }
                    </div>
                    <div className="sm:w-2/3">

                        <h2 className="uppercase">Main point</h2>
                        <h2 className="text-3xl font-bold my-4">{mainContent?.conclusion}</h2>
                        <h2 className="uppercase">Summary</h2>
                        <h2 className="text-lg my-4">{mainContent?.summary}</h2>

                        {/* <h2 className="uppercase mb-4">Connected Content</h2>
                        {relatedContent?.length > 0 && relatedContent.map((content, index) => {
                            return (
                                <div key={index} className="flex flex-col mb-4">
                                    <h1 className="">{content?.child_content?.title}</h1>
                                    <h2 className="font-bold">{content?.child_content?.source_url}</h2>
                                </div>
                            )
                        })} */}
                        <h2 className="uppercase mt-5">The main assertions from the author:</h2>
                        {!assertions_contents?.length || assertions_contents?.length === 0 &&
                            <Spinner />
                        }
                        <ul className="my-4">

                            {assertions_contents?.length > 0 && assertions_contents.map((assertions_content: any, index: number) => {
                                return (
                                    <li key={index} className="mb-16">
                                        <div className="m-8">
                                            <h4 className="text-2xl font-bold my-4">{index + 1}) {assertions_content.assertion.text}</h4>
                                            <h4 className="text-sm my-2"> {assertions_content.assertionContext}</h4>
                                            {/* <h5>assertion id {assertions_content?.assertion?.id}</h5> */}
                                            {assertions_content?.assertion &&
                                                <>
                                                    <Chip color="success" size="lg" className="text-white mr-2"><Icon icon="mdi:approve" className="inline" /> {assertions_content?.assertion?.proEvidenceAggregateScore || 0} / 100</Chip>
                                                    <Chip color="danger" size="lg" className=" text-white"> <Icon icon="ci:stop-sign" className="inline" /> {assertions_content?.assertion?.againstEvidenceAggregateScore || 0} / 100</Chip>
                                                </>
                                            }
                                            <Slider
                                                step={1}
                                                isDisabled
                                                size="lg"
                                                hideThumb={true}
                                                hideValue={true}
                                                color="success"
                                                label={`Importance to conclusion ${assertions_content?.weightConclusion}/10`}
                                                showSteps={false}
                                                maxValue={10}
                                                minValue={0}
                                                defaultValue={Number(assertions_content?.weightConclusion)}
                                                className="max-w-md my-4"
                                            />
                                            {/* <h5 className=" text-sm my-4 font-bold">ass id: {assertions_content.assertion.id}</h5> */}
                                            <h5 className="font-bold uppercase text-sm my-4">The author said (time: {assertions_content?.videoTimestamp}):</h5>
                                            <p className="text-xl italic">&quot;{assertions_content?.assertion.originalSentence}&quot;</p>
                                            {/* <h4 className="text-sm">SEARCH: {assertions_content?.assertion?.assertionSearchVerify}</h4> */}
                                            {/* <h5 className="font-bold uppercase text-sm my-4">What author cites as evidence</h5> */}
                                            {/* <p>{assertions_content.assertion.evidenceType}</p> */}
                                            <h5 className="uppercase font-bold text-sm my-4">Evidence related to assertion</h5>
                                            {!assertions_content?.assertion?.contents_assertions?.length || assertions_content?.assertion?.contents_assertions?.length === 0 &&
                                                <Spinner />
                                            }
                                            {assertions_content?.assertion?.contents_assertions?.length > 0 ?
                                                <>
                                                    {
                                                        assertions_content?.assertion?.contents_assertions.map(
                                                            (o: any, i: number) => (
                                                                <div key={i} id={`assertion_${i}`} className="my-4">
                                                                    <div className="my-3">
                                                                        <Chip
                                                                            color={o?.isProAssertion ? 'success' : 'danger'}
                                                                            className="text-white"
                                                                        >
                                                                            <Icon className="inline text-lg" icon={o?.isProAssertion ? "mdi:approve" : "ci:stop-sign"} />{' '}
                                                                            {/* {o?.is_pro_assertion ? 'supports' : 'refutes'} */}
                                                                            {' '}{Math.round(o?.content?.contentScore || 0)} / 100
                                                                        </Chip>
                                                                    </div>

                                                                    <div className="ml-8 my-2">
                                                                        <h6 className="text-tiny  uppercase">{o?.isCitationFromOriginalContent ? 'From Author' : 'Ai Research'}</h6>
                                                                        <Link href={o?.content?.sourceUrl}>{o?.content?.title}</Link>
                                                                        <h6 className="text-tiny my-3">DOI: {o?.content?.doiNumber}</h6>

                                                                        <h6>{o?.whyRelevant}</h6>
                                                                        <h6>content id: {o?.content?.id}</h6>
                                                                        <div className="my-3">
                                                                            <Chip color="warning" className="text-white">{o?.content?.contentType}</Chip>
                                                                        </div>
                                                                        {o?.content?.sciencePaperClassification ?
                                                                            <>
                                                                                <StudyClassification paperClassification={o?.content?.sciencePaperClassification} />
                                                                                <Button
                                                                                    className="mt-2"
                                                                                    color="primary"
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

                                                                                {/* <h6 className="">{o?.content?.sourceUrl}</h6> */}
                                                                            </div>
                                                                        }
                                                                        {/* <h6 className="text-tiny">{o?.content?.whyRelevant}</h6> */}
                                                                    </div>

                                                                </div>
                                                            ))
                                                    }
                                                </> :
                                                <h6 className="text-red-500 font-bold">* Evidence not yet found</h6>
                                            }

                                        </div>
                                    </li>
                                )
                            })}
                        </ul>
                    </div>
                </CardBody>
                <CardFooter>
                </CardFooter>
                <Divider />

            </Card>
        </ >
    );
}

export default VideoPage