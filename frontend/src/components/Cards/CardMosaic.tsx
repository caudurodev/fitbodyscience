import { Card, CardHeader, Chip, CardFooter, Link, Button } from "@nextui-org/react";
import { useRouter } from 'next/navigation'
import YouTubePlayer from '@/components/YouTubePlayer';
import { Icon } from '@iconify/react';

export const CardMosaic = ({ items }: { items: any[] }) => {
    if (!items) { return null }
    return (
        <div className=" gap-2 grid grid-cols-3">
            {items.map((item, index) => (
                <CardBottomCaptionItem key={index} item={item} />
            ))}

        </div>
    );
}

export const CardFullImageItem = ({ item }: { item: any }) => {
    return (
        <Card className="col-span-12 sm:col-span-4 h-[300px]">
            <CardHeader className="absolute z-10 top-1 flex-col !items-start">
                <p className="text-tiny text-white/60 uppercase font-bold">{item.category}</p>
                <h4 className="text-white font-medium text-large">{item.title}</h4>
            </CardHeader>
            <YouTubePlayer
                videoId={item?.video_id}
                className="z-0 w-full h-full"
            />
        </Card>
    );
}

export const CardBottomCaptionItem = ({ item }: { item: any }) => {
    const router = useRouter()
    return (
        <Card className=" min-h-[300px]">
            {/* <CardHeader className="absolute z-10 top-1 flex-col items-start"> */}
            {/* <p className="text-tiny text-white uppercase font-bold">New</p> */}
            {/* <h4 className="text-black font-medium text-2xl">Acme camera</h4> */}
            {/* </CardHeader> */}
            <YouTubePlayer
                videoId={item?.video_id}
                className="z-0 w-full h-full"
            />
            <CardFooter className="absolute bg-white bottom-0 border-t-1 border-zinc-100/50 z-10 justify-between">
                <div>
                    <Chip className="mr-2 text-white font-bold" color="primary" >
                        <Icon icon="mdi:approve" className="inline mr-2" />
                        {item.pro_aggregate_content_score || 0}
                    </Chip>
                    <Chip color="secondary" className="mr-2 text-white font-bold">
                        <Icon icon="ci:stop-sign" className="inline mr-2" />
                        {item.against_aggregate_content_score || 0}
                    </Chip>
                    {/* <p className="text-black text-tiny">{item.category}</p> */}
                    <p className="mt-2 text-md font-bold">{item.title}</p>
                </div>
                <Button
                    onPress={() => { router.push(`/video/${item.id}`) }}
                    className="text-tiny"
                    color="primary"
                    size="sm"
                >
                    Open <Icon icon="mdi:arrow-right" className="inline text-xl" />
                </Button>
            </CardFooter>
        </Card >
    );
}