import { gql } from '@apollo/client'

/**
 * GetAssertionsQuery
 *
 * Searches for assertions by text or content context and paginates the results.
 *
 * Args:
 *   $search: The search term to query. Defaults to "%%" which matches all assertions.
 *   $offset: The offset of the results. Defaults to 0.
 *   $limit: The limit of the results. Defaults to 10.
 *
 * Returns:
 *   An object with two properties:
 *     - assertions: An array of assertions that match the search criteria.
 *       Each assertion has the following properties:
 *         - id: The id of the assertion.
 *         - slug: The slug of the assertion.
 *         - text: The text of the assertion.
 *         - contentContext: The context of the assertion (e.g. what the assertion is about).
 *         - proEvidenceAggregateScore: The aggregated score of pro evidence of the assertion.
 *         - againstEvidenceAggregateScore: The aggregated score of against evidence of the assertion.
 *     - assertions_aggregate: The total count of assertions that match the search criteria.
 */
export const GET_ASSERTIONS_QUERY = gql`
query GetAssertionsQuery($search: String = "%%", $offset: Int = 0, $limit: Int = 10) {
  assertions(limit: $limit, offset: $offset, where: {_or: [{text: {_ilike: $search}}, {contentContext: {_ilike: $search}}]}) {
    id
    slug
    text
    contentContext
    proEvidenceAggregateScore
    againstEvidenceAggregateScore
  }
  assertions_aggregate(where: {_or: [{text: {_ilike: $search}}, {contentContext: {_ilike: $search}}]}) {
    aggregate {
      count
    }
  }
}
`

export const GET_ASSERTION_FROM_SLUG_QUERY = gql`
query GetAssertionFromSlugQuery($assertionSlug: String!) {
  assertions(where: {slug: {_eq: $assertionSlug}}) {
    id
    slug
    text
    proEvidenceAggregateScore
    againstEvidenceAggregateScore
    contents_assertions {
      content {
        slug
        title
        contentScore
        sciencePaperClassification
      }
    }
    assertions_contents {
      content {
        title
        mediaType
        slug
        influencer_contents {
          influencer {
            slug
          }
        }
      }
    }
  }
}

`
