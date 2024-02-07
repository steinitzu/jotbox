import pytest
import secrets
import time

from redis.asyncio import Redis

from jotbox import Jotbox, Payload
from jotbox.whitelist.redis import RedisWhitelist


@pytest.fixture
def redis_jotbox(redis_whitelist):
    return Jotbox(encode_key=secrets.token_urlsafe(), whitelist=redis_whitelist)


def jti_key(jti):
    return f"JB:WHITE:{jti}"


class TestRedisWhitelist:
    def test__create_whitelist_from_url(self, redis_uri):

        wl = RedisWhitelist[Payload](redis_uri)

        assert isinstance(wl.redis, Redis)

    @pytest.mark.asyncio
    async def test__add__adds_key(self, redis_jotbox):
        payload = redis_jotbox.create_payload()
        until = time.time() + 30

        await redis_jotbox.whitelist.add(payload, until)

        redis = redis_jotbox.whitelist.redis
        key = jti_key(payload.jti)
        assert await redis.get(jti_key(payload.jti)) is not None
        ttl = await redis.ttl(key)
        assert 29 <= ttl <= 30

    @pytest.mark.asyncio
    async def test__touch__existing__updates_px_return_true(self, redis_jotbox):
        until = time.time() + 30
        payload = redis_jotbox.create_payload()
        whitelist = redis_jotbox.whitelist
        await whitelist.add(payload, until)

        until_touch = until + 20
        ret = await whitelist.touch(payload, until_touch)
        ttl = await whitelist.redis.ttl(jti_key(payload.jti))

        assert ret is True
        assert 49 <= ttl <= 50

    @pytest.mark.asyncio
    async def test__touch__not_existing__key_not_exist_return_false(self, redis_jotbox):
        payload = redis_jotbox.create_payload()
        whitelist = redis_jotbox.whitelist

        until_touch = time.time() + 20
        ret = await whitelist.touch(payload, until_touch)
        exists = bool(await whitelist.redis.exists(jti_key(payload.jti)))

        assert ret is False and exists is False

    @pytest.mark.asyncio
    async def test__exists__not_exists__returns_false(self, redis_jotbox):
        payload = redis_jotbox.create_payload()
        whitelist = redis_jotbox.whitelist

        ret = await whitelist.exists(payload)

        assert ret is False

    @pytest.mark.asyncio
    async def test__exists__exists__returns_true(self, redis_jotbox):
        payload = redis_jotbox.create_payload()
        whitelist = redis_jotbox.whitelist
        await whitelist.add(payload, None)

        ret = await whitelist.exists(payload)

        assert ret is True

    @pytest.mark.asyncio
    async def test__delete__deletes_key(self, redis_jotbox):
        payload = redis_jotbox.create_payload()
        whitelist = redis_jotbox.whitelist
        await whitelist.add(payload, None)

        await whitelist.delete(payload)

        assert bool(await whitelist.redis.exists(jti_key(payload.jti))) is False
