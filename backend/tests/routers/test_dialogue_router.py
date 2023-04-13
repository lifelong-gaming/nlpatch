from collections.abc import Sequence

from fastapi import FastAPI
from fastapi.testclient import TestClient

from nlpatch.auth_providers.base import BaseAuthProvider
from nlpatch.routers.dialogue_router import generate_dialogue_router
from nlpatch.storages.base import BaseStorage
from nlpatch.types import Dialogue


def test_list_dialogues(
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


def test_list_dialogues_returns_401_when_invalid_auth(
    storage: BaseStorage, invalid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_dialogue_router(auth_provider=invalid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.get("/api/v1/dialogues", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_list_dialogues_returns_401_when_no_auth_header(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.get("/api/v1/dialogues")
    assert response.status_code == 401


def test_retrieve_dialogue(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider, dialogue_list: Sequence[Dialogue]
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    expected = dialogue_list[0]
    response = client.get(f"/api/v1/dialogues/{dialogue_list[0].id}", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json() == expected.dict()


def test_retrieve_dialogue_returns_401_when_invalid_auth(
    storage: BaseStorage, invalid_auth_provider: BaseAuthProvider, dialogue_ids: Sequence[str]
) -> None:
    sut = generate_dialogue_router(auth_provider=invalid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.get(f"/api/v1/dialogues/{dialogue_ids[0]}", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_retrieve_dialogue_returns_401_when_no_auth_header(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider, dialogue_ids: Sequence[str]
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.get(f"/api/v1/dialogues/{dialogue_ids[0]}")
    assert response.status_code == 401


def test_retrieve_dialogue_returns_404_when_dialogue_not_found(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.get("/api/v1/dialogues/UJuydKCKSjCQ8HeptXFc-Q", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 404
