from collections.abc import Sequence

from fastapi import APIRouter

from .auth_providers.base import BaseAuthProvider
from .storages.base import BaseStorage
from .types import ModelMetadata


def generate_router(auth_provider: BaseAuthProvider, storage: BaseStorage) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_model=Sequence[ModelMetadata])
    def list_model_metadata() -> Sequence[ModelMetadata]:
        return storage.list_model_metadata()

    return router
