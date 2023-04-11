from collections.abc import Callable, Generator, Sequence
from typing import Any, Dict, Generic, TypeVar
from unittest.mock import MagicMock

import pytest
from pydantic_factories import ModelFactory

from nlpatch.auth_providers.base import BaseAuthProvider
from nlpatch.fields import Id, Timestamp, UserId
from nlpatch.storages.base import BaseStorage
from nlpatch.storages.exceptions import ModelMetadataNotFoundError
from nlpatch.types import ModelMetadata, ModelMetadataDetail, User

T = TypeVar("T")


class NlPatchModelFactory(Generic[T], ModelFactory[T]):
    @classmethod
    def get_provider_map(cls) -> Dict[Any, Callable[..., Any]]:
        m = super().get_provider_map()
        m[Id] = Id.generate
        m[Timestamp] = Timestamp.now
        return m


class ModelMetadataFactory(NlPatchModelFactory[ModelMetadata]):
    __model__ = ModelMetadata


class ModelMetadataDetailFactory(NlPatchModelFactory[ModelMetadataDetail]):
    __model__ = ModelMetadataDetail


@pytest.fixture(scope="session")
def model_metadata_detail_list() -> Generator[Sequence[ModelMetadataDetail], None, None]:
    data = [
        ModelMetadataDetailFactory.build(id=Id("52WW-lw2SrOpgoHFJzh0Kg"), inputs=[]),
        ModelMetadataDetailFactory.build(id=Id("C9mJEx_gTX2gi5vFj2AHqw"), inputs=[]),
        ModelMetadataDetailFactory.build(id=Id("mJTIBVyBRgWpHq8zERv0kg"), inputs=[]),
    ]
    yield data


@pytest.fixture(scope="session")
def model_metadata_list(
    model_metadata_detail_list: Sequence[ModelMetadataDetail],
) -> Generator[Sequence[ModelMetadata], None, None]:
    yield [ModelMetadata(**m.dict()) for m in model_metadata_detail_list]


@pytest.fixture(scope="session")
def storage(
    model_metadata_detail_list: Sequence[ModelMetadataDetail], model_metadata_list: Sequence[ModelMetadata]
) -> Generator[BaseStorage, None, None]:
    s = MagicMock(spec=BaseStorage)
    s.list_model_metadata.return_value = model_metadata_list

    def retrieve_model_metadata(model_id: Id) -> ModelMetadataDetail:
        if model_id == Id("52WW-lw2SrOpgoHFJzh0Kg"):
            return model_metadata_detail_list[0]
        elif model_id == Id("C9mJEx_gTX2gi5vFj2AHqw"):
            return model_metadata_detail_list[1]
        elif model_id == Id("mJTIBVyBRgWpHq8zERv0kg"):
            return model_metadata_detail_list[2]
        raise ModelMetadataNotFoundError(model_id=model_id)

    s.retrieve_model_metadata.side_effect = retrieve_model_metadata
    yield s


@pytest.fixture(scope="session")
def valid_auth_provider() -> Generator[BaseAuthProvider, None, None]:
    from fastapi import Depends, Response
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

    class MockAuthProvider(BaseAuthProvider):
        def get_user_token(
            self, response: Response, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
        ) -> User:
            return User(id=UserId("test-user"))

    yield MockAuthProvider()
