'use client'

import { Card, Chip, CardHeader, CardBody, CardFooter, Divider, Button } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_ALL_CONTENT_QUERY } from '@/store/index'

import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()
  const { data, loading } = useQuery(GET_ALL_CONTENT_QUERY, { variables: { mediaType: 'youtube_video' }, fetchPolicy: 'cache-and-network' })
  const contentItems = data?.content
  const isHydrated = useHydration()
  if (!isHydrated) { return null }
  return (
    <main className="p-24 min-h-screen">
      <h1>Browse</h1>
      <div className="grid grid-cols-3 gap-4">
        {!loading && contentItems?.length > 0 && contentItems.map((contentItem: any, index: number) => {
          return (
            <Card key={index} className="my-8 px-4">
              <CardHeader className="flex flex-col gap-2">
                <h1 className="text-xl font-bold">{contentItem.title}</h1>
                <div>
                  <Chip color="success" className="text-white mr-2   "><Icon icon="mdi:approve" className="inline" />
                    {contentItem.pro_aggregate_content_score || 0}
                  </Chip>
                  <Chip color="danger" className="text-white">
                    <Icon icon="ci:stop-sign" className="inline" />
                    {contentItem.against_aggregate_content_score || 0}
                  </Chip>
                </div>
              </CardHeader>
              <CardBody className="h-full">
                <div className="w-full">
                  {/* <LiteYouTubeEmbed
                    id={contentItem.video_id}
                    title="What’s new in Material Design for the web (Chrome Dev Summit 2019)"
                  /> */}
                </div>
                <h2 className="text-lg my-4">{contentItem.conclusion}</h2>
                <Button
                  variant="solid"
                  color="primary"
                  className="bottom-0"
                  size="lg"
                  onPress={() => { router.push(`/video/${contentItem.id}`) }}
                >
                  View
                </Button>
              </CardBody>
              <CardFooter>
              </CardFooter>
              <Divider />
            </Card>
          )
        }
        )}
      </div>
    </main>
  );
}

