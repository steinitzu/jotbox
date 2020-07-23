from math import floor
from datetime import datetime
import time
from typing import AsyncIterable, TypeVar, List, AsyncIterator

from jotbox.types import DateTimeStamp


T = TypeVar("T")


def timestamp_ms(t: DateTimeStamp) -> int:
    if isinstance(t, datetime):
        return floor(t.timestamp() * 1000)
    return floor(t * 1000)


def now_ms() -> int:
    return timestamp_ms(time.time())


async def achunked(iterable: AsyncIterable[T], size: int) -> AsyncIterator[List[T]]:
    chunk = []
    async for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
