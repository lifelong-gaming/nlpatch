import { AppBar, Toolbar, Typography } from "@mui/material"
import { useAuthContext } from "@/src/contexts/AuthContext"
import Link from "next/link"
import AccountMenu from "./AccountMenu"


const AppHeader = () => {
  const { user } = useAuthContext()
  return (
    <AppBar>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          NLPatch
        </Typography>
        {user && <AccountMenu />}
      </Toolbar>
    </AppBar>
  )
}

export default AppHeader
