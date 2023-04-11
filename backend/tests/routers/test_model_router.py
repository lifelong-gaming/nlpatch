from collections.abc import Sequence

from fastapi import FastAPI
from fastapi.testclient import TestClient

from nlpatch.auth_providers.base import BaseAuthProvider
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


def test_list_model_metadata_returns_401(storage: BaseStorage, invalid_auth_provider: BaseAuthProvider) -> None:
    sut = generate_model_router(auth_provider=invalid_auth_provider, storage=storage)
    app = FastAPI()
    app.include_router(sut, prefix="/api/v1/models")
    client = TestClient(app)
    response = client.get("/api/v1/models/", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 401
