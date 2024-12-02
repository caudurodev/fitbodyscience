import { gql } from '@apollo/client'

export const GET_ASSERTIONS_QUERY = gql`
query GetAssertionsQuery($search: String = "%%", $offset: Int = 0, $limit: Int = 10) {
  assertions(limit: $limit, offset: $offset, where: {_or: [{text: {_ilike: $search}}, {contentContext: {_ilike: $search}}]}) {
    id
    slug
    text
    contentContext
    proEvidenceAggregateScore
    againstEvidenceAggregateScore
  }
  assertions_aggregate(where: {_or: [{text: {_ilike: $search}}, {contentContext: {_ilike: $search}}]}) {
    aggregate {
      count
    }
  }
}
`