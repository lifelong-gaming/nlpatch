from collections.abc import Sequence
from datetime import datetime
from typing import cast
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from nlpatch.auth_providers.base import BaseAuthProvider
from nlpatch.fields import Id, Timestamp
from nlpatch.routers.dialogue_router import generate_dialogue_router
from nlpatch.storages.base import BaseStorage
from nlpatch.types import Dialogue, ModelMetadata, User


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


def test_retrieve_dialogue_returns_400_when_invalid_id(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.get(
        "/api/v1/dialogues/invalid-string-as-a-model-id-string", headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 400


def test_retrive_dialogue_returns_404_when_other_users_dialogue_id(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider, dialogue_list: Sequence[Dialogue]
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.get(f"/api/v1/dialogues/{dialogue_list[-1].id}", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 404


def test_create_dialogue(
    storage: BaseStorage,
    valid_auth_provider: BaseAuthProvider,
    model_metadata_list: Sequence[ModelMetadata],
    mocker: MockerFixture,
    user: User,
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    dt = datetime(2021, 1, 1, 1, 23, 45, 678)
    ts = Timestamp(dt)
    mocker.patch.object(Dialogue.__fields__["id"], "default_factory", return_value=Id("0iISHMyJRdmoAF8yoyy6jA"))
    mocker.patch.object(Dialogue.__fields__["created_at"], "default_factory", return_value=ts)
    mocker.patch.object(Dialogue.__fields__["updated_at"], "default_factory", return_value=ts)
    response = client.post(
        "/api/v1/dialogues/",
        headers={"Authorization": "Bearer valid_token"},
        json={"modelId": str(model_metadata_list[0].id)},
    )
    assert response.status_code == 201
    cast(MagicMock, storage.create_dialogue).assert_called_once_with(
        dialogue=Dialogue(
            id=Id("0iISHMyJRdmoAF8yoyy6jA"),
            model_id=model_metadata_list[0].id,
            owner_id=user.id,
            created_at=ts,
            updated_at=ts,
        )
    )


def test_create_dialogue_returns_401_when_invalid_auth(
    storage: BaseStorage, invalid_auth_provider: BaseAuthProvider, model_metadata_list: Sequence[ModelMetadata]
) -> None:
    sut = generate_dialogue_router(auth_provider=invalid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.post(
        "/api/v1/dialogues/",
        headers={"Authorization": "Bearer invalid_token"},
        json={"modelId": str(model_metadata_list[0].id)},
    )
    assert response.status_code == 401


def test_create_dialogue_returns_401_when_no_auth_header(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider, model_metadata_list: Sequence[ModelMetadata]
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.post("/api/v1/dialogues/", json={"modelId": str(model_metadata_list[0].id)})
    assert response.status_code == 401


def test_create_dialogue_returns_400_when_invalid_model_id(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.post(
        "/api/v1/dialogues/", headers={"Authorization": "Bearer valid_token"}, json={"modelId": "invalid"}
    )
    assert response.status_code == 400


def test_create_dialogue_returns_400_when_model_not_exists(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider, model_metadata_ids: Sequence[Id]
) -> None:
    id_ = Id.generate()
    while id_ in model_metadata_ids:
        id_ = Id.generate()
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.post(
        "/api/v1/dialogues/", headers={"Authorization": "Bearer valid_token"}, json={"modelId": str(id_)}
    )
    assert response.status_code == 400


def test_create_dialogue_returns_422_when_no_model_id(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_dialogue_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/dialogues")
    client = TestClient(app)
    response = client.post("/api/v1/dialogues/", headers={"Authorization": "Bearer valid_token"}, json={})
    assert response.status_code == 422
