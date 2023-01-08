import enum
import os
import pathlib
import uuid
from datetime import datetime, timezone
from typing import Any, List, Tuple, Type, cast

import pytest
from sqlalchemy import ARRAY, VARCHAR, Boolean, Column, DateTime, Float, Integer
from sqlalchemy.orm import Session, declarative_base

from chalk import batch
from chalk.features import DataFrame, feature, feature_time, features, has_one
from chalk.features.resolver import OfflineResolver
from chalk.sql import BaseSQLSourceProtocol, ChalkQueryProtocol, PostgreSQLSource, SnowflakeSource, SQLiteFileSource
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.utils.environment_parsing import env_var_bool

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
    if request.param in ("postgres", "postgres_no_csv"):
        if "PGHOST" not in os.environ:
            pytest.skip("No PGHOST is specified; skipping postgres tests")
        if psycopg2 is None:
            pytest.skip("psycopg2 is not installed")
        if request.param == "postgres_no_csv":
            monkeypatch.setenv("CHALK_DISABLE_POSTGRES_CSV_TO_PYARROW", "1")
        return PostgreSQLSource()
    if request.param == "snowflake":
        if "SNOWFLAKE_DATABASE" not in os.environ:
            pytest.skip("No SNOWFLAKE_DATABASE is specified; skipping snowflake tests")
        if snowflake is None:
            pytest.skip("Snowflake is not installed")
        return SnowflakeSource()


@pytest.fixture
def model(sql_source: BaseSQLSourceProtocol):
    randr = str(uuid.uuid4())[10:]

    Base: Type = declarative_base()

    class ExecuteSQLModel(Base):
        __tablename__ = f"execute_sql_table_test_{randr}"

        id = Column(Integer, primary_key=True)
        str_feature = Column(VARCHAR)
        int_feature = Column(Integer)
        enum_feature = Column(VARCHAR)
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
                    enum_feature=EnumFeature.BLUE.value,
                    float_feature=3.14,
                    datetime_feature=datetime(2000, 1, 1, tzinfo=timezone.utc),
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


def get_model_to_features(model: Any):
    return SQLExecuteFeatures(  # type: ignore -- pyright does not understand the constructor
        id=model.id,
        str_feature=model.str_feature,
        int_feature=model.int_feature,
        bool_feature=model.bool_feature,
        float_feature=model.float_feature,
        enum_feature=model.enum_feature,
        datetime_feature=model.datetime_feature,
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


@pytest.fixture
def graph_list(sql_source: BaseSQLSourceProtocol, model: Any):
    @batch
    def sql_execute_resolve_all_list() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.list_feature,
    ]:
        return sql_source.query(get_model_to_list_features(model))

    @batch
    def sql_execute_resolve_not_null_list() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.list_feature,
    ]:
        return sql_source.query(get_model_to_list_features(model)).filter(model.id == 1)

    @batch
    def sql_execute_resolve_null_list() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.list_feature,
    ]:
        return sql_source.query(get_model_to_list_features(model)).filter(model.id == 2)

    return sql_execute_resolve_all_list, sql_execute_resolve_not_null_list, sql_execute_resolve_null_list


@pytest.fixture
def graph(sql_source: BaseSQLSourceProtocol, model: Any):
    @batch
    def sql_execute_resolve_all() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.str_feature,
        SQLExecuteFeatures.bool_feature,
        SQLExecuteFeatures.float_feature,
        SQLExecuteFeatures.int_feature,
        SQLExecuteFeatures.datetime_feature,
        SQLExecuteFeatures.enum_feature,
        SQLExecuteFeatures.nested_features_id,
        SQLExecuteFeatures.nested_features.id,
        SQLExecuteFeatures.nested_features.nested_int,
    ]:
        return sql_source.query(get_model_to_features(model))

    @batch
    def sql_execute_resolve_not_null() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.str_feature,
        SQLExecuteFeatures.bool_feature,
        SQLExecuteFeatures.int_feature,
        SQLExecuteFeatures.float_feature,
        SQLExecuteFeatures.datetime_feature,
        SQLExecuteFeatures.enum_feature,
        SQLExecuteFeatures.nested_features_id,
        SQLExecuteFeatures.nested_features.id,
        SQLExecuteFeatures.nested_features.nested_int,
    ]:
        return sql_source.query(get_model_to_features(model)).filter(model.id == 1)

    @batch
    def sql_execute_resolve_null() -> DataFrame[
        SQLExecuteFeatures.id,
        SQLExecuteFeatures.str_feature,
        SQLExecuteFeatures.bool_feature,
        SQLExecuteFeatures.int_feature,
        SQLExecuteFeatures.enum_feature,
        SQLExecuteFeatures.float_feature,
        SQLExecuteFeatures.datetime_feature,
        SQLExecuteFeatures.nested_features_id,
        SQLExecuteFeatures.nested_features.id,
        SQLExecuteFeatures.nested_features.nested_int,
    ]:
        return sql_source.query(get_model_to_features(model)).filter(model.id == 2)

    return sql_execute_resolve_all, sql_execute_resolve_not_null, sql_execute_resolve_null


@pytest.mark.parametrize("sql_source", ["postgres", "postgres_no_csv", "sqlite", "snowflake"], indirect=True)
@pytest.mark.skipif(pl is None, reason="polars is not installed")
class TestExecute:
    def _test_harness(self, resolver: OfflineResolver[Any, DataFrame], expected: DataFrame):
        # Test that calling the resolver directly returns a dataframe
        direct_query = resolver()
        assert isinstance(direct_query, DataFrame)
        assert (direct_query == expected).all()

        # Also test manually invoking via execute_to_datafrmae
        indirect_query = cast(ChalkQueryProtocol, resolver.fn())
        finalized_query = indirect_query.all()
        if isinstance(resolver.output.features[0], type) and issubclass(resolver.output.features[0], DataFrame):
            features = resolver.output.features[0].columns
        else:
            features = resolver.output.features
        output_df = finalized_query.execute_to_dataframe(features)
        assert (output_df == expected).all()

    def test_resolve_all(self, graph: Tuple[OfflineResolver, OfflineResolver, OfflineResolver]):
        sql_execute_resolve_all = graph[0]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1, 2],
                SQLExecuteFeatures.str_feature: ['hello\n,"Ravi"', None],
                SQLExecuteFeatures.int_feature: [2, None],
                SQLExecuteFeatures.bool_feature: [True, None],
                SQLExecuteFeatures.enum_feature: [EnumFeature.BLUE, None],
                SQLExecuteFeatures.float_feature: [3.14, None],
                SQLExecuteFeatures.datetime_feature: [datetime(2000, 1, 1, tzinfo=timezone.utc), None],
                SQLExecuteFeatures.nested_features_id: [4, None],
                SQLExecuteFeatures.nested_features.id: [4, None],
                SQLExecuteFeatures.nested_features.nested_int: [5, None],
            }
        )
        self._test_harness(sql_execute_resolve_all, expected)

    def test_resolve_not_null(self, graph: Tuple[OfflineResolver, OfflineResolver, OfflineResolver]):
        sql_execute_resolve_not_null = graph[1]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1],
                SQLExecuteFeatures.str_feature: ['hello\n,"Ravi"'],
                SQLExecuteFeatures.int_feature: [2],
                SQLExecuteFeatures.bool_feature: [True],
                SQLExecuteFeatures.enum_feature: [EnumFeature.BLUE],
                SQLExecuteFeatures.float_feature: [3.14],
                SQLExecuteFeatures.datetime_feature: [datetime(2000, 1, 1, tzinfo=timezone.utc)],
                SQLExecuteFeatures.nested_features_id: [4],
                SQLExecuteFeatures.nested_features.id: [4],
                SQLExecuteFeatures.nested_features.nested_int: [5],
            }
        )
        self._test_harness(sql_execute_resolve_not_null, expected)

    def test_resolve_null(self, graph: Tuple[OfflineResolver, OfflineResolver, OfflineResolver]):
        sql_execute_resolve_null = graph[2]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [2],
                SQLExecuteFeatures.str_feature: [None],
                SQLExecuteFeatures.int_feature: [None],
                SQLExecuteFeatures.bool_feature: [None],
                SQLExecuteFeatures.enum_feature: [None],
                SQLExecuteFeatures.float_feature: [None],
                SQLExecuteFeatures.datetime_feature: [None],
                SQLExecuteFeatures.nested_features_id: [None],
                SQLExecuteFeatures.nested_features.id: [None],
                SQLExecuteFeatures.nested_features.nested_int: [None],
            }
        )
        self._test_harness(sql_execute_resolve_null, expected)

    def test_resolve_all_list(
        self, graph_list: Tuple[OfflineResolver, OfflineResolver, OfflineResolver], sql_source: BaseSQLSourceProtocol
    ):
        if not isinstance(sql_source, PostgreSQLSourceImpl):
            pytest.skip("Only postgres supports arrays")
        if not env_var_bool("CHALK_DISABLE_POSTGRES_CSV_TO_PYARROW"):
            pytest.xfail("ARRAY features are not supported with CSV to pyarrow")
        sql_execute_resolve_all = graph_list[0]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1, 2],
                SQLExecuteFeatures.list_feature: [["foo", "bar"], None],
            }
        )
        self._test_harness(sql_execute_resolve_all, expected)

    def test_resolve_not_null_list(
        self, graph_list: Tuple[OfflineResolver, OfflineResolver, OfflineResolver], sql_source: BaseSQLSourceProtocol
    ):
        if not isinstance(sql_source, PostgreSQLSourceImpl):
            pytest.skip("Only postgres supports arrays")
        if not env_var_bool("CHALK_DISABLE_POSTGRES_CSV_TO_PYARROW"):
            pytest.xfail("ARRAY features are not supported with CSV to pyarrow")
        sql_execute_resolve_not_null = graph_list[1]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [1],
                SQLExecuteFeatures.list_feature: [["foo", "bar"]],
            }
        )
        self._test_harness(sql_execute_resolve_not_null, expected)

    def test_resolve_null_list(
        self, graph_list: Tuple[OfflineResolver, OfflineResolver, OfflineResolver], sql_source: BaseSQLSourceProtocol
    ):
        if not isinstance(sql_source, PostgreSQLSourceImpl):
            pytest.skip("Only postgres supports arrays")
        if not env_var_bool("CHALK_DISABLE_POSTGRES_CSV_TO_PYARROW"):
            pytest.xfail("ARRAY features are not supported with CSV to pyarrow")
        sql_execute_resolve_null = graph_list[2]
        expected = DataFrame(
            {
                SQLExecuteFeatures.id: [2],
                SQLExecuteFeatures.list_feature: [None],
            }
        )
        self._test_harness(sql_execute_resolve_null, expected)
