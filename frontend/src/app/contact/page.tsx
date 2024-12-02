'use client'

import { Input, Textarea, Button } from "@nextui-org/react"
import { useForm, SubmitHandler } from "react-hook-form"
import { useState } from 'react'

type FormData = {
  name: string
  email: string
  subject: string
  message: string
  honeypot: string
}

export default function Contact() {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormData>()
  const [status, setStatus] = useState<'idle' | 'sending' | 'success' | 'error'>('idle')


  const onSubmit: SubmitHandler<FormData> = async (data) => {
    // Check if honeypot field is filled (bot detection)
    console.log('Form submitted:', data)
    if (data.honeypot) {
      console.log('Bot detected')
      return
    }

    setStatus('sending')
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: data.email,
          subject: data.subject,
          message: data.message
        }),
      })

      if (response.ok) {
        setStatus('success')
        reset() // Clear form fields
      } else {
        setStatus('error')
      }
    } catch (error) {
      console.error('Error sending message:', error)
      setStatus('error')
    }
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
            {/* Honeypot field (hidden from users) */}
            <input
              type="text"
              {...register('honeypot')}
              style={{ display: 'none' }}
              tabIndex={-1}
              autoComplete="off"
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
            {status === 'success' && <p className="text-green-500">Message sent successfully!</p>}
            {status === 'error' && <p className="text-red-500">Error sending message. Please try again.</p>}
          </form>
        </div>
      </div>
    </div>
  )
}
