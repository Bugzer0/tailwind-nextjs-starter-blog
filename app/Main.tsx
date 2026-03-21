import AppBanner from '@/components/AppBanner'
import Link from '@/components/Link'
import Image from '@/components/Image'
import Tag from '@/components/Tag'
import siteMetadata from '@/data/siteMetadata'
import dictionary from '@/data/dictionary'
import { formatDate } from 'pliny/utils/formatDate'
import NewsletterForm from 'pliny/ui/NewsletterForm'
import { CoreContent } from 'pliny/utils/contentlayer'
import type { Blog } from 'contentlayer/generated'

const MAX_DISPLAY = 7

interface HomeProps {
  posts: CoreContent<Blog>[]
}

export default function Home({ posts }: HomeProps) {
  return (
    <>
      <div className="space-y-2 pb-6">
        <div className="flex flex-col items-center gap-x-12 xl:flex-row">
          <div className="space-y-2">
            <h1 className="text-2xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-3xl sm:leading-9 md:text-4xl md:leading-10 dark:text-gray-100">
              {dictionary.home.latestPosts}
            </h1>
            <p className="text-base leading-7 text-gray-500 sm:text-lg dark:text-gray-400">
              {dictionary.home.description}
            </p>
          </div>
          {siteMetadata.newsletter?.provider && (
            <div className="mx-2 my-12 flex w-[288px] items-center justify-center sm:w-[400px] md:w-[550px]">
              <div className="flex items-center justify-center">
                <NewsletterForm title={dictionary.home.newsletterTitle} apiUrl="/api/newsletter/" />
              </div>
            </div>
          )}
        </div>
      </div>
      <AppBanner />
      <div className="divide-y divide-gray-200 dark:divide-gray-700">
        <ul className="divide-y divide-gray-200 dark:divide-gray-700">
          {!posts.length && dictionary.home.noPosts}
          {posts.slice(0, MAX_DISPLAY).map((post) => {
            const { slug, date, title, summary, tags, images } = post
            return (
              <li key={slug} className="py-12">
                <article>
                  <div className="space-y-2 xl:grid xl:grid-cols-4 xl:space-y-0">
                    <dl className="hidden items-baseline xl:col-start-1 xl:row-start-1 xl:flex">
                      <dt className="sr-only">{dictionary.blog.publishedOn}</dt>
                      <dd className="text-base leading-6 font-medium text-gray-500 dark:text-gray-400">
                        <Link href={`/blog/${slug}`} aria-label={`Read "${title}"`}>
                          <Image
                            src={images?.[0] ?? ''}
                            alt={title}
                            className="thumbnail-image"
                            width={220}
                            height={220}
                            quality={80}
                            sizes="220px"
                            loading="lazy"
                          />
                        </Link>
                      </dd>
                    </dl>
                    <div className="flex flex-col items-baseline space-y-5 xl:col-span-3">
                      <div className="space-y-6">
                        <div>
                          <h2 className="text-2xl leading-8 font-bold tracking-tight">
                            <Link
                              href={`/blog/${slug}`}
                              className="text-gray-900 dark:text-gray-100"
                            >
                              {title}
                            </Link>
                          </h2>
                          <div className="mb-2 text-base leading-6 font-medium text-gray-500 dark:text-gray-400">
                            <time dateTime={date}>{formatDate(date, siteMetadata.locale)}</time>
                          </div>
                          <div className="flex flex-wrap">
                            {tags.map((tag: string) => (
                              <Tag key={tag} text={tag} />
                            ))}
                          </div>
                        </div>
                        <div className="prose max-w-none text-gray-500 dark:text-gray-400">
                          {summary}
                        </div>
                      </div>
                      <div className="text-base leading-6 font-medium">
                        <Link
                          href={`/blog/${slug}`}
                          className="text-primary-500 hover:text-primary-600 dark:hover:text-primary-400"
                          aria-label={`Read more: "${title}"`}
                        >
                          {dictionary.home.readMore} &rarr;
                        </Link>
                      </div>
                    </div>
                  </div>
                </article>
              </li>
            )
          })}
        </ul>
      </div>
      {posts.length > MAX_DISPLAY && (
        <div className="flex justify-end text-base leading-6 font-medium">
          <Link
            href="/blog"
            className="text-primary-500 hover:text-primary-600 dark:hover:text-primary-400"
            aria-label={dictionary.home.allPosts}
          >
            {dictionary.home.allPosts} &rarr;
          </Link>
        </div>
      )}
    </>
  )
}
