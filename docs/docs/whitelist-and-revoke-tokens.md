# Whitelist and revoke tokens

This optional feature gives you the option of revoking tokens on demand or after a
certain [idle timeout](#idle-timeout). A revoked will fail verification.

This requires a database backend to store tokens. Support for Redis is built in,
but you can also roll your own.

The whitelist works by storing the token ID (`jti`) every time you generate a token.
The token is stored until its expiry time (`exp`) or idle timeout has elapsed
(if your token have no expiry time and you don't use idle timeout they will be stored forever)

When you call `Jotbox.verified_payload` it always checks the whitelist.
If the token is not in whitelist it raises a `jotbox.RevokedTokenerror`

## Use the redis whitelist

The built in redis whitelist is simple to use. Import it like this:

```python3
from jotbox.whitelist.redis import RedisWhitelist
```

Instantiate from redis URL:

```python3
...
my_whitelist = RedisWhitelist('redis://localhost')
```

If you want more control over how the redis connection pool
is created, you can pass in an `aredis.StrictRedis` instance directly:

```python3
...
from aredis import StrictRedis

my_redis = StrictRedis(...)
my_whitelist = RedisWhitelist(my_redis)
```

You can also set a custom key prefix if you'd like (the default prefix is `JB:WHITE:`):

```python3
my_whitelist = RedisWhitelist(my_redis, key_prefix="WHITELISTED_TOKEN:")
```

Now pass your whitelist when creating the `Jotbox` instance:

```python3
jot = Jotbox[MyPayload](
    ...,
    whitelist=my_whitelist
)
```

To revoke a token (e.g. when a user logs out), pass the verified payload to `revoke_payload`:

```python3
payload = await jot.verified_payload(encoded_token)
await jot.revoke_payload(payload)
```

## Idle timeout

The idle timeout setting tells `jotbox` to automatically delete
tokens from the whitelist after a number of seconds of inactivity.

When used in conjunction with `expires_at` the token is removed from whitelist
once either the idle timeout or expiry time elapses, whichever happens first.

This can be particularly useful for login sessions as it allows you to automatically log out the user after a period of inactivity while still allowing a long total expiry time on the session.

To use this you need to pass both `idle_timeout` argument to `Jotbox` along with `whitelist`:

```python3
jot = Jotbox[MyPayload](
    ...,
    expires_at=3600*24, # Expire after 24 hours when not idle
    idle_timeout=3600, # Revoke after 1 hour of inactivity
    whitelist=my_whitelist
)
```

```python3
token = await jot.create_token()
encoded_token = token.token

# User sends the token in API call
valid_payload = await jot.verified_payload(encoded_token)
# Success

await asyncio.sleep(3601) # No activity during idle timeout

await jot.verified_payload(encoded_token)
# raises RevokedTokenerror(...)

```

## Use other storage backends

You don't have to use redis for your whitelist.
You can create a subclass of the abstract class `jotbox.whitelist.base.BaseWhitelist` and use any database/storage method you want.

You'll need to implement the `add`, `exists`, `touch` and `delete` methods.

Check source code of the redis whitelist for a reference implementation.

Note that with redis, expiry times are handled by redis itself. With other databases you may
need to explicitly check and clean up expired tokens.






