import { useEffect, useState, useCallback } from 'react'
import { useNhostClient } from '@nhost/nextjs'
import { Image } from '@nextui-org/react'

interface StorageImageProps {
  fileId: string
  alt?: string
  className?: string
  width?: number
  height?: number
  props?: any
}
export const StorageImage = ({
  fileId,
  alt,
  className,
  width = 200,
  height = 200,
  props,
}: StorageImageProps) => {
  const nhostClient = useNhostClient()
  const [imageUrl, setImageUrl] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  const getURL = useCallback(
    async (fileId: string) => {
      try {
        const { presignedUrl } = await nhostClient.storage.getPresignedUrl({
          fileId,
        })
        return presignedUrl?.url || ''
      } catch (error) {
        console.error('Error getting presigned URL:', error)
        return ''
      }
    },
    [nhostClient],
  )

  useEffect(() => {
    if (fileId) {
      setIsLoading(true)
      getURL(fileId).then((url) => {
        if (url) {
          setImageUrl(url)
        } else {
          console.error('Failed to get image URL for fileId:', fileId)
        }
        setIsLoading(false)
      })
    } else {
      setIsLoading(false)
    }
  }, [fileId, getURL])

  if (!fileId) return null

  return (
    <div style={{ minWidth: width, minHeight: height }}>
      {isLoading ? (
        <div style={{ width, height, backgroundColor: '#f0f0f0' }} />
      ) : (
        <Image
          {...props}
          width={width}
          height={height}
          src={imageUrl}
          alt={alt || 'Image'}
          className={className}
        />
      )}
    </div>
  )
}
