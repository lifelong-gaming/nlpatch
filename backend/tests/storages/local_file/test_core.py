import os
from tempfile import TemporaryDirectory
from typing import Sequence

import pytest

from nlpatch.fields import Id, UserId
from nlpatch.storages.exceptions import (
    DialogueNotFoundError,
    ModelMetadataNotFoundError,
)
from nlpatch.storages.local_file import LocalFileStorage
from nlpatch.types import Dialogue, ModelMetadata, ModelMetadataDetail, User

wd = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(wd, "fixtures")


def test_local_file_settings() -> None:
    sut = LocalFileStorage(root_path="/tmp")
    assert sut.root_path == "/tmp"


def test_list_model_metadata(model_metadata_list: Sequence[ModelMetadata]) -> None:
    expected = sorted(model_metadata_list, key=lambda x: x.id)
    sut = LocalFileStorage(root_path=fixture_path)
    actual = sut.list_model_metadata()
    assert sorted(actual, key=lambda x: x.id) == expected


def test_list_model_metadata_returns_empty_if_directory_not_exists() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalFileStorage(root_path=tmpdir)
        actual = sut.list_model_metadata()
        assert actual == []


def test_retrieve_model_metadata(
    model_metadata_ids: Sequence[Id], model_metadata_detail_list: Sequence[ModelMetadataDetail]
) -> None:
    model_id = model_metadata_ids[0]
    expected = model_metadata_detail_list[0]
    sut = LocalFileStorage(root_path=fixture_path)
    actual = sut.retrieve_model_metadata(model_id)
    assert actual == expected


def test_retrieve_model_metadata_raises_error_if_file_not_exists() -> None:
    model_id = Id("0iISHMyJRdmoAF8yoyy6jA")
    sut = LocalFileStorage(root_path=fixture_path)
    with pytest.raises(ModelMetadataNotFoundError):
        sut.retrieve_model_metadata(model_id)


def test_list_dialogues(dialogue_list: Sequence[Dialogue], user: User) -> None:
    sut = LocalFileStorage(root_path=fixture_path)
    actual = sut.list_dialogues(user_id=user.id)
    assert sorted(actual, key=lambda x: x.id) == sorted(dialogue_list[:4], key=lambda x: x.id)


def test_list_dialogues_returns_empty_if_directory_not_exists() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalFileStorage(root_path=tmpdir)
        actual = sut.list_dialogues(user_id=UserId("dummy"))
        assert actual == []


def test_retrieve_dialogue(dialogue_list: Sequence[Dialogue], dialogue_ids: Sequence[Id], user: User) -> None:
    sut = LocalFileStorage(root_path=fixture_path)
    actual = sut.retrieve_dialogue(user_id=user.id, dialogue_id=dialogue_ids[0])
    assert actual == dialogue_list[0]


def test_retieve_dialogue_raises_error_if_file_not_exists() -> None:
    sut = LocalFileStorage(root_path=fixture_path)
    with pytest.raises(DialogueNotFoundError):
        sut.retrieve_dialogue(user_id=UserId("dummy"), dialogue_id=Id("a1EX4W5JSqCO-WFTAfWvxQ"))


def test_retrieve_dialogue_raises_error_if_directory_not_exists() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalFileStorage(root_path=tmpdir)
        with pytest.raises(DialogueNotFoundError):
            sut.retrieve_dialogue(user_id=UserId("dummy"), dialogue_id=Id("a1EX4W5JSqCO-WFTAfWvxQ"))


def test_retrieve_dialogue_raises_error_if_owner_not_matched(dialogue_ids: Sequence[Id], other_user_id: UserId) -> None:
    sut = LocalFileStorage(root_path=fixture_path)
    with pytest.raises(DialogueNotFoundError):
        sut.retrieve_dialogue(user_id=other_user_id, dialogue_id=dialogue_ids[0])


def test_create_dialogue(dialogue_list: Sequence[Dialogue]) -> None:
    dialogue = dialogue_list[0]
    with TemporaryDirectory() as tmpdir:
        sut = LocalFileStorage(root_path=tmpdir)
        sut.create_dialogue(dialogue=dialogue)
        with open(os.path.join(tmpdir, "dialogues", f"{dialogue.id}.json"), "r") as f:
            actual = Dialogue.parse_raw(f.read())
        assert actual == dialogue
