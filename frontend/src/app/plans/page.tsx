'use client'

import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  Divider,
  Chip,
} from "@nextui-org/react"
import { Icon } from '@iconify/react'
import Link from 'next/link'

const features = {
  free: [
    "Unlimited access to all fact-checks",
    "Weekly science newsletter",
    "Basic influencer credibility scores",
    "View all scientific breakdowns",
    "Suggest new influencers to analyze",
  ],
  pro: [
    "Everything in Free, plus:",
    "☕️ Support financially the project",
    "⚡️ Jump the research queue",
    "🔍 Request specific video fact-checks",
    "⭐️ Priority influencer analysis",
    "🧪 Advanced study parsing",
  ]
}

export default function PlansPage() {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <section className="mb-24">
          <div className="space-y-4 text-center">
            <p className="text-primary font-medium">Simple Pricing</p>
            <h1 className="text-6xl font-bold tracking-tight">
              Get the <span className="text-gradient">Truth</span><br />
              Behind Fitness Claims
            </h1>
            <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl mx-auto">
              Your <span className="text-secondary">AI-powered</span>{' '}
              fact-checking assistant for fitness content. Browse unlimited fact-checks and get weekly insights,
              or go Pro to request custom analysis of your favorite influencers.
            </p>
          </div>
        </section>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Free Tier */}
          <Card className="border-none bg-default-50 dark:bg-default-100">
            <CardHeader className="flex flex-col gap-2 p-6">
              <h2 className="text-2xl font-bold">Free Forever</h2>
              <p className="text-default-500">No credit card needed</p>
              <div className="mt-4">
                <span className="text-3xl font-bold">Free</span>
                <span className="text-default-500"> forever</span>
              </div>
            </CardHeader>
            <Divider />
            <CardBody className="gap-4 p-6">
              {features.free.map((feature, index) => (
                <div key={index} className="flex items-center gap-2">
                  <Icon icon="ph:check-circle" className="text-success text-xl" />
                  <span className="text-default-600">
                    {feature === "Suggest new influencers to analyze" ? (
                      <Link href="/influencer-queue" className="text-primary hover:underline">
                        {feature}
                      </Link>
                    ) : feature}
                  </span>
                </div>
              ))}
            </CardBody>
            <CardFooter className="p-6">
              <Button
                className="w-full bg-default-200 hover:bg-default-300"
                size="lg"
              >
                Start Free
              </Button>
            </CardFooter>
          </Card>

          {/* Pro Tier */}
          <Card className="border-none bg-default-50 dark:bg-default-100 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-tr from-pink-500/10 to-yellow-500/10" />
            <CardHeader className="flex flex-col gap-2 p-6 relative">
              <div className="flex items-center gap-2">
                <h2 className="text-2xl font-bold">Pro Credits</h2>
                <Chip
                  className="bg-gradient-to-tr from-pink-500 to-yellow-500 text-white"
                  size="sm"
                >
                  PAY AS YOU GO
                </Chip>
              </div>
              <p className="text-default-500">No subscription, just credits</p>
              <div className="mt-4">
                <span className="text-3xl font-bold">€5</span>
                <span className="text-default-500">/100 credits</span>
              </div>
            </CardHeader>
            <Divider />
            <CardBody className="gap-4 p-6 relative">
              <p className="text-default-500 mb-4">
                Buy credits only when you need them. No subscription, no expiry, no hidden costs.
              </p>
              {features.pro.map((feature, index) => (
                <div key={index} className="flex items-center gap-2">
                  <Icon icon="ph:check-circle-fill" className="text-pink-500 text-xl" />
                  <span className="text-default-600">{feature}</span>
                </div>
              ))}
            </CardBody>
            <CardFooter className="p-6 relative">
              <Button
                className="w-full bg-gradient-to-tr from-pink-500 to-yellow-500 text-white font-semibold shadow-lg"
                size="lg"
              >
                Get Credits
              </Button>
            </CardFooter>
          </Card>
        </div>

        <div className="mt-16 text-center">
          <h3 className="text-2xl font-bold mb-4">
            Credit Usage Guide
          </h3>
          <p className="text-default-500 mb-8 max-w-2xl mx-auto">
            Buy credits only when you need them. Each €5 pack includes 100 credits - use them anytime:
          </p>
          <div className="overflow-x-auto">
            <table className="mx-auto max-w-3xl w-full bg-default-50 dark:bg-default-100 rounded-lg overflow-hidden">
              <thead className="bg-default-200 dark:bg-default-50">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Action</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Credits</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-default-200 dark:divide-default-50">
                <tr>
                  <td className="px-6 py-4">AI Evidence Search</td>
                  <td className="px-6 py-4">1</td>
                  <td className="px-6 py-4 text-default-500">Use AI to search for more supporting or opposing evidence</td>
                </tr>
                <tr>
                  <td className="px-6 py-4">Study Analysis</td>
                  <td className="px-6 py-4">5</td>
                  <td className="px-6 py-4 text-default-500">Access to detailed study analysis</td>
                </tr>
                <tr>
                  <td className="px-6 py-4">Single Video</td>
                  <td className="px-6 py-4">10</td>
                  <td className="px-6 py-4 text-default-500">Fact-check claims in a specific video</td>
                </tr>
                <tr>
                  <td className="px-6 py-4">Add Channel</td>
                  <td className="px-6 py-4">100</td>
                  <td className="px-6 py-4 text-default-500">Add to our list of followed channels</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="text-default-500 mt-4 text-sm">
            Credits never expire. Buy them once, use them anytime.
          </p>
        </div>

        <div className="mt-16 text-center">
          <h3 className="text-2xl font-bold mb-4">
            Frequently Asked Questions
          </h3>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto mt-8 text-left">
            <div className="bg-default-50 dark:bg-default-100 p-6 rounded-lg">
              <h4 className="text-lg font-semibold mb-2">
                Are there any subscriptions?
              </h4>
              <p className="text-default-500">
                No! We don&apos;t believe in subscriptions. Just buy credits when you need them and use them anytime.
                The free tier is always free, and Pro credits never expire.
              </p>
            </div>
            <div className="bg-default-50 dark:bg-default-100 p-6 rounded-lg">
              <h4 className="text-lg font-semibold mb-2">
                Can I suggest new influencers as a free user?
              </h4>
              <p className="text-default-500">
                Yes! Free users can suggest influencers to be analyzed, and we&apos;ll add them to our research queue.
                Pro users can jump the queue and get priority analysis of their requested influencers.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
