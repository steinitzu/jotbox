from abc import abstractmethod, ABC
from typing import Optional, Generic

from jotbox.types import TPayload, DateTimeStamp, TSub, TSession


class Whitelist(ABC, Generic[TPayload]):
    @abstractmethod
    async def add(self, payload: TPayload, until: Optional[DateTimeStamp]) -> None:
        """
        Save a token payload in the whitelist.

        The `until` timestamp if not `None` must be respected
        and the token should be considered expired at this time.

        If `until` is `None` the token should not expire
        """

    @abstractmethod
    async def exists(self, payload: TPayload) -> bool:
        """
        Check whether the token exists and is currently valid in the whitelist.

        return `True` if the token is valid and not expired, otherwise `False`
        """

    @abstractmethod
    async def touch(self, payload: TPayload, until: DateTimeStamp) -> bool:
        """
        Used for the "idle timeout" function.

        Revalidate the token and extend its expiry time up to `until` timestamp
        This method must verify that the token is currently valid before
        revalidation.

        return
           `True` if the token is succesfully "touched"
           `False` if the token is not currently valid in the whitelist.
        """

    @abstractmethod
    async def delete(self, delete: TPayload) -> None:
        """
        Immediately revoke the token from the whitelist
        """


class SessionWhitelist(Whitelist[TSession], Generic[TSession, TSub]):
    @abstractmethod
    async def delete_sub(self, sub: TSub) -> None:
        """
        Delete all tokens with a given `sub` claim
        """
