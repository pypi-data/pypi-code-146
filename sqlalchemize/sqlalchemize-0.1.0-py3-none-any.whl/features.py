from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm.session as sa_session
import sqlalchemy.ext.automap as sa_automap
import sqlalchemy.engine as sa_engine

import sqlalchemize.types as types
import sqlalchemize.exceptions as ex


def primary_key_columns(
    sa_table: sa.Table
) -> list[sa.Column]:
    return list(sa_table.primary_key.columns)


def primary_key_names(
    sa_table: sa.Table
) -> list[str]:
    return [c.name for c in primary_key_columns(sa_table)]


def get_connection(
    connection: types.SqlConnection | sa_session.Session
) -> types.SqlConnection:
    if isinstance(connection, sa_session.Session):
        return connection.connection()
    return connection


def get_metadata(
    connection,
    schema: Optional[str] = None
) -> sa.MetaData:
    return sa.MetaData(bind=connection, schema=schema)


def get_table(
    name: str,
    connection: types.SqlConnection,
    schema: Optional[str] = None
) -> sa.Table:
    metadata = get_metadata(connection, schema)
    autoload_with = get_connection(connection)
    return sa.Table(name,
                 metadata,
                 autoload=True,
                 autoload_with=autoload_with,
                 extend_existing=True,
                 schema=schema)


def get_class(
    name: str,
    connection: types.SqlConnection | sa_session.Session,
    schema: Optional[str] = None
):
    metadata = get_metadata(connection, schema)
    connection = get_connection(connection)

    metadata.reflect(connection, only=[name], schema=schema)
    Base = sa_automap.automap_base(metadata=metadata)
    Base.prepare()
    if name not in Base.classes:
        raise types.MissingPrimaryKey()
    return Base.classes[name]


def get_column(
    sa_table: sa.Table,
    column_name: str
) -> sa.Column:
    return sa_table.c[column_name]


def get_table_constraints(sa_table: sa.Table):
    return sa_table.constraints


def get_primary_key_constraints(
    sa_table: sa.Table
) -> tuple[str, list[str]]:
    cons = get_table_constraints(sa_table)
    for con in cons:
        if isinstance(con, sa.PrimaryKeyConstraint):
            return con.name, [col.name for col in con.columns]
    return tuple()


def missing_primary_key(
    sa_table: sa.Table,
):
    pks = get_primary_key_constraints(sa_table)
    return pks[0] is None


def get_column_types(sa_table: sa.Table) -> dict:
    return {c.name: c.type for c in sa_table.c}


def get_column_names(sa_table: sa.Table) -> list[str]:
    return [c.name for c in sa_table.columns]


def get_table_names(
    engine: sa_engine.Engine,
    schema: Optional[str] = None
) -> list[str]:
    return sa.inspect(engine).get_table_names(schema)


def get_row_count(
    sa_table: sa.Table,
    session: Optional[types.SqlConnection] = None
) -> int:
    session = ex.check_for_engine(sa_table, session)
    col_name = get_column_names(sa_table)[0]
    col = get_column(sa_table, col_name)
    result = session.execute(sa.func.count(col)).scalar()
    return result if result is not None else 0


def get_schemas(engine: sa_engine.Engine) -> list[str]:
    insp = sa.inspect(engine)
    return insp.get_schema_names()


def get_where_clause(
    sa_table: sa.Table,
    record: types.Record
) -> list[bool]:
    return [sa_table.c[key_name]==key_value for key_name, key_value in record.items()]