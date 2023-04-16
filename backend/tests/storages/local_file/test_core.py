import os
from tempfile import TemporaryDirectory
from typing import Sequence

import pytest

from nlpatch.fields import Id, InputType, Timestamp
from nlpatch.storages.exceptions import ModelMetadataNotFoundError
from nlpatch.storages.local_file import LocalFileStorage
from nlpatch.types import BaseInput, ModelMetadata, ModelMetadataDetail

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


def test_retrieve_model_metadata() -> None:
    model_id = Id("52WW-lw2SrOpgoHFJzh0Kg")
    expected = ModelMetadataDetail(
        id=model_id,
        name="ping",
        description="this is the ping",
        created_at=Timestamp(1681102727441831),
        updated_at=Timestamp(1681102727441835),
        version="0.1.0",
        inputs=[
            BaseInput(
                id=Id("_IIA5p11QgSUlFm7k2wj3A"),
                created_at=Timestamp(1681102727441761),
                updated_at=Timestamp(1681102727441772),
                field_name="message",
                type=InputType.LONG_TEXT,
            )
        ],
    )
    sut = LocalFileStorage(root_path=fixture_path)
    actual = sut.retrieve_model_metadata(model_id)
    assert actual == expected


def test_retrieve_model_metadata_raises_error_if_file_not_exists() -> None:
    model_id = Id("0iISHMyJRdmoAF8yoyy6jA")
    sut = LocalFileStorage(root_path=fixture_path)
    with pytest.raises(ModelMetadataNotFoundError):
        sut.retrieve_model_metadata(model_id)
