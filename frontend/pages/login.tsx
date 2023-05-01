import React from "react"
import { useRouter } from "next/router"

import LoginForm from "@/components/LoginForm"
import Head from "next/head"
import { enqueueSnackbar } from "notistack"

const Login = () => {
  const router = useRouter()
  const handleLogin = () => {
    enqueueSnackbar("Login success", { variant: "success" })
    router.push("/")
  }

  return (
    <>
      <Head>
        <title>Login</title>
      </Head>
      <LoginForm onLoginSucceded={handleLogin} />
    </>
  )
}

export default Login