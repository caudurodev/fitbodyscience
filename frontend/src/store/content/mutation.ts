import { gql } from '@apollo/client'

export const ADD_VIDEO_MUTATION = gql`
  mutation UserAddContentMutation($contentType: String, $mediaType: String, $url: String!) {
    userAddContent(url: $url, mediaType: $mediaType, contentType: $contentType) {
      message
      slug
      success
    }
  }
`


export const RECALCULATE_AGGREGATE_SCORES_MUTATION = gql`
  mutation RecalculateAggregateScoreMutation($contentId: String!) {
    recalculateAggregateScore(contentId: $contentId) {
      success
    }
  }
`


export const USER_ANALYSE_CONTENT_MUTATION = gql`
  mutation UserAnalyseContentMutation($contentId: String!) {
    userAnalyseContent(contentId: $contentId) {
      message
      success
    }
  }
`


export const DELETE_CONTENT_MUTATION = gql`
mutation DeleteContentMutation($contentId: uuid!) {
  delete_content_activity(where: {contentId: {_eq: $contentId}}) {
    affected_rows
  }
  delete_influencer_contents(where: {contentId: {_eq: $contentId}}) {
    affected_rows
  }
  
  delete_assertions_content(where: {contentId: {_eq: $contentId}}) {
    affected_rows
  }
  delete_contents_assertion(where: {_or: [{contentId: {_eq: $contentId}}, {assertion: {contentId: {_eq: $contentId}}}]}) {
    affected_rows
  }
  delete_assertions(where: {_or: [{contentId: {_eq: $contentId}}, {citationContentId: {_eq: $contentId}}]}) {
    affected_rows
  }
  delete_content(where: {id: {_eq: $contentId}}) {
    affected_rows
  }
}
`

export const DELETE_RELATED_CONTENT_AND_RELATIONSHIPS_MUTATION = gql`
  mutation DeleteRelatedContentAndRelationshipsMutation($contentId: uuid!) {
    delete_content_relationship(where: {parentContentId: {_eq: $contentId}}) {
      affected_rows
    }
    delete_content(where: {content_relationships: {parentContentId: {_eq: $contentId}}}) {
      affected_rows
      returning {
        id
      }
    }
  }
`

export const CLASSIFY_CONTENT_MUTATION = gql`
  mutation UserClassifyEvidenceMutation($contentId: String!) {
    userClassifyEvidence(contentId: $contentId) {
      message
      success
    }
  }
`

export const USER_UPDATE_EVIDENCE_SCORE_MUTATION = gql`
mutation UserUpdateEvidenceScoreMutation($contentId: String!) {
  userUpdateEvidenceScore(contentId: $contentId) {
    message
    success
  }
}
`

export const USER_UPDATE_ASSERTIONS_SCORE_MUTATION = gql`
mutation UserUpdateAssertionsScoreMutation($contentId: String!) {
  updateAssertionsScore(contentId: $contentId) {
    message
    success
  }
}
`