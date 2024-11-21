import { gql } from '@apollo/client'

export const USER_SEARCH_MORE_EVIDENCE_MUTATION = gql`
mutation UserSearchMoreEvidenceMutation($assertionId: String!) {
  userSearchMoreEvidence(assertionId: $assertionId) {
    message
    success
  }
}
`
