from collections.abc import Sequence

from fastapi import APIRouter, Depends

from ..auth_providers.base import BaseAuthProvider
from ..fields import Id
from ..storages.base import BaseStorage
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
        return storage.retrieve_dialogue(dialogue_id=Id(dialogue_id), user_id=user.id)

    return router
