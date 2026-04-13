from contextlib import nullcontext as does_not_raise

import pytest

from app.database.models import Message
from sqlalchemy.orm import DeclarativeBase
from src.calculator import Calculator


@pytest.mark.parametrize("x, y, res", [(1, 2, 3), (5, -1, 4)])
def test_create_message(x, y, res):
    assert x + y == res


def test_is_instance_message():
    assert issubclass(Message, DeclarativeBase)


class TestCalculator:
    @pytest.mark.parametrize("x, y, res", [(1, 2, 3), (4, 5, 9), (6, 7, 13)])
    def test_add(self, x, y, res):
        assert Calculator().add(x, y) == res

    @pytest.mark.parametrize(
        "x, y, res, expectation",
        [
            (1, 2, 0.5, does_not_raise()),
            (2, 2, 1, does_not_raise()),
            (1, 1, 1, does_not_raise()),
            (1, 0, float("inf"), pytest.raises(ZeroDivisionError)),
        ],
    )
    def test_divide(self, x, y, res, expectation):
        with expectation:
            assert Calculator().divide(x, y) == res
