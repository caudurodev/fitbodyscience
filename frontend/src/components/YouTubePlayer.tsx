import { useState, useEffect } from 'react';
import YouTube from 'react-youtube';

interface YouTubePlayerProps {
    videoId?: string;
    currentTimestamp?: number;
    className?: string;
    onPlayerReady?: (player: any) => void;
}

export const YouTubePlayer = ({
    videoId,
    currentTimestamp = 0,
    className = "w-full aspect-video",
    onPlayerReady,
}: YouTubePlayerProps) => {
    const [player, setPlayer] = useState<any>(null);
    const [isReady, setIsReady] = useState(false);
    const [showPlayer, setShowPlayer] = useState(false);

    const opts = {
        width: '100%',
        height: '100%',
        playerVars: {
            modestbranding: 1,
            rel: 0,
            enablejsapi: 1,
            autoplay: 1,
            controls: 1,
            playsinline: 1,
        },
    };

    const handleReady = (event: any) => {
        const playerInstance = event.target;
        setPlayer(playerInstance);
        setIsReady(true);
        if (onPlayerReady) {
            onPlayerReady(playerInstance);
        }
    };

    useEffect(() => {
        if (isReady && player && typeof currentTimestamp === 'number') {
            try {
                player.seekTo(currentTimestamp);
            } catch (error) {
                console.error('Error controlling YouTube player:', error);
            }
        }
    }, [currentTimestamp, player, isReady]);

    if (!showPlayer) {
        return (
            <div
                className={`${className} relative cursor-pointer`}
                onClick={() => setShowPlayer(true)}
            >
                <img
                    src={`https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`}
                    alt="Video thumbnail"
                    className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-16 h-12 bg-red-600 rounded-lg flex items-center justify-center">
                        <div className="w-0 h-0 border-t-8 border-t-transparent border-l-[16px] border-l-white border-b-8 border-b-transparent ml-1">
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className={className}>
            <YouTube
                videoId={videoId}
                opts={opts}
                onReady={handleReady}
                className="w-full h-full"
                iframeClassName="w-full h-full"
            />
        </div>
    );
};

export default YouTubePlayer; 