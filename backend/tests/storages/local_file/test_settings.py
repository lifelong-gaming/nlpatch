from nlpatch.settings import GlobalSettings, StorageType
from nlpatch.storages.local_file.settings import LocalFileStorageSettings


def test_local_storage_settings() -> None:
    sut = LocalFileStorageSettings(root_path="/tmp")
    assert sut.root_path == "/tmp"


def test_local_storage_settings_from_global_settings() -> None:
    sut = LocalFileStorageSettings.from_global_settings(
        GlobalSettings(storage_type=StorageType.LOCAL_FILE, storage_settings={"root_path": "/tmp"})
    )
    assert sut.root_path == "/tmp"
