'use client'

import { Button, Spinner } from "@nextui-org/react";
import { useHydration } from '@/hooks/useHydration'
import { CardMosaic } from '@/components/Cards/CardMosaic'
import { useQuery } from '@apollo/client'
import { GET_ALL_CONTENT_QUERY } from '@/store/content/query'
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter()
  const { data, loading } = useQuery(
    GET_ALL_CONTENT_QUERY,
    { variables: { mediaType: 'youtube_video' }, fetchPolicy: 'network-only' }
  )
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
            A simple, <span className="text-secondary">intuitive</span>
            platform for science-checking influence content. Use our
            scoring system to evaluate content credibility and sources of online claims.
          </p>
          <div className="flex gap-4 pt-4">
            <Button
              size="lg"
              variant="bordered"
              color="secondary"
              onPress={() => { router.push('/influencers') }}
            >
              Browse
            </Button>
            <Button
              size="lg"
              color="primary"
              variant="solid"
              onPress={() => { router.push('/add') }}
            >
              Add
            </Button>
          </div>
        </div>
      </section>

      <h2 className="text-gradient text-2xl font-bold uppercase py-2">Latest Videos</h2>
      <section className="mb-24">
        {
          loading ?
            <Spinner /> :
            <CardMosaic items={contentItems} />
        }
      </section>

    </>
  );
}

