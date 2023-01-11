from typing import Optional, Sequence

import sqlalchemy as sa
import sqlalchemy.engine as sa_engine
import sqlalchemy.orm.session as sa_session
from sqlalchemy.sql.expression import Select

import sqlalchemize.features as features
import sqlalchemize.types as types
import sqlalchemize.exceptions as ex


def delete_records_session(
    sa_table: sa.Table,
    col_name: str,
    values: Sequence,
    session: sa_session.Session
) -> None:
    """
    Example
    -------
    >>> import sqlalchemy as sa
    >>> import sqlalchemy.orm.session as session
    >>> from sqlalchemize.test_setup import create_test_table, insert_test_records
    >>> from sqlalchmize.select import select_all_records
    >>> from sqlalchmize.delete import delete_records_session

    >>> engine = sa.create_engine('data/sqlite:///test.db')
    >>> table = create_test_table(engine)
    >>> insert_test_records(table)

    >>> select_all_records(table)
    [{'id': 1, 'x': 1, 'y': 2}, {'id': 2, 'x': 2, 'y': 4}]

    >>> session = session.Session(engine)
    >>> delete_records_session(table, 'id', [1], session)

    >>> select_all_records(table)
    [{'id': 1, 'x': 1, 'y': 2}, {'id': 2, 'x': 2, 'y': 4}]

    >>> session.commit()

    >>> select_all_records(table)
    [{'id': 2, 'x': 2, 'y': 4}]
    """
    col = features.get_column(sa_table, col_name)
    session.query(sa_table).filter(col.in_(values)).delete(synchronize_session=False)


def delete_records(
    sa_table: sa.Table,
    col_name: str,
    values: Sequence,
    engine: Optional[sa_engine.Engine] = None
) -> None:
    """
    Example
    -------
    >>> import sqlalchemy as sa
    >>> from sqlalchemize.test_setup import create_test_table, insert_test_records
    >>> from sqlalchmize.delete import delete_records
    >>> from sqlalchmize.select import select_all_records

    >>> engine = sa.create_engine('data/sqlite:///test.db')
    >>> table = create_test_table(engine)
    >>> insert_test_records(table)

    >>> select_all_records(table)
    [{'id': 1, 'x': 1, 'y': 2}, {'id': 2, 'x': 2, 'y': 4}]

    >>> delete_records(table, 'id', [1])

    >>> select_all_records(table)
    [{'id': 2, 'x': 2, 'y': 4}]
    """
    engine = ex.check_for_engine(sa_table, engine)
    session = sa_session.Session(engine)
    delete_records_session(sa_table, col_name, values, session)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def delete_records_by_values(
    sa_table: sa.Table,
    engine: sa.engine.Engine,
    records: list[dict]
) -> None:
    session = sa_session.Session(engine)
    try:
        delete_records_by_values_session(sa_table, records, session)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def delete_record_by_values_session(
    sa_table: sa.Table,
    record: types.Record,
    session: sa_session.Session
) -> None:
    delete = build_delete_from_record(sa_table, record)
    session.execute(delete)


def delete_records_by_values_session(
    sa_table: sa.Table,
    records: Sequence[types.Record],
    session: sa_session.Session
) -> None:
    for record in records:
        delete_record_by_values_session(sa_table, record, session)

        
def build_where_from_record(
    sa_table: sa.Table,
    record: types.Record
) -> Select:
    s = sa.select(sa_table)
    for col, val in record.items():
        s = s.where(sa_table.c[col]==val)
    return s


def build_delete_from_record(
    sa_table: sa.Table,
    record
) -> sa.sql.Delete:
    d = sa.delete(sa_table)
    for column, value in record.items():
        d = d.where(sa_table.c[column]==value)
    return d


def delete_all_records_session(
    table: sa.Table,
    session: sa_session.Session
) -> None:
    """
    Example
    -------
    >>> import sqlalchemy as sa
    >>> import sqlalchemy.orm.session as session
    >>> from sqlalchemize.test_setup import create_test_table, insert_test_records
    >>> from sqlalchmize.select import select_all_records
    >>> from sqlalchmize.delete import delete_all_records_session

    >>> engine = sa.create_engine('data/sqlite:///test.db')
    >>> table = create_test_table(engine)
    >>> insert_test_records(table)

    >>> select_all_records(table)
    [{'id': 1, 'x': 1, 'y': 2}, {'id': 2, 'x': 2, 'y': 4}]

    >>> session = session.Session(engine)
    >>> delete_all_records_session(table, session)

    >>> select_all_records(table)
    [{'id': 1, 'x': 1, 'y': 2}, {'id': 2, 'x': 2, 'y': 4}]

    >>> session.commit()

    >>> select_all_records(table)
    []
    """
    session.query(table).delete()


def delete_all_records(
    sa_table: sa.Table,
    engine: Optional[sa_engine.Engine] = None
) -> None:
    """
    Example
    -------
    >>> import sqlalchemy as sa
    >>> from sqlalchemize.test_setup import create_test_table, insert_test_records
    >>> from sqlalchmize.select import select_all_records
    >>> from sqlalchmize.delete import delete_all_records

    >>> engine = sa.create_engine('data/sqlite:///test.db')
    >>> table = create_test_table(engine)
    >>> insert_test_records(table)

    >>> select_all_records(table)
    [{'id': 1, 'x': 1, 'y': 2}, {'id': 2, 'x': 2, 'y': 4}]

    >>> delete_all_records(table)

    >>> select_all_records(table)
    []
    """
    engine = ex.check_for_engine(sa_table, engine)
    session = sa_session.Session(engine)
    try:
        delete_all_records_session(sa_table, session)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e