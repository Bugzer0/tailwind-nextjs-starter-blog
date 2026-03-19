'use client'

import { useEffect } from 'react'
import { unstable_rethrow } from 'next/navigation'
import dictionary from '@/data/dictionary'

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
    <div className="flex min-h-[400px] flex-col items-center justify-center px-4">
      <div className="max-w-md text-center">
        <h2 className="mb-4 text-3xl font-bold text-gray-900 dark:text-gray-100">
          {dictionary.error.somethingWentWrong}
        </h2>
        <p className="mb-6 text-gray-600 dark:text-gray-400">{dictionary.error.errorDescription}</p>
        {error.digest && (
          <p className="mb-6 text-sm text-gray-500 dark:text-gray-500">
            {dictionary.error.errorId}: {error.digest}
          </p>
        )}
        <button
          onClick={reset}
          className="rounded-lg border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-xs transition-colors duration-150 hover:bg-blue-700 focus:outline-hidden dark:hover:bg-blue-500"
        >
          {dictionary.error.tryAgain}
        </button>
      </div>
    </div>
  )
}
