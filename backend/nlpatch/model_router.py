from collections.abc import Sequence

from fastapi import APIRouter

from .auth_providers.base import BaseAuthProvider
from .fields import Id
from .storages.base import BaseStorage
from .types import ModelMetadata, ModelMetadataDetail


def generate_router(auth_provider: BaseAuthProvider, storage: BaseStorage) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_model=Sequence[ModelMetadata])
    def list_model_metadata() -> Sequence[ModelMetadata]:
        return storage.list_model_metadata()

    @router.get("/{model_id}", response_model=ModelMetadataDetail)
    def get_model_metadata(model_id: str) -> ModelMetadataDetail:
        return storage.get_model_metadata(Id(model_id))

    return router
