import React, { useState } from "react";
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import Button from '@mui/material/Button';

import { useSnackbar } from 'notistack';
import { getAuth, signInWithEmailAndPassword } from "firebase/auth"
import { app } from "@/src/firebase"
import { Paper } from "@mui/material";

interface Prop {
  onLoginSucceded: () => void;
}

const LoginForm = (props: Prop) => {
  const { enqueueSnackbar } = useSnackbar();
  const [showPassword, setShowPassword] = useState(false);
  const { onLoginSucceded } = props;
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const auth = getAuth(app)
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    signInWithEmailAndPassword(auth, email, password).then((userCredential) => {
      enqueueSnackbar("Login succeeded", {variant: "success"});
      onLoginSucceded();
    }).catch((error) => {
      enqueueSnackbar(error.message, {variant: "error"});
    })
  }
  const handleChangeEmail = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.currentTarget.value);
  }
  const handleChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.currentTarget.value);
  }
  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };
  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };
  return (
    <Paper sx={{width: "100%"}}>
      <form onSubmit={handleSubmit}>
        <Box
          sx={{
            py: 2,
            display: 'grid',
            gap: 2,
            alignItems: 'center',
            flexWrap: 'wrap',
            p: 4
          }}
        >
          <TextField
            label="email address"
            onChange={handleChangeEmail}
          />
          <FormControl variant="outlined">
            <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
            <OutlinedInput
              onChange={handleChangePassword}
              id="outlined-adornment-password"
              type={showPassword ? 'text' : 'password'}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword}
                    onMouseDown={handleMouseDownPassword}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Password"
              />
          </FormControl>
          <Button type="submit" variant="contained">Login</Button>
        </Box>
      </form>  
   </Paper>
  )
};

export default LoginForm;
