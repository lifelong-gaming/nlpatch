import Head from 'next/head'
import styles from '@/styles/Home.module.css'
import { useApiContext } from '@/src/contexts/ApiContext'
import { useEffect } from 'react'
import { useSnackbar } from 'notistack';
import { Button } from '@mui/material';

export default function Home() {
  const { api } = useApiContext()
  const { enqueueSnackbar } = useSnackbar();
  useEffect(() => {
    if (!!api) {
      enqueueSnackbar('API is ready', { variant: 'success' })
    } else {
      enqueueSnackbar('API is not ready', { variant: 'error' })
    }
  }, [api])
  return (
    <>
      <Head>
        <title>NLPatch</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Button onClick={() => {
        api?.getUserMe().then((res) => {
          enqueueSnackbar(JSON.stringify(res), { variant: 'success' })
        }).catch((err) => {
          enqueueSnackbar(JSON.stringify(err), { variant: 'error' })
        })
      }}>Click me</Button>
    </>
  )
}
