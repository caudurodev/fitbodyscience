'use client'

import { useHydration } from '@/hooks/useHydration'
import { useQuery } from '@apollo/client'
import { GET_ASSERTION_FROM_SLUG_QUERY } from '@/store/assertion/query'
import { Link, Chip } from "@nextui-org/react";
import { Icon } from '@iconify/react'

export default function Page({ params }: { params: { slug: string } }) {
  const { data, loading } = useQuery(
    GET_ASSERTION_FROM_SLUG_QUERY,
    { variables: { assertionSlug: params?.slug }, fetchPolicy: 'network-only' }
  )
  const assertionInfo = data?.assertions?.[0]
  const assertionEvidence = assertionInfo?.contents_assertions
  console.log({ assertionEvidence })

  const isHydrated = useHydration()
  if (!isHydrated) { return null }
  return (
    <section className="mb-24">
      <h6 className="text-tiny uppercase text-primary font-bold my-2">Assertion</h6>
      <h1 className="text-6xl font-bold tracking-tight">{assertionInfo?.text}</h1>
      <div className="flex gap-2 p-4 my-4">
        <h4 className="uppercase font-bold text-primary-500 text-xs my-2">Our Score</h4>
        <div className="mb-2">
          <Chip color="success" size="lg" className="mr-2">
            <Icon icon="mdi:success-bold" className="inline mr-2" />
            {assertionInfo?.proEvidenceAggregateScore} / 100
          </Chip>
          <Chip color="danger" size="lg" className="mr-2">
            <Icon icon="maki:cross" className="inline mr-2" />
            {assertionInfo?.againstEvidenceAggregateScore} / 100
          </Chip>
        </div>
      </div>
      <h2 className="text-2xl font-bold mb-4">Evidence</h2>
      <ul>
        {assertionEvidence?.map((contents_assertion, index) => (
          <li key={index}>
            <AssertionEvidence content={contents_assertion?.content} />
          </li>
        ))}
      </ul>
    </section>
  );
}

export const AssertionEvidence = ({ content }) => {
  return (
    <div>
      <Link href={`/papers/${content?.slug}`}><h3>{content?.title}</h3></Link>
    </div>
  )
}

