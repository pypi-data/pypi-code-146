# db_functions.py
# -*- coding: utf-8 -*-

"""
Functions which serve for database purposes
"""

import warnings

from collections import namedtuple
import pandas as pd
from tqdm import tqdm

import sqlalchemy as sa
from sqlalchemy import exc

from .util_functions import input_prompt


# ______________________________________________________________________________________________________________________


def create_db_engine(db_cfg: dict, db_conn_info: dict, db_name: str = None) -> tuple:
    """
    Opens a connection to a database you can choose or specify upfront

    Args:
        db_cfg: dictionary containing the configuration information for the database
        db_conn_info: dictionary with the available database names as keys and connection information as values
        db_name: (optional) name of database, if None lets you choose from all available databases

    Returns:
        a named tuple with the following fields: db_name, engine
    """

    # db_cfg = cfg.Database.toDict(); db_conn_info = db_available; db_name = None; verbose = True

    fields = ('db_name', 'engine')
    DB = namedtuple('DB', fields, defaults=(None,) * len(fields))

    if not db_name:
        db_name = input_prompt(
            name='database',
            choices=tuple(db_conn_info.keys()),
            enum=True,
        )

    conn_str = None
    if db_cfg[db_name]['type'] == 'MS SQL Server':
        conn_str = db_cfg[db_name]['driver'] + ':///?odbc_connect='
    elif db_cfg[db_name]['type'] in ('MariaDB', 'PostgreSQL'):
        conn_str = db_cfg[db_name]['driver'] + '://'
    elif db_cfg[db_name]['type'] == 'SQLite3':
        conn_str = db_cfg[db_name]['driver'] + ':///'
    conn_str += str(db_conn_info[db_name])

    engine = sa.create_engine(conn_str, future=True)

    return DB(db_name=db_name, engine=engine)


# ______________________________________________________________________________________________________________________


def execute_raw_sql(qry: str | sa.sql.elements.TextClause, con: sa.engine.Connection | sa.engine.Engine) -> None:
    """
    Executes a sql statement and does not return anything

    Args:
        qry: the sql query to be executed, either a string or sqlalchemy text clause
        con: either the sqlalchemy connection or engine to the database

    Returns:
        Executes and commits the statement against the database and returns None
    """

    if type(qry).__name__ == 'str':
        qry = sa.text(qry)
    elif type(qry).__name__ != 'TextClause':
        raise TypeError('argument qry must be either a string or sqlalchemy.text!')

    con_type = type(con).__name__
    if con_type == 'Engine':
        con = con.connect()
    try:
        con.execute(qry)
        con.commit()
    except Exception as ex:
        raise ex
    finally:
        if con_type == 'Engine':
            con.close()

    return None


# ______________________________________________________________________________________________________________________


def loop_insert_df_to_table(
        df: pd.DataFrame,
        tbl_name: str,
        tbl_schema: str,
        con: sa.engine.Connection | sa.engine.Engine,
        if_exists: str = 'append',
        verbose: bool = False,
) -> list:
    """
    inserts rows to a database table in a loop

    Args:
        df: the dataframe which should be inserted
        tbl_name: the name of the database table
        tbl_schema: the name of the database schema where the table is located
        con: either the sqlalchemy connection or engine to the database
        if_exists: what to do if the table already exists
        verbose: whether to show a loop progress bar and print statements

    Returns:
        a list with the indexes of the rows which where NOT inserted due to integrity errors
    """

    dup_rows = []
    len_df = len(df)
    df.reset_index(drop=True, inplace=True)
    sequence = tqdm(range(len_df)) if verbose else range(len_df)
    for i in sequence:
        try:
            df.loc[i:i].to_sql(tbl_name, schema=tbl_schema, index=False, con=con, if_exists=if_exists, method=None)
        except exc.IntegrityError:
            dup_rows.append(i)
    if len(dup_rows) > 0:
        warnings.warn(f'{len(dup_rows)} integrity error(s) due to duplicate row(s)')
    if verbose:
        stmt = f'{len_df - len(dup_rows)} row(s) inserted'
        stmt += f', {len(dup_rows)} duplicate row(s) where not inserted' if len(dup_rows) > 0 else ''
        print(stmt)

    return dup_rows

# ______________________________________________________________________________________________________________________
