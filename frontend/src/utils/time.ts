export const convertTimestampToSeconds = (timestamp: string) => {
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