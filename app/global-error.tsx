'use client'

import { useEffect } from 'react'
import { unstable_rethrow } from 'next/navigation'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  // Re-throw Next.js navigation errors (redirect, notFound, etc)
  unstable_rethrow(error)

  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <div className="flex flex-col items-center justify-center min-h-screen px-4 bg-white dark:bg-black">
          <div className="max-w-md text-center">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-4">
              Application Error
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              A critical error occurred. Please refresh the page or contact support if the problem
              persists.
            </p>
            {error.digest && (
              <p className="text-sm text-gray-500 dark:text-gray-500 mb-6">
                Error ID: {error.digest}
              </p>
            )}
            <button
              onClick={reset}
              className="rounded-lg border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-xs transition-colors duration-150 hover:bg-blue-700 focus:outline-hidden dark:hover:bg-blue-500"
            >
              Try again
            </button>
          </div>
        </div>
      </body>
    </html>
  )
}
