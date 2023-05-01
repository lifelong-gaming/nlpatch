import React from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import { useApiContext } from '@/src/contexts/ApiContext'
import { useEffect } from 'react'
import { enqueueSnackbar } from 'notistack';
import ModelMetadataDetail from '@/types/ModelMetadataDetail';
import Dialogue from '@/types/Dialogue';
import { CircularProgress } from '@mui/material';
import InputFormForModel from '@/components/InputFormForModel';


export default function DialogueId() {
  const router = useRouter()
  const { api } = useApiContext()
  const { dialogueId } = router.query
  const [title, setTitle] = React.useState<string>('NLPatch / dialogue')
  const [modelMetadataDetail, setModelMetadata] = React.useState<ModelMetadataDetail | null>(null)
  const [dialogueData, setDialogueData] = React.useState<Dialogue | null>(null)
  useEffect(() => {
    if (!api || !dialogueData) {
      return
    }
    api.getModelMetadata(dialogueData.modelId).then((res) => {
      setModelMetadata(res)
      setTitle(`NLPatch / dialogue with ${res.name}`)
      console.log(res)
    }).catch((err) => {
      enqueueSnackbar(JSON.stringify(err), { variant: 'error' })
    })
  }, [api, dialogueData])
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
        <title>{title}</title>
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

