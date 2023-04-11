import os
from tempfile import TemporaryDirectory

from nlpatch.fields import Id, InputType, Timestamp
from nlpatch.storages.local_file import LocalFileStorage
from nlpatch.types import BaseInput, ModelMetadata, ModelMetadataDetail

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


def test_local_storage_retrieve_model_metadata() -> None:
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
