import { Card, CardBody, CardHeader, Chip, CardFooter, Link, Button } from "@nextui-org/react";
import { useRouter } from 'next/navigation'
import YouTubePlayer from '@/components/YouTubePlayer';
import { Icon } from '@iconify/react';

export const CardMosaic = ({ items }: { items: any[] }) => {
    if (!items) { return null }
    return (
        <div className=" gap-6 grid grid-cols-3">
            {items.map((item, index) => (
                <CardBottomCaptionItem key={index} item={item} />
            ))}

        </div>
    );
}

export const CardFullImageItem = ({ item }: { item: any }) => {
    const router = useRouter()
    const videoSlug = item?.influencer_contents?.[0]?.influencer?.slug + '/' + item?.slug
    return (
        <Card className="col-span-12 sm:col-span-4 h-[300px]"
            isPressable
            onPress={() => { router.push(`/video/${videoSlug}`) }}
        >
            <CardHeader className="absolute z-10 top-1 flex-col !items-start">
                <p className="text-tiny text-white/60 uppercase font-bold">{item.category}</p>
                <h4 className="text-white font-medium text-large">{item.title}</h4>
            </CardHeader>
            <CardBody className="overflow-visible py-2">
                <YouTubePlayer
                    videoId={item?.videoId}
                    className="z-0 w-full h-full object-cover rounded-xl"
                />
            </CardBody>
        </Card>
    );
}

export const CardBottomCaptionItem = ({ item }: { item: any }) => {
    const router = useRouter()
    const videoSlug = item?.influencer_contents?.[0]?.influencer?.slug + '/' + item?.slug
    return (
        <Card className="min-h-[300px] flex flex-col"
            isPressable
            onPress={() => { router.push(`/video/${videoSlug}`) }}
        >
            <CardBody className="overflow-visible p-0 flex-none">
                <YouTubePlayer
                    videoId={item?.videoId}
                />
            </CardBody>
            <CardFooter className="flex flex-col items-start gap-3 p-4">
                <div className="flex gap-2">
                    <Chip size="sm" color="primary" >
                        <Icon icon="mdi:approve" className="inline mr-2" />
                        {item.proAggregateContentScore || 0}
                    </Chip>
                    <Chip
                        classNames={{
                            base: "bg-gradient-to-br from-primary to-secondary border-small border-white/50 shadow-pink-500/30",
                            content: "drop-shadow shadow-black text-white",
                        }}
                        size="sm" color="secondary">
                        <Icon icon="ci:stop-sign" className="inline mr-2" />
                        {item.againstAggregateContentScore || 0}
                    </Chip>
                </div>
                <h4 className="text-left">{item.title}</h4>
            </CardFooter>
        </Card >
    );
}