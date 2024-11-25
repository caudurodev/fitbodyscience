'use client'

import { Spinner, ScrollShadow, Card, CardBody } from "@nextui-org/react";
import { useQuery, useSubscription } from '@apollo/client'
import 'react-toastify/dist/ReactToastify.css'
import { GET_CONTENT_ACTIVITY_SUBSCRIPTION, GET_CONTENT_ACTIVITY_QUERY } from '@/store/content_activity/query'
import { motion } from 'framer-motion'
import { differenceInSeconds, differenceInMinutes } from 'date-fns'
import { useEffect, useRef, useState } from 'react'


interface ContentActivity {
    id: string
    name: string
    description?: string
    type?: string
    createdAt: string
    contentId: string
}

interface ContentNotificationProps {
    contentId: string
}

export const ContentActivityFeed = ({ contentId }: ContentNotificationProps) => {
    const { data: queryData, loading: queryLoading } = useQuery<{ content_activity: ContentActivity[] }>(
        GET_CONTENT_ACTIVITY_QUERY,
        {
            variables: { contentId }
        }
    );

    const { data: subscriptionData } = useSubscription<{ content_activity: ContentActivity[] }>(
        GET_CONTENT_ACTIVITY_SUBSCRIPTION,
        {
            variables: { contentId },
            shouldResubscribe: true
        }
    );

    // Use subscription data if available, otherwise fall back to query data
    const data = subscriptionData || queryData;
    const loading = queryLoading;

    const scrollRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTo({
                top: scrollRef.current.scrollHeight,
                behavior: 'smooth'
            })
        }
    }, [data?.content_activity])

    const totalNotifications = data?.content_activity?.length || 1

    return (
        <div className="p-2 ">
            <h6 className="text-xs uppercase font-bold text-primary">Content Activity</h6>
            <div className="my-2">
                {loading && <Spinner />}
            </div>
            <ScrollShadow ref={scrollRef} className="max-h-[140px] bg-default-200 px-2 rounde">
                <ul >
                    {data?.content_activity?.map((activity, index) => {
                        const firstActivityTime = data.content_activity[0]?.createdAt;
                        const currentActivityTime = activity.createdAt;
                        const diffInSeconds = differenceInSeconds(new Date(currentActivityTime), new Date(firstActivityTime));
                        const diffInMinutes = differenceInMinutes(new Date(currentActivityTime), new Date(firstActivityTime));

                        const timeDisplay = index === 0 ? 'Start' :
                            diffInMinutes > 0 ? `+${diffInMinutes}m` : `+${diffInSeconds}s`;

                        return (
                            <motion.li
                                className="text-xs my-2"
                                key={index}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.2, delay: (totalNotifications - index) * 0.1 }}
                            >
                                <Card radius="sm" shadow="sm">
                                    <CardBody className="py-2">
                                        {activity.name}
                                        <span className="ml-2 text-default-400">{timeDisplay}</span>
                                    </CardBody>
                                </Card>
                            </motion.li>
                        );
                    })}
                </ul>
            </ScrollShadow>
        </div>
    )
}
