'use client'

import { Card, Chip, CardHeader, CardBody, CardFooter, Divider, Button } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_ALL_CONTENT_QUERY } from '@/store/index'
import YouTubePlayer from '@/components/YouTubePlayer';

import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()
  const { data, loading } = useQuery(GET_ALL_CONTENT_QUERY, { variables: { mediaType: 'youtube_video' }, fetchPolicy: 'cache-and-network' })
  const contentItems = data?.content
  const isHydrated = useHydration()
  if (!isHydrated) { return null }
  return (
    <>
      <section className="mb-24">
        <div className="space-y-4">
          <p className="text-primary font-medium">The science of fitness</p>
          <h1 className="text-6xl font-bold tracking-tight">
            Discover the <span className="text-gradient">Science</span><br />
            behind fitness
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            A simple, <span className="text-secondary">intuitive</span> platform for fact-checking videos. Use our community-driven scoring system to evaluate content credibility and authenticity.
          </p>
          <div className="flex gap-4 pt-4">
            <Button
              size="lg"
              variant="bordered"
              color="secondary"
            >
              Browse Examples
            </Button>
            <Button
              size="lg"
              color="primary"
              variant="solid"
            >
              Get Started
            </Button>
          </div>
        </div>
      </section>
      <div className="md:grid md:grid-cols-3 gap-4">
        {!loading && contentItems?.length > 0 && contentItems.map((contentItem: any, index: number) => {
          return (
            <Card key={index} className="my-8 px-4">
              <CardHeader className="flex flex-col gap-2">
                <h1 className="text-xl font-bold">{contentItem.title}</h1>
                <div>
                  <Chip color="success" className="mr-2">
                    <Icon icon="mdi:approve" className="inline" />
                    {contentItem.pro_aggregate_content_score || 0}
                  </Chip>
                  <Chip color="danger">
                    <Icon icon="ci:stop-sign" className="inline" />
                    {contentItem.against_aggregate_content_score || 0}
                  </Chip>
                </div>
              </CardHeader>
              <CardBody className="h-full">
                <YouTubePlayer
                  videoId={contentItem?.video_id}
                  className="w-full aspect-video"
                />
                <h2 className="text-lg my-4 text-sm">{contentItem.conclusion}</h2>
                <Button
                  variant="solid"
                  color="primary"
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
    </>
  );
}

