import Link from '@/components/Link'
import PageTitle from '@/components/PageTitle'
import SectionContainer from '@/components/SectionContainer'

export default function NewsletterConfirmPage() {
  return (
    <SectionContainer>
      <div className="divide-y divide-gray-200 dark:divide-gray-700">
        <div className="space-y-2 pt-6 pb-8 md:space-y-5">
          <PageTitle>Newsletter Subscription Confirmed</PageTitle>
        </div>
        <div className="py-12">
          <div className="mb-8 text-center">
            <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900">
              <svg
                className="h-8 w-8 text-green-600 dark:text-green-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <h2 className="mb-4 text-2xl font-bold text-gray-900 dark:text-gray-100">
              Thank you for subscribing!
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              You're now part of the GlucoAI community.
            </p>
          </div>

          <div className="mb-8 rounded-lg border border-gray-200 bg-gray-50 p-6 dark:border-gray-700 dark:bg-gray-800">
            <h3 className="mb-4 text-lg font-semibold text-gray-900 dark:text-gray-100">
              What's next?
            </h3>
            <ul className="space-y-3 text-gray-700 dark:text-gray-300">
              <li className="flex items-start">
                <span className="mr-2">📚</span>
                <span>Explore our latest blog posts</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">💡</span>
                <span>Get weekly health tips and insights</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">🎯</span>
                <span>Learn about blood glucose management</span>
              </li>
            </ul>
          </div>

          <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/"
              className="bg-primary-500 hover:bg-primary-600 dark:bg-primary-600 dark:hover:bg-primary-500 inline-flex w-full items-center justify-center rounded-md px-6 py-3 text-base font-medium text-white sm:w-48 dark:text-white"
            >
              Back to Home
            </Link>
            <Link
              href="/blog"
              className="hover:border-primary-500 hover:text-primary-500 dark:hover:border-primary-400 dark:hover:text-primary-400 inline-flex w-full items-center justify-center rounded-md border-2 border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 sm:w-48 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300"
            >
              Read Latest Posts
            </Link>
          </div>
        </div>
      </div>
    </SectionContainer>
  )
}
