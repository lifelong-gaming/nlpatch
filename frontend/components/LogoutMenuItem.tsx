import React from 'react'
import { MenuItem, ListItemIcon } from '@mui/material'
import { getAuth, signOut } from 'firebase/auth'
import { useRouter } from 'next/router'
import { Logout } from '@mui/icons-material'

interface Prop {
  onClick: () => void
}

const LogoutMenuItem = (props: Prop) => {
  const { onClick } = props
  const auth = getAuth()
  const router = useRouter()
  const handleClick = async () => {
    onClick()
    await signOut(auth)
    await router.push('/login')
  }
  return (
    <MenuItem onClick={handleClick}>
      <ListItemIcon>
        <Logout fontSize="small" />
      </ListItemIcon>
      Logout
    </MenuItem>
  )
}

export default LogoutMenuItem