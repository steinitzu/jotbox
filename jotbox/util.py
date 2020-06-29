from math import floor
from datetime import datetime
import time

from jotbox.types import DateTimeStamp


def timestamp_ms(t: DateTimeStamp) -> int:
    if isinstance(t, datetime):
        return floor(t.timestamp() * 1000)
    return floor(t * 1000)


def now_ms() -> int:
    return timestamp_ms(time.time())
