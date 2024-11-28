'use client'

import { Input, Textarea, Button } from "@nextui-org/react"
import { useForm } from "react-hook-form"

type FormData = {
  name: string
  email: string
  subject: string
  message: string
}

export default function Contact() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>()

  const onSubmit = (data: FormData) => {
    // TODO: Implement form submission
    console.log('Form submitted:', data)
  }

  return (
    <div className="y-8 px-4">
      <section className="mb-8">
        <div className="space-y-4">
          <p className="text-primary font-medium">Hi there!</p>
          <h1 className="text-6xl font-bold tracking-tight">
            Send us a <span className="text-gradient">message</span><br />
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            Send us a <span className="text-secondary">message</span>{' '} and we&apos;ll get back to you as soon!
          </p>
        </div>
      </section>
      <div className="max-w-lg">
        <div className="space-y-8">
          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6">
            <Input
              label="Name"
              color="secondary"
              variant="flat"
              placeholder="Your name"
              {...register("name", { required: "Name is required" })}
              isInvalid={!!errors.name}
              errorMessage={errors.name?.message}
              isRequired
            />
            <Input
              label="Email"
              placeholder="your.email@example.com"
              type="email"
              color="secondary"
              variant="flat"
              {...register("email", {
                required: "Email is required",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "Invalid email address"
                }
              })}
              isInvalid={!!errors.email}
              errorMessage={errors.email?.message}
              isRequired
            />
            <Input
              label="Subject"
              color="secondary"
              variant="flat"
              placeholder="What is this regarding?"
              {...register("subject", { required: "Subject is required" })}
              isInvalid={!!errors.subject}
              errorMessage={errors.subject?.message}
              isRequired
            />
            <Textarea
              label="Message"
              color="secondary"
              variant="flat"
              placeholder="Your message"
              {...register("message", {
                required: "Message is required",
                minLength: {
                  value: 10,
                  message: "Message must be at least 10 characters"
                }
              })}
              isInvalid={!!errors.message}
              errorMessage={errors.message?.message}
              minRows={4}
              isRequired
            />
            <Button color="primary" type="submit">
              Send Message
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
