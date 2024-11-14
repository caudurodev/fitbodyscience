import YouTubePlayer from '@/components/YouTubePlayer';
import { Card, CardHeader, CardBody, Image, CardFooter, Button } from "@nextui-org/react";

export const Card1 = ({ item }: { item: any }) => {
    if (!item) { return null }
    return (
        <Card className="py-4 h-[200px] overflow-hidden" isFooterBlurred>
            {/* <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
                <p className="text-tiny uppercase font-bold">{item.category}</p>
                <small className="text-default-500">{item.title}</small>
                {/* <h4 className="font-bold text-large">{item.title}</h4> */}
            {/* </CardHeader> */}
            {/* // <CardBody className="overflow-visible py-2 "> */}
            <YouTubePlayer
                videoId={item?.video_id}
                className=" w-full h-[250px] object-cover"
            />
            {/* </CardBody> */}
            <CardFooter className="justify-between before:bg-white/10 border-white/20 border-1 overflow-hidden py-1 absolute before:rounded-xl rounded-large bottom-1 w-[calc(100%_-_8px)] shadow-small ml-1 z-10">
                <p className="text-tiny text-white/80">Available soon.</p>
                <Button className="text-tiny text-white bg-black/20" variant="flat" color="default" radius="lg" size="sm">
                    Notify me
                </Button>
            </CardFooter>
        </Card>
    );
}