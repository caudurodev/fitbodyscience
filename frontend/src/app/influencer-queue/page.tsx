'use client'

import { 
  Card, 
  CardBody, 
  CardHeader, 
  Button, 
  Chip,
  Input,
  Textarea,
  Spinner
} from "@nextui-org/react"
import { useHydration } from '@/hooks/useHydration'
import { useQuery, useMutation } from '@apollo/client'
import { useAuth } from '@nhost/nextjs'
import { useState } from 'react'
import { gql } from '@apollo/client'
import { Icon } from '@iconify/react'

const GET_SUGGESTIONS_QUERY = gql`
  query GetSuggestions {
    influencer_suggestions(order_by: {created_at: desc}) {
      id
      youtube_channel_id
      channel_name
      status
      subscriber_count
      channel_description
      thumbnail_url
      created_at
      suggested_by_user {
        displayName
      }
    }
  }
`

const INSERT_SUGGESTION_MUTATION = gql`
  mutation InsertSuggestion($youtube_channel_id: String!, $channel_name: String!, $channel_description: String) {
    insert_influencer_suggestions_one(object: {
      youtube_channel_id: $youtube_channel_id,
      channel_name: $channel_name,
      channel_description: $channel_description
    }) {
      id
    }
  }
`

const UPDATE_SUGGESTION_STATUS = gql`
  mutation UpdateSuggestionStatus($id: uuid!, $status: String!, $processed_by_user_id: uuid!) {
    update_influencer_suggestions_by_pk(
      pk_columns: {id: $id}, 
      _set: {
        status: $status,
        processed_at: "now()",
        processed_by_user_id: $processed_by_user_id
      }
    ) {
      id
      status
    }
  }
`

export default function InfluencerQueue() {
  const { isAuthenticated, isAdmin, user } = useAuth()
  const [newChannel, setNewChannel] = useState({ id: '', name: '', description: '' })
  const { data, loading } = useQuery(GET_SUGGESTIONS_QUERY)
  const [insertSuggestion] = useMutation(INSERT_SUGGESTION_MUTATION, {
    refetchQueries: [{ query: GET_SUGGESTIONS_QUERY }]
  })
  const [updateStatus] = useMutation(UPDATE_SUGGESTION_STATUS, {
    refetchQueries: [{ query: GET_SUGGESTIONS_QUERY }]
  })
  const isHydrated = useHydration()

  if (!isHydrated) return null
  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
        <h2 className="text-2xl font-bold">Please Login</h2>
        <p className="text-default-500">You need to be logged in to view and suggest influencers.</p>
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await insertSuggestion({
        variables: {
          youtube_channel_id: newChannel.id,
          channel_name: newChannel.name,
          channel_description: newChannel.description
        }
      })
      setNewChannel({ id: '', name: '', description: '' })
    } catch (error) {
      console.error('Error submitting suggestion:', error)
    }
  }

  const handleStatusUpdate = async (id: string, newStatus: 'approved' | 'rejected') => {
    try {
      await updateStatus({
        variables: {
          id,
          status: newStatus,
          processed_by_user_id: user?.id
        }
      })
    } catch (error) {
      console.error('Error updating status:', error)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'success'
      case 'rejected': return 'danger'
      default: return 'warning'
    }
  }

  return (
    <>
      <section className="mb-24">
        <div className="space-y-4">
          <p className="text-primary font-medium">Influencer Queue</p>
          <h1 className="text-6xl font-bold tracking-tight">
            Suggest new <span className="text-gradient">Influencers</span><br />
            for analysis
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            Help us grow our database by suggesting fitness influencers for analysis.
            {!isAdmin && " Pro users get priority processing of their suggestions."}
          </p>
        </div>
      </section>

      {/* Suggestion Form */}
      <section className="mb-12">
        <Card className="max-w-2xl">
          <CardBody className="gap-4">
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="YouTube Channel ID"
                placeholder="Enter channel ID"
                value={newChannel.id}
                onChange={(e) => setNewChannel(prev => ({ ...prev, id: e.target.value }))}
                required
                variant="bordered"
                startContent={
                  <Icon icon="mdi:youtube" className="text-2xl text-default-400" />
                }
              />
              <Input
                label="Channel Name"
                placeholder="Enter channel name"
                value={newChannel.name}
                onChange={(e) => setNewChannel(prev => ({ ...prev, name: e.target.value }))}
                required
                variant="bordered"
                startContent={
                  <Icon icon="mdi:account" className="text-2xl text-default-400" />
                }
              />
              <Textarea
                label="Channel Description"
                placeholder="Enter channel description"
                value={newChannel.description}
                onChange={(e) => setNewChannel(prev => ({ ...prev, description: e.target.value }))}
                variant="bordered"
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

      {/* Queue List */}
      <section className="mb-24">
        <h2 className="text-gradient text-2xl font-bold uppercase py-2">Suggestion Queue</h2>
        {loading ? (
          <div className="flex justify-center py-12">
            <Spinner size="lg" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data?.influencer_suggestions.map((suggestion: any) => (
              <Card key={suggestion.id} className="bg-default-50 dark:bg-default-100">
                <CardHeader className="flex justify-between">
                  <div>
                    <h3 className="text-lg font-semibold">{suggestion.channel_name}</h3>
                    <p className="text-small text-default-500">
                      by {suggestion.suggested_by_user.displayName}
                    </p>
                  </div>
                  <Chip 
                    color={getStatusColor(suggestion.status)}
                    variant="flat"
                    startContent={
                      suggestion.status === 'pending' ? 
                        <Icon icon="mdi:clock-outline" /> :
                      suggestion.status === 'approved' ?
                        <Icon icon="mdi:check" /> :
                        <Icon icon="mdi:close" />
                    }
                  >
                    {suggestion.status}
                  </Chip>
                </CardHeader>
                <CardBody>
                  <p className="text-small text-default-500">
                    {suggestion.channel_description || 'No description provided'}
                  </p>
                  {isAdmin && suggestion.status === 'pending' && (
                    <div className="flex gap-2 mt-4">
                      <Button 
                        color="success" 
                        size="sm"
                        onClick={() => handleStatusUpdate(suggestion.id, 'approved')}
                        startContent={<Icon icon="mdi:check" />}
                      >
                        Approve
                      </Button>
                      <Button 
                        color="danger" 
                        size="sm"
                        onClick={() => handleStatusUpdate(suggestion.id, 'rejected')}
                        startContent={<Icon icon="mdi:close" />}
                      >
                        Reject
                      </Button>
                    </div>
                  )}
                </CardBody>
              </Card>
            ))}
          </div>
        )}
      </section>
    </>
  )
}
