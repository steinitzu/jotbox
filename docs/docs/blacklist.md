# Blacklist

Tokens can be blacklisted by storing their ID in a database. A blacklisted token
will always fail verification.  
This can be used for example to support a secure logout in a web application.  

JotBox ships with blacklist backends for redis and postgresql

You can also implement your own blacklist with by subclassing the base class

For example a rudementary in memory blacklist could be implemented like this:


```python3
from jotbox.store.base import Blacklist
from jotbox.types import TPayload


class MemoryBlacklist(Blacklist[TPayload]):
    def __init__(self) -> None:
        self.tokens = set()

    async def add(self, payload: TPayload) -> None:
        self.tokens.add(payload.jti)

    async def exists(self, payload: TPayload) -> bool:
        return payload.jti in self.tokens

    async def delete(self, payload: TPayload) -> None:
        self.tokens.discard(payload.jti)
    
```

## Use the redis blacklist

**NOTE:** This requires `aredis` to be installed

```python3
{!../examples/redisblacklist.py!}
```

Redis will automatically delete tokens shortly after they expire, so you don't have to worry about cleaning up.

By default the token IDs are stored in redis with key prefix `"JB:BLACK:"`. You can change the prefix by passing `key_prefix="MY:PREFIX:"` when instantiating the blacklist.


## Use the database blacklist

**NOTE:** This requires `databases` and `aiopg` to be installed. Currently only postgresql is supported.

```python3
{!../examples/pgblacklist.py!}
```
 
You may want to clean up expired token from the blacklist periodically.  
This can be called on demand to run cleanup.

```python3
await blacklist.delete_expired()
```
