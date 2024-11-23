import { gql } from '@apollo/client'

export const GET_CONTENT_ACTIVITY_SUBSCRIPTION = gql`
  subscription GetContentActivitySubscription($contentId: uuid!) {
    content_activity(
      where: {contentId: {_eq: $contentId}}
      order_by: {createdAt: desc}
    ) {
      id
      createdAt
      description
      expiresAt
      name
      type
      contentId
    }
  }
`
