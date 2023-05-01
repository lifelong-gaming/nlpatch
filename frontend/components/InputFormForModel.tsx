import { useState, Dispatch, SetStateAction } from "react"
import { BaseInput } from "@/types/Input"
import { Box, TextField, Paper, Button } from "@mui/material"
import { KeyboardEvent, ChangeEvent } from "react"

interface Prop {
  inputs: BaseInput[]
  onSubmit: () => void
}

const InputFormForModel = (props: Prop) => {
  const { inputs, onSubmit } = props
  const [ inputValues, setInputValues ] = useState<
    Map<string, string>
  >(new Map<string, string>())

  const handleInputChange = (inputId: string, event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setInputValues(
      new Map<string, string>(inputValues.set(inputId, event.target.value))
    )
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    console.log(e)
    e.preventDefault()
    const query = inputs.map((input) => {
      return {
        id: input.id,
        value: inputValues.get(input.id) || ""
      }
    })
    onSubmit()
  }
  return (
    <Paper component="footer" sx={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      p: 2,
      width: "100%",
      zIndex: "appBar",
      backgroundColor: "background.paper"
  }} elevation={3}>
    <form onSubmit={handleSubmit}>
      <Box
        sx={{
          display: 'grid',
          gap: 2,
          flexWrap: 'wrap',
        }}
      >
        {inputs.map((input, index) => {
          if (input.type === "longText") {
            return (
              <TextField
                key={input.id}
                label={input.fieldName}
                onChange={(event) => handleInputChange(input.id, event)}
                multiline
                minRows={2}
              />
            )
          } else if (input.type === "shortText") {
            return (
              <TextField
                key={input.id}
                label={input.fieldName}
                maxRows={1}
                onKeyDown={(event: KeyboardEvent<HTMLDivElement>) => {
                  if (event.key === "Enter") {
                    event.preventDefault()
                  }
                }}
                onChange={(event) => handleInputChange(input.id, event)}
              />
            )
          } else if (input.type === "number") {
            return (
              <TextField
                key={input.id}
                label={input.fieldName}
                onChange={(event) => handleInputChange(input.id, event)}
                type="number"
              />
            )
          } else {
            return (
              <TextField
                key={index}
                label={input.fieldName}
              />
            )
          }
        })}
        <Button type="submit" variant="contained">Submit</Button>
        </Box>
      </form>
    </Paper>
  )
}

export default InputFormForModel
