from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from firebase_admin import auth, credentials, initialize_app
from ..base import BaseAuthProvider
from .settings import FirebaseAuthProviderSettings
from ...types import User

class FirebaseAuthProvider(BaseAuthProvider):
    def __init__(self, settings: FirebaseAuthProviderSettings):
        self._credential = credentials.Certificate(settings.firebase_credentials)
        self._app = initialize_app(credential=self._credential)


    def get_user_token(self, res: Response, credential: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))) -> User:
        if credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authentication is needed",
                headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
            )
        try:
            decoded_token = auth.verify_id_token(credential.credentials)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication from Firebase. {err}",
                headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
            )
        res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
        return User(id=decoded_token["uid"])
