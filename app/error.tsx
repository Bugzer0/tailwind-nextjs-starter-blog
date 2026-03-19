'use client'

import { useEffect } from 'react'
import { unstable_rethrow } from 'next/navigation'

export default function Error({
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
    <div className="flex flex-col items-center justify-center min-h-[400px] px-4">
      <div className="max-w-md text-center">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">
          Something went wrong!
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          An error occurred while loading this page. Please try again.
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
  )
}
