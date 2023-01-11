from typing import Any, Generator, Optional, Sequence

import sqlalchemy as sa

import sqlalchemize.types as types
import sqlalchemize.features as features
import sqlalchemize.exceptions as exceptions
import sqlalchemy.sql.elements as sa_elements
import sqlalchemize.exceptions as ex


def select_records_all(
    sa_table: sa.Table,
    connection: Optional[types.SqlConnection],
    sorted: bool = False,
    include_columns: Optional[Sequence[str]] = None
) -> list[types.Record]:
    connection = ex.check_for_engine(sa_table, connection)
    if include_columns is not None:
        columns = [features.get_column(sa_table, column_name) for column_name in include_columns]
        query = sa.select(*columns)
    else:
        query = sa.select(sa_table)

    if sorted:
        query = query.order_by(*features.primary_key_columns(sa_table))
    results = connection.execute(query)
    return [dict(r) for r in results]


def select_records_chunks(
    sa_table: sa.Table,
    connection: Optional[types.SqlConnection],
    chunksize: int = 2,
    sorted: bool = False,
    include_columns: Optional[Sequence[str]] = None
) -> Generator[list[types.Record], None, None]:
    connection = ex.check_for_engine(sa_table, connection)
    if include_columns is not None:
        columns = [features.get_column(sa_table, column_name) for column_name in include_columns]
        query = sa.select(*columns)
    else:
        query = sa.select(sa_table)

    if sorted:
        query = query.order_by(*features.primary_key_columns(sa_table))
    stream = connection.execute(query, execution_options={'stream_results': True})
    for results in stream.partitions(chunksize):
        yield [dict(r) for r in results]


def select_existing_values(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    column_name: str,
    values: Sequence,
) -> list:
    column = features.get_column(sa_table, column_name)
    query = sa.select([column]).where(column.in_(values))
    return connection.execute(query).scalars().fetchall()


def select_column_values_all(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    column_name: str
) -> list:
    query = sa.select(features.get_column(sa_table, column_name))
    return connection.execute(query).scalars().all()


def select_column_values_chunks(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    column_name: str,
    chunksize: int
) -> Generator[list, None, None]:
    query = sa.select(features.get_column(sa_table, column_name))
    stream = connection.execute(query, execution_options={'stream_results': True})
    for results in stream.scalars().partitions(chunksize):  # type: ignore
        yield results


def select_records_slice(
    sa_table: sa.Table,
    connection: Optional[types.SqlConnection] = None,
    start: Optional[int] = None,
    stop: Optional[int] = None,
    sorted: bool = False,
    include_columns: Optional[Sequence[str]] = None
) -> list[types.Record]:
    connection = ex.check_for_engine(sa_table, connection)
    start, stop = _convert_slice_indexes(sa_table, connection, start, stop)
    if stop < start:
        raise exceptions.SliceError('stop cannot be less than start.')
    if include_columns is not None:
        columns = [features.get_column(sa_table, column_name) for column_name in include_columns]
        query = sa.select(*columns)
    else:
        query = sa.select(sa_table)
    if sorted:
        query = query.order_by(*features.primary_key_columns(sa_table))
    query = query.slice(start, stop)
    results = connection.execute(query)
    return [dict(r) for r in results]


def _convert_slice_indexes(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    start: Optional[int] = None,
    stop: Optional[int] = None
) -> tuple[int, int]:
    # start index is 0 if None
    start = 0 if start is None else start
    row_count = features.get_row_count(sa_table, connection)
    
    # stop index is row count if None
    stop = row_count if stop is None else stop
    # convert negative indexes
    start = _calc_positive_index(start, row_count)
    start = _stop_underflow_index(start, row_count)
    stop = _calc_positive_index(stop, row_count)
    stop = _stop_overflow_index(stop, row_count)

    if row_count == 0:
        return 0, 0

    return start, stop


def _calc_positive_index(
    index: int,
    row_count: int
) -> int:
    # convert negative index to real index
    if index < 0:
        index = row_count + index
    return index


def _stop_overflow_index(
    index: int,
    row_count: int
) -> int:
    if index > row_count - 1:
        return row_count
    return index

    
def _stop_underflow_index(
    index: int,
    row_count: int
) -> int:
    if index < 0 and index < -row_count:
        return 0
    return index


def select_column_values_by_slice(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    column_name: str,
    start: Optional[int] = None,
    stop: Optional[int] = None
) -> list:
    start, stop = _convert_slice_indexes(sa_table, connection, start, stop)
    if stop < start:
        raise exceptions.SliceError('stop cannot be less than start.')
    query = sa.select(features.get_column(sa_table, column_name)).slice(start, stop)
    return connection.execute(query).scalars().all()


def select_column_value_by_index(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    column_name: str,
    index: int
) -> Any:
    if index < 0:
        row_count = features.get_row_count(sa_table, connection)
        if index < -row_count:
            raise IndexError('Index out of range.') 
        index = _calc_positive_index(index, row_count)
    query = sa.select(features.get_column(sa_table, column_name)).slice(index, index+1)
    return connection.execute(query).scalars().all()[0]


def select_primary_key_records_by_slice(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    _slice: slice,
    sorted: bool = False
) -> list[types.Record]:
    start = _slice.start
    stop = _slice.stop
    start, stop = _convert_slice_indexes(sa_table, connection, start, stop)
    if stop < start:
        raise exceptions.SliceError('stop cannot be less than start.')
    primary_key_values = features.primary_key_columns(sa_table)
    if sorted:
        query = sa.select(primary_key_values).order_by(*primary_key_values).slice(start, stop)
    else:
        query = sa.select(primary_key_values).slice(start, stop)
    results = connection.execute(query)
    return [dict(r) for r in results]


def select_record_by_primary_key(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    primary_key_value: types.Record,
    include_columns: Optional[Sequence[str]] = None
) -> types.Record:
    # TODO: check if primary key values exist
    where_clause = features.get_where_clause(sa_table, primary_key_value)
    if len(where_clause) == 0:
        raise exceptions.MissingPrimaryKey('Primary key values missing in table.')
    if include_columns is not None:
        columns = [features.get_column(sa_table, column_name) for column_name in include_columns]
        query = sa.select(*columns).where((sa_elements.and_(*where_clause)))
    else:
        query = sa.select(sa_table).where((sa_elements.and_(*where_clause)))
    results = connection.execute(query)
    results = [dict(x) for x in results]
    if len(results) == 0:
        raise exceptions.MissingPrimaryKey('Primary key values missing in table.')
    return results[0]


def select_records_by_primary_keys(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    primary_keys_values: Sequence[types.Record],
    schema: Optional[str] = None,
    include_columns: Optional[Sequence[str]] = None
) -> list[types.Record]:
    # TODO: check if primary key values exist
    where_clauses = []
    for record in primary_keys_values:
        where_clause = features.get_where_clause(sa_table, record)
        where_clauses.append(sa_elements.and_(*where_clause))
    if len(where_clauses) == 0:
        return []
    if include_columns is not None:
        columns = [features.get_column(sa_table, column_name) for column_name in include_columns]
        query = sa.select(*columns).where((sa_elements.or_(*where_clauses)))
    else:
        query = sa.select(sa_table).where((sa_elements.or_(*where_clauses)))
    results = connection.execute(query)
    return [dict(r) for r in results]


def select_column_values_by_primary_keys(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    column_name: str,
    primary_keys_values: Sequence[types.Record]
) -> list:
    # TODO: check if primary key values exist
    where_clauses = []
    for record in primary_keys_values:
        where_clause = features.get_where_clause(sa_table, record)
        where_clauses.append(sa_elements.and_(*where_clause))

    if len(where_clauses) == 0:
        return []
    query = sa.select(features.get_column(sa_table, column_name)).where((sa_elements.or_(*where_clauses)))
    results = connection.execute(query)
    return results.scalars().fetchall()


def select_value_by_primary_keys(
    sa_table: sa.Table,
    connection: types.SqlConnection,
    column_name: str,
    primary_key_value: types.Record,
    schema: Optional[str] = None
) -> Any:
    # TODO: check if primary key values exist
    where_clause = features.get_where_clause(sa_table, primary_key_value)
    if len(where_clause) == 0:
        raise KeyError('No such primary key values exist in table.')
    query = sa.select(features.get_column(sa_table, column_name)).where((sa_elements.and_(*where_clause)))
    return connection.execute(query).scalars().all()[0]