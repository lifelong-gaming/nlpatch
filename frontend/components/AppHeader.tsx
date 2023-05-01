import { AppBar, Box, Toolbar, Typography } from "@mui/material"
import { useAuthContext } from "@/src/contexts/AuthContext"
import Link from "next/link"
import AccountMenu from "./AccountMenu"


const AppHeader = () => {
  const { user } = useAuthContext()
  return (
    <AppBar>
      <Toolbar>
        <Link href={!!user?"/":"/login"}>
          <Typography variant="h5">
            NLPatch
          </Typography>
        </Link>
        <Box sx={{ flexGrow: 1 }} />
        {user && <AccountMenu />}
      </Toolbar>
    </AppBar>
  )
}

export default AppHeader
