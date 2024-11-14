'use client'

import {
    Input,
    Button,
    CardHeader,
    CardBody,
    Card,
} from '@nextui-org/react'
import { Icon } from '@iconify/react'
import { toast } from 'react-hot-toast'
import { useForm, SubmitHandler } from 'react-hook-form'
import { useEffect, useState } from 'react'
import { useSignInEmailPasswordless } from '@nhost/nextjs'

import { useAnalytics } from '@/hooks/useAnalytics';

interface IFormMagicLinkCreateAccount {
    email: string
}

export const RegisterMagicLink = () => {
    const { signInEmailPasswordless, isLoading, isSuccess, isError, error } =
        useSignInEmailPasswordless({ redirectTo: '/account' })

    const [serverError, setServerError] = useState<string | null>(null)

    const {
        register: registerCreate,
        handleSubmit: handleSubmitCreate,
        reset: resetCreateForm,
        formState: { errors: createErrors, isSubmitted },
    } = useForm<IFormMagicLinkCreateAccount>({
        mode: 'onSubmit',
        defaultValues: {
            email: '',
        },
    })

    const { trackEvent } = useAnalytics();

    const onSubmitCreate: SubmitHandler<IFormMagicLinkCreateAccount> = async (data) => {
        try {
            // Track the signup attempt
            trackEvent({
                action: 'signupmagiclink',
                category: 'engagement',
                label: 'Magic Link Signup'
            });

            const result = await signInEmailPasswordless(data.email)

            if (result.error) {
                setServerError(result.error.message)
                toast.error(result.error.message)
            } else {
                toast.success("Signed up successfully! Check your email for a magic link.")
            }
        } catch (e: any) {
            const errorMessage = e.message || "Server error signing up"
            setServerError(errorMessage)
            toast.error(errorMessage)
        }
    }

    useEffect(() => {
        resetCreateForm()
    }, [resetCreateForm])

    return (
        <div>
            {
                !isSuccess || isError ?
                    <form
                        onSubmit={handleSubmitCreate(onSubmitCreate)}
                    >
                        < div className="flex gap-3 sm:gap-4" >
                            <Input
                                size="lg"
                                isRequired
                                className="bg-white text-gray-600"
                                placeholder="email..."
                                variant="bordered"
                                isInvalid={!!createErrors.email}
                                errorMessage={createErrors.email && 'A valid email is required'}
                                {...registerCreate('email', {
                                    required: true,
                                    pattern: {
                                        value: /\S+@\S+\.\S+/,
                                        message: 'A valid Email is required',
                                    },
                                })}
                            />
                            <Button
                                color="primary"
                                type="submit"
                                variant="solid"
                                size="lg"
                                data-testid="signup-button"
                                // className="px-2"
                                disableAnimation={isLoading}
                                isLoading={isLoading}
                            >
                                Sign up Free!
                            </Button>
                        </div >
                        {serverError && (
                            <p className="text-danger text-sm text-center">Error! {serverError}</p>
                        )}
                    </form > :
                    <Card className="text-xl font-bold p-2 flex flex-col ">
                        <CardHeader className="flex justify-center text-6xl text-primary">
                            <Icon icon="tabler:mail" />
                        </CardHeader>
                        <CardBody>
                            <h6 className="inline text-primary text-center">Success! - Check your email for your signup confirmation..</h6>
                            <p className="text-sm mt-2 text-gray-500 text-center">With the magic link you will be able to manage your account.</p>
                        </CardBody>
                    </Card>
            }
        </div>
    )

}