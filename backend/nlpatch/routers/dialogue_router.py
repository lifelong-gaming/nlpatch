from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException

from ..auth_providers.base import BaseAuthProvider
from ..fields import Id
from ..storages.base import BaseStorage
from ..storages.exceptions import DialogueNotFoundError
from ..types import BaseType, Dialogue, User


class DialogueListResponse(BaseType):
    dialogues: Sequence[Dialogue]


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

    return router
