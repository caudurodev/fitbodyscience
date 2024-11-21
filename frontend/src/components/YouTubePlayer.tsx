import { useState, useEffect } from 'react';
import YouTube from 'react-youtube';
import Image from 'next/image';
import { motion } from 'framer-motion';

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
        if (!videoId) {
            return <div className={className}>No video ID provided</div>;
        }

        return (
            <div
                className={`${className} relative cursor-pointer group overflow-hidden rounded-xl border-4 border-primary`}
                onClick={() => setShowPlayer(true)}
            >
                <Image
                    src={`https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`}
                    alt="Video thumbnail"
                    fill
                    className="object-cover z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 "
                    priority
                    sizes="(max-width: 768px) 100vw, 33vw"
                />
                <Image
                    src={`https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`}
                    alt="Video thumbnail"
                    fill
                    className="object-cover grayscale"
                    priority
                    sizes="(max-width: 768px) 100vw, 33vw"
                />
                <div className="absolute inset-0 bg-primary/30 mix-blend-multiply group-hover:opacity-0 transition-opacity duration-300" />

                {/* <motion.div
                    className="absolute inset-0 flex items-center justify-center z-20"
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileHover={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.2 }}
                >
                    <motion.div
                        className="w-16 h-16 bg-white/30 backdrop-blur-sm rounded-full flex items-center justify-center"
                        whileHover={{ scale: 1.1 }}
                    >
                        <svg
                            className="w-8 h-8 text-white"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path d="M8 5v14l11-7z" />
                        </svg>
                    </motion.div>
                </motion.div> */}
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