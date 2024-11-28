'use client'

export default function FAQ() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-8">Frequently Asked Questions</h1>
      <div className="bg-content1 rounded-large p-8 shadow-small">
        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-bold mb-4">About Our Platform</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">What is FitBody Science?</h3>
                <p className="text-default-500">
                  FitBody Science is an AI-powered platform that analyzes fitness influencer content to provide scientific insights 
                  and fact-checking. We help users make informed decisions about fitness advice and trends.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">How accurate is the AI analysis?</h3>
                <p className="text-default-500">
                  Our AI system is trained on peer-reviewed scientific literature and expert knowledge. While we strive for high 
                  accuracy, we recommend using our insights as a starting point and consulting with qualified professionals for 
                  personalized advice.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Using the Platform</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">How do I get started?</h3>
                <p className="text-default-500">
                  Simply create an account and start exploring fitness content. You can search for specific influencers, topics, 
                  or browse through our curated collections of analyzed content.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Is the platform free to use?</h3>
                <p className="text-default-500">
                  We offer both free and premium tiers. The free tier gives you access to basic analysis features, while our 
                  premium subscription unlocks advanced insights and detailed scientific breakdowns.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Technical Questions</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">Which browsers are supported?</h3>
                <p className="text-default-500">
                  Our platform works best with modern browsers like Chrome, Firefox, Safari, and Edge. Make sure to keep your 
                  browser updated for the best experience.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Is my data secure?</h3>
                <p className="text-default-500">
                  Yes, we use industry-standard encryption and security measures to protect your data. You can learn more about 
                  our security practices in our Privacy Policy.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Account Management</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">How do I update my account settings?</h3>
                <p className="text-default-500">
                  You can manage your account settings, including notification preferences and subscription details, from your 
                  account dashboard. Look for the settings icon in the top navigation bar.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Can I delete my account?</h3>
                <p className="text-default-500">
                  Yes, you can delete your account at any time from the account settings page. Please note that this action is 
                  permanent and will remove all your saved data and preferences.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Still Have Questions?</h2>
            <p className="text-default-500">
              If you couldn&apos;t find the answer you&apos;re looking for, please visit our <a href="/contact" className="text-primary">Contact page</a> to 
              reach out to our support team. We&apos;re here to help!
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}
