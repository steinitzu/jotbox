from typing import Union, Optional

from aredis import StrictRedis


from jotbox.types import TPayload, DateTimeStamp
from jotbox.util import timestamp_ms, now_ms
from jotbox.whitelist.base import BaseWhitelist


RedisOrURL = Union[StrictRedis, str]


class RedisWhitelist(BaseWhitelist[TPayload]):
    def __init__(self, redis: RedisOrURL, key_prefix: str = "JB:WHITE:") -> None:
        self.key_prefix = key_prefix
        if isinstance(redis, str):
            self.redis = StrictRedis.from_url(redis)
        else:
            self.redis = redis

    async def add(self, payload: TPayload, until: Optional[DateTimeStamp]) -> None:
        px = None
        if until:
            px = timestamp_ms(until) - now_ms()
        key = self.make_key(payload)
        await self.redis.set(key, 1, px=px, nx=True)

    async def touch(self, payload: TPayload, until: DateTimeStamp) -> bool:
        key = self.make_key(payload)
        px = timestamp_ms(until) - now_ms()
        return bool(await self.redis.pexpire(key, px))

    async def exists(self, payload: TPayload) -> bool:
        return bool(await self.redis.exists(self.make_key(payload)))

    async def delete(self, payload: TPayload) -> None:
        await self.redis.delete(self.make_key(payload))

    def make_key(self, payload: TPayload) -> str:
        return self.key_prefix + payload.jti.hex
