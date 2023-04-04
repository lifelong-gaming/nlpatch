from abc import ABCMeta, abstractmethod
from fastapi import Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class BaseAuthProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_user_token(
        self, response: Response, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
    ):
        raise NotImplementedError
