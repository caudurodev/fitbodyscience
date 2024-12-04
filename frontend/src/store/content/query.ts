import { gql } from '@apollo/client'


export const GET_CONTENT_SUBSCRIPTION = gql`
  subscription GetContentTreeSubscription($contentSlug: String!, $influencerSlug: String!) {
    content(where: {slug: {_eq: $contentSlug}, influencer_contents: {influencer: {slug: {_eq: $influencerSlug}}}}) {
      id
      isParsed
      contentType
      title
      summary
      summaryJsonb
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
      influencer_contents{
        influencer{
          name
          slug
        }
      }  
      assertions_contents(order_by: {weightConclusion: desc}) {
        weightConclusion
        whyRelevant
        whyNotRelevant
        isProContent
        videoTimestamp
        assertionContext
        assertion {
          id
          text
          slug
          standaloneAssertionReliability
          citationContentId
          evidenceType
          originalSentence
          assertionSearchVerify
          proEvidenceAggregateScore
          againstEvidenceAggregateScore
          contents_assertions {
            isCitationFromOriginalContent
            isProAssertion
            whyRelevant
            content {
              id
              title
              contentType
              sourceUrl
              videoId
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
      summaryJsonb
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
      influencer_contents{
        influencer{
          name
          slug
        }
      }  
      assertions_contents(order_by: {weightConclusion: desc}) {
        weightConclusion
        whyRelevant
        whyNotRelevant
        isProContent
        videoTimestamp
        assertionContext
        assertion {
          id
          text
          slug
          standaloneAssertionReliability
          citationContentId
          evidenceType
          originalSentence
          assertionSearchVerify
          proEvidenceAggregateScore
          againstEvidenceAggregateScore
          contents_assertions {
            isCitationFromOriginalContent
            isProAssertion
            whyRelevant
            content {
              id
              title
              contentType
              videoId
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


export const GET_INFLUENCER_CONTENT_QUERY = gql`
query GetInfluencerContentQuery($influencerSlug: String! ) {
  influencers(where: {slug: {_eq: $influencerSlug}}) {
    ytLastUpdated
    ytUrl
    profileImg
    name
    influencer_contents {
      content {
        id
        slug
        videoId
        title
        dateAdded
        contentType
        proAggregateContentScore
        againstAggregateContentScore
        influencer_contents{
        influencer{
          slug
        }
      }
      }
    }
  }
}
`


export const GET_ALL_CONTENT_QUERY = gql`
  query GetAllContentQuery($mediaType: String!) {
    content(where: {mediaType: {_eq: $mediaType}}) {
      id
      contentType
      title
      summary
      conclusion
      videoId
      proAggregateContentScore
      againstAggregateContentScore
      slug
      influencer_contents{
        influencer{
          slug
        }
      }
    }
  }
`



export const SEARCH_SCIENCE_PAPERS_QUERY = gql`
query SearchSciencePapersQuery($search: String = "%%", $offset: Int = 0, $limit: Int = 10) {
  content(limit: $limit, offset: $offset, where: {_or: [{title: {_ilike: $search}}, {contentType: {_eq: "scientific_paper"}}]}) {
    id
    title
    doiNumber
    slug
    contentScore
    sciencePaperClassification
  }
  content_aggregate(where: {_or: [{title: {_ilike: $search}}, {contentType: {_eq: "scientific_paper"}}]}) {
    aggregate {
      count
    }
  }
}
  `


export const GET_PAPER_FROM_SLUG_QUERY = gql`
query GetPaperFromSlugQuery($paperSlug: String!) {
  content(where: {slug: {_eq: $paperSlug}, contentType: {_eq: "scientific_paper"}}) {
    id
    title
    doiNumber
    slug
    contentScore
    sciencePaperClassification
    contents_assertions {
      assertion {
        text
        slug
      }
    }
  }
}
  `