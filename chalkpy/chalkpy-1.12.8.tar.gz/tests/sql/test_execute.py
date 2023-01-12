import enum
import logging
import os
import pathlib
import uuid
from datetime import date, datetime, timezone
from typing import Any, List, Tuple, Type, cast

import pytest
from sqlalchemy import ARRAY, TIMESTAMP, VARCHAR, Boolean, Column, Date, DateTime, Enum, Float, Integer
from sqlalchemy.orm import Session, declarative_base

from chalk import batch
from chalk.features import DataFrame, feature, feature_time, features, has_one
from chalk.features.resolver import OfflineResolver
from chalk.sql import BaseSQLSourceProtocol, ChalkQueryProtocol, PostgreSQLSource, SnowflakeSource, SQLiteFileSource
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.sql._internal.integrations.sqlite import SQLiteFileSourceImpl

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    import snowflake
    import snowflake.sqlalchemy
except ImportError:
    snowflake = None

try:
    import polars as pl
except ImportError:
    pl = None


@features
class SQLExecuteNestedFeatures:
    id: int = feature(primary=True)
    nested_int: int


class EnumFeature(enum.Enum):
    RED = "red"
    BLUE = "blue"


@features
class SQLExecuteFeatures:
    id: int = feature(primary=True)
    ts: datetime = feature_time()
    str_feature: str
    int_feature: int
    bool_feature: bool
    enum_feature: EnumFeature
    date_feature: date
    timestamp_feature: datetime
    float_feature: float
    datetime_feature: datetime
    list_feature: List[str]
    nested_features_id: int
    nested_features: SQLExecuteNestedFeatures = has_one(
        lambda: SQLExecuteFeatures.nested_features_id == SQLExecuteNestedFeatures.id
    )


@pytest.fixture
def sql_source(request, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    if request.param == "sqlite":
        return SQLiteFileSource(str(tmp_path / "db.sqlite"))
    if request.param in ("postgres"):
        if "PGHOST" not in os.environ:
            pytest.skip("No PGHOST is specified; skipping postgres tests")
        if psycopg2 is None:
            pytest.skip("psycopg2 is not installed")
        return PostgreSQLSource()
    if request.param == "snowflake":
        if "SNOWFLAKE_DATABASE" not in os.environ:
            pytest.skip("No SNOWFLAKE_DATABASE is specified; skipping snowflake tests")
        if snowflake is None:
            pytest.skip("Snowflake is not installed")
        return SnowflakeSource()


@pytest.fixture
def model(sql_source: BaseSQLSourceProtocol):
    randr = str(uuid.uuid4())[10:].replace("-", "_")

    Base: Type = declarative_base()

    class ExecuteSQLModel(Base):
        __tablename__ = f"execute_sql_table_test_{randr}"

        id = Column(Integer, primary_key=True)
        str_feature = Column(VARCHAR)
        int_feature = Column(Integer)
        enum_feature = Column(Enum(EnumFeature, name=f"enum_feature_{randr}"))
        enum_as_string_feature = Column(
            VARCHAR
        )  # The enum feature, but manually stored as a string of the enum's value
        date_feature = Column(Date)
        timestamp_feature = Column(TIMESTAMP)

        bool_feature = Column(Boolean)
        float_feature = Column(Float)
        datetime_feature = Column(DateTime)
        nested_features_id = Column(Integer)
        nested_features_nested_int = Column(Integer)
        if isinstance(sql_source, PostgreSQLSourceImpl):
            list_feature = Column(ARRAY(VARCHAR))

    Base.metadata.create_all(sql_source.get_engine())
    try:
        with Session(sql_source.get_engine()) as session, session.begin():
            session.add(
                ExecuteSQLModel(
                    id=1,
                    # Including a newline and quotes in the value to ensure that escaping works properly
                    str_feature='hello\n,"Ravi"',
                    int_feature=2,
                    bool_feature=True,
                    enum_feature=EnumFeature.RED,
                    date_feature=date(2000, 1, 2),
                    timestamp_feature=datetime(2000, 1, 3, tzinfo=timezone.utc),
                    enum_as_string_feature=EnumFeature.BLUE.value,
                    float_feature=3.14,
                    datetime_feature=datetime(2000, 1, 1),
                    **({"list_feature": ["foo", "bar"]} if isinstance(sql_source, PostgreSQLSourceImpl) else {}),
                    nested_features_id=4,
                    nested_features_nested_int=5,
                )
            )
            session.add(
                ExecuteSQLModel(
                    id=2,
                    str_feature=None,
                    int_feature=None,
                    bool_feature=None,
                    enum_feature=None,
                    date_feature=None,
                    timestamp_feature=None,
                    enum_as_string_feature=None,
                    float_feature=None,
                    datetime_feature=None,
                    **({"list_feature": None} if isinstance(sql_source, PostgreSQLSourceImpl) else {}),
                    nested_features_id=None,
                    nested_features_nested_int=None,
                )
            )
        yield ExecuteSQLModel
    finally:
        Base.metadata.drop_all(sql_source.get_engine())


def get_model_to_primitive_features(model: Any):
    return SQLExecuteFeatures(  # type: ignore -- pyright does not understand the constructor
        id=model.id,
        str_feature=model.str_feature,
        bool_feature=model.bool_feature,
        float_feature=model.float_feature,
        int_feature=model.int_feature,
        date_feature=model.date_feature,
        timestamp_feature=model.timestamp_feature,
        datetime_feature=model.datetime_feature,
        enum_feature=model.enum_as_string_feature,
        nested_features_id=model.nested_features_id,
        nested_features=SQLExecuteNestedFeatures(  # type: ignore -- pyright does not understand the constructor
            id=model.nested_features_id,
            nested_int=model.nested_features_nested_int,
        ),
    )


def get_model_to_list_features(model: Any):
    return SQLExecuteFeatures(  # type: ignore -- pyright does not understand the constructor
        id=model.id,
        list_feature=model.list_feature,
    )


def get_model_to_enum_features(model: Any):
    return SQLExecuteFeatures(  # type: ignore -- pyright does not understand the constructor
        id=model.id,
        enum_feature=model.enum_feature,
    )


@pytest.fixture
def graph_list(sql_source: BaseSQLSourceProtocol, model: Any, request: pytest.FixtureRequest):
    string_query: bool = request.param

    @batch
    def sql_execute_resolve_all_list() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.list_feature,
    ]:
        if string_query:
            return sql_source.query_string(f"select id, list_feature from {model.__tablename__}")
        else:
            return sql_source.query(get_model_to_list_features(model))

    @batch
    def sql_execute_resolve_not_null_list() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.list_feature,
    ]:
        if string_query:
            return sql_source.query_string(f"select id, list_feature from {model.__tablename__} where id = 1")
        else:
            return sql_source.query(get_model_to_list_features(model)).filter(model.id == 1)

    @batch
    def sql_execute_resolve_null_list() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.list_feature,
    ]:
        if string_query:
            return sql_source.query_string(f"select id, list_feature from {model.__tablename__} where id = 2")
        else:
            return sql_source.query(get_model_to_list_features(model)).filter(model.id == 2)

    return sql_execute_resolve_all_list, sql_execute_resolve_not_null_list, sql_execute_resolve_null_list


@pytest.fixture
def graph_enum(sql_source: BaseSQLSourceProtocol, model: Any, request: pytest.FixtureRequest):
    string_query = request.param

    @batch
    def sql_execute_resolve_all_enum() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.enum_feature,
    ]:
        if string_query:
            return sql_source.query_string(f"select id, enum_feature from {model.__tablename__}")
        else:
            return sql_source.query(get_model_to_enum_features(model))

    @batch
    def sql_execute_resolve_not_null_enum() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.enum_feature,
    ]:
        if string_query:
            return sql_source.query_string(f"select id, enum_feature from {model.__tablename__} where id = 1")
        else:
            return sql_source.query(get_model_to_enum_features(model)).filter(model.id == 1)

    @batch
    def sql_execute_resolve_null_enum() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.enum_feature,
    ]:
        if string_query:
            return sql_source.query_string(f"select id, enum_feature from {model.__tablename__} where id = 2")
        else:
            return sql_source.query(get_model_to_enum_features(model)).filter(model.id == 2)

    return sql_execute_resolve_all_enum, sql_execute_resolve_not_null_enum, sql_execute_resolve_null_enum


@pytest.fixture
def graph(sql_source: BaseSQLSourceProtocol, model: Any, request: pytest.FixtureRequest):
    string_query: bool = request.param

    @batch
    def sql_execute_resolve_all() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.str_feature,
        SQLExecuteFeatures.bool_feature,
        SQLExecuteFeatures.float_feature,
        SQLExecuteFeatures.int_feature,
        SQLExecuteFeatures.date_feature,
        SQLExecuteFeatures.timestamp_feature,
        SQLExecuteFeatures.datetime_feature,
        SQLExecuteFeatures.enum_feature,
        SQLExecuteFeatures.nested_features_id,
        SQLExecuteFeatures.nested_features.id,
        SQLExecuteFeatures.nested_features.nested_int,
    ]:
        if string_query:
            return sql_source.query_string(
                f"""select
                id,
                str_feature,
                bool_feature,
                float_feature,
                int_feature,
                date_feature,
                timestamp_feature,
                datetime_feature,
                enum_as_string_feature as enum_feature,
                nested_features_id,
                nested_features_id as "nested_features.id",
                nested_features_nested_int as "nested_features.nested_int"
                from {model.__tablename__}"""
            )
        else:
            return sql_source.query(get_model_to_primitive_features(model))

    @batch
    def sql_execute_resolve_not_null() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.str_feature,
        SQLExecuteFeatures.bool_feature,
        SQLExecuteFeatures.int_feature,
        SQLExecuteFeatures.date_feature,
        SQLExecuteFeatures.timestamp_feature,
        SQLExecuteFeatures.float_feature,
        SQLExecuteFeatures.datetime_feature,
        SQLExecuteFeatures.enum_feature,
        SQLExecuteFeatures.nested_features_id,
        SQLExecuteFeatures.nested_features.id,
        SQLExecuteFeatures.nested_features.nested_int,
    ]:
        if string_query:
            return sql_source.query_string(
                f"""select
                id,
                str_feature,
                bool_feature,
                float_feature,
                int_feature,
                date_feature,
                timestamp_feature,
                datetime_feature,
                enum_as_string_feature as enum_feature,
                nested_features_id,
                nested_features_id as "nested_features.id",
                nested_features_nested_int as "nested_features.nested_int"
                from {model.__tablename__} where id = 1"""
            )
        else:
            return sql_source.query(get_model_to_primitive_features(model)).filter(model.id == 1)

    @batch
    def sql_execute_resolve_null() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.str_feature,
        SQLExecuteFeatures.bool_feature,
        SQLExecuteFeatures.int_feature,
        SQLExecuteFeatures.date_feature,
        SQLExecuteFeatures.timestamp_feature,
        SQLExecuteFeatures.enum_feature,
        SQLExecuteFeatures.float_feature,
        SQLExecuteFeatures.datetime_feature,
        SQLExecuteFeatures.nested_features_id,
        SQLExecuteFeatures.nested_features.id,
        SQLExecuteFeatures.nested_features.nested_int,
    ]:
        if string_query:
            return sql_source.query_string(
                f"""select
                id,
                str_feature,
                bool_feature,
                float_feature,
                int_feature,
                date_feature,
                timestamp_feature,
                datetime_feature,
                enum_as_string_feature as enum_feature,
                nested_features_id,
                nested_features_id as "nested_features.id",
                nested_features_nested_int as "nested_features.nested_int"
                from {model.__tablename__} where id = 2"""
            )
        else:
            return sql_source.query(get_model_to_primitive_features(model)).filter(model.id == 2)

    return sql_execute_resolve_all, sql_execute_resolve_not_null, sql_execute_resolve_null


@pytest.fixture
def force_sqlalchemy_query_execution(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> bool:
    if request.param:
        monkeypatch.setenv("CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION", "1")
    return request.param


@pytest.mark.parametrize("sql_source", ["postgres", "sqlite", "snowflake"], indirect=True)
@pytest.mark.parametrize("force_sqlalchemy_query_execution", [True, False], indirect=True)
@pytest.mark.skipif(pl is None, reason="polars is not installed")
class TestExecute:
    def _test_harness(
        self,
        resolver: OfflineResolver[Any, DataFrame],
        expected: DataFrame,
    ):
        # Test that calling the resolver directly returns a dataframe
        direct_query = resolver()
        assert isinstance(direct_query, DataFrame)
        assert (direct_query[expected.columns] == expected).all()

        # Also test manually invoking via execute_to_datafrmae
        indirect_query = cast(ChalkQueryProtocol, resolver.fn())
        finalized_query = indirect_query.all()
        if isinstance(resolver.output.features[0], type) and issubclass(resolver.output.features[0], DataFrame):
            features = resolver.output.features[0].columns
        else:
            features = resolver.output.features
        output_df = finalized_query.execute_to_dataframe(features)
        assert (output_df == expected).all()

    def _assert_efficient_execution(self, caplog: pytest.LogCaptureFixture):
        for logger_name, log_level, message in caplog.record_tuples:
            assert "The SQL statement will be executed into SQLAlchemy objects" not in message

    def _assert_sqlalchemy_execution(self, caplog: pytest.LogCaptureFixture):
        found = False
        for logger_name, log_level, message in caplog.record_tuples:
            if "The SQL statement will be executed into SQLAlchemy objects" in message:
                found = True
        assert found

    @pytest.mark.parametrize("graph", [True, False], indirect=True)
    def test_resolve_all(
        self,
        graph: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        caplog: pytest.LogCaptureFixture,
        force_sqlalchemy_query_execution: bool,
        sql_source: BaseSQLSourceProtocol,
    ):
        caplog.set_level(logging.INFO)

        sql_execute_resolve_all = graph[0]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1, 2],
                SQLExecuteFeatures.str_feature: ['hello\n,"Ravi"', None],
                SQLExecuteFeatures.int_feature: [2, None],
                SQLExecuteFeatures.bool_feature: [True, None],
                SQLExecuteFeatures.enum_feature: [EnumFeature.BLUE, None],
                SQLExecuteFeatures.date_feature: [datetime(2000, 1, 2), None],
                SQLExecuteFeatures.timestamp_feature: [datetime(2000, 1, 3, tzinfo=timezone.utc), None],
                SQLExecuteFeatures.float_feature: [3.14, None],
                SQLExecuteFeatures.datetime_feature: [datetime(2000, 1, 1), None],
                SQLExecuteFeatures.nested_features_id: [4, None],
                SQLExecuteFeatures.nested_features.id: [4, None],
                SQLExecuteFeatures.nested_features.nested_int: [5, None],
            }
        )
        self._test_harness(sql_execute_resolve_all, expected)
        if force_sqlalchemy_query_execution or isinstance(sql_source, SQLiteFileSourceImpl):
            self._assert_sqlalchemy_execution(caplog)
        else:
            self._assert_efficient_execution(caplog=caplog)

    @pytest.mark.parametrize("graph", [True, False], indirect=True)
    def test_resolve_not_null(
        self,
        graph: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        caplog: pytest.LogCaptureFixture,
        force_sqlalchemy_query_execution: bool,
        sql_source: BaseSQLSourceProtocol,
    ):
        caplog.set_level(logging.INFO)
        sql_execute_resolve_not_null = graph[1]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1],
                SQLExecuteFeatures.str_feature: ['hello\n,"Ravi"'],
                SQLExecuteFeatures.int_feature: [2],
                SQLExecuteFeatures.bool_feature: [True],
                SQLExecuteFeatures.enum_feature: [EnumFeature.BLUE],
                SQLExecuteFeatures.float_feature: [3.14],
                SQLExecuteFeatures.date_feature: [datetime(2000, 1, 2)],
                SQLExecuteFeatures.timestamp_feature: [datetime(2000, 1, 3, tzinfo=timezone.utc)],
                SQLExecuteFeatures.datetime_feature: [datetime(2000, 1, 1)],
                SQLExecuteFeatures.nested_features_id: [4],
                SQLExecuteFeatures.nested_features.id: [4],
                SQLExecuteFeatures.nested_features.nested_int: [5],
            }
        )
        self._test_harness(sql_execute_resolve_not_null, expected)
        if force_sqlalchemy_query_execution or isinstance(sql_source, SQLiteFileSourceImpl):
            self._assert_sqlalchemy_execution(caplog)
        else:
            self._assert_efficient_execution(caplog=caplog)

    @pytest.mark.parametrize("graph", [True, False], indirect=True)
    def test_resolve_null(
        self,
        graph: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        caplog: pytest.LogCaptureFixture,
        force_sqlalchemy_query_execution: bool,
        sql_source: BaseSQLSourceProtocol,
    ):
        caplog.set_level(logging.INFO)
        sql_execute_resolve_null = graph[2]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [2],
                SQLExecuteFeatures.str_feature: [None],
                SQLExecuteFeatures.int_feature: [None],
                SQLExecuteFeatures.bool_feature: [None],
                SQLExecuteFeatures.enum_feature: [None],
                SQLExecuteFeatures.date_feature: [None],
                SQLExecuteFeatures.timestamp_feature: [None],
                SQLExecuteFeatures.float_feature: [None],
                SQLExecuteFeatures.datetime_feature: [None],
                SQLExecuteFeatures.nested_features_id: [None],
                SQLExecuteFeatures.nested_features.id: [None],
                SQLExecuteFeatures.nested_features.nested_int: [None],
            }
        )
        self._test_harness(sql_execute_resolve_null, expected)
        if force_sqlalchemy_query_execution or isinstance(sql_source, SQLiteFileSourceImpl):
            self._assert_sqlalchemy_execution(caplog)
        else:
            self._assert_efficient_execution(caplog=caplog)

    @pytest.mark.parametrize(
        "graph_list",
        [pytest.param(True, marks=pytest.mark.xfail(reason="String list queries don't work")), False],
        indirect=True,
    )
    def test_resolve_all_list(
        self,
        graph_list: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        sql_source: BaseSQLSourceProtocol,
        force_sqlalchemy_query_execution: bool,
    ):
        if not isinstance(sql_source, PostgreSQLSourceImpl):
            pytest.skip("Only postgres supports arrays")
        sql_execute_resolve_all = graph_list[0]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1, 2],
                SQLExecuteFeatures.list_feature: [["foo", "bar"], None],
            }
        )
        self._test_harness(sql_execute_resolve_all, expected)

    @pytest.mark.parametrize(
        "graph_list",
        [pytest.param(True, marks=pytest.mark.xfail(reason="String list queries don't work")), False],
        indirect=True,
    )
    def test_resolve_not_null_list(
        self,
        graph_list: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        sql_source: BaseSQLSourceProtocol,
        force_sqlalchemy_query_execution: bool,
    ):
        if not isinstance(sql_source, PostgreSQLSourceImpl):
            pytest.skip("Only postgres supports arrays")
        sql_execute_resolve_not_null = graph_list[1]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1],
                SQLExecuteFeatures.list_feature: [["foo", "bar"]],
            }
        )
        self._test_harness(sql_execute_resolve_not_null, expected)

    @pytest.mark.parametrize("graph_list", [True, False], indirect=True)
    def test_resolve_null_list(
        self,
        graph_list: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        sql_source: BaseSQLSourceProtocol,
        force_sqlalchemy_query_execution: bool,
    ):
        if not isinstance(sql_source, PostgreSQLSourceImpl):
            pytest.skip("Only postgres supports arrays")
        sql_execute_resolve_null = graph_list[2]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [2],
                SQLExecuteFeatures.list_feature: [None],
            }
        )
        self._test_harness(sql_execute_resolve_null, expected)

    @pytest.mark.parametrize(
        "graph_enum",
        [pytest.param(True, marks=pytest.mark.xfail(reason="Enum string queries don't work")), False],
        indirect=True,
    )
    def test_resolve_all_enum(
        self,
        graph_enum: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        force_sqlalchemy_query_execution: bool,
    ):
        sql_execute_resolve_all = graph_enum[0]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1, 2],
                SQLExecuteFeatures.enum_feature: [EnumFeature.RED, None],
            }
        )
        self._test_harness(sql_execute_resolve_all, expected)

    @pytest.mark.parametrize(
        "graph_enum",
        [pytest.param(True, marks=pytest.mark.xfail(reason="Enum string queries don't work")), False],
        indirect=True,
    )
    def test_resolve_not_null_enum(
        self,
        graph_enum: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        force_sqlalchemy_query_execution: bool,
    ):
        sql_execute_resolve_not_null = graph_enum[1]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1],
                SQLExecuteFeatures.enum_feature: [EnumFeature.RED],
            }
        )
        self._test_harness(sql_execute_resolve_not_null, expected)

    @pytest.mark.parametrize("graph_enum", [True, False], indirect=True)
    def test_resolve_null_enum(
        self,
        graph_enum: Tuple[OfflineResolver, OfflineResolver, OfflineResolver],
        force_sqlalchemy_query_execution: bool,
    ):
        sql_execute_resolve_null = graph_enum[2]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [2],
                SQLExecuteFeatures.enum_feature: [None],
            }
        )
        self._test_harness(sql_execute_resolve_null, expected)
