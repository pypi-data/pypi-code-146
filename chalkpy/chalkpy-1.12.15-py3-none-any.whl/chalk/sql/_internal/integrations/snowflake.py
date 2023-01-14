import contextlib
from typing import Any, Optional

from sqlalchemy import (
    BIGINT,
    BINARY,
    BLOB,
    BOOLEAN,
    CHAR,
    DATETIME,
    FLOAT,
    INTEGER,
    SMALLINT,
    TEXT,
    TIMESTAMP,
    VARBINARY,
    VARCHAR,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    LargeBinary,
    SmallInteger,
    String,
    Text,
    Time,
)
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import Select

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, validate_dtypes_for_efficient_execution
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.missing_dependency import missing_dependency_exception

_SUPPORTED_SQLALCHEMY_TYPES_FOR_PA_QUERYING = (
    BigInteger,
    Boolean,
    BINARY,
    BLOB,
    LargeBinary,
    Float,
    Integer,
    Time,
    String,
    Text,
    VARBINARY,
    DateTime,
    Date,
    SmallInteger,
    BIGINT,
    BOOLEAN,
    CHAR,
    DATETIME,
    FLOAT,
    INTEGER,
    SMALLINT,
    TEXT,
    TIMESTAMP,
    VARCHAR,
)


class SnowflakeSourceImpl(BaseSQLSource):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        account_identifier: Optional[str] = None,
        warehouse: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        db: Optional[str] = None,
        schema: Optional[str] = None,
        role: Optional[str] = None,
    ):
        try:
            import snowflake  # noqa
            import snowflake.sqlalchemy  # noqa
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[snowflake]")
        del snowflake  # unused

        self.account_identifier = account_identifier or load_integration_variable(
            integration_name=name, name="SNOWFLAKE_ACCOUNT_ID"
        )
        self.warehouse = warehouse or load_integration_variable(integration_name=name, name="SNOWFLAKE_WAREHOUSE")
        self.user = user or load_integration_variable(integration_name=name, name="SNOWFLAKE_USER")
        self.password = password or load_integration_variable(integration_name=name, name="SNOWFLAKE_PASSWORD")
        self.db = db or load_integration_variable(integration_name=name, name="SNOWFLAKE_DATABASE")
        self.schema = schema or load_integration_variable(integration_name=name, name="SNOWFLAKE_SCHEMA")
        self.role = role or load_integration_variable(integration_name=name, name="SNOWFLAKE_ROLE")
        BaseSQLSource.__init__(self, name=name)

    def local_engine_url(self) -> URL:
        query = {
            k: v
            for k, v in (
                {
                    "database": self.db,
                    "schema": self.schema,
                    "warehouse": self.warehouse,
                    "role": self.role,
                }
            ).items()
            if v is not None
        }
        return URL.create(
            drivername="snowflake",
            username=self.user,
            password=self.password,
            host=self.account_identifier,
            query=query,
        )

    def execute_query_efficient(self, finalized_query: FinalizedChalkQuery, connection: Optional[Any] = None):
        # this import is safe because the only way we end up here is if we have a valid SnowflakeSource constructed,
        # which already gates this import
        import snowflake.connector

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(finalized_query.query, _SUPPORTED_SQLALCHEMY_TYPES_FOR_PA_QUERYING)

        with (
            snowflake.connector.connect(
                user=self.user,
                account=self.account_identifier,
                password=self.password,
                warehouse=self.warehouse,
                schema=self.schema,
                database=self.db,
            )
            if connection is None
            else contextlib.nullcontext(connection)
        ) as con:
            assert con is not None
            sql, positional_params, named_params = self.compile_query(finalized_query)
            assert len(positional_params) == 0, "using named param style"
            with con.cursor() as cursor:
                res = cursor.execute(sql, named_params)
                assert res is not None

                arrows = cursor.fetch_arrow_all()
                assert arrows is not None
                return arrows
