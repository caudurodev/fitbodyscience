'use client'

export default function PrivacyPolicy() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
      <div className="">
        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-bold mb-4">Information Collection and Use</h2>
            <p className="text-default-500">
              We collect information to provide better services to our users. This includes:
            </p>
            <ul className="list-disc list-inside mt-4 space-y-2 text-default-500">
              <li>Basic account information (email, name)</li>
              <li>Usage data and preferences</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Cookies and Tracking</h2>
            <p className="text-default-500">
              We use cookies and similar tracking technologies to improve your experience on our platform. These help us
              understand how you interact with our services and allow us to remember your preferences.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Third-Party Services</h2>
            <p className="text-default-500">
              We may use third-party services to help us operate our platform. These services may collect and process
              information as required for their functionality. All third-party providers are carefully selected and required
              to maintain high privacy standards.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Your Rights</h2>
            <p className="text-default-500">
              You have the right to access, correct, or delete your personal information. You can also request a copy of
              your data or ask us to restrict its processing. Contact us through our contact form for any privacy-related
              requests.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">Data Deletion</h2>
            <p className="text-default-500">
              You can permanently delete all your personal information by accessing your account settings and selecting 
              the &ldquo;Delete Account&rdquo; option. Please note that this action is irreversible - once you delete your data, we 
              will completely remove it from our systems and will not maintain any backup copies. This includes:
            </p>
            <ul className="list-disc list-inside mt-4 space-y-2 text-default-500">
              <li>Your account information and profile data</li>
              <li>Your usage history and preferences</li>
              <li>Any content or interactions you&apos;ve created on our platform</li>
            </ul>
            <p className="text-default-500 mt-4">
              If you wish to use our services again after deletion, you&apos;ll need to create a new account and start fresh.
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}
