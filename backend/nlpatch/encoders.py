from json import JSONEncoder
from typing import Any

from .fields import Serializable
from .types import BaseType


class Encoder(JSONEncoder):
    """
    >>> from nlpatch.fields import Timestamp, Bytes, Id, InputType
    >>> a = {"id": Id("T3HW7dZ5SjCtODQLQkY8eA"), "data": Bytes(b"kenbun"), "created_at": Timestamp(1610000000), "input_type": InputType.LONG_TEXT}
    >>> Encoder().encode(a)
    '{"id": "T3HW7dZ5SjCtODQLQkY8eA", "data": "a2VuYnVu", "created_at": 1610000000, "input_type": "longText"}'
    >>> class A(BaseType):
    ...     id: Id
    ...     data: Bytes
    ...     created_at: Timestamp
    ...     input_type: InputType
    >>> a = A(**a)
    >>> Encoder().encode(a)
    '{"id": "T3HW7dZ5SjCtODQLQkY8eA", "data": "a2VuYnVu", "createdAt": 1610000000, "inputType": "longText"}'
    """  # noqa: E501

    def default(self, o: Any) -> Any:
        if isinstance(o, BaseType):
            return o.dict()
        if isinstance(o, Serializable):
            return o.serialize()
        return super().default(o)
