from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ..auth_providers.base import BaseAuthProvider
from ..fields import Id
from ..storages.base import BaseStorage
from ..storages.exceptions import DialogueNotFoundError, ModelMetadataNotFoundError
from ..types import BaseType, Dialogue, User


class DialogueListResponse(BaseType):
    dialogues: Sequence[Dialogue]


class DialogueCreateRequest(BaseType):
    model_id: str


def generate_dialogue_router(auth_provider: BaseAuthProvider, storage: BaseStorage) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_model=DialogueListResponse)
    def list_dialogues(user: User = Depends(auth_provider.get_user_token)) -> DialogueListResponse:
        return DialogueListResponse(dialogues=storage.list_dialogues(user_id=user.id))

    @router.get("/{dialogue_id}", response_model=Dialogue)
    def retrieve_dialogue(dialogue_id: str, user: User = Depends(auth_provider.get_user_token)) -> Dialogue:
        try:
            id_ = Id(dialogue_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        try:
            res = storage.retrieve_dialogue(dialogue_id=id_, user_id=user.id)
        except DialogueNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return res

    @router.post("/", response_model=Dialogue)
    def create_dialogue(
        query: DialogueCreateRequest, user: User = Depends(auth_provider.get_user_token)
    ) -> JSONResponse:
        try:
            model_id = Id(query.model_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        try:
            storage.retrieve_model_metadata(model_id)
        except ModelMetadataNotFoundError as e:
            raise HTTPException(status_code=400, detail=str(e))
        d = Dialogue(owner_id=user.id, model_id=model_id)
        storage.create_dialogue(dialogue=d)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=d.dict())

    return router
