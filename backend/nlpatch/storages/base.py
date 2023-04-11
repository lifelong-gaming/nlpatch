from abc import ABCMeta, abstractmethod
from collections.abc import Sequence

from ..fields import Id
from ..types import ModelMetadata, ModelMetadataDetail


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def list_model_metadata(self) -> Sequence[ModelMetadata]:
        ...

    @abstractmethod
    def retrieve_model_metadata(self, model_id: Id) -> ModelMetadataDetail:
        ...
