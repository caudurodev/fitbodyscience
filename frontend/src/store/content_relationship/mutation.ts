import { gql } from '@apollo/client'

export const DELETE_CONTENT_RELATIONSHIP_MUTATION = gql`
mutation DeleteChildContentRelationshipMutation($childContentId: uuid!, $_eq: uuid = "") {
  delete_content_relationship(where: {childContentId: {_eq: $childContentId}}) {
    affected_rows
    returning {
      id
    }
  }
  delete_contents_assertion(where: {contentId: {_eq: $childContentId}}) {
    affected_rows
    returning {
      id
    }
  }
}


`

