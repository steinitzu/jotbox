from typing import TypeVar, Generic, Type, cast

from pydantic.generics import GenericModel

from jotbox.tokens import Jotbox
from jotbox.types import TSession, TSub, Session
from jotbox.whitelist.base import SessionWhitelist


class SessionBox(Jotbox[TSession], Generic[TSession, TSub]):
    whitelist: SessionWhitelist[TSession, TSub]

    def __init__(
        self,
        *,
        whitelist: SessionWhitelist,
        payload_type: Type[TSession] = cast(Type[TSession], Session),
        **kwargs
    ) -> None:
        super().__init__(whitelist=whitelist, payload_type=payload_type, **kwargs)
        if not self.whitelist:
            raise ValueError("whitelist argument is required")

    async def revoke_subject(self, sub: TSub) -> None:
        """
        Revoke all tokens with given `sub` claim
        """
        await self.whitelist.delete_sub(sub)
