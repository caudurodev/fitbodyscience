import { useCallback } from 'react';
// import posthog from 'posthog-js';

interface AnalyticsEvent {
    action: string;
    category?: string;
    label?: string;
    value?: number;
    [key: string]: any; // Allow additional properties
}

export const useAnalytics = () => {
    const trackEvent = useCallback(({ action, category, label, value, ...otherProps }: AnalyticsEvent) => {
        // Track event with Google Analytics
        if (typeof window !== 'undefined' && (window as any).gtag) {
            (window as any).gtag('event', action, {
                event_category: category,
                event_label: label,
                value: value,
                ...otherProps
            });
        }

        // Track event with PostHog
        // if (typeof window !== 'undefined' && posthog) {
        //     posthog.capture(action, { category, label, value, ...otherProps });
        // }

        // Console log for development
        if (process.env.NODE_ENV === 'development') {
            console.log('Analytics event tracked:', { action, category, label, value, ...otherProps });
        }
    }, []);

    return { trackEvent };
};
