from typing import List
import asyncio
import secrets

from jotbox import SessionBox, Session, RevokedTokenError
from jotbox.whitelist.redis import SessionRedisWhitelist


# Create our session model
# The `sub` claim is of type int, but you can use any type you want
UserSession = Session[int]

sessions = SessionBox[UserSession, int](
    encode_key=secrets.token_urlsafe(),
    payload_type=UserSession,
    whitelist=SessionRedisWhitelist("redis://127.0.0.1"),
    idle_timeout=3600,
    expires_in=24 * 3600,
    leeway=10,
)


async def run():
    token = await sessions.create_token(sub=42)

    encoded_token = token.token

    # Verify the token
    await sessions.verified_payload(encoded_token)

    # Revoke all tokens for the user
    await sessions.revoke_subject(token.payload.sub)

    # Now verification fails
    try:
        await sessions.verified_payload(encoded_token)
    except RevokedTokenError:
        print("The token has been revoked")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
