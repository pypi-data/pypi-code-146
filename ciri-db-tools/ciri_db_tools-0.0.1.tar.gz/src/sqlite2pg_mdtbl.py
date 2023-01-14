import unicodedata
import psycopg2  # pip install psycopg2. It is a Python Driver for PostgreSQL.
import sqlite3
from sqlite3 import Error
import pandas as pds
from sqlalchemy import create_engine
import os


# This script connects to a SQLITE DB and creates table entries in the metadata schema of the pg db.
def sqlite2pg_copy(db_input, us_input, pw_input, hs_input, pt_input, loc_input):
    database = db_input #'schematest2'
    user = us_input #'postgres'
    password = pw_input #'cmpt276'
    host = hs_input #'localhost'
    port = pt_input #'5432'
    pgConnection = 'postgresql://' + user + ':' + \
        password + '@' + host + ':' + port + '/' + database
    SQLITE_DB_LOCATION = loc_input #"./ciri_results_db/csvConverters"

    #file = ""
    tblNmDcDm = []
    try:
        print("start")
        conn = sqlite3.connect(SQLITE_DB_LOCATION)
        cursor = conn.cursor()
        cursor.execute('SELECT name from sqlite_master where type= "table"')
        tables = cursor.fetchall()
        for table in tables:
            col_list = []
            table_name = table[0]
            table_description = table_name + " description"
            database_name = "NS_14_2BTUpdate_results"
            cursor.execute("PRAGMA table_info('" + table_name + "')")
            columns = cursor.fetchall()
            for column in columns:
                col_list.append(column[1])
            col_string = str(col_list)
            col_string_1 = col_string.replace("[", "{")
            column_list = col_string_1.replace("]","}")
            tblNmDcDm.append({"table_name": table_name, "table_description": table_description, "database_name": database_name, "column_list": column_list})
        tblIgnoreList = []
        pgConn = psycopg2.connect(pgConnection)
        pgCursor = pgConn.cursor()
        pgCursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='metadata'")
        pgTbls = pgCursor.fetchall()
        for pgTbl in pgTbls:
            tblIgnoreList.append(pgTbl[0])

        pgCursor.execute("BEGIN TRANSACTION;")
        for item in tblNmDcDm:
            if item["table_name"] not in tblIgnoreList:
                print(item["table_name"])
                pgCursor.execute("INSERT INTO metadata.table_metadata (table_name, table_description, database_name, column_list) VALUES (%s, %s, %s, %s);",
                (item["table_name"], item["table_description"], item["database_name"], item["column_list"]))
        pgCursor.execute("COMMIT;")
        pgConn.close()
    except Error as e:
        print(e)

    finally:
        print("done")