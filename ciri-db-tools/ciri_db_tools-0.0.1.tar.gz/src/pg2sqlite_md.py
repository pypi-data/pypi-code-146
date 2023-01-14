import unicodedata
import psycopg2  # pip install psycopg2. It is a Python Driver for PostgreSQL.
import sqlite3
from sqlite3 import Error
import pandas as pds
from sqlalchemy import create_engine

def pg2sqlite_copy(pgconn_input, loc_input):
    SQLITE_LOCATION = loc_input
    connectionString = pgconn_input #'postgresql://postgres:cmpt276@localhost:5432/schematest2'
    # Connection String last updated Jan. 10, 2023.
    try:
        #   Establish pg and sqlite3 db connections, get all table names from pg db
        pgConnection = psycopg2.connect(connectionString)
        pgCursor = pgConnection.cursor()
        pgCursor.execute(
            "SELECT schema_name FROM information_schema.schemata;"
        )
        schema_list_unfiltered = pgCursor.fetchall()
        schema_list = []
        IGNORE_SCHEMA = ['pg_toast', 'public', 'pg_catalog', 'information_schema']
        for item in schema_list_unfiltered:
            schema_list.append(item[0])
        for ign_sch in IGNORE_SCHEMA:
            schema_list.remove(ign_sch)

        for schema in schema_list:
            pgCursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = %(schema)s;", {"schema": schema})
            tables = pgCursor.fetchall()
            alchemyEngine = create_engine(connectionString)
            connection = sqlite3.connect(SQLITE_LOCATION + schema + ".db")
            #sqliteCursor = connection.cursor()
            # connection.text_factory = lambda x: unicodedata(x, 'utf-8', 'ignore')
            
            # Convert pg db contents to pandas df, then write df to sqlite3 db
            for table in tables:
                dbConnection = alchemyEngine.connect()
                dbQuery = 'SELECT * from "' + schema + '"."' + table[0] + '";'
                dataFrame = pds.read_sql(dbQuery, dbConnection)
                pds.set_option('display.expand_frame_repr', False)
                dbConnection.close()
                try:
                    dataFrame.to_sql(table[0], connection,
                                    if_exists='replace', index=False)

                    #   For columns with datatypes not supported by sqlite (like TEXT[], change them to type TEXT)
                except Error as e:
                    invalidParameterIndex = int(
                        ''.join(filter(str.isdigit, str(e))))
                    err_col = dataFrame.head(0).columns[invalidParameterIndex]
                    dataFrame[err_col] = dataFrame[err_col].astype(str)
                    dataFrame.to_sql(table[0], connection,
                                    if_exists='replace', index=False)
            if connection:
                connection.close()
        #   Close connection and finish script execution.
    except Error as e:
        print(e)
    finally:
        print("POSTGRES TO SQLITE CONVERSION COMPLETE")
