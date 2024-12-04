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
mutation UserRemoveContentMutation($contentId: String!) {
  userRemoveContent(contentId: $contentId) {
    message
    success
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