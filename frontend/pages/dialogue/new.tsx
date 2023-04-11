import React, {useState} from 'react'
import Head from 'next/head'
import styles from '@/styles/Home.module.css'
import { useApiContext } from '@/src/contexts/ApiContext'
import { useEffect } from 'react'
import { useSnackbar } from 'notistack';
import { Button, Typography } from '@mui/material';
import ModelMetadataCards from '@/components/ModelMetadataCards';
import ModelMetadata from '@/types/ModelMetadata'
import LoadingIndicator from '@/components/LoadingIndicator'

export default function DialogueNew() {
  const { api } = useApiContext()
  const [modelMetadataList, setModelMetadataList] = useState<ModelMetadata[] | null>(null)
  const { enqueueSnackbar } = useSnackbar();
  useEffect(() => {
    if (!api) {
      return
    }
    api.listModelMetadata().then((res) => {
      setModelMetadataList(res)
    }).catch((err) => {
      enqueueSnackbar(JSON.stringify(err), { variant: 'error' })
    })
  }, [api])
  return (
    <>
      <Head>
        <title>NLPatch / new dialogue</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
        {
          modelMetadataList === null ? <LoadingIndicator></LoadingIndicator>:
            modelMetadataList.length > 0?
              <ModelMetadataCards modelMetadataList={modelMetadataList}></ModelMetadataCards>:
              <Typography>{"モデルがありません"}</Typography>
        }
        <Button>start dialogue</Button>
      </main>
    </>
  )
}
