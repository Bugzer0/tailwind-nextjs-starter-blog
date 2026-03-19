import Link from '@/components/Link'
import dictionary from '@/data/dictionary'

const APP_STORE_URL = 'https://apps.apple.com/us/app/blood-sugar-monitor-glucoai/id6751217849'

export default function AppBanner() {
  return (
    <div className="my-6 overflow-hidden rounded-2xl border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-sm dark:border-blue-800/40 dark:from-blue-950/40 dark:to-indigo-950/30">
      <div className="flex flex-col items-center gap-5 px-6 py-5 sm:flex-row sm:px-8">
        <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-100 text-2xl dark:bg-blue-900/50">
          📱
        </div>
        <div className="flex-1 text-center sm:text-left">
          <h3 className="text-base font-semibold text-gray-800 dark:text-gray-100">
            {dictionary.appBanner.title}
          </h3>
          <p className="mt-0.5 text-sm text-gray-500 dark:text-gray-400">
            {dictionary.appBanner.description}
          </p>
        </div>
        <Link
          href={APP_STORE_URL}
          className="group relative inline-flex shrink-0 items-center gap-2 rounded-full bg-gray-900 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-all duration-200 hover:scale-[1.03] hover:bg-black hover:shadow-md active:scale-[0.97] dark:bg-gray-900 dark:hover:bg-black"
          aria-label={dictionary.appBanner.download}
        >
          <span className="absolute inset-0 animate-pulse rounded-full bg-gray-500/20 dark:bg-gray-400/15" />
          <svg
            className="relative h-4 w-4 transition-transform duration-200 group-hover:-translate-y-0.5"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
          </svg>
          <span className="relative">{dictionary.appBanner.download}</span>
        </Link>
      </div>
    </div>
  )
}
