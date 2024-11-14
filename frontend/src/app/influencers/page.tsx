'use client'

import { Button } from "@nextui-org/react";
import { Icon } from '@iconify/react'
import { useHydration } from '@/hooks/useHydration'
import { CardMosaic } from '@/components/Cards/CardMosaic'
import { useQuery } from '@apollo/client'
import { GET_INFLUENCERS_QUERY } from '@/store/influencers'
import { StorageImage } from '@/components/assets/StorageImage'

import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()
  const { data, loading } = useQuery(GET_INFLUENCERS_QUERY)
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

      <h2 className="text-gradient text-2xl font-bold uppercase py-2">Influencers</h2>
      <section className="mb-24">
        {influencers?.map((influencer: any) => (
          <div key={influencer.id}>
            {influencer.name}
            <StorageImage fileId={influencer.profileImg} />
          </div>
        ))}
      </section>


    </>
  );
}

