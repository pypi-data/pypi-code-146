import contextlib
import io
from typing import Any, Dict, Mapping, Optional, Union

import pyarrow as pa
import pyarrow.csv
from sqlalchemy import (
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
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.engine import URL, Connection
from sqlalchemy.sql import Select

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, TableIngestMixIn, validate_dtypes_for_efficient_execution
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.missing_dependency import missing_dependency_exception

_SUPPORTED_SQLALCHEMY_TYPES_FOR_PA_CSV_QUERYING = (
    BigInteger,
    Boolean,
    Float,
    Integer,
    String,
    Text,
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

from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)


class PostgreSQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ):
        try:
            import psycopg2
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        self.host = host or load_integration_variable(integration_name=name, name="PGHOST")
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(integration_name=name, name="PGPORT", parser=int)
        )
        self.db = db or load_integration_variable(integration_name=name, name="PGDATABASE")
        self.user = user or load_integration_variable(integration_name=name, name="PGUSER")
        self.password = password or load_integration_variable(integration_name=name, name="PGPASSWORD")
        self.ingested_tables: Dict[str, Any] = {}
        BaseSQLSource.__init__(self, name=name)

    def engine_args(self) -> Mapping[str, Any]:
        return dict(
            pool_size=20,
            max_overflow=60,
            pool_pre_ping=True,
            # Trying to fix mysterious dead connection issue
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )

    def local_engine_url(self) -> URL:
        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def execute_query_efficient(
        self, finalized_query: FinalizedChalkQuery, connection: Optional[Connection] = None
    ) -> pa.Table:
        import psycopg2.sql

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(
                finalized_query.query, _SUPPORTED_SQLALCHEMY_TYPES_FOR_PA_CSV_QUERYING
            )
        stmt, positional_params, named_params = self.compile_query(finalized_query, paramstyle="named")
        assert len(positional_params) == 0, "should not have any positional params"
        # Forcing quote so the unquoted empty string will represent null values
        stmt = f"COPY ({stmt}) TO STDOUT (FORMAT CSV, HEADER true, FORCE_QUOTE *, ESCAPE '\\')"
        # Convert the param style to python3-style {}, which is what psycopg2.sql.SQL.format expects
        for named_param in named_params:
            stmt = stmt.replace(f":{named_param}", ("{" f"{named_param}" "}"))
        formatted_stmt = psycopg2.sql.SQL(stmt).format(
            **{k: psycopg2.sql.Literal(v) for (k, v) in named_params.items()}
        )
        with (self.get_engine().connect() if connection is None else contextlib.nullcontext(connection)) as cnx:
            dbapi = cnx.connection
            with dbapi.cursor() as cursor:
                buffer = io.BytesIO()
                cursor.copy_expert(formatted_stmt, buffer)
        buffer.seek(0)
        return pyarrow.csv.read_csv(
            buffer,
            parse_options=pyarrow.csv.ParseOptions(
                newlines_in_values=True,
                escape_char="\\",
                double_quote=False,
            ),
            convert_options=pyarrow.csv.ConvertOptions(
                true_values=["t"],
                false_values=["f"],
                strings_can_be_null=True,
                quoted_strings_can_be_null=False,
            ),
        )
