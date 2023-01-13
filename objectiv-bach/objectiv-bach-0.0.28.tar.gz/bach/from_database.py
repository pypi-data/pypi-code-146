"""
Copyright 2022 Objectiv B.V.
"""
from typing import Dict, Tuple, Mapping, Optional, List, Union, NamedTuple

from sqlalchemy.engine import Engine, Dialect

from bach.expression import Expression, join_expressions
from bach.types import get_dtype_from_db_dtype, StructuredDtype
from bach.utils import escape_parameter_characters
from sql_models.constants import DBDialect
from sql_models.model import SqlModel, CustomSqlModelBuilder
from sql_models.sql_generator import to_sql
from sql_models.util import is_postgres, DatabaseNotSupportedException, is_bigquery, is_athena

_DB_TYPE_CODE_TO_DB_TYPE: Mapping[DBDialect, Mapping[Union[int, str], str]] = {
    # mapping from database driver type-code to actual database types. See inline comments of
    # get_dtypes_from_model() for more information.
    DBDialect.POSTGRES: {
        # Based on `select oid, typname from pg_type order by oid;`
        16: 'boolean',
        20: 'bigint',
        25: 'text',
        114: 'json',
        701: 'double precision',
        1082: 'date',
        1083: 'time',
        1114: 'timestamp without time zone',
        1186: 'interval',
        2950: 'uuid',
        3906: 'numrange',
    },
    DBDialect.ATHENA: {},
    DBDialect.BIGQUERY: {
        # Based on experimental
        'BOOLEAN': 'BOOL',
        'FLOAT': 'FLOAT64',
        'INTEGER': 'INT64',
    }
}


class _NameType(NamedTuple):
    column_name: str
    db_dtype: str


def get_dtypes_from_model(
        engine: Engine,
        node: SqlModel,
        name_to_column_mapping: Optional[Mapping[str, str]] = None
) -> Dict[str, StructuredDtype]:
    """
    Execute the model with limit 0 and use result to deduce the model's dtypes.

    This function relies on a static mapping of the type-code returned by the database driver to the database
    type. As a result custom types might not work.

    :return: Dictionary with as key the column names, and as values the dtype of the column.
    """
    name_to_column_mapping = name_to_column_mapping if name_to_column_mapping else {}
    type_code_mapping = _DB_TYPE_CODE_TO_DB_TYPE[DBDialect.from_engine(engine)]

    new_node = CustomSqlModelBuilder(sql='select * from {{previous}} limit 0')(previous=node)
    select_statement = to_sql(dialect=engine.dialect, model=new_node)
    with engine.connect() as conn:
        sql = escape_parameter_characters(conn, select_statement)
        res = conn.execute(sql)
        # See https://peps.python.org/pep-0249/#description for information what is in description.
        # Unfortunately, the type_code is not the same as the database type on all databases. Therefore, we
        # need to map it to the actual database type
        description = res.cursor.description

    rows = [
        _NameType(column_name=row[0], db_dtype=type_code_mapping.get(row[1], row[1]))
        for row in description
    ]
    result = _get_dtype_from_db_type(
        dialect=engine.dialect,
        rows=rows,
        name_to_column_mapping=name_to_column_mapping
    )
    return result


def get_dtypes_from_table(
    engine: Engine,
    table_name: str,
    name_to_column_mapping: Optional[Mapping[str, str]] = None
) -> Dict[str, StructuredDtype]:
    """
    Query database to get dtypes of the given table.
    :param engine: sqlalchemy engine for the database.
    :param table_name: the table name for which to get the dtypes. Can include project_id and dataset on
        BigQuery, e.g. 'project_id.dataset.table_name'
    :param name_to_column_mapping: Optional mapping from series-name to column-names. The names in the
        returned dictionary will be reverse mapped with this mapping. If a column name is missing, then the
        table's column name will be assumed to be the series-names.
    :return: Dictionary with as key the series names, and as values the dtype of the matching column.
    """
    name_to_column_mapping = name_to_column_mapping if name_to_column_mapping else {}

    filters_expr = []
    if is_postgres(engine):
        meta_data_table = 'INFORMATION_SCHEMA.COLUMNS'
    elif is_bigquery(engine):
        meta_data_table, table_name = _get_bq_meta_data_table_from_table_name(table_name)
    elif is_athena(engine):
        catalog_name = (
            f"{engine.url.query['catalog_name']}." if 'catalog_name' in engine.url.query else ''
        )
        meta_data_table = f'{catalog_name}INFORMATION_SCHEMA.COLUMNS'
        # This filter is needed because athena does not limit to data from the current schema
        filters_expr.append(Expression.construct(f"table_schema='{engine.url.database}'"))
    else:
        raise DatabaseNotSupportedException(engine)

    filters_expr.append(Expression.construct(f"table_name='{table_name}'"))
    filters_stmt = join_expressions(filters_expr, join_str=' AND ').to_sql(engine.dialect)
    sql = f"""
        select column_name, data_type
        from {meta_data_table}
        where {filters_stmt}
        order by ordinal_position;
    """
    return _get_dtypes_from_information_schema_query(
        engine=engine,
        query=sql,
        name_to_column_mapping=name_to_column_mapping
    )


def _get_bq_meta_data_table_from_table_name(table_name) -> Tuple[str, str]:
    """
    From a BigQuery table name, get the meta-data table name that contains the column information for that
    table, and the short table name.
    Examples:
        'project_id.dataset.table1' -> ('project_id.dataset.INFORMATION_SCHEMA.COLUMNS', 'table1')
        'table1' -> ('INFORMATION_SCHEMA.COLUMNS', 'table1')
    :param table_name: a table name, a table name including dataset or including project_id and dataset
    :return: a tuple: the metadata table containing column information, the simple table name
    """
    parts = table_name.rsplit('.', maxsplit=1)
    if len(parts) == 2:
        project_id_dataset = parts[0] + '.'
        table_name = parts[1]
    else:
        project_id_dataset = ''
        table_name = parts[0]
    return f'{project_id_dataset}INFORMATION_SCHEMA.COLUMNS', table_name


def _get_dtypes_from_information_schema_query(
        engine: Engine,
        query: str,
        name_to_column_mapping: Mapping[str, str]
) -> Dict[str, StructuredDtype]:
    """
    Execute query and parse information_schema.columns data to a dictionary mapping Series-names to dtypes.

    If name_to_column_mapping is incomplete, the column names that the query renders will be assumed to be
    series-names.
    """
    with engine.connect() as conn:
        sql = escape_parameter_characters(conn, query)
        res = conn.execute(sql)
        rows = [_NameType(column_name=row[0], db_dtype=row[1]) for row in res.fetchall()]

    return _get_dtype_from_db_type(
        dialect=engine.dialect,
        rows=rows,
        name_to_column_mapping=name_to_column_mapping
    )


def _get_dtype_from_db_type(
        dialect: Dialect,
        rows: List[_NameType],
        name_to_column_mapping: Mapping[str, str]
) -> Dict[str, StructuredDtype]:
    """
    Return dictionary mapping series names to dtypes.
    :param dialect: dialect
    :param rows: List of tuples. Each tuple: [0] column name, [1] db_dtype
    :param name_to_column_mapping: Used to map series names to column names
    """
    db_dialect = DBDialect.from_dialect(dialect)
    column_to_name_mapping = {column: name for name, column in name_to_column_mapping.items()}
    result = {}
    for row in rows:
        series_name = column_to_name_mapping.get(row.column_name, row.column_name)
        result[series_name] = get_dtype_from_db_dtype(db_dialect, row.db_dtype)
    return result
