'use client'

import { Button, Card, CardBody, CardFooter, CardHeader, Chip } from "@nextui-org/react";
import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_INFLUENCERS_QUERY } from '@/store/influencers'
import { StorageImage } from '@/components/assets/StorageImage'

import { useRouter } from 'next/navigation'
import { Icon } from "@iconify/react/dist/iconify.js";

export default function Home() {
  const router = useRouter()
  const { data } = useQuery(GET_INFLUENCERS_QUERY, { fetchPolicy: 'cache-and-network' })
  const influencers = data?.influencers
  const isHydrated = useHydration()
  if (!isHydrated) { return null }
  return (
    <>
      <section className="mb-12">
        <div className="space-y-4">
          <p className="text-primary font-medium">We are currently checking</p>
          <h1 className="text-6xl font-bold tracking-tight">
            Science <span className="text-gradient">Influencers</span> we<br />
            have researched
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            See below our list of influencers being researched.
          </p>
          <div className="flex gap-4 pt-4">
            <Button
              size="lg"
              color="primary"
              variant="solid"
              onPress={() => { router.push('/influencer-queue') }}
            >
              Suggest Influencer
            </Button>
          </div>
        </div>


      </section>

      <h2 className="text-gradient text-2xl font-bold uppercase py-4">Influencers we have researched</h2>
      <section className="mb-24 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {influencers?.map((influencer: any) => (
          <Card key={influencer?.id} isPressable onPress={() => { router.push(`/video/${influencer?.slug}`) }}>
            <CardBody className="flex flex-col gap-2">
              <StorageImage fileId={influencer?.profileImg} />
              <h2 className="text-lg text-foreground font-bold">{influencer?.name}</h2>
            </CardBody>
            <CardFooter className="flex-col gap-2 items-start text-left">
              <div className="flex gap-2">
                <Chip
                  variant="bordered"
                  color="secondary"
                >
                  videos: {influencer?.influencer_contents_aggregate?.aggregate.count}
                </Chip>
                {influencer.isFollowed && <Chip variant="dot" color="secondary">Followed</Chip>}
              </div>
              <Button
                color="primary"
                variant="solid"
                fullWidth
                onPress={() => { router.push(`/video/${influencer?.slug}`) }}
              >
                Open <Icon icon="tabler:arrow-right" />
              </Button>
            </CardFooter>
          </Card>
        ))}
      </section >


    </>
  );
}
