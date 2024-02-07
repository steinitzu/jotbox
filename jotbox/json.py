import json
from typing import Type, Optional

from jotbox.types import TPayload
from jotbox.compat import pydantic_major_version


_JSON_ENCODERS: dict = {}


def make_json_encoder(t: Type[TPayload]) -> Optional[Type[json.JSONEncoder]]:
    if pydantic_major_version > 1:
        return None
    if t not in _JSON_ENCODERS:
        _JSON_ENCODERS[t] = type(
            "CustomJsonEncoder",
            (json.JSONEncoder,),
            {"default": lambda self, x: t.__json_encoder__(x)},  # type: ignore[attr-defined]
        )
    return _JSON_ENCODERS[t]
