'use client'

import {
    Input,
    Button,
    Checkbox,
} from '@nextui-org/react'
import { Icon } from '@iconify/react'
import { toast } from 'react-hot-toast'
import { useForm, SubmitHandler } from 'react-hook-form'
import { useEffect, useState } from 'react'
import { useSignUpEmailPassword, useProviderLink } from '@nhost/nextjs'
import { useRouter } from 'next/navigation'
import { AuthMethods } from '@/components/auth/AuthMethods'
import Link from 'next/link'
import { useAnalytics } from '@/hooks/useAnalytics'

interface IFormCreateAccount {
    name: string
    email: string
    password: string
    acceptTerms: boolean
    acceptPrivacy: boolean  // Add this line
}
const authMethods = [
    {
        name: 'Google',
        icon: 'dashicons:google',
    },
]

export const Register = ({ onRegister, onLogin }: { onRegister: () => void, onLogin: () => void }) => {
    const { google } = useProviderLink({ redirectTo: '/account' })
    const { trackEvent } = useAnalytics()

    const loginWithAuth = async (authType: string) => {
        trackEvent({ action: 'registration_attempt', category: 'Authentication', label: authType })
        if (authType === 'Google' && google) window.location.href = google
    }

    const { signUpEmailPassword, isLoading, error, isSuccess } =
        useSignUpEmailPassword()
    const [serverError, setServerError] = useState<string | null>(null)
    const router = useRouter()

    const {
        register: registerCreate,
        handleSubmit: handleSubmitCreate,
        reset: resetCreateForm,
        formState: { errors: createErrors, isSubmitted },
        setValue,
        watch,
    } = useForm<IFormCreateAccount>({
        mode: 'onSubmit',
        defaultValues: {
            name: '',
            email: '',
            password: '',
            acceptTerms: false,
            acceptPrivacy: false,  // Add this line
        },
    })

    const watchTerms = watch('acceptTerms')
    const watchPrivacy = watch('acceptPrivacy')

    useEffect(() => {
        if (isSubmitted) {
            if (!watchTerms) {
                setValue('acceptTerms', false, { shouldValidate: true })
            }
            if (!watchPrivacy) {
                setValue('acceptPrivacy', false, { shouldValidate: true })
            }
        }
    }, [isSubmitted, watchTerms, watchPrivacy, setValue])

    const onSubmitCreate: SubmitHandler<IFormCreateAccount> = async (data) => {
        if (!data.acceptTerms || !data.acceptPrivacy) {
            setServerError("You must accept both the Terms and Conditions and the Privacy Policy to register.")
            toast.error("You must accept both the Terms and Conditions and the Privacy Policy to register.")
            trackEvent({ action: 'registration_error', category: 'Authentication', label: 'Terms and Privacy not accepted' })
            return
        }

        try {
            trackEvent({ action: 'registration_attempt', category: 'Authentication', label: 'Email' })
            const result = await signUpEmailPassword(
                data.email,
                data.password,
                {
                    displayName: data.name
                }
            )

            if (result.error) {
                setServerError(result.error.message)
                toast.error(result.error.message)
                trackEvent({ action: 'registration_error', category: 'Authentication', label: result.error.message })
            } else {
                toast.success("Signed up successfully!")
                trackEvent({ action: 'registration_success', category: 'Authentication', label: 'Email' })
                // Use router.push instead of setTimeout
                router.push('/account')
            }
        } catch (e: any) {
            const errorMessage = e.message || "Server error signing up"
            setServerError(errorMessage)
            toast.error(errorMessage)
            trackEvent({ action: 'registration_error', category: 'Authentication', label: errorMessage })
        }
    }

    useEffect(() => {
        resetCreateForm()
    }, [resetCreateForm])

    return (
        <form
            className="flex flex-col gap-3 mt-2"
            onSubmit={handleSubmitCreate(onSubmitCreate)}
        >
            <AuthMethods authMethods={authMethods} onPress={loginWithAuth} />
            <h3 className="text-sm text-brandmain font-bold">Or with Email</h3>
            <Input
                endContent={
                    <Icon
                        icon="tabler:user"
                        className="text-2xl text-default-400 pointer-events-none flex-shrink-0"
                    />
                }
                isRequired
                label="Name"
                placeholder="Your name..."
                variant="bordered"
                isInvalid={!!createErrors.name}
                errorMessage={createErrors.name && createErrors.name.message}
                {...registerCreate('name', {
                    required: 'Name is required',
                    pattern: {
                        value: /^[a-zA-Z0-9\s,.'-]+$/,
                        message: 'Name contains invalid characters',
                    },
                    maxLength: {
                        value: 100,
                        message: 'Name must be 100 characters or less',
                    },
                })}
            />
            <Input
                endContent={
                    <Icon
                        icon="tabler:mail"
                        className="text-2xl text-default-400 pointer-events-none flex-shrink-0"
                    />
                }
                isRequired
                label="Email"
                placeholder="Your email..."
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
            <Input
                endContent={
                    <Icon
                        icon="tabler:lock"
                        className="text-2xl text-default-400 pointer-events-none flex-shrink-0"
                    />
                }
                isRequired
                label="Create Password"
                placeholder="password..."
                type="password"
                variant="bordered"
                isInvalid={!!createErrors.password}
                errorMessage={
                    createErrors.password
                        ? createErrors.password.type === 'required'
                            ? "Password is required"
                            : createErrors.password.type === 'minLength'
                                ? "Password is not long enouth"
                                : "Invalid password"
                        : null
                }
                {...registerCreate('password', { required: true, minLength: 9 })}
            />

            <div className="flex flex-col  mx-4 mb-4">
                <Checkbox
                    size='sm'
                    isRequired
                    onValueChange={(isSelected) => setValue('acceptTerms', isSelected, { shouldValidate: true })}
                    isInvalid={!!createErrors.acceptTerms}
                    {...registerCreate('acceptTerms', { required: true })}
                >
                    I accept the <Link href="/terms" className="text-primary" target="_blank" rel="noopener noreferrer">Terms and Conditions</Link>
                </Checkbox>
                {createErrors.acceptTerms && (
                    <p className="text-danger text-sm">You must accept the Terms and Conditions to register.</p>
                )}

                <Checkbox
                    size='sm'
                    isRequired
                    onValueChange={(isSelected) => setValue('acceptPrivacy', isSelected, { shouldValidate: true })}
                    isInvalid={!!createErrors.acceptPrivacy}
                    {...registerCreate('acceptPrivacy', { required: true })}
                >
                    I accept the <Link href="/privacy" className="text-primary" target="_blank" rel="noopener noreferrer">Privacy Policy</Link>
                </Checkbox>
                {createErrors.acceptPrivacy && (
                    <p className="text-danger text-sm">You must accept the Privacy Policy to register.</p>
                )}
            </div>
            <div>
                <p className="text-center text-small">
                    {"Already have an account?"}{' '}
                </p>
                <Button
                    size="sm"
                    variant="light"
                    color="secondary"
                    onPress={() => {
                        trackEvent({ action: 'login_start', category: 'Authentication' })
                        if (onLogin) onLogin()
                    }}
                >
                    Login
                </Button>
            </div>


            {serverError && (
                <p className="text-danger text-sm text-center">Error! {serverError}</p>
            )}

            <div className="flex gap-2 justify-end">
                <Button
                    fullWidth
                    color="primary"
                    type="submit"
                    data-testid="signup-button"
                    disableAnimation={isLoading}
                    isLoading={isLoading}
                >
                    Sign up Free
                </Button>
            </div>
        </form>
    )
}