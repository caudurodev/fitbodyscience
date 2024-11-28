'use client'

import { useUserId, useSignOut, useAuthenticationStatus } from '@nhost/nextjs'
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
} from '@nextui-org/react'
import { useRouter } from 'next/navigation'
import { toast } from 'react-hot-toast'
import { useEffect } from 'react'
import { useMutation } from '@apollo/client'
import { DELETE_USER_ACCOUNT_AND_CONTENT_MUTATION } from '@/store/user'

export default function AccountPage() {
  const { isOpen, onOpen, onOpenChange } = useDisclosure()
  const { isAuthenticated, isLoading: isLoadingAuth } =
    useAuthenticationStatus()
  const router = useRouter()
  const { signOut } = useSignOut()
  const userId = useUserId()
  const [deleteUserAccountAndContent] = useMutation(
    DELETE_USER_ACCOUNT_AND_CONTENT_MUTATION
  )

  useEffect(() => {
    if (isLoadingAuth || isAuthenticated) return
    router.push('/login')
  }, [isLoadingAuth, isAuthenticated, router])

  return (
    <div className="max-w-7xl mx-auto py-8 px-4">
      <section className="mb-8">
        <div className="space-y-4">
          <h1 className="text-6xl font-bold tracking-tight">
            Account <span className="text-gradient">Settings</span>
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-xl max-w-2xl">
            Manage your account settings and preferences
          </p>
        </div>
      </section>

      <div className="mt-8 space-y-8 max-w-3xl">
        <div className="flex flex-col space-y-4">
          <div>
            <h2 className="text-3xl font-bold text-danger mb-4">
              Delete Account
            </h2>
            <p className="mb-4 text-default-500">
              Warning: Deleting your account will permanently remove all your data and cannot be undone.
              This includes your profile, preferences, and all interactions on the platform.
            </p>
            <Button onPress={onOpen} color="danger" variant="flat" data-testid="show-delete-modal">
              Delete Account
            </Button>
          </div>
        </div>

        <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
          <ModalContent>
            {(onClose) => (
              <>
                <ModalHeader className="flex flex-col gap-1 text-danger">
                  Delete Account
                </ModalHeader>
                <ModalBody>
                  <h1 className="text-3xl text-danger">
                    Warning: This action cannot be undone
                  </h1>
                  <p className="text-default-500">
                    Are you sure you want to delete your account? This will permanently remove all your data
                    from our systems. You&apos;ll lose access to all your saved preferences and interactions.
                  </p>
                </ModalBody>
                <ModalFooter>
                  <Button color="default" variant="light" onPress={onClose}>
                    Cancel
                  </Button>
                  <Button
                    color="danger"
                    data-testid="delete-account"
                    onPress={async () => {
                      try {
                        toast.loading('Deleting account...')
                        await deleteUserAccountAndContent({
                          variables: { userId },
                        })
                        await signOut()
                        toast.success('Account deleted successfully')
                        router.push('/')
                      } catch (e) {
                        toast.error('Error deleting account')
                        console.error(e)
                      }
                    }}
                  >
                    Delete Account
                  </Button>
                </ModalFooter>
              </>
            )}
          </ModalContent>
        </Modal>
      </div>
    </div>
  )
}
