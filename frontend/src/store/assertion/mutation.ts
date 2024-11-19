import { gql } from '@apollo/client'

export const USER_UPDATE_ASSERTION_SCORE_MUTATION = gql`
mutation UserUpdateAssertionScoreMutation($assertionId: String!) {
  userUpdateAssertionScore(assertionId: $assertionId) {
    message
    success
  }
}

`
