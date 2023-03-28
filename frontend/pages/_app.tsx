import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import { AuthProvider } from '@/src/contexts/AuthContext'
import AppHeader from '@/components/AppHeader'
import { SnackbarProvider } from 'notistack';
import { ApiProvider } from '@/src/contexts/ApiContext';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <SnackbarProvider maxSnack={10}>
      <AuthProvider>
        <ApiProvider>
          <AppHeader />
          <Component {...pageProps} />
        </ApiProvider>
      </AuthProvider>
    </SnackbarProvider>
  )
}
