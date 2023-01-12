import enum
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, List, Optional, Set

import pendulum
import pyarrow as pa
import pytest

from chalk.features import feature, features, unwrap_feature
from chalk.serialization.codec import FEATURE_CODEC

try:
    import polars as pl
except ImportError:
    pl = None


class CustomClass:
    def __init__(self, w: str):
        self.w = w

    def __eq__(self, other: object):
        return isinstance(other, CustomClass) and self.w == other.w


class Color(enum.Enum):
    blue = "blue"
    green = "green"
    orange = "orange"


@dataclass
class MyDataclass:
    foo: int
    bar: str
    baz: Optional[int]
    sub_list: List[int]


@features
class Hello:
    a: str
    b: int
    c: datetime
    d: Color
    e: date
    f: MyDataclass
    y: Set[int]
    z: List[str]
    fancy: CustomClass = feature(encoder=lambda x: x.w, decoder=lambda x: CustomClass(x))


def _check_roundtrip(f: Any, value: Any):
    f = unwrap_feature(f)
    encoded = FEATURE_CODEC.encode(f, value)
    decoded = FEATURE_CODEC.decode(f, encoded)
    assert decoded == value


def test_datetime():
    serialized = "2022-04-08T22:26:03.303000+00:00"
    decoded = FEATURE_CODEC.decode(unwrap_feature(Hello.c), serialized)
    assert decoded == pendulum.parse(serialized)
    re_encoded = FEATURE_CODEC.encode(unwrap_feature(Hello.c), decoded)
    assert serialized == re_encoded


def test_custom_codecs():
    _check_roundtrip(Hello.fancy, CustomClass("hihi"))


def test_color():
    _check_roundtrip(Hello.d, Color.green)


def test_date():
    assert "2022-04-08" == FEATURE_CODEC.encode(unwrap_feature(Hello.e), date.fromisoformat("2022-04-08"))
    _check_roundtrip(Hello.e, date.fromisoformat("2022-04-08"))


def test_list():
    _check_roundtrip(Hello.z, ["hello", "there"])


@pytest.mark.skipif(pl is None, reason="Polars is not installed")
def test_get_polars_dtype():
    assert pl is not None
    assert FEATURE_CODEC.get_polars_dtype("hello.a") == pl.Utf8
    assert FEATURE_CODEC.get_polars_dtype("hello.b") == pl.Int64
    assert FEATURE_CODEC.get_polars_dtype("hello.c") == pl.Datetime("us", "UTC")
    assert FEATURE_CODEC.get_polars_dtype("hello.d") == pl.Utf8  # Colors are string enums
    assert FEATURE_CODEC.get_polars_dtype("hello.e") == pl.Date
    assert FEATURE_CODEC.get_polars_dtype("hello.f") == pl.Struct(
        [
            pl.Field("foo", pl.Int64),
            pl.Field("bar", pl.Utf8),
            pl.Field("baz", pl.Int64),
            pl.Field("sub_list", pl.List(pl.Int64)),
        ]
    )
    assert FEATURE_CODEC.get_polars_dtype("hello.y") == pl.List(pl.Int64)
    assert FEATURE_CODEC.get_polars_dtype("hello.z") == pl.List(pl.Utf8)


def test_get_pyarrow_dtype():
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.a") == pa.string()
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.b") == pa.int64()
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.c") == pa.timestamp("us", "UTC")
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.d") == pa.string()  # Colors are string enums
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.e") == pa.date64()
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.f") == pa.struct(
        [
            pa.field("foo", pa.int64()),
            pa.field("bar", pa.utf8()),
            pa.field("baz", pa.int64()),
            pa.field("sub_list", pa.list_(pa.int64())),
        ]
    )
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.y") == pa.list_(pa.int64())
    assert FEATURE_CODEC.get_pyarrow_dtype("hello.z") == pa.list_(pa.string())
    with pytest.raises(ValueError):
        FEATURE_CODEC.get_pyarrow_dtype("hello.fancy")
