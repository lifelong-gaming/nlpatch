from ...settings import GlobalSettings
from ..settings import BaseStorageSettings


class LocalFileStorageSettings(BaseStorageSettings):
    """
    Settings for the local file storage backend.

    Attributes:
        root_path: The root path of the local file storage.

    >>> settings = LocalFileStorageSettings(root_path="/tmp")
    >>> settings.root_path
    '/tmp'
    """

    root_path: str

    @classmethod
    def from_global_settings(
        cls: type["LocalFileStorageSettings"], settings: GlobalSettings
    ) -> "LocalFileStorageSettings":
        """
        Create a new instance of the settings from the global settings.

        Args:
            settings: The global settings.

        Returns:
            The new instance of the settings.

        >>> settings = GlobalSettings(storage_settings={"root_path": "/tmp"})
        >>> LocalFileStorageSettings.from_global_settings(settings).root_path
        '/tmp'
        """

        return cls(root_path=settings.storage_settings["root_path"])
