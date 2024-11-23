'use client'

import { useEffect, useRef } from 'react'
import { useSubscription } from '@apollo/client'
import { toast, ToastContainer } from 'react-toastify'
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

const toastClasses = {
    success: 'bg-success text-success-foreground !bg-opacity-100',
    error: 'bg-danger text-danger-foreground !bg-opacity-100',
    info: 'bg-primary text-primary-foreground !bg-opacity-100',
    warning: 'bg-warning text-warning-foreground !bg-opacity-100',
} as const

type ToastType = keyof typeof toastClasses

export const ContentNotification = ({ contentId }: ContentNotificationProps) => {
    const { data } = useSubscription<{ content_activity: ContentActivity[] }>(GET_CONTENT_ACTIVITY_SUBSCRIPTION, {
        variables: { contentId },
        shouldResubscribe: true
    })

    const lastActivityIdsRef = useRef<Set<string>>(new Set())
    const isFirstLoadRef = useRef(true)

    const showNotification = (message: string, type: ToastType = 'info') => {
        toast(message, {
            position: "bottom-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            toastId: new Date().getTime(),
            type,
            className: `${toastClasses[type]} rounded-lg !bg-opacity-100`,
            bodyClassName: 'text-sm font-medium',
            progressClassName: `${type === 'error'
                ? 'bg-danger !bg-opacity-100'
                : type === 'success'
                    ? 'bg-success !bg-opacity-100'
                    : type === 'warning'
                        ? 'bg-warning !bg-opacity-100'
                        : 'bg-primary !bg-opacity-100'
                }`,
            theme: document?.documentElement?.classList.contains('dark') ? 'dark' : 'light'
        })
    }

    useEffect(() => {
        if (data?.content_activity && data.content_activity.length > 0) {
            if (isFirstLoadRef.current) {
                // On first load, just record all existing activity IDs without showing notifications
                data.content_activity.forEach(activity => {
                    lastActivityIdsRef.current.add(activity.id)
                })
                isFirstLoadRef.current = false
            } else {
                // After first load, only show notifications for new activities
                data.content_activity.slice().reverse().forEach(activity => {
                    if (!lastActivityIdsRef.current.has(activity.id)) {
                        lastActivityIdsRef.current.add(activity.id)
                        const message = activity.description || activity.name || 'New activity'
                        const toastType = (activity.type?.toLowerCase() || 'info') as ToastType
                        showNotification(message, toastType)
                    }
                })
            }
        }
    }, [data?.content_activity])

    return (
        <ToastContainer
            position="bottom-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            theme={document?.documentElement?.classList.contains('dark') ? 'dark' : 'light'}
            limit={5}
            toastClassName={() =>
                'relative flex p-4 min-h-10 rounded-lg justify-between overflow-hidden cursor-pointer'
            }
        />
    )
}

ContentNotification.displayName = 'ContentNotification'

export default ContentNotification