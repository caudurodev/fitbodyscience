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
  delete_influencer_contents(where: {contentId: {_eq: $contentId}}) {
    affected_rows
  }
  delete_content_relationship(where: {_or: [{childContentId: {_eq: $contentId}}, {parentContentId: {_eq: $contentId}}]}) {
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

export const CLASSIFY_CONTENT_MUTATION = gql`
  mutation ClassifyContentMutation($contentId: String!) {
    classifyContent(contentId: $contentId) {
      message
      success
    }
  }
`
