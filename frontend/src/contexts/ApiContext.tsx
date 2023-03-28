import { ReactNode, createContext, useState, useContext, useEffect } from "react"
import { useAuthContext } from "./AuthContext"


class APIHandler {
  constructor(public accessToken: string) { }
  rootURL: string = process.env.NEXT_PUBLIC_API_ROOT || "";
}

export type ApiContextProps = {
  api: APIHandler | null
}

export type ApiProps = {
  children: ReactNode
}

const ApiContext = createContext<Partial<ApiContextProps>>({})

export const useApiContext = () => {
  return useContext(ApiContext)
}

export const ApiProvider = ({ children }: ApiProps) => {
  const { user } = useAuthContext()
  const [api, setApi] = useState<APIHandler | null>(null)
  useEffect(() => {
    console.log(user)
    user?.getIdToken().then((token) => {
      setApi(new APIHandler(token))
    }).catch((error) => {
      setApi(null)
    })
  }, [user])
  const value = {
    api, 
  }

  return (
    <ApiContext.Provider value={value}>
      {children}
    </ApiContext.Provider>
  )
}
