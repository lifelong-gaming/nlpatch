from collections.abc import Callable, Generator, Sequence
from typing import Any, Dict, Generic, TypeVar
from unittest.mock import MagicMock

import pytest
from fastapi import Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic_factories import ModelFactory

from nlpatch.auth_providers.base import BaseAuthProvider
from nlpatch.fields import Id, Timestamp, UserId
from nlpatch.storages.base import BaseStorage
from nlpatch.storages.exceptions import (
    DialogueNotFoundError,
    ModelMetadataNotFoundError,
)
from nlpatch.types import (
    Dialogue,
    LongTextInput,
    ModelMetadata,
    ModelMetadataDetail,
    User,
)

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


class DialogueFactory(NlPatchModelFactory[Dialogue]):
    __model__ = Dialogue


class UserFactory(NlPatchModelFactory[User]):
    __model__ = User


@pytest.fixture(scope="session")
def user_id() -> Generator[UserId, None, None]:
    yield UserId("test")


@pytest.fixture(scope="session")
def user(user_id: UserId) -> Generator[User, None, None]:
    yield User(id=user_id)


@pytest.fixture(scope="session")
def other_user_id() -> Generator[UserId, None, None]:
    yield UserId("other")


@pytest.fixture(scope="session")
def other_user(other_user_id: UserId) -> Generator[User, None, None]:
    yield User(id=other_user_id)


@pytest.fixture(scope="session")
def model_metadata_ids() -> Generator[Sequence[Id], None, None]:
    ids = [Id("52WW-lw2SrOpgoHFJzh0Kg"), Id("C9mJEx_gTX2gi5vFj2AHqw"), Id("mJTIBVyBRgWpHq8zERv0kg")]
    yield ids


@pytest.fixture(scope="session")
def model_metadata_detail_list(
    model_metadata_ids: Sequence[Id],
) -> Generator[Sequence[ModelMetadataDetail], None, None]:
    data = [
        ModelMetadataDetailFactory.build(
            id=model_metadata_ids[0],
            created_at=Timestamp(1681102727441831),
            updated_at=Timestamp(1681102727441835),
            name="ping",
            description="this is the ping",
            version="0.1.0",
            inputs=[
                LongTextInput(
                    id=Id("_IIA5p11QgSUlFm7k2wj3A"),
                    created_at=Timestamp(1681102727441761),
                    updated_at=Timestamp(1681102727441772),
                    field_name="message",
                )
            ],
        ),
        ModelMetadataDetailFactory.build(
            id=model_metadata_ids[1],
            created_at=Timestamp(1681012647318673),
            updated_at=Timestamp(1681012647318711),
            name="echo",
            description="this is the echo",
            version="0.1.0",
            inputs=[
                LongTextInput(
                    id=Id("O99SxID2QSChcx2aTSaFNA"),
                    created_at=Timestamp(1681102727441761),
                    updated_at=Timestamp(1681102727441772),
                    field_name="message",
                )
            ],
        ),
        ModelMetadataDetailFactory.build(
            id=model_metadata_ids[2],
            created_at=Timestamp(1681012967478480),
            updated_at=Timestamp(1681012967478493),
            name="pong",
            description="this is the pong",
            version="0.1.1",
            inputs=[
                LongTextInput(
                    id=Id("SEtNn-cGQp66V6flBNO2GQ"),
                    created_at=Timestamp(1681102727441761),
                    updated_at=Timestamp(1681102727441772),
                    field_name="message",
                )
            ],
        ),
    ]
    yield data


@pytest.fixture(scope="session")
def model_metadata_list(
    model_metadata_detail_list: Sequence[ModelMetadataDetail],
) -> Generator[Sequence[ModelMetadata], None, None]:
    yield [ModelMetadata(**m.dict()) for m in model_metadata_detail_list]


@pytest.fixture(scope="session")
def dialogue_ids() -> Generator[Sequence[Id], None, None]:
    yield [
        Id("hCy6ZRX6RpWiNCkEx8PwyA"),
        Id('UBwpUv57Sh6XNzGsUmF5jw'),
        Id('or9FYegbTkWQh1_CFIsJiw'),
        Id('93KkiQUbQ3GmdOxkV-ET9Q'),
        Id('IhgttuvNSxGZzdqGVhz4yw'),
        Id('s9H2iEswRjStaXPigzknVA'),
    ]


@pytest.fixture(scope="session")
def dialogue_list(
    model_metadata_list: Sequence[ModelMetadata], dialogue_ids: Sequence[Id], user: User, other_user: User
) -> Generator[Sequence[Dialogue], None, None]:
    yield [
        DialogueFactory.build(
            model_id=model_metadata_list[0].id,
            id=dialogue_ids[0],
            owner_id=user.id,
            created_at=Timestamp(1681609003878453),
            updated_at=Timestamp(1681609003878583),
        ),
        DialogueFactory.build(
            model_id=model_metadata_list[0].id,
            id=dialogue_ids[1],
            owner_id=user.id,
            created_at=Timestamp(1681609003878846),
            updated_at=Timestamp(1681609003878962),
        ),
        DialogueFactory.build(
            model_id=model_metadata_list[1].id,
            id=dialogue_ids[2],
            owner_id=user.id,
            created_at=Timestamp(1681609003879122),
            updated_at=Timestamp(1681609003879236),
        ),
        DialogueFactory.build(
            model_id=model_metadata_list[1].id,
            id=dialogue_ids[3],
            owner_id=user.id,
            created_at=Timestamp(1681609003879390),
            updated_at=Timestamp(1681609003879502),
        ),
        DialogueFactory.build(
            model_id=model_metadata_list[0].id,
            id=dialogue_ids[4],
            owner_id=other_user.id,
            created_at=Timestamp(1681609003879655),
            updated_at=Timestamp(1681609003879763),
        ),
        DialogueFactory.build(
            model_id=model_metadata_list[1].id,
            id=dialogue_ids[5],
            owner_id=other_user.id,
            created_at=Timestamp(1681609003879913),
            updated_at=Timestamp(1681609003880021),
        ),
    ]


@pytest.fixture(scope="function")
def storage(
    model_metadata_detail_list: Sequence[ModelMetadataDetail],
    model_metadata_list: Sequence[ModelMetadata],
    dialogue_list: Sequence[Dialogue],
) -> Generator[BaseStorage, None, None]:
    s = MagicMock(spec=BaseStorage)
    s.list_model_metadata.return_value = model_metadata_list

    def list_dialogues(user_id: UserId) -> Sequence[Dialogue]:
        return [d for d in dialogue_list if d.owner_id == user_id]

    s.list_dialogues.side_effect = list_dialogues

    def retrieve_dialogue(dialogue_id: Id, user_id: UserId) -> Dialogue:
        for d in dialogue_list:
            if d.id == dialogue_id and d.owner_id == user_id:
                return d
        raise DialogueNotFoundError(dialogue_id=dialogue_id)

    s.retrieve_dialogue.side_effect = retrieve_dialogue

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
def valid_auth_provider(user: User) -> Generator[BaseAuthProvider, None, None]:
    class MockAuthProvider(BaseAuthProvider):
        def get_user_token(
            self, response: Response, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
        ) -> User:
            if credentials is None:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return user

    yield MockAuthProvider()


@pytest.fixture(scope="session")
def invalid_auth_provider() -> Generator[BaseAuthProvider, None, None]:
    class MockAuthProvider(BaseAuthProvider):
        def get_user_token(
            self, response: Response, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
        ) -> User:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    yield MockAuthProvider()
