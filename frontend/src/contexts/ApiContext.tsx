import { ReactNode, createContext, useState, useContext, useEffect } from "react"
import { useAuthContext } from "./AuthContext"
import User from "@/types/User"

class APIHandler {
  constructor(public accessToken: string) { }
  rootURL: string = process.env.NEXT_PUBLIC_API_ROOT || "";

  constructUrl = (path: string) => {
    return `${this.rootURL.replace(/\/$/, "")}/${path.replace(/^\//, "")}`
  }
  constructHeaders = () => {
    return {
      "Authorization": `Bearer ${this.accessToken}`
    }
  }

  getUserMe: () => Promise<User> = () => {
    return fetch(
      this.constructUrl("/user/me"), {
        headers: this.constructHeaders()
      }
    ).then((res: Response) => res.json())
  }
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
