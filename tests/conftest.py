import os
import pytest
import asyncio

from aredis import StrictRedis

from jotbox.whitelist.redis import RedisWhitelist


@pytest.fixture(scope="session")
def redis_uri():
    return os.environ["TEST_REDIS_URI"]


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    """
    https://github.com/pytest-dev/pytest-asyncio/issues/38
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def redis(redis_uri):
    r = StrictRedis.from_url(redis_uri)
    try:
        yield r
    finally:
        await r.flushall()


@pytest.fixture()
async def redis_whitelist(redis):
    return RedisWhitelist(redis)
