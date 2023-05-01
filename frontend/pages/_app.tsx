import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import theme from '@/styles/theme'
import { ThemeProvider } from '@mui/material/styles';
import { AuthProvider } from '@/src/contexts/AuthContext'
import AppHeader from '@/components/AppHeader'
import { SnackbarProvider } from 'notistack';
import { ApiProvider } from '@/src/contexts/ApiContext';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider theme={theme}>
      <SnackbarProvider maxSnack={10}>
        <AuthProvider>
          <ApiProvider>
            <AppHeader />
            <Component {...pageProps} />
          </ApiProvider>
        </AuthProvider>
      </SnackbarProvider>
    </ThemeProvider>
  )
}
