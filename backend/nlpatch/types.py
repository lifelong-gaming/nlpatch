from collections.abc import Mapping
from typing import AbstractSet, Any, Dict, Optional, Union

from pydantic import BaseModel as _BaseModel
from pydantic import Field

from .fields import Bytes, Id, Timestamp, UserId
from .utils import Camelizer


class BaseType(_BaseModel):
    class Config:
        allow_mutation = False
        alias_generator = Camelizer(["id"])
        allow_population_by_field_name = True

    def dict(
        self,
        *,
        include: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], None] = None,
        exclude: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], None] = None,
        by_alias: bool = True,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        return super(BaseType, self).dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )


class User(BaseType):
    id: UserId


class BaseEntity(BaseType):
    id: Id = Field(default_factory=Id.generate)
    created_at: Timestamp = Field(default_factory=Timestamp.now)
    updated_at: Timestamp = Field(default_factory=Timestamp.now)


class ModelMetadata(BaseEntity):
    name: str
    description: str
    version: str


class BaseUserEntity(BaseEntity):
    owner: User


class Blob(BaseEntity):
    data: Bytes
