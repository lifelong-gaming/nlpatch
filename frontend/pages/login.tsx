import React from "react"
import { useRouter } from "next/router"

import LoginForm from "@/components/LoginForm"
import { useAuthContext } from "@/src/contexts/AuthContext"
import Head from "next/head"
import styles from '@/styles/Home.module.css'

const Login = () => {
  const router = useRouter()
  const handleLogin = () => {
    router.push("/")
  }
  const handleClose = async () => {
    await router.push("/")
  }

  return (
    <>
      <Head>
        <title>Login</title>
      </Head>
      <main className={styles.main}>
        <LoginForm onLoginSucceded={handleLogin} />
      </main>
    </>
  )
}

export default Login