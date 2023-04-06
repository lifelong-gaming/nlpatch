from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any
import io
import csv
from enum import Enum
from pydantic import BaseSettings as _BaseSettings

S = TypeVar("S", bound="BaseSettings")


class AuthProviderType(str, Enum):
    FIREBASE = "firebase"


class StorageType(str, Enum):
    LOCAL_FILE = "local_file"


class BaseSettings(_BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


class GlobalSettings(BaseSettings):
    auth_provider: AuthProviderType = AuthProviderType.FIREBASE
    auth_provider_settings: dict[str, Any] = {}
    storage_type: StorageType = StorageType.LOCAL_FILE
    storage_settings: dict[str, Any] = {}
    origins: list[str] = []

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == 'origins':
                if raw_val == '':
                    return []
                return list(filter(lambda x: len(x) > 1, next(csv.reader(io.StringIO(raw_val)))))
            return cls.json_loads(raw_val)


class BaseComponentSettings(BaseSettings, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_global_settings(cls: type[S], settings: GlobalSettings) -> S:
        raise NotImplementedError
