from ..settings import GlobalSettings, StorageType
from .base import BaseStorage
from .local_file.core import LocalFileStorage
from .local_file.settings import LocalFileStorageSettings


def create_storage(settings: GlobalSettings) -> BaseStorage:
    if settings.storage_type == StorageType.LOCAL_FILE:
        storage_settings = LocalFileStorageSettings.from_global_settings(settings=settings)
        return LocalFileStorage(root_path=storage_settings.root_path)
    else:
        raise ValueError(f"Unknown storage: {settings.storage_type}")
