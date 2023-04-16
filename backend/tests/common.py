from collections.abc import Mapping
from typing import Any, Type

from pytest_mock import MockerFixture

from nlpatch.types import BaseType


def override_defaults(mocker: MockerFixture, model: Type[BaseType], overrides: Mapping[str, Any]) -> None:
    for k, v in overrides.items():
        mocker.patch.object(model.__fields__[k], "default_factory", return_value=v)
