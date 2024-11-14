
import { gql } from '@apollo/client'

export const GET_INFLUENCERS_QUERY = gql`
query GetInfluencersQuery {
  influencers {
    name
    profileImg
    ytChannelInfoJsonb
    ytDescription
    ytLastUpdated
    ytUrl
  }
  influencers_aggregate {
    aggregate {
      count
    }
  }
}
`
