import json
from typing import Type

from jotbox.types import TPayload


_JSON_ENCODERS: dict = {}


def make_json_encoder(t: Type[TPayload]):
    if t not in _JSON_ENCODERS:
        _JSON_ENCODERS[t] = type(
            "CustomJsonEncoder",
            (json.JSONEncoder,),
            {"default": lambda self, x: t.__json_encoder__(x)},
        )
    return _JSON_ENCODERS[t]
