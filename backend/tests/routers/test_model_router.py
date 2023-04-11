from collections.abc import Sequence

from fastapi import FastAPI
from fastapi.testclient import TestClient

from nlpatch.auth_providers.base import BaseAuthProvider
from nlpatch.fields import Id
from nlpatch.routers.model_router import generate_model_router
from nlpatch.storages.base import BaseStorage
from nlpatch.types import ModelMetadata


def test_list_model_metadata(
    model_metadata_list: Sequence[ModelMetadata], storage: BaseStorage, valid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_model_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json() == model_metadata_list


def test_list_model_metadata_returns_401_when_invalid_auth(
    storage: BaseStorage, invalid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_model_router(auth_provider=invalid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 401


def test_list_model_metadata_returns_401_when_no_auth_header(
    storage: BaseStorage, valid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_model_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/")
    assert response.status_code == 401


def test_retrieve_model_metadata(
    model_metadata_ids: Sequence[Id],
    model_metadata_detail_list: Sequence[ModelMetadata],
    storage: BaseStorage,
    valid_auth_provider: BaseAuthProvider,
) -> None:
    sut = generate_model_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    for i, expected in zip(model_metadata_ids, model_metadata_detail_list):
        response = client.get(f"/api/v1/models/{i}", headers={"Authorization": "Bearer valid_token"})
        assert response.status_code == 200
        assert response.json() == expected.dict()


def test_retrieve_model_metadata_returns_404_when_non_such_id(
    storage: BaseStorage,
    valid_auth_provider: BaseAuthProvider,
) -> None:
    sut = generate_model_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/vzvEVHq-Q8OXFoKCVQzFWg", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 404


def test_retrieve_model_metadata_returns_400_when_invalid_id(
    storage: BaseStorage,
    valid_auth_provider: BaseAuthProvider,
) -> None:
    sut = generate_model_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/invalid-as-model-id-string", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 400


def test_retrieve_model_metadata_returns_401_when_no_auth_header(
    storage: BaseStorage,
    valid_auth_provider: BaseAuthProvider,
) -> None:
    sut = generate_model_router(auth_provider=valid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/vzvEVHq-Q8OXFoKCVQzFWg")
    assert response.status_code == 401


def test_retrieve_model_metadata_returns_401_when_invalid_auth(
    storage: BaseStorage, invalid_auth_provider: BaseAuthProvider
) -> None:
    sut = generate_model_router(auth_provider=invalid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/vzvEVHq-Q8OXFoKCVQzFWg", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
