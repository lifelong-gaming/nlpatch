import os
from tempfile import TemporaryDirectory
from typing import Sequence

import pytest

from nlpatch.fields import Id
from nlpatch.storages.exceptions import ModelMetadataNotFoundError
from nlpatch.storages.local_file import LocalFileStorage
from nlpatch.types import ModelMetadata, ModelMetadataDetail

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


def test_retrieve_model_metadata(model_metadata_detail_list: Sequence[ModelMetadataDetail]) -> None:
    model_id = Id("52WW-lw2SrOpgoHFJzh0Kg")
    expected = model_metadata_detail_list[0]
    sut = LocalFileStorage(root_path=fixture_path)
    actual = sut.retrieve_model_metadata(model_id)
    assert actual == expected


def test_retrieve_model_metadata_raises_error_if_file_not_exists() -> None:
    model_id = Id("0iISHMyJRdmoAF8yoyy6jA")
    sut = LocalFileStorage(root_path=fixture_path)
    with pytest.raises(ModelMetadataNotFoundError):
        sut.retrieve_model_metadata(model_id)
