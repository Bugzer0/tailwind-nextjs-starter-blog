import { ReactNode } from 'react'
import type { Policy } from 'contentlayer/generated'

interface Props {
  children: ReactNode
  content: Omit<Policy, '_id' | '_raw' | 'body'>
}

export default function PolicyLayout({ children, content }: Props) {
  return (
    <>
      <div className="divide-y divide-gray-200 dark:divide-gray-700">
        <div className="space-y-2 pt-6 pb-8 md:space-y-5">
          <h1 className="text-3xl leading-9 font-extrabold tracking-tight text-gray-900 sm:text-4xl sm:leading-10 md:text-6xl md:leading-14 dark:text-gray-100">
            {content.title}
          </h1>
        </div>
        <div className="prose dark:prose-invert max-w-none pt-8 pb-8 xl:col-span-2">{children}</div>
      </div>
    </>
  )
}
