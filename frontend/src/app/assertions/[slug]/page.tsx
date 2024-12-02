'use client'

import { Spinner } from "@nextui-org/react";
import { useHydration } from '@/hooks/useHydration'
import { CardMosaic } from '@/components/Cards/CardMosaic'
import { useQuery } from '@apollo/client'
import { GET_INFLUENCER_CONTENT_QUERY } from '@/store/content/query'
import { useRouter } from "next/navigation";

export default function Page({ params }: { params: { slug: string } }) {
  const router = useRouter()
  const { data, loading } = useQuery(
    GET_INFLUENCER_CONTENT_QUERY,
    { variables: { influencerSlug: params?.slug, mediaType: 'youtube_video' }, fetchPolicy: 'network-only' }
  )
  const influencerInfo = data?.influencers?.[0]
  const influencerName = influencerInfo?.name
  const influencerContent = influencerInfo?.influencer_contents.map((content: any) => content.content)
  const isHydrated = useHydration()
  if (!isHydrated) { return null }
  return (
    <>
      <section className="mb-24">
        <div className="space-y-4">
          <p className="text-primary font-medium">The science of fitness</p>
          <h1 className="text-6xl font-bold tracking-tight">
            Content from <span className="text-gradient">{influencerName}</span><br />
            Added
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            See below our list of content from <span className="text-secondary">{influencerName}</span>.
            Where we have <span className="text-secondary">analysed the content</span> and evaluated the science behind what as
            stated in the content.
          </p>

        </div>
      </section>

      {influencerContent?.length > 0 ?
        <h2 className="text-gradient text-2xl font-bold uppercase py-2">
          Videos
        </h2> :
        <p className=" text-lg font-bold py-2">
          No videos analysed for {influencerName}
        </p>
      }
      <section className="mb-24">
        {
          loading ?
            <Spinner /> :
            <CardMosaic items={influencerContent} />
        }
      </section>

    </>
  );
}

