from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException

from ..auth_providers.base import BaseAuthProvider
from ..fields import Id
from ..storages.base import BaseStorage
from ..storages.exceptions import ModelMetadataNotFoundError
from ..types import ModelMetadata, ModelMetadataDetail, User


def generate_model_router(auth_provider: BaseAuthProvider, storage: BaseStorage) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_model=Sequence[ModelMetadata])
    def list_model_metadata(user: User = Depends(auth_provider.get_user_token)) -> Sequence[ModelMetadata]:
        return storage.list_model_metadata()

    @router.get("/{model_id}", response_model=ModelMetadataDetail)
    def retrieve_model_metadata(
        model_id: str, user: User = Depends(auth_provider.get_user_token)
    ) -> ModelMetadataDetail:
        try:
            id_ = Id(model_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        try:
            return storage.retrieve_model_metadata(id_)
        except ModelMetadataNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return router
