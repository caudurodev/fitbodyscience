'use client'

import { Card, Spinner, Slider, CardBody, CardFooter, Divider, Button, Link, Chip } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { motion } from 'framer-motion'
import { useSubscription, useMutation } from '@apollo/client'
import { GET_CONTENT_SUBSCRIPTION, RECALCULATE_AGGREGATE_SCORES_MUTATION } from '@/store/index'
import { useHydration } from '@/hooks/useHydration'
import StudyClassification from "@/components/StudyClassification";
import { AnimatedNumber } from "@/components/AnimatedNumber";
import { useState } from 'react'
import YouTubePlayer from '@/components/YouTubePlayer';

export const VideoPage = ({ params }: { params: { id: string } }) => {
    const { data } = useSubscription(
        GET_CONTENT_SUBSCRIPTION,
        {
            variables: {
                contentId: params?.id
            },
            skip: !params.id
        },
    )
    const [recalculateAggregateScores] = useMutation(RECALCULATE_AGGREGATE_SCORES_MUTATION)
    const mainContent = data?.content?.[0]
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
        <main className="p-24 min-h-screen">
            <Card>

                <CardBody className="flex flex-row gap-x-8">
                    <div className="w-1/3">
                        <YouTubePlayer
                            videoId={mainContent?.video_id}
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
                                {mainContent?.against_aggregate_content_score} / 100
                            </Chip>
                            <Chip color="success" size="lg" className="mr-2 text-white">
                                <Icon icon="mdi:approve" className="inline mr-2" />
                                {mainContent?.pro_aggregate_content_score} / 100
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
                                    assertions_contents?.length > 0 && assertions_contents.map((assertions_content, index) => (
                                        <Card className="mb-4" key={`assertion_content_${index}`}>
                                            <CardBody >
                                                <Link
                                                    onPress={() => {
                                                        if (!player) return;
                                                        const seconds = convertTimestampToSeconds(assertions_content?.video_timestamp);
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
                                                    {index + 1}) (time: {assertions_content?.video_timestamp}): {assertions_content?.assertion.text}
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
                                                    defaultValue={Number(assertions_content?.weight_conclusion)}
                                                    className="max-w-md mb-2"
                                                />
                                                <div>
                                                    <Chip color="success" className="text-white mr-2 ">
                                                        <Icon icon="mdi:approve" className="inline" />{' '}
                                                        <AnimatedNumber targetNumber={assertions_content?.assertion?.pro_evidence_aggregate_score || 0} /> / 100
                                                    </Chip>
                                                    <Chip color="danger" className="text-white">
                                                        <Icon icon="ci:stop-sign" className="inline" />{' '}
                                                        <AnimatedNumber targetNumber={assertions_content?.assertion?.against_evidence_aggregate_score || 0} /> / 100
                                                    </Chip>
                                                </div>
                                                <div className="block mt-3">
                                                    {
                                                        assertions_content?.assertion?.contents_assertions.map((o, i) => (
                                                            <Chip
                                                                key={i}
                                                                color={o?.is_pro_assertion === true ? 'success' : 'danger'}
                                                                className="text-white mr-2"
                                                            // className={`${o?.is_pro_assertion === true ? 'bg-green-500' : 'bg-red-500'} px-4 text-tiny  inline-block mr-2 p-1 text-white rounded-full`}
                                                            >
                                                                {/* {o?.is_pro_assertion === true ? <Icon icon="mdi:approve" className="inline" /> : <Icon icon="ci:stop-sign" className="inline" />} */}
                                                                {/* {Math.round(o?.content?.content_score) || 0} */}
                                                                <AnimatedNumber targetNumber={Math.round(o?.content?.content_score) || 0} /> / 100
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
                    <div className="w-2/3">

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
                            {assertions_contents?.length > 0 && assertions_contents.map((assertions_content, index) => {
                                return (
                                    <li key={index} className="mb-16">
                                        <div className="m-8">
                                            <h4 className="text-2xl font-bold my-4">{index + 1}) {assertions_content.assertion.text}</h4>
                                            <h4 className="text-sm my-2"> {assertions_content.assertion_context}</h4>
                                            {/* <h5>assertion id {assertions_content?.assertion?.id}</h5> */}
                                            {assertions_content?.assertion &&
                                                <>
                                                    <Chip color="success" size="lg" className="text-white mr-2"><Icon icon="mdi:approve" className="inline" /> {assertions_content?.assertion?.pro_evidence_aggregate_score || 0} / 100</Chip>
                                                    <Chip color="danger" size="lg" className=" text-white"> <Icon icon="ci:stop-sign" className="inline" /> {assertions_content?.assertion?.against_evidence_aggregate_score || 0} / 100</Chip>
                                                </>
                                            }
                                            <Slider
                                                step={1}
                                                isDisabled
                                                size="lg"
                                                hideThumb={true}
                                                hideValue={true}
                                                color="success"
                                                label={`Importance to conclusion ${assertions_content?.weight_conclusion}/10`}
                                                showSteps={false}
                                                maxValue={10}
                                                minValue={0}
                                                defaultValue={Number(assertions_content?.weight_conclusion)}
                                                className="max-w-md my-4"
                                            />
                                            {/* <h5 className=" text-sm my-4 font-bold">ass id: {assertions_content.assertion.id}</h5> */}
                                            <h5 className="font-bold uppercase text-sm my-4">The author said (time: {assertions_content?.video_timestamp}):</h5>
                                            <p className="text-xl italic">"{assertions_content?.assertion.original_sentence}"</p>
                                            {/* <h4 className="text-sm">SEARCH: {assertions_content?.assertion?.assertion_search_verify}</h4> */}
                                            {/* <h5 className="font-bold uppercase text-sm my-4">What author cites as evidence</h5> */}
                                            {/* <p>{assertions_content.assertion.evidence_type}</p> */}
                                            <h5 className="uppercase font-bold text-sm my-4">Evidence related to assertion</h5>
                                            {!assertions_content?.assertion?.contents_assertions?.length || assertions_content?.assertion?.contents_assertions?.length === 0 &&
                                                <Spinner />
                                            }
                                            {assertions_content?.assertion?.contents_assertions?.length > 0 ?
                                                <>
                                                    {
                                                        assertions_content?.assertion?.contents_assertions.map(
                                                            (o, i) => (
                                                                <div key={i} id={`assertion_${i}`} className="my-4">
                                                                    <div className="my-3">
                                                                        <Chip
                                                                            color={o?.is_pro_assertion ? 'success' : 'danger'}
                                                                            className="text-white"
                                                                        >
                                                                            <Icon className="inline text-lg" icon={o?.is_pro_assertion ? "mdi:approve" : "ci:stop-sign"} />{' '}
                                                                            {/* {o?.is_pro_assertion ? 'supports' : 'refutes'} */}
                                                                            {' '}{Math.round(o?.content?.content_score || 0)} / 100
                                                                        </Chip>
                                                                    </div>

                                                                    <div className="ml-8 my-2">
                                                                        <h6 className="text-tiny mb-4 uppercase">{o?.is_citation_from_original_content ? 'From Author' : 'Ai Research'}</h6>
                                                                        {/* {o?.content?.content_score === 0 ?
                                                                            <Chip color="default">0</Chip> :
                                                                            <Chip
                                                                                color={o?.content?.content_score > 0 ? "success" : "danger"}
                                                                                className="mr-2 text-white"
                                                                            >
                                                                                <Icon
                                                                                    icon={o?.is_pro_assertion ? "mdi:approve" : "ci:stop-sign"}
                                                                                    className="inline"
                                                                                />
                                                                                {Math.round(o?.content?.content_score || 0)}
                                                                            </Chip>
                                                                        } */}
                                                                        <Link href={o?.content?.source_url}>{o?.content?.title}</Link>
                                                                        <h6 className="text-tiny my-3">DOI: {o?.content?.doi_number}</h6>

                                                                        <h6>{o?.why_relevant}</h6>
                                                                        <h6>content id: {o?.content?.id}</h6>
                                                                        <div className="my-3">
                                                                            <Chip color="warning" className="text-white">{o?.content?.content_type}</Chip>
                                                                        </div>
                                                                        {o?.content?.science_paper_classification ?
                                                                            <StudyClassification paperClassification={o?.content?.science_paper_classification} /> :
                                                                            <div>
                                                                                <h6 className="text-red-500 font-bold">* Evidence not yet classified</h6>
                                                                                {/* <h6 className="">{o?.content?.source_url}</h6> */}
                                                                            </div>
                                                                        }
                                                                        {/* <h6 className="text-tiny">{o?.content?.why_relevant}</h6> */}
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
        </main >
    );
}


export default VideoPage