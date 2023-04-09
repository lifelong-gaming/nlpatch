from abc import ABCMeta, abstractmethod
from collections.abc import Sequence

from ..types import ModelMetadata


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def list_model_metadata(self) -> Sequence[ModelMetadata]:
        ...
