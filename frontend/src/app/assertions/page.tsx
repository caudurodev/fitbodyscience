'use client'

import { Card, CardBody, CardFooter, Chip, Input, Pagination } from "@nextui-org/react";
import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_ASSERTIONS_QUERY } from '@/store/assertion/query'
import { useDebounce } from '@/hooks/useDebounce'
import { useState, useMemo, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useResponsive } from '@/hooks/useResponsive'
import { useRouter } from 'next/navigation'
import { Icon } from "@iconify/react/dist/iconify.js";

const ITEMS_PER_PAGE = 12;
const MOBILE_HEADER_HEIGHT = 64;

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
  const debouncedSearch = useDebounce(searchTerm, 500)
  const resultsRef = useRef<HTMLDivElement>(null)
  const searchInputRef = useRef<HTMLDivElement>(null)
  const { isMobile } = useResponsive()

  const { data, loading } = useQuery(GET_ASSERTIONS_QUERY, {
    variables: {
      search: debouncedSearch ? `%${debouncedSearch}%` : '%%',
      offset: (currentPage - 1) * ITEMS_PER_PAGE,
      limit: ITEMS_PER_PAGE
    },
    fetchPolicy: 'cache-and-network'
  })

  const assertions = data?.assertions
  const totalCount = data?.assertions_aggregate?.aggregate?.count || 0
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
      requestAnimationFrame(() => {
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
        }, 100);
      });
    }
  }, [loading, shouldScroll, searchTerm, currentPage, isMobile]);

  // Local search for instant feedback
  const filteredAssertions = useMemo(() => {
    if (!assertions && !loading) return []
    if (!assertions) return []
    if (!searchTerm) return assertions

    const searchLower = searchTerm.toLowerCase()
    return assertions.filter((assertion: any) =>
      assertion.text.toLowerCase().includes(searchLower) ||
      assertion.contentContext?.toLowerCase().includes(searchLower)
    )
  }, [assertions, searchTerm, loading])

  return (
    <div className="w-full flex flex-col gap-8 p-4 md:p-8">
      <div ref={searchInputRef}>
        <Input
          value={searchTerm}
          onValueChange={setSearchTerm}
          placeholder="Search assertions..."
          startContent={<Icon icon="mdi:magnify" width={24} />}
          size="lg"
          variant="bordered"
          className="w-full"
        />
      </div>

      <div ref={resultsRef}>
        {isHydrated && (
          <motion.div
            variants={container}
            initial="hidden"
            animate="show"
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            {loading ? (
              Array.from({ length: ITEMS_PER_PAGE }).map((_, index) => (
                <motion.div key={index} variants={item}>
                  <Card className="w-full h-[200px] space-y-5 p-4" radius="lg">
                    <div className="h-24 rounded-lg bg-default-300"></div>
                    <div className="space-y-3">
                      <div className="w-3/5 h-3 rounded-lg bg-default-300"></div>
                      <div className="w-4/5 h-3 rounded-lg bg-default-200"></div>
                      <div className="w-2/5 h-3 rounded-lg bg-default-300"></div>
                    </div>
                  </Card>
                </motion.div>
              ))
            ) : (
              filteredAssertions.map((assertion: any) => (
                <motion.div key={assertion.id} variants={item}>
                  <Card
                    isPressable
                    onPress={() => router.push(`/assertions/${assertion.slug}`)}
                    className="w-full"
                  >
                    <CardBody className="gap-4">
                      <p className="text-lg font-semibold line-clamp-2">
                        {assertion.text}
                      </p>
                      {assertion.contentContext && (
                        <p className="text-sm text-default-500 line-clamp-3">
                          {assertion.contentContext}
                        </p>
                      )}
                    </CardBody>
                    <CardFooter className="gap-2 justify-between">
                      <div className="flex gap-1">
                        <Chip color="success" size="sm" className="mr-2">
                          <Icon icon="mdi:success-bold" className="inline mr-2" />
                          {assertion?.proAggregateContentScore} / 100
                        </Chip>
                        <Chip color="danger" size="sm" className="mr-2">
                          <Icon icon="maki:cross" className="inline mr-2" />
                          {assertion?.againstAggregateContentScore} / 100
                        </Chip>

                      </div>
                    </CardFooter>
                  </Card>
                </motion.div>
              ))
            )}
          </motion.div>
        )}

        {totalPages > 1 && (
          <div className="flex justify-center mt-8">
            <Pagination
              showControls
              total={totalPages}
              initialPage={1}
              page={currentPage}
              onChange={setCurrentPage}
            />
          </div>
        )}
      </div>
    </div>
  )
}
