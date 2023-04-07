from nlpatch.settings import GlobalSettings, AuthProviderType, StorageType
from nlpatch.storages.local_file.settings import LocalFileStorageSettings


def test_from_global_settings() -> None:
    settings = GlobalSettings(
        auth_provider=AuthProviderType.FIREBASE,
        auth_provider_settings={},
        storage_type=StorageType.LOCAL_FILE,
        storage_settings={"root_path": "/tmp"},
        origins=[],
    )
    storage_settings = LocalFileStorageSettings.from_global_settings(settings)
    assert storage_settings.root_path == "/tmp"
