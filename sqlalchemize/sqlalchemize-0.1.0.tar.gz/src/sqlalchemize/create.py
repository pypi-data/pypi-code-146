from typing import Any, Iterable, Optional, Sequence
import decimal
import datetime

import sqlalchemy as sa
import sqlalchemy.engine as sa_engine
import sqlalchemy.schema as sa_schema
from tinytim.rows import row_dicts_to_data
from tinytim.data import column_names

import sqlalchemize.type_convert as type_convert
import sqlalchemize.features as features
import sqlalchemize.insert as insert

Record = dict[str, Any]


def create_table(
    table_name: str,
    column_names: Sequence[str],
    column_types: Sequence,
    primary_key: str,
    engine: sa_engine.Engine,
    schema: Optional[str] = None,
    autoincrement: Optional[bool] = True,
    if_exists: Optional[str] = 'error'
) -> sa.Table:
    
    cols = []
    
    for name, python_type in zip(column_names, column_types):
        sa_type = type_convert._type_convert[python_type]
        if name == primary_key:
            col = sa.Column(name, sa_type,
                            primary_key=True,
                            autoincrement=autoincrement)
        else:
            col = sa.Column(name, sa_type)
        cols.append(col)

    metadata = sa.MetaData(engine)
    table = sa.Table(table_name, metadata, *cols, schema=schema)
    if if_exists == 'replace':
        drop_table_sql = sa_schema.DropTable(table, if_exists=True)
        engine.execute(drop_table_sql)
    table_creation_sql = sa_schema.CreateTable(table)
    engine.execute(table_creation_sql)
    return features.get_table(table_name, engine, schema=schema)


def create_table_from_records(
    table_name: str,
    records: Sequence[Record],
    primary_key: str,
    engine: sa_engine.Engine,
    column_types: Optional[Sequence] = None,
    schema: Optional[str] = None,
    autoincrement: Optional[bool] = True,
    if_exists: Optional[str] = 'error',
    columns: Optional[Sequence[str]] = None,
    missing_value: Optional[Any] = None
) -> sa.Table:
    data = row_dicts_to_data(records, columns, missing_value)
    if column_types is None:
        column_types = [column_datatype(values) for values in data.values()]
    col_names = column_names(data)
    table = create_table(table_name, col_names, column_types, primary_key, engine, schema, autoincrement, if_exists)
    insert.insert_records(table, records, engine)
    return table


def column_datatype(values: Iterable) -> type:
    dtypes = [
        int, str, int | float, decimal.Decimal, datetime.datetime,
        bytes, bool, datetime.date, datetime.time, 
        datetime.timedelta, list, dict
    ]
    for value in values:
        for dtype in list(dtypes):
            if not isinstance(value, dtype):
                dtypes.pop(dtypes.index(dtype))
    if len(dtypes) == 2:
        if set([int, float | int]) == {int, float | int}:
            return int
    if len(dtypes) == 1:
        if dtypes[0] == float | int:
            return float
        return dtypes[0]
    return str
    
