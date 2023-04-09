import React from 'react'
import { MenuItem, ListItemIcon } from '@mui/material'
import { useRouter } from 'next/router'
import { Add } from '@mui/icons-material'

interface Prop {
  onClick: () => void
}

const NewDialogueMenuItem = (props: Prop) => {
  const router = useRouter()
  const { onClick } = props
  const handleClick = async () => {
    onClick()
    await router.push('/dialogue/new')
  }
  return (
    <MenuItem onClick={handleClick}>
      <ListItemIcon>
        <Add fontSize="small" />
      </ListItemIcon>
      New Dialogue
    </MenuItem>
  )
}

export default NewDialogueMenuItem
