
import { gql } from '@apollo/client'

export const GET_INFLUENCERS_QUERY = gql`
  query GetInfluencersQuery {
    influencers {
      name
      slug
      profileImg
      ytChannelInfoJsonb
      ytDescription
      ytLastUpdated
      ytUrl
      influencer_contents_aggregate{
        aggregate{
          count
        }
      }
    }
    influencers_aggregate {
      aggregate {
        count
      }
    }
  }
`
