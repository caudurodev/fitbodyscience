import { gql } from '@apollo/client'

export const USER_SEARCH_MORE_EVIDENCE_MUTATION = gql`
mutation UserSearchMoreEvidenceMutation($assertionId: String!) {
  userSearchMoreEvidence(assertionId: $assertionId) {
    message
    success
  }
}
`


export const USER_APPEND_EVIDENCE_TO_ASSERTION_MUTATION = gql`
mutation UserAppendEvidenceToAssertionMutation($contentUrl: String!, $assertionId: String!) {
  userAppendEvidenceToAssertion(assertionId: $assertionId, contentUrl: $contentUrl) {
    message
    success
  }
}

`
