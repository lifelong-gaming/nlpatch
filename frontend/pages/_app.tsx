import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import theme from '@/styles/theme'
import { ThemeProvider } from '@mui/material/styles';
import { AuthProvider } from '@/src/contexts/AuthContext'
import AppHeader from '@/components/AppHeader'
import { SnackbarProvider } from 'notistack';
import { ApiProvider } from '@/src/contexts/ApiContext';
import { Box, Container, CssBaseline } from '@mui/material';


export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SnackbarProvider maxSnack={10} />
        <AuthProvider>
          <ApiProvider>
            <AppHeader />
            <Box component="main" sx={
              {
                flexGrow: 1,
                pb: 2,
                px: 2,
                pt: 10,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                minHeight: "100vh",
              }
            }>
              <Component {...pageProps} />
            </Box>
          </ApiProvider>
        </AuthProvider>
    </ThemeProvider>
  )
}
