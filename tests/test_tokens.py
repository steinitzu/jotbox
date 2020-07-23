import time
from secrets import token_urlsafe
import math
import json
from unittest import mock

import pytest
import asyncmock
import jwt

from jotbox import Jotbox
from jotbox import tokens

KEY = token_urlsafe()


class TestCreatePayload:
    @pytest.mark.asyncio
    async def test__exp_is_added(self):
        expires_in = 4400
        jot = Jotbox(encode_key=KEY, expires_in=4400)

        payload = jot.create_payload()

        assert payload.exp == math.floor(time.time() + expires_in)


class TestVerifiedPayload:
    @pytest.mark.asyncio
    async def test__args_passed_to_pyjwt(self):
        jot = Jotbox(
            encode_key=KEY,
            expires_in=4400,
            leeway=30,
            jwt_options=dict(require_exp=True, require_iat=True),
        )

        payload = jot.create_payload()
        payload_raw = json.loads(payload.json(exclude_unset=True))
        token = await jot.create_token(payload)

        with mock.patch.object(
            tokens, "jwt_decode", autospec=True, return_value=payload_raw
        ) as m:
            _ = await jot.verified_payload(token.token)

        m.assert_called_once_with(
            token.token,
            key=KEY,
            algorithms=jot.decode_algorithms,
            leeway=jot.leeway,
            options=jot.jwt_options,
        )

    @pytest.mark.asyncio
    async def test__idle_timeout__calls_whitelist_with_until(self, redis_whitelist):
        jot = Jotbox(
            encode_key=KEY,
            expires_in=4400,
            leeway=30,
            jwt_options=dict(require_exp=True, require_iat=True),
            whitelist=redis_whitelist,
            idle_timeout=300,
        )

        payload = jot.create_payload()
        payload_raw = json.loads(payload.json(exclude_unset=True))
        token = await jot.create_token(payload)

        with mock.patch.object(
            tokens, "jwt_decode", autospec=True, return_value=payload_raw
        ) as m:
            _ = await jot.verified_payload(token.token)

        raise NotImplementedError("Test not complete")


class TestAddToWhitelist:
    @pytest.mark.asyncio
    async def test__idle_timeout_no_exp__until_correct(self, redis_whitelist):
        jot = Jotbox(
            encode_key=KEY, leeway=10, idle_timeout=3600, whitelist=redis_whitelist
        )
        payload = jot.create_payload()

        start = time.time()
        with asyncmock.patch.object(
            jot.whitelist, "add", autospec=True, return_value=None
        ) as m:
            await jot.add_to_whitelist(payload)
        now = time.time()
        until = m.await_args[0][1]

        m.assert_awaited_once()
        assert until >= start + jot.leeway + jot.idle_timeout
        assert until <= now + jot.leeway + jot.idle_timeout

    @pytest.mark.asyncio
    async def test__exp_no_idle_timeout__until_correct(self, redis_whitelist):
        jot = Jotbox(
            encode_key=KEY, leeway=10, expires_in=3500, whitelist=redis_whitelist
        )
        payload = jot.create_payload()

        start = time.time()
        with asyncmock.patch.object(
            jot.whitelist, "add", autospec=True, return_value=None
        ) as m:
            await jot.add_to_whitelist(payload)
        now = time.time()
        until = m.await_args[0][1]

        m.assert_awaited_once()
        assert until >= math.floor(start + jot.leeway + jot.expires_in)
        assert until <= now + jot.leeway + jot.expires_in

    @pytest.mark.asyncio
    async def test__exp_and_idle_timeout_lower__until_correct(self, redis_whitelist):

        jot = Jotbox(
            encode_key=KEY,
            leeway=10,
            expires_in=3500,
            whitelist=redis_whitelist,
            idle_timeout=300,
        )
        payload = jot.create_payload()

        start = time.time()
        with asyncmock.patch.object(
            jot.whitelist, "add", autospec=True, return_value=None
        ) as m:
            await jot.add_to_whitelist(payload)
        now = time.time()
        until = m.await_args[0][1]

        m.assert_awaited_once()
        assert until >= start + jot.leeway + jot.idle_timeout
        assert until <= now + jot.leeway + jot.idle_timeout