'use client'

import { useState, useEffect } from 'react'
import { toast } from 'react-hot-toast'
import { Icon } from '@iconify/react'
import { useRouter } from 'next/navigation'
import {
  Button,
  useDisclosure,
  Input,
} from '@nextui-org/react'
import { useMutation } from '@apollo/client'
import { useForm, Controller } from 'react-hook-form'
import { ADD_VIDEO_MUTATION } from '@/store/index'

export default function Home() {
  const router = useRouter()
  const [success, setSuccess] = useState(false)
  const { isOpen, onOpen, onClose, onOpenChange } = useDisclosure()
  const [addVideoMutation, { loading }] = useMutation(ADD_VIDEO_MUTATION)
  const {
    handleSubmit,
    control,
    formState: { errors },
    reset,
  } = useForm()

  const onSubmit = async (data: any) => {
    try {
      console.log({ data })
      const result = await addVideoMutation({
        variables: {
          mediaType: 'video',
          contentType: 'youtube_video',
          sourceUrl: data.videoUrl,
        },
      })
      // setSuccess(true)
      toast.success(`Message sent - Thanks for the feedback!`)
      const videoId = result?.data?.insert_content?.returning?.[0]?.id
      router.push('/video/' + videoId)
    } catch (e) {
      setSuccess(false)
      //console.log((e)
      toast.error(`Server Error saving feedback!`)
    }
  }

  useEffect(() => {
    if (isOpen) {
      reset()
      setSuccess(false)
    }
  }, [isOpen, setSuccess, reset])
  return (
    <main className="p-24 min-h-screen">
      <h1>Add Video</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="">
        <Controller
          name="videoUrl"
          control={control}
          rules={{
            required: true,
            pattern: /https:\/\/www.youtube.com\/watch\?v=([a-zA-Z0-9_-]+)/,

          }}
          render={({ field }) => (
            <Input
              {...field}
              isDisabled={loading}
              label="Youtube Video URL"
              placeholder="Type here..."
              variant="bordered"
              size="lg"
              color="primary"
              startContent={
                <div className="pointer-events-none flex items-center">
                  <Icon icon="material-symbols:link" />
                </div>
              }
              onChange={(e) => field.onChange(e.target.value)}
              errorMessage={
                !errors.videoUrl
                  ? ''
                  : 'Invalid Youtube URL'
              }
              isInvalid={!errors.videoUrl ? false : true}
            />
          )}
        />
        <div className="my-4 flex self-end w-full">
          <Button
            isDisabled={loading}
            isLoading={loading}
            color="primary"
            onPress={() => {
              handleSubmit(onSubmit)()
            }}
          >
            Send
          </Button>
        </div>
      </form>

    </main>
  );
}

