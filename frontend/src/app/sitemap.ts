import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://fitbodyscience.com'

  // Define base routes
  const routes = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 1,
    },
    {
      url: `${baseUrl}/creators`,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/assertions`,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/studies`,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/faq`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.5,
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.3,
    },
    {
      url: `${baseUrl}/terms`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.3,
    },
    {
      url: `${baseUrl}/privacy-policy`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.3,
    },
  ]

  const dynamicRoutes: MetadataRoute.Sitemap = []

  // Fetch dynamic creator pages
  try {
    console.log('Fetching creators for sitemap...')
    const creatorQuery = `
      query GetInfluencersQuery {
        influencers {
          slug
          updated_at
        }
      }
    `

    const graphqlUrl = process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT
    console.log('GraphQL URL:', graphqlUrl)

    if (!graphqlUrl) {
      throw new Error('NEXT_PUBLIC_GRAPHQL_ENDPOINT is not defined')
    }

    const response = await fetch(graphqlUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: creatorQuery }),
      cache: 'no-store'
    })

    if (!response.ok) {
      const text = await response.text()
      console.error('GraphQL response not OK:', response.status, response.statusText)
      console.error('Response text:', text)
      throw new Error(`GraphQL request failed: ${response.status} ${response.statusText}`)
    }

    const responseData = await response.json()
    console.log('GraphQL response:', JSON.stringify(responseData, null, 2))

    const { data } = responseData
    if (!data?.influencers) {
      console.error('No influencers data in response:', responseData)
      throw new Error('No influencers data in response')
    }

    const creatorRoutes = data.influencers.map((creator: any) => ({
      url: `${baseUrl}/creators/${creator.slug}`,
      lastModified: creator.updated_at ? new Date(creator.updated_at) : new Date(),
      changeFrequency: 'daily' as const,
      priority: 0.8,
    }))

    console.log('Generated creator routes:', creatorRoutes)
    dynamicRoutes.push(...creatorRoutes)
  } catch (error) {
    console.error('Error fetching creators for sitemap:', error)
    if (error instanceof Error) {
      console.error('Error details:', error.message)
      console.error('Error stack:', error.stack)
    }
  }

  // Fetch dynamic video content pages
  try {
    console.log('Fetching video content pages for sitemap...')
    const query = `
      query sitemapQuery {
        content(where: {slug: {_is_null: false}}) {
          slug
          influencer_contents {
            influencer {
              slug
            }
          }
        }
      }
    `

    const graphqlUrl = process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT
    console.log('GraphQL URL:', graphqlUrl)

    if (!graphqlUrl) {
      throw new Error('NEXT_PUBLIC_GRAPHQL_ENDPOINT is not defined')
    }

    const response = await fetch(graphqlUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
      cache: 'no-store'
    })

    if (!response.ok) {
      console.error('GraphQL response not OK:', response.status, response.statusText)
      const text = await response.text()
      console.error('Response text:', text)
      throw new Error(`GraphQL request failed: ${response.status} ${response.statusText}`)
    }

    const responseData = await response.json()
    console.log('GraphQL response:', JSON.stringify(responseData, null, 2))

    const { data } = responseData
    if (!data || !data.content) {
      console.error('No content data in response:', responseData)
      throw new Error('No content data in response')
    }

    const videoRoutes = data.content.flatMap((content: any) =>
      content.influencer_contents.map((ic: any) => ({
        url: `${baseUrl}/video/${ic.influencer.slug}/${content.slug}`,
        lastModified: new Date(),
        changeFrequency: 'weekly' as const,
        priority: 0.9,
      }))
    )

    const creatorRoutes = data.content.flatMap((content: any) => ({
      url: `${baseUrl}/creators/${content.influencer_contents[0].influencer.slug}`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.9,
    }))

    console.log('Generated video routes:', videoRoutes)
    dynamicRoutes.push(...videoRoutes)
    dynamicRoutes.push(...creatorRoutes)
  } catch (error) {
    console.error('Error fetching content for sitemap:', error)
    if (error instanceof Error) {
      console.error('Error details:', error.message)
      console.error('Error stack:', error.stack)
    }
  }

  // Fetch assertions pages
  try {
    console.log('Fetching assertions for sitemap...')
    const assertionsQuery = `
      query GetAssertionsQuery {
        assertions {
          slug
          updated_at
        }
      }
    `

    const response = await fetch(process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT!, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: assertionsQuery }),
      cache: 'no-store'
    })

    if (!response.ok) {
      throw new Error(`GraphQL request failed: ${response.status} ${response.statusText}`)
    }

    const { data } = await response.json()
    if (data?.assertions) {
      const assertionRoutes = data.assertions.map((assertion: any) => ({
        url: `${baseUrl}/assertions/${assertion.slug}`,
        lastModified: assertion.updated_at ? new Date(assertion.updated_at) : new Date(),
        changeFrequency: 'daily' as const,
        priority: 0.9,
      }))
      console.log('Generated assertion routes:', assertionRoutes)
      dynamicRoutes.push(...assertionRoutes)
    }
  } catch (error) {
    console.error('Error fetching assertions for sitemap:', error)
  }

  // Fetch studies pages
  try {
    console.log('Fetching studies for sitemap...')
    const studiesQuery = `
      query GetStudiesQuery {
        content(where: {contentType: {_eq: "scientific_paper"}}) {
          slug
          updated_at
        }
      }
    `

    const response = await fetch(process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT!, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: studiesQuery }),
      cache: 'no-store'
    })

    if (!response.ok) {
      throw new Error(`GraphQL request failed: ${response.status} ${response.statusText}`)
    }

    const { data } = await response.json()
    if (data?.content) {
      const studyRoutes = data.content.map((study: any) => ({
        url: `${baseUrl}/studies/${study.slug}`,
        lastModified: study.updated_at ? new Date(study.updated_at) : new Date(),
        changeFrequency: 'weekly' as const,
        priority: 0.8,
      }))
      console.log('Generated study routes:', studyRoutes)
      dynamicRoutes.push(...studyRoutes)
    }
  } catch (error) {
    console.error('Error fetching studies for sitemap:', error)
  }

  const allRoutes = [...routes, ...dynamicRoutes]
  console.log('All routes in sitemap:', allRoutes)

  return allRoutes
}
