import math
from typing import Generic, Dict, Any, Type, Sequence, Optional, cast
from uuid import uuid4
import time

from jwt import decode as jwt_decode, encode as jwt_encode, PyJWTError


from jotbox.types import EncodedToken, StrBytes, TPayload, Payload
from jotbox.json import make_json_encoder
from jotbox.whitelist.base import Whitelist
from jotbox.exceptions import JWTDecodeError, RevokedTokenError


class Jotbox(Generic[TPayload]):
    whitelist: Optional[Whitelist]

    def __init__(
        self,
        *,
        encode_key: StrBytes,
        payload_type: Type[TPayload] = cast(Type[TPayload], Payload),
        decode_key: Optional[StrBytes] = None,
        encode_algorithm: str = "HS512",
        decode_algorithms: Sequence[str] = ("HS512",),
        leeway: int = 0,
        expires_in: Optional[int] = None,
        idle_timeout: Optional[int] = None,
        whitelist: Optional[Whitelist[TPayload]] = None,
        jwt_options: Dict[str, bool] = None,
    ) -> None:
        if idle_timeout is not None and whitelist is None:
            raise ValueError("idle_timeout is not possible without whitelist")
        self.payload_type = payload_type
        self.encode_key = encode_key
        self.decode_key = decode_key if decode_key is not None else encode_key
        self.encode_algorithm = encode_algorithm
        self.decode_algorithms = decode_algorithms
        self.leeway = leeway
        self.expires_in = expires_in
        self.idle_timeout = idle_timeout
        self.jwt_options = jwt_options
        self.whitelist = whitelist

        self.encoded_token_type = EncodedToken[self.payload_type]  # type: ignore

    def _create_payload_dict(self, **claims) -> Dict[str, Any]:
        iat = math.floor(time.time())
        claims = dict(claims, jti=uuid4(), iat=iat)
        if self.expires_in is not None and "exp" not in claims:
            claims["exp"] = claims["iat"] + self.expires_in
        return claims

    def create_payload(self, **claims) -> TPayload:
        return self.payload_type(**self._create_payload_dict(**claims))

    def _create_until(self, exp: Optional[int]) -> Optional[float]:
        if self.idle_timeout is None:
            return exp + self.leeway if exp is not None else None
        else:
            idle_until = time.time() + self.idle_timeout + self.leeway
        if exp is None:
            return idle_until
        return min(idle_until, exp + self.leeway)

    async def add_to_whitelist(self, payload: TPayload) -> None:
        if not self.whitelist:
            return
        until = self._create_until(payload.exp)
        await self.whitelist.add(payload, until)

    async def create_token(
        self, _payload: Optional[TPayload] = None, **claims
    ) -> EncodedToken[TPayload]:
        encoded = self.encode_payload(_payload=_payload, **claims)
        await self.add_to_whitelist(encoded.payload)
        return encoded

    def encode_payload(
        self, _payload: Optional[TPayload] = None, **claims
    ) -> EncodedToken[TPayload]:
        payload = _payload or self.create_payload(**claims)
        token = jwt_encode(
            payload.dict(exclude_unset=True),
            key=self.encode_key,
            algorithm=self.encode_algorithm,
            json_encoder=make_json_encoder(self.payload_type),
        ).decode()
        return self.encoded_token_type(token=token, payload=payload)

    async def verified_payload(self, token: str, **jwt_kwargs) -> TPayload:
        try:
            raw_payload = jwt_decode(
                token,
                key=self.decode_key,
                algorithms=self.decode_algorithms,
                options=self.jwt_options,
                leeway=self.leeway,
                **jwt_kwargs,
            )
        except PyJWTError as e:
            raise JWTDecodeError("Failed to decode token") from e
        payload = self.payload_type(**raw_payload)
        await self._verify_whitelist(payload)
        return payload

    async def _verify_whitelist(self, payload: TPayload) -> None:
        if not self.whitelist:
            return
        if self.idle_timeout:
            until = cast(float, self._create_until(payload.exp))
            exists = await self.whitelist.touch(payload, until)
        else:
            exists = await self.whitelist.exists(payload)
        if not exists:
            raise RevokedTokenError(f"Token ID {payload.jti} has been revoked")

    async def revoke_payload(self, payload: TPayload) -> None:
        if not self.whitelist:
            raise NotImplementedError(
                "This operation is not supported without whitelist"
            )
        await self.whitelist.delete(payload)
