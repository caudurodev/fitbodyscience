'use client'

import {
  Modal,
  ModalContent,
  useDisclosure,
  Button,
  Tabs,
  Tab,
  Card,
  CardBody,
} from '@nextui-org/react'
// import { useResponsive } from '@/hooks/useResponsive'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Register } from '@/components/auth/Register'
import { Login } from '@/components/auth/Login'
import { SignedIn, SignedOut } from '@nhost/nextjs'
import { Icon } from '@iconify/react'

interface ILoginModalProps {
  buttonVariant?:
  | 'ghost'
  | 'flat'
  | 'light'
  | 'shadow'
  | 'solid'
  | 'bordered'
  | 'faded'
  responsiveHide?: boolean
  defaultTab?: 'register' | 'login'
  toggleOpen?: boolean
  buttonLabel?: string
  mainTestId?: string
  setToggleOpen?: (toggle: boolean) => void
}

export const LoginModal = ({
  buttonVariant = 'solid',
  defaultTab = 'register',
  buttonLabel = 'login or join',
  toggleOpen = false,
  mainTestId = '',
  setToggleOpen,
}: ILoginModalProps) => {

  // const { isMobile } = useResponsive()
  const [selected, setSelected] = useState(defaultTab)
  const router = useRouter()
  const { isOpen, onOpen, onOpenChange } = useDisclosure()

  useEffect(() => {
    setSelected('register')
    if (toggleOpen) {
      onOpen()
      if (setToggleOpen) setToggleOpen(false)

    }
  }, [toggleOpen, setToggleOpen, onOpen])

  useEffect(() => {
    setSelected(defaultTab)
  }, [isOpen, defaultTab])


  return (
    <span data-testid={mainTestId}>
      <SignedIn>
        {/* signedin */}
      </SignedIn>
      <SignedOut>
        <Button
          fullWidth
          size="sm"
          data-testid="login-modal-button"
          variant={buttonVariant}
          color="primary"
          onClick={() => {
            setSelected('login')
            onOpen()
          }}
        >
          {buttonLabel} <Icon icon="ic:round-login" className="inline" />
        </Button>
      </SignedOut>
      <Modal
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        placement="center"
        className="mt-4 mx-4"
        size="sm"
        data-testid="login-modal-main"
      >
        <ModalContent>
          <div className="flex flex-col w-full">
            <Card className="max-w-full">
              <CardBody className="overflow-hidden text-center">
                <Tabs
                  selectedKey={selected}
                  onSelectionChange={(s) => { setSelected(s as any) }}
                  aria-label="Options"
                  className="flex justify-center"
                >
                  <Tab key="login" title="Login">
                    <Login
                      onRegister={() => { setSelected('register') }}
                      onLogin={() => {
                        router.push('/account')
                        console.log('onLogin')
                      }}
                    />
                  </Tab>
                  <Tab key="register" title="Signup"  >
                    <Register
                      onRegister={() => { console.log('onRegister') }}
                      onLogin={() => { setSelected('login') }}
                    />
                  </Tab>
                </Tabs>
              </CardBody>
            </Card>
          </div>
        </ModalContent>
      </Modal>
    </span>
  )
}

export default LoginModal
