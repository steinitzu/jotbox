from datetime import datetime
from typing import TypeVar, Generic, Union, Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel

from jotbox.compat import pydantic_major_version


if pydantic_major_version == 2:
    from pydantic import field_serializer  # type: ignore[attr-defined]


StrBytes = Union[str, bytes]


class Payload(BaseModel):
    class Config:
        if pydantic_major_version == 2:
            json_encoders = {UUID: lambda v: v.hex}

    jti: UUID
    iat: int
    exp: Optional[int] = None

    if pydantic_major_version == 2:

        @field_serializer("jti", when_used="json-unless-none")
        def serialize_jti(self, v: UUID) -> str:
            return v.hex


class ExpiringPayload(Payload):
    exp: int


TPayload = TypeVar("TPayload", bound=Payload)
TExpiringPayload = TypeVar("TExpiringPayload", bound=ExpiringPayload)


class EncodedToken(GenericModel, Generic[TPayload]):
    payload: TPayload
    token: str


DateTimeStamp = Union[datetime, float]


TSub = TypeVar("TSub")


class Session(Payload, GenericModel, Generic[TSub]):
    sub: TSub


TSession = TypeVar("TSession", bound=Session)
