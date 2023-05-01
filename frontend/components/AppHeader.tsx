import { AppBar, Box, Toolbar, Typography } from "@mui/material"
import { useAuthContext } from "@/src/contexts/AuthContext"
import NextLink from "next/link"
import AccountMenu from "./AccountMenu"


const AppHeader = () => {
  const { user } = useAuthContext()
  return (
    <AppBar>
      <Toolbar>
        <NextLink href={!!user?"/":"/login"}>
          <Typography variant="h5">
            NLPatch
          </Typography>
        </NextLink>
        <Box sx={{ flexGrow: 1 }} />
        {user && <AccountMenu />}
      </Toolbar>
    </AppBar>
  )
}

export default AppHeader
