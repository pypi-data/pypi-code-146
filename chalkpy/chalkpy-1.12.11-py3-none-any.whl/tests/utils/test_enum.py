import contextlib
import enum
from typing import Type

import pytest

from chalk.utils.enum import get_enum_value_type


class EmptyEnum(enum.Enum):
    pass


class ValidEnum(enum.Enum):
    A = 2
    B = 3


class IntFloatEnum(enum.Enum):
    A = 2
    B = 3.0


class FloatIntEnum(enum.Enum):
    A = 2.0
    B = 3


class InvalidEnum(enum.Enum):
    A = 3
    B = "hello"


@pytest.mark.parametrize(
    "enum_cls,expected_type,raises",
    [
        (ValidEnum, int, False),
        (IntFloatEnum, float, False),
        (FloatIntEnum, float, False),
        (InvalidEnum, None, True),
    ],
)
def test_get_enum_value_type(enum_cls: Type[enum.Enum], expected_type: Type, raises: bool):
    with pytest.raises(TypeError) if raises else contextlib.nullcontext():
        assert get_enum_value_type(enum_cls) is expected_type
