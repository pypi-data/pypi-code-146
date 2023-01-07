import datetime
import pandas as pd
from canner.adapters import ParquetReader
from canner.adapters.query_reader.parquet_reader import ParquetSourceType
from canner.utils import *
from pandas import DataFrame, Timestamp
from .config import TestConfig


expecteds = {
    "cbool": True,
    "ctinyint": pow(2, 7) - 1,
    "csmallint": pow(2, 15) - 1,
    "cint": pow(2, 31) - 1,
    "cbigint": pow(2, 62),
    "creal": 10.3,
    "cdouble": 10.3,
    "cdecimal": 100.34,
    "cvarchar": "abcdefghijk",
    "cchar": "abcdefghijk",
    "cvarbinary": b"abcdefghijk",
    "cjson": '{"a":1,"b":2}',
    "cdate": Timestamp("2001-08-22"),
    "ctimestamp": Timestamp(
        datetime.datetime.strptime("2001-08-21 19:04:05.321000", "%Y-%m-%d %H:%M:%S.%f")
    ).tz_localize(None),
    "ctimestampwithtz": "2001-08-22 03:04:05.321 America/Los_Angeles",
    "carray": [1, 2, 3],
    "cmap": {b"foo": b"foo1", b"boo": b"boo1"},
    "cipaddress": "10.0.0.1",
    "cuuid": "12151fd2-7586-11e9-8f9e-2a86e4085a59",
    "crow.x": 1,
    "crow.y": 2.0,
}


def test_parquet_to_list():
    # Arrange
    sources = [TestConfig.SAMPLE_01_MULTIPLE_TYPE_FIELDS_FORMAT_PARQUET]

    # Act
    columns, data = ParquetReader(ParquetSourceType.FILE_PATH, sources).read_to_list()
    data = list(data_factory(data_format="list", columns=columns, data=data))

    # Assert columns
    data_columns = data[0]
    assert len(expecteds) == len(data_columns)

    # Assert data
    for col in range(len(data_columns)):
        actual = data[1][col]
        # TODO: ignore the precision issue for now, we would fix it in the future.
        # Expected 10.3 but actual is 10.300000190734863.
        if data[0][col] == "creal":
            actual = round(actual, 2)
        expected = expecteds[data[0][col]]

        assert (
            actual == expected
        ), f"data[{str(col)}] expected: {str(expecteds[data[0][col]])}, but actual: {str(data[1][col])}"


def test_parquet_to_df():
    # Arrange
    sources = [TestConfig.SAMPLE_01_MULTIPLE_TYPE_FIELDS_FORMAT_PARQUET]

    # Act
    columns, data = ParquetReader(ParquetSourceType.FILE_PATH, sources).read_to_list()
    data = DataFrame(data_factory(data_format="df", columns=columns, data=data))

    # Assert columns
    assert len(expecteds) == len(data.columns)

    # Assert data
    for col in range(len(data.columns)):
        actual = data[data.columns[col]][0]
        if data.columns[col] == "creal":
            actual = round(actual, 2)
        expected = expecteds[data.columns[col]]

        assert (
            actual == expected
        ), f"data[{str(col)}] expected: {str(expecteds[data.columns[col]])}, but actual: {str(data[data.columns[col]].values[0])}"


def test_parquet_to_np():
    # Arrange
    sources = [TestConfig.SAMPLE_01_MULTIPLE_TYPE_FIELDS_FORMAT_PARQUET]

    # Act
    df = ParquetReader(ParquetSourceType.FILE_PATH, sources).read_to_df()
    columns, data = ParquetReader.convert_to_list(df)
    data = data_factory(data_format="np", columns=columns, data=data)

    # Assert columns
    assert len(expecteds) == len(df.columns)

    # Assert data
    for col in range(len(df.columns)):
        actual = data[0][col]
        if df.columns[col] == "creal":
            actual = round(actual, 2)
        expected = expecteds[df.columns[col]]

        assert (
            actual == expected
        ), f"data[{str(col)}] expected: {str(expecteds[df.columns[col]])}, but actual: {str(data[0][col])}"


def test_format_should_be_correct_when_query_only_timestamp_fields():
    # Arrange
    expecteds = {
        "only_timestamp": Timestamp(
            datetime.datetime.strptime(
                "2021-10-26 04:08:35.608", "%Y-%m-%d %H:%M:%S.%f"
            )
        ),
        "only_timestamp_1": Timestamp(
            datetime.datetime.strptime(
                "2021-10-26 04:08:35.608", "%Y-%m-%d %H:%M:%S.%f"
            )
        ),
    }
    sources = [TestConfig.SAMPLE_02_ONLY_TIMESTAMP_FIELDS_FORMAT_PARQUET]

    # Act
    columns, data = ParquetReader(ParquetSourceType.FILE_PATH, sources).read_to_list()
    data = list(data_factory(data_format="list", columns=columns, data=data))

    # Assert columns
    data_columns = data[0]
    assert len(data_columns) == len(expecteds)
    # Assert data
    for col in range(len(data_columns)):
        actual = data[1][col]
        expected = expecteds[data_columns[col]]
        assert actual == expected


def test_format_should_be_correct_when_query_only_timestamp_zone_fields():
    # Arrange
    expecteds = {
        "timestamp_with_zone": "2021-10-26 05:47:57.710 UTC",
        "timestamp_with_zone_1": "2021-10-26 05:47:57.710 UTC",
    }
    sources = [TestConfig.SAMPLE_03_ONLY_TIMESTAMP_ZONE_FIELDS_FORMAT_PARQUET]

    # Act
    columns, data = ParquetReader(ParquetSourceType.FILE_PATH, sources).read_to_list()
    data = list(data_factory(data_format="list", columns=columns, data=data))

    # Assert columns
    data_columns = data[0]
    assert len(data_columns) == len(expecteds)
    # Assert data
    for col in range(len(data_columns)):
        actual = data[1][col]
        expected = expecteds[data_columns[col]]
        assert actual == expected


def test_format_should_be_correct_when_query_timestamp_zone_with_only_timestamp_fields():
    # Arrange
    expecteds = {
        "only_timestamp": Timestamp(
            datetime.datetime.strptime(
                "2021-10-26 06:03:43.870", "%Y-%m-%d %H:%M:%S.%f"
            )
        ),
        "timestamp_with_zone": "2021-10-26 06:03:43.870 UTC",
    }
    sources = [TestConfig.SAMPLE_04_TIMESTAMP_WITH_TIMESTAMP_ZONE_FIELDS_FORMAT_PARQUET]

    # Act
    columns, data = ParquetReader(ParquetSourceType.FILE_PATH, sources).read_to_list()
    data = list(data_factory(data_format="list", columns=columns, data=data))

    # Assert columns
    data_columns = data[0]
    assert len(data_columns) == len(expecteds)
    # Assert data
    for col in range(len(data_columns)):
        actual = data[1][col]
        expected = expecteds[data_columns[col]]
        assert actual == expected
