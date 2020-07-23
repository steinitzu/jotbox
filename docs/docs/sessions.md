# Sessions

The `SessionBox` class extends `JotBox` with features that
are particularly useful for working with login sessions.

It adds first-class support for the
[subject](https://tools.ietf.org/html/rfc7519#section-4.1.2) (`sub`) claim
of JWT. That is often used to encode a user ID or username into a JWT.

Currently id only adds support for revoking all tokens created for a 
particular subject. E.g. you can use this for a "Log out on all devices" feature.

Here is a quick example:

```python3
{!../examples/sessions.py!}
```

To break it down:

## Session model

```python3
from jotbox import Session

...

UserSession = Session[int]
```

This is the model for our payload that gets encded to JWT.
This is the same as the default [`Payload`](payload-model)
but adds one extra field `sub`

This is a generic class and you must specify the data type type of your sub claim.
It can be any type you want, for example if your user IDs are uuids, you can use:

```python3
from uuid import UUID

UserSession = Session[UUID]
```

You can also subclass and add extra fields as needed:

```python3
from typing import List

class UserSession(Session[UUID]):
    permissions: List[str]
    email: str
```


## Session whitelist

```
from jotbox.whitelist.redis import SessionRedisWhitelist

...
    whitelist=SessionRedisWhitelist("redis://127.0.0.1"),
...
```

This implementation of redis whitelist is extended from the regular [whitelist](whitelist-and-revoke-tokens).
It includes the value of `sub` when storing tokens and adds the ability to delete
all tokens of a given `sub`.

You can also use a different storage method by creating your own whitelist class
based on `jotbox.whitelist.base.SessionWhitelist` and implementing the
`add`, `touch`, `exists`, `delete` and `delete_sub` methods.

