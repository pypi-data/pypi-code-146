from enum import Enum

import pytest

from typepigeon import to_type


class ValueTest:
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: "ValueTest") -> bool:
        return self.value == other.value


class EnumerationTest(Enum):
    test_1 = "test_1"


def test_convert_class():
    class_1 = to_type(5, ValueTest)

    enum_1 = to_type("test_1", EnumerationTest)
    enum_2 = to_type(EnumerationTest.test_1, str)

    with pytest.raises((KeyError, ValueError)):
        to_type(5, EnumerationTest)

    assert class_1 == ValueTest(5)

    assert enum_1 == EnumerationTest.test_1
    assert enum_2 == "test_1"
