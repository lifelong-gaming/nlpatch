from abc import ABCMeta, abstractmethod
from collections.abc import Sequence

from ..fields import Id, UserId
from ..types import Dialogue, ModelMetadata, ModelMetadataDetail


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def list_model_metadata(self) -> Sequence[ModelMetadata]:
        ...

    @abstractmethod
    def retrieve_model_metadata(self, model_id: Id) -> ModelMetadataDetail:
        ...

    @abstractmethod
    def list_dialogues(self, user_id: UserId) -> Sequence[Dialogue]:
        ...

    @abstractmethod
    def retrieve_dialogue(self, user_id: UserId, dialogue_id: Id) -> Dialogue:
        ...

    @abstractmethod
    def create_dialogue(self, dialogue: Dialogue) -> Dialogue:
        ...

    @abstractmethod
    def delete_dialogue(self, user_id: UserId, dialogue_id: Id) -> None:
        ...
