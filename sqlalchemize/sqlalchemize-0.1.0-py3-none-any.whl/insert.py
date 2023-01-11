from typing import Optional, Sequence

import sqlalchemy as sa
import sqlalchemy.orm.session as sa_session
import sqlalchemy.engine as sa_engine

import sqlalchemize.types as types
import sqlalchemize.features as features
import sqlalchemize.exceptions as ex


def insert_from_table_session(
    sa_table1: sa.Table,
    sa_table2: sa.Table,
    session: sa_session.Session
) -> None:
    session.execute(sa_table2.insert().from_select(sa_table1.columns.keys(), sa_table1))


def insert_from_table(
    sa_table1: sa.Table,
    sa_table2: sa.Table,
    engine: Optional[sa_engine.Engine] = None
) -> None:
    """neither table needs primary key"""
    engine = ex.check_for_engine(sa_table1, engine)
    session = sa_session.Session(engine)
    try:
        insert_from_table_session(sa_table1, sa_table2, session)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    

def insert_records_session(
    sa_table: sa.Table,
    records: Sequence[types.Record],
    session: sa_session.Session
) -> None:
    if features.missing_primary_key(sa_table):
        insert_records_slow_session(sa_table, records, session)
    else:
        insert_records_fast_session(sa_table, records, session)


def insert_records(
    sa_table: sa.Table,
    records: Sequence[types.Record],
    engine: Optional[sa_engine.Engine] = None
) -> None:
    engine = ex.check_for_engine(sa_table, engine)
    session = sa_session.Session(engine)
    try:
        insert_records_session(sa_table, records, session)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def insert_records_fast(
    sa_table: sa.Table,
    records: Sequence[types.Record],
    engine: Optional[sa_engine.Engine] = None
) -> None:
    """Fast insert needs primary key."""
    if features.missing_primary_key(sa_table):
        raise ex.MissingPrimaryKey()
    engine = ex.check_for_engine(sa_table, engine)
    session = sa_session.Session(engine)
    try:
        insert_records_fast_session(sa_table, records, session)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def insert_records_fast_session(
    sa_table: sa.Table,
    records: Sequence[types.Record],
    session: sa_session.Session
) -> None:
    """Fast insert needs primary key."""
    if features.missing_primary_key(sa_table):
        raise ex.MissingPrimaryKey()
    table_class = features.get_class(sa_table.name, session, schema=sa_table.schema)
    mapper = sa.inspect(table_class)
    session.bulk_insert_mappings(mapper, records)


def insert_records_slow_session(
    sa_table: sa.Table,
    records: Sequence[types.Record],
    session: sa_session.Session
) -> None:
    """Slow insert does not need primary key."""
    session.execute(sa_table.insert(), records)


def insert_records_slow(
    sa_table: sa.Table,
    records: Sequence[types.Record],
    engine: Optional[sa_engine.Engine] = None
) -> None:
    """Slow insert does not need primary key."""
    engine = ex.check_for_engine(sa_table, engine)
    session = sa_session.Session(engine)
    try:
        insert_records_slow_session(sa_table, records, session)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e