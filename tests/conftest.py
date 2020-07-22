import os
import pytest

from aredis import StrictRedis

from jotbox.whitelist.redis import RedisWhitelist

REDIS_URI = os.getenv("TEST_REDIS_URI")


@pytest.fixture(scope="session")
def redis():
    return StrictRedis.from_url(REDIS_URI)


@pytest.fixture()
async def redis_whitelist(redis):
    return RedisWhitelist(redis)
