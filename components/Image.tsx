'use client'

import { useState } from 'react'
import NextImage, { ImageProps } from 'next/image'

const basePath = process.env.BASE_PATH

const PLACEHOLDER =
  'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxIiBoZWlnaHQ9IjEiPjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNlNWU3ZWIiLz48L3N2Zz4='

const Image = ({ src, onError, ...rest }: ImageProps) => {
  const [errored, setErrored] = useState(false)

  if (errored || !src) {
    return <NextImage src={PLACEHOLDER} unoptimized {...rest} />
  }

  return (
    <NextImage
      src={`${basePath || ''}${src}`}
      onError={(e) => {
        setErrored(true)
        onError?.(e)
      }}
      {...rest}
    />
  )
}

export default Image
