from uuid import uuid4, UUID
import time

import pytest
from pydantic import ValidationError

from jotbox.sessions import Session


class TestSessionModel:
    def test__sub_type__no_subclass(self):
        S = Session[int]

        s = S(jti=uuid4(), iat=time.time(), sub=42)

        assert isinstance(s.jti, UUID)
        assert isinstance(s.iat, int)
        assert s.sub == 42
        assert s.exp is None

    def test__sub_type_required_exp__validation_error(self):
        class S(Session[int]):
            exp: int

        with pytest.raises(ValidationError) as einfo:
            S(jti=uuid4(), iat=time.time(), sub=42)

        assert einfo.value.errors()[0]["loc"] == ("exp",)

    def test__sub_type_required_exp__valid_data(self):
        class S(Session[int]):
            exp: int

        s = S(jti=uuid4(), iat=time.time(), sub=42, exp=time.time())

        assert isinstance(s.jti, UUID)
        assert isinstance(s.iat, int)
        assert isinstance(s.exp, int)
        assert s.sub == 42
