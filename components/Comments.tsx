'use client'

import { Comments as CommentsComponent } from 'pliny/comments'
import { useState } from 'react'
import siteMetadata from '@/data/siteMetadata'
import dictionary from '@/data/dictionary'

export default function Comments({ slug }: { slug: string }) {
  const [loadComments, setLoadComments] = useState(process.env.NODE_ENV === 'production')

  if (!siteMetadata.comments?.provider) {
    return null
  }
  return (
    <>
      {loadComments ? (
        <CommentsComponent commentsConfig={siteMetadata.comments} slug={slug} />
      ) : (
        <button onClick={() => setLoadComments(true)}>{dictionary.comments.loadComments}</button>
      )}
    </>
  )
}
