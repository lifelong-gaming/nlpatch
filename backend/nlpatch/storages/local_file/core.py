import os
from collections.abc import Sequence
from typing import List

from ...fields import Id, UserId
from ...types import Dialogue, ModelMetadata, ModelMetadataDetail
from ..base import BaseStorage


class LocalFileStorage(BaseStorage):
    """
    Local file storage.

    Attributes:
        root_path: The root path of the local file storage.

    >>> storage = LocalFileStorage(root_path="/tmp")
    >>> storage.root_path
    '/tmp'
    """

    def __init__(self, root_path: str) -> None:
        self._root_path = root_path

    @property
    def root_path(self) -> str:
        return self._root_path

    def list_model_metadata(self) -> Sequence[ModelMetadata]:
        res: List[ModelMetadata] = []
        dirname = os.path.join(self.root_path, "model_metadata")
        if not os.path.exists(dirname):
            return res
        for fn in os.listdir(dirname):
            with open(os.path.join(dirname, fn), "rb") as f:
                res.append(ModelMetadata.parse_raw(f.read()))
        return res

    def retrieve_model_metadata(self, model_id: Id) -> ModelMetadataDetail:
        dirname = os.path.join(self.root_path, "model_metadata")
        with open(os.path.join(dirname, f"{model_id}.json"), "rb") as f:
            return ModelMetadataDetail.parse_raw(f.read())

    def list_dialogues(self, user_id: UserId) -> Sequence[Dialogue]:
        raise NotImplementedError()

    def retrieve_dialogue(self, user_id: UserId, dialogue_id: Id) -> Dialogue:
        raise NotImplementedError()
