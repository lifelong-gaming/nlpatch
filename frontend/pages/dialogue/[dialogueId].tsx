import React from 'react'
import Head from 'next/head'
import styles from '@/styles/Home.module.css'
import { useRouter } from 'next/router'
import { useApiContext } from '@/src/contexts/ApiContext'
import { useEffect } from 'react'
import { useSnackbar } from 'notistack';
import ModelMetadataDetail from '@/types/ModelMetadataDetail';
import Dialogue from '@/types/Dialogue';
import { CircularProgress, Slider, Stack, Typography } from '@mui/material';
import InputFormForModel from '@/components/InputFormForModel';


export default function DialogueId() {
  const router = useRouter()
  const { api } = useApiContext()
  const { enqueueSnackbar } = useSnackbar();
  const { dialogueId } = router.query
  const [modelMetadataDetail, setModelMetadata] = React.useState<ModelMetadataDetail | null>(null)
  const [dialogueData, setDialogueData] = React.useState<Dialogue | null>(null)
  useEffect(() => {
    if (!api || !dialogueData) {
      return
    }
    api.getModelMetadata(dialogueData.modelId).then((res) => {
      setModelMetadata(res)
      console.log(res)
    }).catch((err) => {
      enqueueSnackbar(JSON.stringify(err), { variant: 'error' })
    })
  }, [dialogueData])
  useEffect(() => {
    if (!api || !dialogueId) {
      return
    }
    api.getDialogue(dialogueId as string).then((res) => {
      setDialogueData(res)
      console.log(res)
    }).catch((err) => {
      enqueueSnackbar(JSON.stringify(err), { variant: 'error' })
    })
  }, [api, dialogueId])
  return (
    <>
      <Head>
        <title>NLPatch / dialogue{ modelMetadataDetail?` with ${modelMetadataDetail.name}`:"" }</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {
        modelMetadataDetail?(
          <InputFormForModel inputs={modelMetadataDetail.inputs} onSubmit={() => {}} />
        ):
        <CircularProgress />
      }
    </>
  )
}

