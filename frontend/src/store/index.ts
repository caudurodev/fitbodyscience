
import { gql } from '@apollo/client'

export const GET_CONTENT_SUBSCRIPTION = gql`
  subscription GetContentTreeSubscription($contentSlug: String!, $influencerSlug: String!) {
    content(where: {slug: {_eq: $contentSlug}, influencer_contents: {influencer: {slug: {_eq: $influencerSlug}}}}) {
      id
      isParsed
      contentType
      title
      summary
      conclusion
      videoId
      contentScore
      proAggregateContentScore
      againstAggregateContentScore
      parent_content {
        child_content {
          title
          sourceUrl
          contentScore
          proAggregateContentScore
          againstAggregateContentScore
        }
      }
      assertions_contents(order_by: {weight_conclusion: desc}) {
        weight_conclusion
        why_relevant
        why_not_relevant
        is_pro_content
        video_timestamp
        assertion_context
        assertion {
          id
          text
          standalone_assertion_reliability
          citation_content_id
          evidence_type
          original_sentence
          assertion_search_verify
          pro_evidence_aggregate_score
          against_evidence_aggregate_score
          contents_assertions {
            is_citation_from_original_content
            is_pro_assertion
            why_relevant
            content {
              id
              title
              contentType
              sourceUrl
              contentScore
              doiNumber
              sciencePaperClassification
              proAggregateContentScore
              againstAggregateContentScore
            }
          }
        }
      }
    }
  }
`

export const GET_CONTENT_QUERY = gql`
  query GetContentQuery($contentSlug: String!, $influencerSlug: String!) {
    content(where: {slug: {_eq: $contentSlug}, influencer_contents: {influencer: {slug: {_eq: $influencerSlug}}}}) {
      id
      isParsed
      contentType
      title
      summary
      conclusion
      videoId
      contentScore
      proAggregateContentScore
      againstAggregateContentScore
      parent_content {
        child_content {
          title
          sourceUrl
          contentScore
          proAggregateContentScore
          againstAggregateContentScore
        }
      }
      assertions_contents(order_by: {weight_conclusion: desc}) {
        weight_conclusion
        why_relevant
        why_not_relevant
        is_pro_content
        video_timestamp
        assertion_context
        assertion {
          id
          text
          standalone_assertion_reliability
          citation_content_id
          evidence_type
          original_sentence
          assertion_search_verify
          pro_evidence_aggregate_score
          against_evidence_aggregate_score
          contents_assertions {
            is_citation_from_original_content
            is_pro_assertion
            why_relevant
            content {
              id
              title
              contentType
              sourceUrl
              contentScore
              doiNumber
              sciencePaperClassification
              proAggregateContentScore
              againstAggregateContentScore
            }
          }
        }
      }
    }
  }
`



export const GET_ALL_CONTENT_QUERY = gql`
  query GetAllContentQuery($mediaType: String!) {
    content(where: {media_type: {_eq: $mediaType}}) {
      id
      content_type
      title
      summary
      conclusion
      video_id
      pro_aggregate_content_score
      against_aggregate_content_score
    }
  }
`


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