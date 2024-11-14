import { Button } from '@nextui-org/react'
import { Icon } from '@iconify/react'


type AuthMethod = {
  name: string
  icon: string
}
interface AuthMethods {
  authMethods: AuthMethod[]
  onPress: (methodName: string) => void
}
export const AuthMethods = ({ authMethods, onPress }: AuthMethods) => {
  return (
    <div className="my-4 mx-16 grid grid-cols-1 gap-2 place-content-center">
      <h3 className="text-sm text-brandmain font-bold mb-4">With Google</h3>
      {authMethods.map((authMethod, index) => (
        <Button
          key={index}
          onPress={() => onPress(authMethod.name)}
          variant="ghost"
          color="primary"
          className="rounded-full"
        >
          <span className="hidden sm:inline-block">With {authMethod.name}</span>
          <span className="sm:hidden"> With {authMethod.name}</span>
          <Icon icon={authMethod.icon} className="text-2xl mx-2 inline" />
        </Button>
      ))}
    </div>
  )
}
