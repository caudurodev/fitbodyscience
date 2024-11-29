'use client'

import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Button,
    useDisclosure
} from "@nextui-org/react"
import { ReactNode, forwardRef, useImperativeHandle } from "react"
import { useUserData, useAuthenticationStatus } from '@nhost/nextjs'
import { useCallback, useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'

interface ProWarningModalProps {
    children?: ReactNode;
}

export interface ProWarningModalHandle {
    open: () => void;
    close: () => void;
}


export const useIsProUser = () => {
    const userData = useUserData()
    const { isAuthenticated, isLoading } =
        useAuthenticationStatus()
    const [isPro, setIsPro] = useState(false)
    const showModalVerdict = useCallback(() => {
        if (isLoading) return false
        if (!isAuthenticated || !userData) return false
        const isProRoleFound = userData?.defaultRole === 'pro' || !!userData?.roles.find(role => role === 'pro')
        if (!isProRoleFound) return false
        return true
    }, [userData, isAuthenticated, isLoading])
    useEffect(() => {
        if (isLoading) return
        const result = showModalVerdict()
        setIsPro(result)
    }, [isPro, showModalVerdict, isLoading])
    return { showModalVerdict, isPro }
}


const ProWarningModalComponent = forwardRef<ProWarningModalHandle, ProWarningModalProps>((props, ref) => {
    const { isOpen, onOpen, onClose, onOpenChange } = useDisclosure()
    const router = useRouter()
    useImperativeHandle(ref, () => ({
        open: () => onOpen(),
        close: () => onClose()
    }))
    return (
        <Modal
            isOpen={isOpen}
            onOpenChange={onOpenChange}
            placement="center"
        >
            <ModalContent>
                {(onClose) => (
                    <>
                        <ModalHeader className="flex flex-col gap-1">
                            Upgrade to Pro
                        </ModalHeader>
                        <ModalBody>
                            <p className="text-default-500">
                                This feature is only available for Pro users. Upgrade your account to access:
                            </p>
                            <ul className="list-disc list-inside space-y-2 text-default-500">
                                <li>Advanced evidence search</li>
                                <li>Unlimited assertions</li>
                                <li>Priority support</li>
                                <li>And more...</li>
                            </ul>
                        </ModalBody>
                        <ModalFooter>
                            <Button color="danger" variant="light" onPress={onClose}>
                                Maybe Later
                            </Button>
                            <Button
                                color="primary"
                                onPress={() => {
                                    router.push('/plans')
                                }}
                                className="bg-gradient-to-tr from-pink-500 to-yellow-500 text-white shadow-lg"
                            >
                                Upgrade to Pro
                            </Button>
                        </ModalFooter>
                    </>
                )}
            </ModalContent>
        </Modal>
    )
})

ProWarningModalComponent.displayName = 'ProWarningModal'


export const ProWarningModal = ProWarningModalComponent
