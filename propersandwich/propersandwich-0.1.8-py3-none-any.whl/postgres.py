"""
This module will help to perform CRUD operations with Postgres databases
"""

import psycopg2
from dotenv import load_dotenv
import os
import io
import logging
import pandas as pd

load_dotenv()


def connection(database):
    """
    Create a session with a given database and return a new connection object.


    :param str database: the name of the database that will be used as prefix to get its credentials

    :returns: connection object
    :rtype: connection

    """

    dbname = os.getenv(f'{database}_DBNAME')
    user = os.getenv(f'{database}_USER')
    password = os.getenv(f'{database}_PASSWORD')
    host = os.getenv(f'{database}_HOST')
    port = os.getenv(f'{database}_PORT')

    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)


def query(database, sql_query) -> list:
    """
    Run a query against a database then returns it's result as a list


    :param str database: the name of the database that will be used as prefix to get its credentials
    :param str sql_query: The sql query that will be executed

    :returns: a list of records
    :rtype: list

    """
    try:
        conn = connection(database)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()

        # Convert the data to a dataframe
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

    except (Exception, psycopg2.Error) as error: # pragma: no cover
        logging.error(f'Error while executing query on {database} database', error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info(f'The connection to {database} database is now closed')

    return df


def replace_table(database, table, data) -> bool:
    """
    Replace an existing table with a new one or create it if it doesn't exist yet

    :param str database: The name of the database.
    :param str table: The name of the table.
    :param pd.Dataframe data: The dataframe that contains the data to write to the table.

    :return: True if the write was successful, False otherwise.
    :rtype: bool

    """

    try:
        conn = connection(database)
        cursor = conn.cursor()

        # Drop table if it exists
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
        conn.commit()

        # Create table
        columns = {col: str(_get_postgres_type(data[col].dtype)) for col in data.columns}
        create_table(database, table, columns)

        # Insert data
        with io.StringIO() as output:
            data.to_csv(output, sep=';', header=False, index=False)
            output.seek(0)
            output.getvalue()
            cursor.copy_from(output, table, sep=';', null='')
            conn.commit()

        logging.info(f'The data has been written to {table} table')

    except (Exception, psycopg2.Error) as error: # pragma: no cover
        logging.error(f'Error while executing query on {database} database', error)
        return False

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info(f'The connection to {database} database is now closed')
    return True


def upsert(database, table, data, index_column) -> bool:
    """
    Insert or update data in a table

    :param str database: The name of the database.
    :param str table: The name of the table.
    :param pd.Dataframe data: The dataframe that contains the data to write to the table.
    :param str index_column: The name of the column that will be used as index.

    :return: True if the write was successful, False otherwise.
    :rtype: bool

    """

    try:
        conn = connection(database)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        columns = {col: str(_get_postgres_type(data[col].dtype)) for col in data.columns}
        create_table(database, table, columns, primary_key=index_column)

        # If table exist, setup primary key if it doesn't exist
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM pg_constraint WHERE conname = '{table}_pkey')")
        primary_key_exist = cursor.fetchone()[0]

        if not primary_key_exist:
            cursor.execute(f'ALTER TABLE {table} ADD PRIMARY KEY ({index_column})')
            conn.commit()

        # Create an insert statement with the on conflict clause
        cols = '", "'.join(data.columns)
        cols = f'"{cols}"'
        vals = ', '.join(['%s'] * len(data.columns))
        on_conflict_stmt = f"ON CONFLICT ({index_column}) DO UPDATE SET "
        on_conflict_stmt += ', '.join([f'"{col}" = EXCLUDED."{col}"' for col in data.columns if col != index_column])
        insert_stmt = f"INSERT INTO {table} ({cols}) VALUES ({vals}) {on_conflict_stmt}"

        # Execute the insert statement
        cursor.executemany(insert_stmt, [tuple(x) for x in data.values])

        # Commit the changes and close the connection
        conn.commit()

        logging.info(f'{len(data)} rows has been upserted to {table} table')

    except (Exception, psycopg2.Error) as error: # pragma: no cover
        logging.error(f'Error while executing query on {database} database', error)
        return False

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info(f'The connection to {database} database is now closed')
    return True


def create_table(database, table, columns, primary_key=None) -> bool:
    """
    Create a table with the given columns and set primary_key if provided

    :param str database: The name of the database.
    :param str table: The name of the table.
    :param dict columns: A dictionary that contains the columns names and their types.
    :param str primary_key: The name of the column that will be used as primary key.

    :return: True if the write was successful, False otherwise.
    :rtype: bool

    """

    try:
        conn = connection(database)
        cursor = conn.cursor()

        # Create table
        column_defs = ", ".join(
            [f'"{column_name}" {column_type}' for column_name, column_type in columns.items()])
        if column_defs:
            column_defs = f"{column_defs}"
        if primary_key:
            column_defs += f", PRIMARY KEY ({primary_key})"
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ({column_defs})')
        conn.commit()

        logging.info(f'The table {table} has been created')

    except (Exception, psycopg2.Error) as error: # pragma: no cover
        logging.error(f'Error while executing query on {database} database', error)
        return False

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info(f'The connection to {database} database is now closed')
    return True


def delete_table(database, table):
    """
    Delete a table

    :param str database: The name of the database.
    :param str table: The name of the table.

    :return: True if the write was successful, False otherwise.
    :rtype: bool

    """

    try:
        conn = connection(database)
        cursor = conn.cursor()

        # Create table
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
        conn.commit()

        logging.info(f'The table {table} has been deleted')

    except (Exception, psycopg2.Error) as error: # pragma: no cover
        logging.error(f'Error while executing query on {database} database', error)
        return False

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info(f'The connection to {database} database is now closed')
    return True


def _get_postgres_type(dtype):
    """
    Map a pandas dtype to a PostgreSQL type.

    :param dtype dtype: The dtype to map.

    :return: The corresponding PostgreSQL type.
    :rtype: str
    """
    if dtype == 'bool':
        return 'boolean'
    elif dtype == 'datetime64[ns]':
        return 'timestamp'
    elif dtype in ['float16', 'float32']:
        return 'real'
    elif dtype == 'float64':
        return 'double precision'
    elif dtype in ['int32', 'uint16']:
        return 'integer'
    elif dtype in ['int64', 'uint32', 'uint64']:
        return 'bigint'
    elif dtype in ['int8', 'int16', 'uint8']:
        return 'smallint'
    elif dtype == 'timedelta[ns]':
        return 'interval'
    else:
        return 'text'
