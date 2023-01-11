from datetime import datetime
from enum import Enum
from pathlib import Path

from typepigeon import to_json


class FloatTest:
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)


class IntegerTest:
    def __init__(self, value: int):
        self.value = value

    def __int__(self) -> int:
        return int(self.value)


class EnumerationTest(Enum):
    test_1 = "test_1"


def test_convert_to_json():
    result_1 = to_json(5)
    result_2 = to_json("5")

    result_3 = to_json(FloatTest(5))
    result_4 = to_json(IntegerTest(5.0))
    result_5 = to_json(FloatTest(5.5))

    result_6 = to_json("test")
    result_7 = to_json(datetime(2021, 3, 26))

    result_8 = to_json(
        to_json([FloatTest(5), "6", {3: datetime(2021, 3, 27)}])
    )
    result_9 = to_json(
        to_json({"test": [FloatTest(5), "6", {3: datetime(2021, 3, 27)}]})
    )

    result_10 = to_json(EnumerationTest.test_1)

    result_11 = to_json(Path("/path/test"))

    assert result_1 == 5
    assert result_2 == "5"

    assert result_3 == 5.0
    assert result_4 == 5
    assert result_5 == 5.5

    assert result_6 == "test"
    assert result_7 == "2021-03-26 00:00:00"

    assert result_8 == [5, "6", {3: "2021-03-27 00:00:00"}]
    assert result_9 == {"test": [5, "6", {3: "2021-03-27 00:00:00"}]}

    assert result_10 == "test_1"

    assert result_11 == "/path/test"
