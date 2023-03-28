import React from 'react'
import { Button } from '@mui/material'
import { getAuth, signOut } from 'firebase/auth'
import { useRouter } from 'next/router'

const LogoutButton = () => {
  const auth = getAuth()
  const router = useRouter()
  const logout = async () => {
    await signOut(auth)
    await router.push('/login')
  }
  return (
    <Button color="inherit" onClick={logout}>
      Logout
    </Button>
  )
}

export default LogoutButton