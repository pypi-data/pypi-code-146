"""
This script reads in either a .db file or connects to a postgres db,
converts them into pandas dataframes,
and then reads those dataframes to a CSV file
Mandatory installations:
pip install pandas
pip install sqlalchemy
"""

import pandas as pd
from sqlite3 import Error
import sqlite3
import os
from sqlalchemy import create_engine
import psycopg2;

# Set to either SQLite or PG database
PG2CSV = False
SQLITE2CSV = False

TARGET_TABLES = ["tblEcoBoundary", "tblAdminBoundary"]

# Where you want the CSV files to generate.
RESULTPATH = './ciri_results_db/csvConverters/csvResults/'
try:
    print("START")
    if SQLITE2CSV == True:
        print("SQLITE2CSV-START")
        SQLITE_LOCATION = "./ciri_results_db/sample_dbs/special_dbs"
        for file in os.listdir(SQLITE_LOCATION):
            if file.endswith(".db"):
                fullpath = "./ciri_results_db/sample_dbs/" + file
                conn = sqlite3.connect(fullpath)
                filename = file.split(".")[0]
                for table in TARGET_TABLES:
                    sqliteDF = pd.read_sql("SELECT * FROM " + table, conn)
                    sqliteDF.to_csv(RESULTPATH + filename + "-" + table + ".csv", mode='w', index=False)
        print("SQLITE2CSV-END")

    if PG2CSV == True:
        print("PG2CSV-START")
        PG_CONN = 'postgresql://postgres:cmpt276@localhost:5432/schematest2'
        schema_conn = psycopg2.connect(PG_CONN)
        cursor = schema_conn.cursor()
        conn = create_engine(PG_CONN)
        for table in TARGET_TABLES:
            cursor.execute("SELECT table_schema FROM information_schema.tables WHERE table_name=%(tbl)s;", {"tbl": table})
            results = cursor.fetchall()
            for result in results:
                pgDF = pd.read_sql("SELECT * FROM \"" + result[0] + "\".\"" + table + "\"", conn)
                pgDF.to_csv(RESULTPATH + result[0] + "-" + table + ".csv", mode='w', index=False)
        print("PG2CSV-END")
except Error as e:
    print(e)

finally:
    print("END")
