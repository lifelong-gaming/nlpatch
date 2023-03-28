import { AppBar, Toolbar, Typography, Button } from "@mui/material"
import { useAuthContext } from "@/src/contexts/AuthContext"
import LogoutButton from "@/components/LogoutButton"

const AppHeader = () => {
  const { user } = useAuthContext()
  return (
    <AppBar>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          NLPatch
        </Typography>
        {user && <LogoutButton />}
      </Toolbar>
    </AppBar>
  )
}

export default AppHeader
