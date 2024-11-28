'use client'

import { Button, Card, CardBody, CardFooter, Chip, Input, Pagination } from "@nextui-org/react";
import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_INFLUENCERS_QUERY } from '@/store/influencers'
import { StorageImage } from '@/components/assets/StorageImage'
import { useDebounce } from '@/hooks/useDebounce'
import { useState, useMemo, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useResponsive } from '@/hooks/useResponsive'

import { useRouter } from 'next/navigation'
import { Icon } from "@iconify/react/dist/iconify.js";

const ITEMS_PER_PAGE = 12;
const MOBILE_HEADER_HEIGHT = 64; // Height of mobile header

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

export default function Home() {
  const router = useRouter()
  const [searchTerm, setSearchTerm] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [shouldScroll, setShouldScroll] = useState(false)
  const [previousResults, setPreviousResults] = useState<string>('')
  const debouncedSearch = useDebounce(searchTerm, 500)
  const resultsRef = useRef<HTMLDivElement>(null)
  const searchInputRef = useRef<HTMLDivElement>(null)
  const { isMobile } = useResponsive()

  const { data, loading } = useQuery(GET_INFLUENCERS_QUERY, {
    variables: {
      search: debouncedSearch ? `%${debouncedSearch}%` : '%%',
      offset: (currentPage - 1) * ITEMS_PER_PAGE,
      limit: ITEMS_PER_PAGE
    },
    fetchPolicy: 'cache-and-network'
  })

  const influencers = data?.influencers
  const totalCount = data?.influencers_aggregate?.aggregate?.count || 0
  const totalPages = Math.ceil(totalCount / ITEMS_PER_PAGE)
  const isHydrated = useHydration()

  // Reset to first page when search changes
  useEffect(() => {
    setCurrentPage(1)
  }, [debouncedSearch])

  // Set scroll flag when search term changes or page changes
  useEffect(() => {
    if (isMobile) {
      setShouldScroll(true);
    }
  }, [searchTerm, currentPage, isMobile]);

  // Handle scrolling after content loads
  useEffect(() => {
    if (!loading && shouldScroll && isMobile) {
      // Wait for the next frame to ensure content is rendered
      requestAnimationFrame(() => {
        // Add a small delay to ensure dynamic content is stable
        setTimeout(() => {
          if (searchTerm && searchInputRef.current) {
            const yOffset = -MOBILE_HEADER_HEIGHT + 20;
            const y = searchInputRef.current.getBoundingClientRect().top + window.pageYOffset + yOffset;
            window.scrollTo({ top: y, behavior: 'smooth' });
          } else if (currentPage > 1 && resultsRef.current) {
            const yOffset = -20;
            const y = resultsRef.current.getBoundingClientRect().top + window.pageYOffset + yOffset;
            window.scrollTo({ top: y, behavior: 'smooth' });
          }
          setShouldScroll(false);
        }, 100); // Small delay to ensure content is stable
      });
    }
  }, [loading, shouldScroll, searchTerm, currentPage, isMobile]);

  // Local search for instant feedback
  const filteredInfluencers = useMemo(() => {
    if (!influencers && !loading) return []
    if (!influencers) return []
    if (!searchTerm) return influencers

    const searchLower = searchTerm.toLowerCase()
    return influencers.filter((influencer: any) =>
      influencer.name.toLowerCase().includes(searchLower) ||
      (influencer.ytDescription && influencer.ytDescription.toLowerCase().includes(searchLower))
    )
  }, [influencers, searchTerm, loading])

  // Generate a key based on results content
  const resultsKey = useMemo(() => {
    if (!influencers?.length) return 'empty';
    return influencers.map((inf: any) => inf.id).join(',');
  }, [influencers]);

  // Update previous results and determine if animation should occur
  useEffect(() => {
    if (resultsKey !== previousResults) {
      setPreviousResults(resultsKey);
    }
  }, [resultsKey, previousResults]);

  const shouldAnimate = resultsKey !== previousResults;

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
            See <span className="text-danger"> below
              <Chip variant="light" color="danger" className="mx-0">
                <Icon icon="fa:arrow-down" />
              </Chip>
            </span>
            our list of influencers being researched.
          </p>
          <div className="flex flex-col justify-between sm:flex-row gap-4 pt-4" ref={searchInputRef}>
            <Input
              value={searchTerm}
              onValueChange={setSearchTerm}
              placeholder="Search influencers..."
              startContent={<Icon icon="tabler:search" className="text-default-400" />}
              size="lg"
              className="max-w-md"
              isClearable
              classNames={{
                input: "text-small",
                inputWrapper: "h-12",
              }}
            />
            <div className="text-right">
              <h6 className="text-xs my-2">Not finding who you are looking for?</h6>
              <Button
                size="sm"
                color="primary"
                variant="solid"
                onPress={() => { router.push('/influencer-queue') }}
              >
                Add Influencer
              </Button>
            </div>
          </div>
        </div>
      </section>

      <div className="flex sm:flex-row flex-col justify-between sm:items-center mb-4" ref={resultsRef}>
        <h2 className="text-gradient text-lg sm:text-2xl font-bold uppercase">
          Influencers we have researched
          {loading && <Chip size="sm" variant="flat" color="default" className="ml-2">Searching...</Chip>}
        </h2>
        {totalCount > 0 && (
          <p className="text-default-500 text-small">
            Showing {((currentPage - 1) * ITEMS_PER_PAGE) + 1} to {Math.min(currentPage * ITEMS_PER_PAGE, totalCount)} of {totalCount} influencers
          </p>
        )}
      </div>

      <section className="mb-8">
        <motion.div
          className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
          variants={container}
          initial={shouldAnimate ? "hidden" : false}
          animate={shouldAnimate ? "show" : false}
          key={shouldAnimate ? currentPage + debouncedSearch : undefined}
        >
          {(filteredInfluencers?.length > 0 || loading) ? (
            <div className="col-span-full min-h-[50vh]">
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {filteredInfluencers?.map((influencer: any) => (
                  <motion.div
                    key={influencer?.id}
                    variants={shouldAnimate ? item : undefined}
                    initial={shouldAnimate ? { opacity: 0 } : false}
                    animate={shouldAnimate ? { opacity: 1 } : false}
                    className="w-full h-full"
                  >
                    <Card isPressable onPress={() => { router.push(`/video/${influencer?.slug}`) }} className="w-full h-full">
                      <CardBody className="flex flex-col gap-2 p-3">
                        <div className="w-full">
                          <StorageImage
                            fileId={influencer?.profileImg}
                            alt={influencer?.name}
                            className="rounded-lg"
                          />
                        </div>
                        <h2 className="text-lg text-foreground font-bold line-clamp-1">{influencer?.name}</h2>
                      </CardBody>
                      <CardFooter className="flex-col gap-2 items-start text-left p-3 pt-0">
                        <div className="flex gap-2 flex-wrap">
                          <Chip
                            variant="bordered"
                            color="secondary"
                            size="sm"
                          >
                            videos: {influencer?.influencer_contents_aggregate?.aggregate.count}
                          </Chip>
                          {influencer.isFollowed && <Chip variant="dot" color="secondary" size="sm">Followed</Chip>}
                        </div>
                        <Button
                          color="primary"
                          variant="solid"
                          fullWidth
                          size="sm"
                          onPress={() => { router.push(`/video/${influencer?.slug}`) }}
                        >
                          Open <Icon icon="tabler:arrow-right" />
                        </Button>
                      </CardFooter>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </div>
          ) : (
            !loading && (
              <motion.div
                initial={shouldAnimate ? { opacity: 0 } : false}
                animate={shouldAnimate ? { opacity: 1 } : false}
                className="col-span-full min-h-[50vh] flex items-start"
              >
                <div className="flex flex-col items-start justify-start gap-4">
                  <p className="text-default-500">No influencers found matching your search criteria.</p>
                  <Button
                    color="primary"
                    variant="flat"
                    onPress={() => setSearchTerm("")}
                  >
                    Clear search
                  </Button>
                </div>
              </motion.div>
            )
          )}
        </motion.div>
        <div className="flex justify-center mb-24">
          <Pagination
            showControls
            total={totalPages}
            initialPage={1}
            page={currentPage}
            onChange={setCurrentPage}
            classNames={{
              wrapper: "gap-2",
              item: "w-8 h-8 text-small rounded-lg",
              cursor:
                "bg-gradient-to-b from-default-500 to-default-600 text-white font-bold",
            }}
          />
        </div>
      </section>
    </>
  );
}
