'use client'

export default function Terms() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-8">Terms &amp; Conditions</h1>
      <div className="bg-content1 rounded-large p-8 shadow-small">
        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-bold mb-4">Acceptance of Terms</h2>
            <p className="text-default-500">
              By accessing and using this platform, you accept and agree to be bound by these Terms and Conditions. 
              If you do not agree to these terms, please do not use our services.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">AI-Generated Content Disclaimer</h2>
            <p className="text-default-500">
              Our platform utilizes artificial intelligence to analyze and generate content about fitness influencers. 
              While we strive for accuracy, this content may contain errors or misinterpretations. Users should not 
              rely solely on this information for making health or fitness decisions.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Medical Advice Disclaimer</h2>
            <p className="text-default-500">
              The content provided on this platform is for informational purposes only and is not intended as medical 
              advice. Always consult with qualified healthcare professionals regarding any health-related decisions 
              or concerns.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">User Responsibilities</h2>
            <p className="text-default-500">
              Users are responsible for:
            </p>
            <ul className="list-disc list-inside mt-4 space-y-2 text-default-500">
              <li>Verifying information from multiple reliable sources</li>
              <li>Using the platform in compliance with applicable laws</li>
              <li>Maintaining the security of their account credentials</li>
              <li>Reporting any inaccuracies or issues they encounter</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Intellectual Property</h2>
            <p className="text-default-500">
              All content on this platform, including but not limited to text, graphics, logos, and AI-generated 
              analysis, is protected by intellectual property rights and may not be used without permission.
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}
