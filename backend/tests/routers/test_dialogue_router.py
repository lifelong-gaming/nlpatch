from collections.abc import Sequence

from fastapi import FastAPI
from fastapi.testclient import TestClient

from nlpatch.auth_providers.base import BaseAuthProvider
from nlpatch.routers.dialogue_router import generate_dialogue_router
from nlpatch.storages.base import BaseStorage
from nlpatch.types import Dialogue


def test_dialogue_router_retrieve_dialogue(
    dialogue_list: Sequence[Dialogue],
    storage: BaseStorage,
    valid_auth_provider: BaseAuthProvider,
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    expected = {"dialogues": dialogue_list[:4]}
    response = client.get("/api/v1/dialogues", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json() == expected
