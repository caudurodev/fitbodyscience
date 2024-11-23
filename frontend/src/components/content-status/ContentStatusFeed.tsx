'use client'

import { useEffect, useRef } from 'react'
import { useSubscription } from '@apollo/client'
import 'react-toastify/dist/ReactToastify.css'
import { GET_CONTENT_ACTIVITY_SUBSCRIPTION } from '@/store/content_activity/query'

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

export const ContentStatusFeed = ({ contentId }: ContentNotificationProps) => {
    const { data } = useSubscription<{ content_activity: ContentActivity[] }>(GET_CONTENT_ACTIVITY_SUBSCRIPTION, {
        variables: { contentId },
        shouldResubscribe: true
    })
    return <div>
        {data?.content_activity.map((activity, index) => <div key={activity.id}>({index})-{activity.name}</div>)}
    </div>;
};