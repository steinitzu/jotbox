from datetime import datetime
from typing import TypeVar, Generic, Union, Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel


StrBytes = Union[str, bytes]


class Payload(BaseModel):
    class Config:
        json_encoders = {UUID: lambda v: v.hex}

    jti: UUID
    iat: int
    exp: Optional[int]


class ExpiringPayload(Payload):
    exp: int


TPayload = TypeVar("TPayload", bound=Payload)
TExpiringPayload = TypeVar("TExpiringPayload", bound=ExpiringPayload)


class EncodedToken(GenericModel, Generic[TPayload]):
    payload: TPayload
    token: str


DateTimeStamp = Union[datetime, float]


TSub = TypeVar("TSub")


class Session(GenericModel, Generic[TSub], Payload):
    sub: TSub


TSession = TypeVar("TSession", bound=Session)
