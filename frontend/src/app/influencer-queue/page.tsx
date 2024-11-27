'use client'

import {
  Card,
  CardBody,
  Button,
  Input,
  Spinner,
  Table,
  TableHeader,
  TableBody,
  TableColumn,
  TableRow,
  TableCell,
  useDisclosure
} from "@nextui-org/react"
import { useHydration } from '@/hooks/useHydration'
import { useQuery, useMutation } from '@apollo/client'
import { useUserData, useAuthenticationStatus } from '@nhost/nextjs'
import { useState } from 'react'
import { gql } from '@apollo/client'
import { Icon } from '@iconify/react'
import { useIsProUser } from '@/components/subscription/ProWarningModal'
import { StorageImage } from '@/components/assets/StorageImage'

const GET_INFLUENCERS_QUERY = gql`
  query GetInfluencers {
    followed: influencers(where: {isFollowed: {_eq: true}}) {
      id
      name
      ytUrl
      profileImg
      userRequestsToFollow
    }
    requested: influencers(
      where: {isFollowed: {_eq: false}}
      order_by: {userRequestsToFollow: desc}
    ) {
      id
      name
      ytUrl
      profileImg
      userRequestsToFollow
    }
  }
`

const INSERT_INFLUENCER_MUTATION = gql`
  mutation InsertInfluencer($ytUrl: String!) {
    insert_influencers_one(object: {
      ytUrl: $ytUrl,
      userRequestsToFollow: 1
    }) {
      id
      ytUrl
    }
  }
`

const UPDATE_REQUESTS_MUTATION = gql`
  mutation UpdateRequests($id: uuid!) {
    update_influencers_by_pk(
      pk_columns: {id: $id},
      _inc: {userRequestsToFollow: 1}
    ) {
      id
      userRequestsToFollow
    }
  }
`

export default function InfluencerQueue() {
  const { isAuthenticated, isLoading: isLoadingAuth } = useAuthenticationStatus()
  const userData = useUserData()
  const isPro = useIsProUser()
  const [ytUrl, setYtUrl] = useState('')
  const { data, loading } = useQuery(GET_INFLUENCERS_QUERY, {
    fetchPolicy: 'cache-and-network'
  })
  const [insertInfluencer] = useMutation(INSERT_INFLUENCER_MUTATION, {
    refetchQueries: [{ query: GET_INFLUENCERS_QUERY }]
  })
  const [updateRequests] = useMutation(UPDATE_REQUESTS_MUTATION, {
    refetchQueries: [{ query: GET_INFLUENCERS_QUERY }]
  })
  const isHydrated = useHydration()

  if (!isHydrated) return null
  if (isLoadingAuth) {
    return (
      <div className="flex justify-center py-12">
        <Spinner size="lg" />
      </div>
    )
  }
  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
        <h2 className="text-2xl font-bold">Please Login</h2>
        <p className="text-default-500">You need to be logged in to suggest influencers.</p>
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await insertInfluencer({
        variables: { ytUrl }
      })
      setYtUrl('')
    } catch (error) {
      console.error('Error submitting influencer:', error)
    }
  }

  const handleVote = async (id: string) => {
    try {
      await updateRequests({
        variables: { id }
      })
    } catch (error) {
      console.error('Error updating votes:', error)
    }
  }

  const renderTable = (influencers: any[], title: string) => (
    <Card className="my-4">
      <CardBody>
        <h3 className="text-xl font-bold mb-4">{title}</h3>
        <Table aria-label={title}>
          <TableHeader>
            <TableColumn>INFLUENCER</TableColumn>
            <TableColumn>CHANNEL</TableColumn>
            <TableColumn>REQUESTS</TableColumn>
            <TableColumn>ACTIONS</TableColumn>
          </TableHeader>
          <TableBody>
            {influencers?.map((influencer) => (
              <TableRow key={influencer.id}>
                <TableCell className="flex items-center gap-2">
                  {influencer.profileImg && (
                    <div className="w-10 h-10 rounded-full overflow-hidden">
                      <StorageImage fileId={influencer.profileImg} />
                    </div>
                  )}
                  {influencer.name || 'Unnamed Channel'}
                </TableCell>
                <TableCell>
                  <a href={influencer.ytUrl} target="_blank" rel="noopener noreferrer" className="text-primary">
                    View Channel
                  </a>
                </TableCell>
                <TableCell>{influencer.userRequestsToFollow}</TableCell>
                <TableCell>
                  {!influencer.isFollowed && (
                    <Button
                      size="sm"
                      color="primary"
                      variant="flat"
                      onClick={() => handleVote(influencer.id)}
                      startContent={<Icon icon="mdi:thumb-up" />}
                    >
                      Vote
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardBody>
    </Card>
  )

  return (
    <>
      <section className="mb-24">
        <div className="space-y-4">
          <p className="text-primary font-medium">Suggest Influencers</p>
          <h1 className="text-6xl font-bold tracking-tight">
            Add new <span className="text-gradient">Influencers</span><br />
            for analysis
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            Help us grow our database by suggesting fitness influencers for analysis.
            {!isPro && " Pro users get priority processing of their suggestions."}
          </p>
        </div>
      </section>

      {/* Suggestion Form */}
      <section className="mb-12">
        <Card className="max-w-2xl">
          <CardBody>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="YouTube Channel or Video URL"
                placeholder="Enter YouTube URL"
                value={ytUrl}
                onChange={(e) => setYtUrl(e.target.value)}
                required
                variant="bordered"
                startContent={
                  <Icon icon="mdi:youtube" className="text-2xl text-default-400" />
                }
              />
              <Button
                color="primary"
                type="submit"
                className="w-full"
                startContent={<Icon icon="mdi:plus" />}
              >
                Submit Suggestion
              </Button>
            </form>
          </CardBody>
        </Card>
      </section>

      {/* Influencers Tables */}
      <section className="mb-24">
        <h2 className="text-gradient text-2xl font-bold uppercase py-2">Current Influencers</h2>
        {loading ? (
          <div className="flex justify-center py-12">
            <Spinner size="lg" />
          </div>
        ) : (
          <>
            {renderTable(data?.followed, 'Currently Following')}
            {renderTable(data?.requested, 'Requested Influencers')}
          </>
        )}
      </section>
    </>
  )
}
