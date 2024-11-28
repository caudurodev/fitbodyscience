import { gql } from '@apollo/client'

export const DELETE_USER_ACCOUNT_AND_CONTENT_MUTATION = gql`
  mutation DeleteUserAccountAndContent($userId: uuid!) {
    deleteUser(id: $userId) {
      id
    }
  }
`
