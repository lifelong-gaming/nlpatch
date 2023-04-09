import os
from tempfile import TemporaryDirectory

from nlpatch.storages.local_file import LocalFileStorage
from nlpatch.types import ModelMetadata

wd = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(wd, "fixtures")


def test_local_storage_settings() -> None:
    sut = LocalFileStorage(root_path="/tmp")
    assert sut.root_path == "/tmp"


def test_local_storage_list_model_metadata() -> None:
    expected = []
    for fn in os.listdir(os.path.join(fixture_path, "model_metadata")):
        with open(os.path.join(fixture_path, "model_metadata", fn), "rb") as f:
            expected.append(ModelMetadata.parse_raw(f.read()))
    sut = LocalFileStorage(root_path=fixture_path)
    actual = sut.list_model_metadata()
    assert actual == expected


def test_local_storage_list_model_metadata_returns_empty_if_directory_not_exists() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalFileStorage(root_path=tmpdir)
        actual = sut.list_model_metadata()
        assert actual == []
