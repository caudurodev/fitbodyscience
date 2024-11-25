'use client'

import { Card, CardBody, CardHeader } from "@nextui-org/react";
import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_INFLUENCERS_QUERY } from '@/store/influencers'
import { StorageImage } from '@/components/assets/StorageImage'

import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()
  const { data } = useQuery(GET_INFLUENCERS_QUERY, { fetchPolicy: 'cache-and-network' })
  const influencers = data?.influencers
  const isHydrated = useHydration()
  if (!isHydrated) { return null }
  return (
    <>
      <section className="mb-24">
        <div className="space-y-4">
          <p className="text-primary font-medium">We are currently checking</p>
          <h1 className="text-6xl font-bold tracking-tight">
            Our list of <span className="text-gradient">Influencers</span><br />
            being checked
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            See below our list of influencers being checked.
          </p>

        </div>
      </section>
      ``
      <h2 className="text-gradient text-2xl font-bold uppercase py-2">Influencers</h2>
      <section className="mb-24 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {influencers?.map((influencer: any) => (
          <Card key={influencer.id} isPressable onPress={() => { router.push(`/video/${influencer.slug}`) }}>
            <CardHeader className="flex-row gap-2 items-start text-left">
              <h2 className="text-xl font-bold">{influencer.name}</h2>
              <h6 className="text-sm">({influencer.influencer_contents_aggregate.aggregate.count})</h6>
            </CardHeader>
            <CardBody className="w-full">
              <StorageImage fileId={influencer.profileImg} />
            </CardBody>
          </Card>
        ))}
      </section >


    </>
  );
}

