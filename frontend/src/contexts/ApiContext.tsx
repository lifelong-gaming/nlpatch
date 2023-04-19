import { ReactNode, createContext, useState, useContext, useEffect } from "react"
import { useAuthContext, UserType } from "./AuthContext"
import User from "@/types/User"
import ModelMetadata from "@/types/ModelMetadata"
import Dialogue from "@/types/Dialogue"
import { resolve } from "path";

class APIHandler {
  constructor(public user: UserType, public accessToken: string) { }
  rootURL: string = process.env.NEXT_PUBLIC_API_ROOT || "";

  constructUrl = (path: string) => {
    return `${this.rootURL.replace(/\/$/, "")}/${path.replace(/^\//, "")}`
  }
  constructHeaders = () => {
    return {
      "Authorization": `Bearer ${this.accessToken}`
    }
  }
  refreshAccessToken: () => Promise<string> = () => {
    if (this.user === null) return Promise.reject("User is not logged in")
    return this.user.getIdToken().then((token) => {
      this.accessToken = token
      return token
    })
  }

  withRefresh<T>(func: () => Promise<T>): Promise<T> {
    return func().catch((error) => {
      if (error === "Unauthorized") {
        return this.refreshAccessToken().then(() => {
          return func()
        })
      }
      return Promise.reject(error)
    })
  }

  getUserMe: () => Promise<User> = () => {
    return this.withRefresh(() => fetch(
      this.constructUrl("/v1/user/me"), {
        headers: this.constructHeaders()
      }
    ).then((res: Response) => {
      if (res.status === 401) return Promise.reject("Unauthorized")
      if (res.status !== 200) return Promise.reject(`${res.statusText} (${res.status})`)
      return res.json()
    }))
  }

  listModelMetadata: () => Promise<ModelMetadata[]> = () => {
    return this.withRefresh(() => fetch(
      this.constructUrl("/v1/models"), {
        headers: this.constructHeaders()
      }
    ).then((res: Response) => {
      if (res.status === 401) return Promise.reject("Unauthorized")
      if (res.status !== 200) return Promise.reject(`${res.statusText} (${res.status})`)
      return res.json()
    }))
  }

  createDialogue: (modelId: string) => Promise<Dialogue> = (modelId) => {
    return this.withRefresh(() => fetch(
      this.constructUrl("/v1/dialogues"), {
        method: "POST",
        headers: {...this.constructHeaders(), "Content-Type": "application/json"},
        body: JSON.stringify({
          modelId
        })
      }
    ).then((res: Response) => {
      if (res.status === 401) return Promise.reject("Unauthorized")
      if (res.status !== 201) return Promise.reject(`${res.statusText} (${res.status})`)
      return res.json()
    }))
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
    console.log(user)
    user?.getIdToken().then((token) => {
      setApi(new APIHandler(user, token))
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
