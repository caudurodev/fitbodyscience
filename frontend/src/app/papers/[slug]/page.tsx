'use client'

import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_PAPER_FROM_SLUG_QUERY } from '@/store/content/query'
import { Link, Chip } from "@nextui-org/react";
import { Icon } from '@iconify/react'

export default function Page({ params }: { params: { slug: string } }) {

  const { data, loading } = useQuery(
    GET_PAPER_FROM_SLUG_QUERY,
    { variables: { paperSlug: params?.slug }, fetchPolicy: 'network-only' }
  )
  const paperInfo = data?.content?.[0]
  const sciencePaperClassification = paperInfo?.sciencePaperClassification
  const title = sciencePaperClassification?.paperDetails?.title ? sciencePaperClassification?.paperDetails?.title : paperInfo?.title

  const assertions = paperInfo?.contents_assertions
  console.log({ assertions })
  const isHydrated = useHydration()
  if (!isHydrated) { return null }
  return (
    <section className="mb-24">
      <h6 className="text-tiny uppercase text-primary font-bold my-2">Paper</h6>
      <h1 className="text-6xl font-bold tracking-tight">{title}</h1>
      <div className="flex flex-col gap-2 p-4 my-4">
        <h3>DOI: <Link href={`${paperInfo?.doiNumber}`}>{paperInfo?.doiNumber}</Link></h3>

        <h3>DOI: {paperInfo?.doiNumber}</h3>
      </div>
      <h6 className="text-primary font-bold text-tiny uppercase my-2">
        Assertions that use this paper
      </h6>
      <ul>
        {assertions?.map((assertion: any) => {
          return (
            <li key={assertion?.assertion?.id}>
              <Assertion assertion={assertion?.assertion} />
            </li>
          )
        })}
      </ul>
    </section>
  );
}


export const Assertion = ({ assertion }) => {
  return (
    <div className="my-2">
      <Link href={`/assertions/${assertion?.slug}`} color="secondary"><h3>{assertion?.text}</h3></Link>
      <div className="flex flex-row gap-2 my-2">
        <Chip color="success" size="sm" className="mr-2">
          <Icon icon="mdi:success-bold" className="inline mr-2" />
          {assertion?.proEvidenceAggregateScore} / 100
        </Chip>
        <Chip color="danger" size="sm" className="mr-2">
          <Icon icon="maki:cross" className="inline mr-2" />
          {assertion?.againstEvidenceAggregateScore} / 100
        </Chip>
      </div>
    </div>
  )
} 
