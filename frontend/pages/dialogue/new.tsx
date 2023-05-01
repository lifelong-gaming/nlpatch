import React, {useState} from 'react'
import Head from 'next/head'
import { useApiContext } from '@/src/contexts/ApiContext'
import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { enqueueSnackbar } from 'notistack';
import { Typography } from '@mui/material';
import ModelMetadataCards from '@/components/ModelMetadataCards';
import ModelMetadata from '@/types/ModelMetadata'
import LoadingIndicator from '@/components/LoadingIndicator'

export default function DialogueNew() {
  const { api } = useApiContext()
  const [modelMetadataList, setModelMetadataList] = useState<ModelMetadata[] | null>(null)
  const router = useRouter()
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
  const onStartDialogue = (id: string) => {
    api?.createDialogue(id).then((res) => {
      enqueueSnackbar("dialogue created", { variant: 'success' })
      router.push(`/dialogue/${res.id}`)
    }).catch((err) => {
      enqueueSnackbar(JSON.stringify(err), { variant: 'error' })
    })
  }
  return (
    <>
      <Head>
        <title>NLPatch / new dialogue</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {
        modelMetadataList === null ? <LoadingIndicator></LoadingIndicator>:
          modelMetadataList.length > 0?
            <ModelMetadataCards onStartDialogue={onStartDialogue} modelMetadataList={modelMetadataList}></ModelMetadataCards>:
            <Typography>{"モデルがありません"}</Typography>
      }
    </>
  )
}
