from typing import Type

from ..exceptions import BaseError
from ..fields import Id
from ..types import BaseType, Blob, ModelMetadata


class StorageError(BaseError):
    """Base exception class for storage errors."""

    pass


class EntityNotFoundError(StorageError, KeyError):
    """Raised when an entity is not found in storage."""

    def __init__(self, entity_id: Id, type: Type[BaseType]):
        super().__init__(f"{type.__name__} with ID {entity_id} not found")


class BlobNotFoundError(EntityNotFoundError):
    """Raised when a blob is not found in storage."""

    def __init__(self, blob_id: Id):
        super().__init__(blob_id, Blob)


class ModelMetadataNotFoundError(EntityNotFoundError):
    """Raised when a model metadata is not found in storage."""

    def __init__(self, model_id: Id):
        super().__init__(model_id, ModelMetadata)
