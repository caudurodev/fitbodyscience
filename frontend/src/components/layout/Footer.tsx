import Link from 'next/link'

export const Footer = () => {
  return (
    <footer className="w-full py-8 px-8 mt-auto text-gray-500">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          <div className="col-span-1 sm:col-span-2 md:col-span-2">
            <h3 className="text-lg font-bold mb-4">Important Disclaimer</h3>
            <p className="text-small ">
              The research and content presented on this platform is generated and analyzed by artificial intelligence.
              While we strive for accuracy, this information should not be considered medical advice. The AI system may
              occasionally produce errors or misinterpretations. Always consult qualified healthcare professionals for
              medical advice and verify information from multiple reliable sources.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/privacy-policy" className="text-small text-gray-500 hover:text-primary transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-small text-gray-500 hover:text-primary transition-colors">
                  Terms & Conditions
                </Link>
              </li>
              <li>
                <Link href="/faq" className="text-small text-gray-500 hover:text-primary transition-colors">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Contact</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/contact" className="text-small text-gray-500 hover:text-primary transition-colors">
                  Contact Form
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  )
}
