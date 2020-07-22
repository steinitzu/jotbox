# The Payload model

The Payload is a `pydantic` model to control and validate
the info that's encoded into the JWT.

By default it contains the standard JWT claims: `jti`, `iat`, `exp` (optional)

You can override it and customize like any pydantic model.
E.g. add some user info and make expiry mandatory:

```python3
from typing import List

from jotbox import Payload

class MyPayload(Payload):
    email: str
    permissions: List[str]
    exp: int
```

Pass this to jotbox and use it.

```python3
from jotbox import Jotbox

jot = Jotbox[MyPayload](
    encode_key=os.environ['MY_SECRET_KEY'],
    payload_type=MyPayload,
    expires_in=3600,
    ...
)
```
> **Note**: the `[MyPayload]` part of `Jotbox[MyPayload]` is not required
but gives you type safety and better code completion in your IDE

Now you can create tokens with your extra fields

```python3
await jot.create_token(
    email='user@example.com',
    permissions=['articles-read', 'articles-publish']
)
```

The arguments passed to `create_token` are validated with your payload model
so passing invalid/wrong type arguments will fail.
`exp` is added automatically by the `expires_in` setting by you can override it
on a case by case basis by passing your own timestamp:

```python3
import time
import math

await jot.create_token(
    email='user@example.com',
    permissions=['articles-read', 'articles-publish'],
    exp=math.floor(time.time() + 1800)
)
```

