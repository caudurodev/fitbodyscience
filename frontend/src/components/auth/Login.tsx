'use client'

import {
    Input,
    Link,
    Button,
} from '@nextui-org/react'
import { Icon } from '@iconify/react'
import { toast } from 'react-hot-toast'
import { useForm, SubmitHandler } from 'react-hook-form'
import { useEffect } from 'react'
import { useSignInEmailPassword, useProviderLink } from '@nhost/nextjs'
import { AuthMethods } from '@/components/auth/AuthMethods'
import { useAnalytics } from '@/hooks/useAnalytics'

const authMethods = [
    {
        name: 'Google',
        icon: 'dashicons:google',
    },
]


interface IFormLoginAccount {
    email: string
    password: string
}

export const Login = ({ onRegister, onLogin }: { onRegister: () => void, onLogin: () => void }) => {
    const { trackEvent } = useAnalytics()
    const { google } = useProviderLink({ redirectTo: '/account' })

    const loginWithAuth = async (authType: string) => {
        trackEvent({ action: 'login_attempt', category: 'Authentication', label: authType })
        if (authType === 'Google' && google) window.location.href = google
    }

    const {
        signInEmailPassword,
        needsEmailVerification,
        isLoading,
        isSuccess,
        isError,
        error
    } = useSignInEmailPassword()


    const onSubmitLogin: SubmitHandler<IFormLoginAccount> = async (data) => {
        try {
            trackEvent({ action: 'login_attempt', category: 'Authentication', label: 'Email' })
            const result = await signInEmailPassword(data.email, data.password)

            if (result?.error) {
                toast.error(result?.error.message)
                trackEvent({ action: 'login_error', category: 'Authentication', label: result.error.message })
            } else {
                toast.success('Success logging in')
                trackEvent({ action: 'login_success', category: 'Authentication', label: 'Email' })
                if (onLogin) onLogin()
            }
        } catch (e: any) {
            toast.error('Server Error logging in')
            trackEvent({ action: 'login_error', category: 'Authentication', label: 'Server Error' })
        }
    }

    const {
        register: registerLogin,
        handleSubmit: handleSubmitLogin,
        reset: resetLoginForm,
        formState: { errors: loginErrors },
    } = useForm<IFormLoginAccount>({
        mode: 'onBlur',
        defaultValues: {
            email: '',
            password: '',
        },
    })

    useEffect(() => {
        resetLoginForm()
    }, [resetLoginForm])

    return (
        <form
            className="flex flex-col gap-2 mt-0"
            onSubmit={handleSubmitLogin(onSubmitLogin)}
        >
            <AuthMethods authMethods={authMethods} onPress={loginWithAuth} />
            <h3 className="text-sm text-brandmain font-bold mb-4">{'Login with Email'}</h3>
            <Input
                endContent={
                    <Icon
                        icon="tabler:mail"
                        className="text-2xl text-default-400 pointer-events-none flex-shrink-0"
                    />
                }
                isRequired
                disabled={isLoading}
                label="Email"
                placeholder="email..."
                variant="bordered"
                isInvalid={!!loginErrors.email}
                errorMessage={
                    loginErrors.email ? 'Invalid Email' : null
                }
                {...registerLogin('email', {
                    required: true,
                    pattern: {
                        value: /\S+@\S+\.\S+/,
                        message: 'Invalid Email',
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
                label="Password"
                disabled={isLoading}
                placeholder="password..."
                type="password"
                variant="bordered"
                isInvalid={!!loginErrors.password}
                errorMessage={
                    loginErrors.password
                        ? loginErrors.password.type === 'required'
                            ? 'Password Required'
                            : loginErrors.password.type === 'minLength'
                                ? 'Password Required'
                                : 'Password Required'
                        : null
                }
                {...registerLogin('password', {
                    required: true,
                    minLength: 9,
                })}
            />
            <div className="my-2">
                <p className="text-center text-small">
                    {"Don't yet have an account?"}{' '}

                </p>
                <Button
                    size="sm"
                    variant="light"
                    color="secondary"
                    onPress={() => {
                        trackEvent({ action: 'registration_start', category: 'Authentication' })
                        if (onRegister) onRegister()
                    }}
                >
                    Sign up Free
                </Button>
            </div>
            <div className="flex gap-2 justify-end">
                <Button
                    fullWidth
                    color="primary"
                    type="submit"
                    disabled={isLoading}
                    isLoading={isLoading}
                >
                    Login
                </Button>
            </div>
        </form>
    )
}