import { gql } from '@apollo/client'

export const GET_INFLUENCERS_QUERY = gql`
  query GetInfluencersQuery($search: String, $offset: Int, $limit: Int) {
    influencers(
      where: {
        _or: [
          { name: { _ilike: $search } },
          { ytDescription: { _ilike: $search } }
        ]
      }
      limit: $limit
      offset: $offset
      order_by: { name: asc }
    ) {
      id
      name
      slug
      profileImg
      ytChannelInfoJsonb
      ytDescription
      ytLastUpdated
      ytUrl
      isFollowed
      userRequestsToFollow
      influencer_contents_aggregate{
        aggregate{
          count
        }
      }
    }
    influencers_aggregate(
      where: {
        _or: [
          { name: { _ilike: $search } },
          { ytDescription: { _ilike: $search } }
        ]
      }
    ) {
      aggregate {
        count
      }
    }
  }
`
