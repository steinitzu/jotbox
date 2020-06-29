import os
import asyncio

from jotbox import Jotbox, Payload, TokenVerificationError
from jotbox.whitelist.redis import RedisWhitelist


class AccessPayload(Payload):
    user_id: int


jot = Jotbox[AccessPayload](  # Provide the payload type for static type safety
    encode_key=os.environ["MY_ENCODE_KEY"],
    payload_type=AccessPayload,
    leeway=10,
    expires_in=7200,  # Expire tokens after 2 hours (optional)
    # Whitelist is optional
    idle_timeout=600,  # Revoke token after 10 minutes without use
    whitelist=RedisWhitelist("redis://localhost"),
)


async def run():
    # Create a token
    token = await jot.create_token(user_id=42)

    print(token.token)  # the encoded token as string
    # >> eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJkMDFlYmVmNjlk...

    print(repr(token.payload))  # The payload object
    # >> AccessPayload(jti=UUID('d682eabf-...'), iat=1593638317, user_id=42)

    # Verify the encoded token
    payload = await jot.verified_payload(token.token)
    print(payload)
    # >> AccessPayload(jti=UUID('d682eabf-...'), iat=1593638317, user_id=42)

    # revoke the token (logout) (this requires whitelist)
    await jot.revoke_payload(payload)

    try:
        await jot.verified_payload(token.token)
    except TokenVerificationError as e:
        print(repr(e))
        # >> RevokedTokenError('Token ID d682eabf-... has been revoked')


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
