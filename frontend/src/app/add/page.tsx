'use client'

import { toast } from 'react-hot-toast'
import { Icon } from '@iconify/react'
import { useRouter } from 'next/navigation'
import { Button, Input } from '@nextui-org/react'
import { useMutation } from '@apollo/client'
import { useForm, Controller } from 'react-hook-form'
import { ADD_VIDEO_MUTATION } from '@/store/content/mutation'

export default function Home() {
  const router = useRouter()
  const [addVideoMutation, { loading }] = useMutation(ADD_VIDEO_MUTATION)
  const { handleSubmit, control, formState: { errors } } = useForm()

  const onSubmit = async (data: any) => {
    try {
      const result = await addVideoMutation({
        variables: {
          mediaType: 'video',
          contentType: 'youtube_video',
          url: data.videoUrl,
        },
      })
      const slug = result?.data?.userAddContent?.slug
      const isSuccess = result?.data?.userAddContent?.success
      if (slug?.length > 0 && isSuccess) {
        toast.success(`Added!`)
        router.push('/video/' + slug)
      } else {
        toast.error(`Server Error saving feedback!`)
      }
    } catch (e) {
      toast.error(`Server Error saving feedback!`)
    }
  }

  return (
    <main className="py-8">
      <h1 className="text-6xl font-bold tracking-tight mb-8">
        Add a <span className="text-gradient">Youtube Video</span> to be<br />
        researched
      </h1>
      <form onSubmit={handleSubmit(onSubmit)} className=" flex gap-4">
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
              variant="flat"
              size="md"
              color="secondary"
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
        <Button
          isDisabled={loading}
          isLoading={loading}
          color="primary"
          size="lg"
          variant="solid"
          onPress={() => {
            handleSubmit(onSubmit)()
          }}
        >
          {loading ? 'Adding...' : 'Add'}
        </Button>
      </form>
    </main>
  );
}

