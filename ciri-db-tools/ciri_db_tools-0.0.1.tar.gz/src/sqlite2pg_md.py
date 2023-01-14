import unicodedata
import psycopg2  # pip install psycopg2. It is a Python Driver for PostgreSQL.
import sqlite3
from sqlite3 import Error
import pandas as pds
from sqlalchemy import create_engine
import os

#connectionString = 'postgresql://dhylimydnuzuha:fef5693da1e3ac7a2fd02c551364deb52077dbd0e28e8f9dd129fd39c7b273b6@ec2-23-21-207-93.compute-1.amazonaws.com:5432/d87qv5eqqfjqfd'
# Connection String last updated Oct. 14th, 2022.

#   Target database credentials go here. Note, create the database first before connecting to it.
def sqlite2pg_copy(db_input, us_input, pw_input, hs_input, pt_input, dir_input):
    database = db_input #'schematest2'
    user = us_input #'postgres'
    password = pw_input #'cmpt276'
    host = hs_input #'localhost'
    port = pt_input #'5432'
    pgConnection = 'postgresql://' + user + ':' + \
        password + '@' + host + ':' + port + '/' + database
    SQLITE_DB_DIRECTORY = dir_input #"./ciri_results_db/csvConverters"
    try:
        for file in os.listdir(SQLITE_DB_DIRECTORY):
            if file.endswith(".db"):
                filename = file.split(".")[0]
                #print(filename)
                #   Connect to sqlite DB, get all sqlite DB table names, and then create postgres connection
                connection = sqlite3.connect("./ciri_results_db/csvConverters/" + file) 
                sqliteCursor = connection.cursor()
                #connection.text_factory = lambda x: unicodedata(x, 'utf-8', 'ignore')
                sqliteCursor.execute('SELECT name from sqlite_master where type= "table"')
                tables = sqliteCursor.fetchall()
                alchemyEngine = create_engine(pgConnection)

                schemaQuery = "CREATE SCHEMA IF NOT EXISTS \"" + filename + "\";"
                schemataConn = psycopg2.connect(pgConnection)
                schemataCursor = schemataConn.cursor()
                schemataCursor.execute("SELECT schema_name from information_schema.schemata;")
                results = schemataCursor.fetchall()
                print(results)
                schemataCursor.execute(schemaQuery)
                schemataConn.commit()
                #   Get all data from each sqlite tbl, store it in a pandas df, connect to pg db and write the df to it
                for table in tables:
                    table_name = filename + "." + table[0]
                    dbQuery = 'SELECT * from "' + table[0] + '";'
                    #print(dbQuery)
                    dataFrame = pds.read_sql(dbQuery, connection)
                    pds.set_option('display.expand_frame_repr', False)
                    dbConnection = alchemyEngine.connect()

                    try:
                        dataFrame.to_sql(table[0], dbConnection, schema= filename,
                                        if_exists='replace', index=False)
                        dbConnection.close()

                        psycopg2Connection = psycopg2.connect(pgConnection)
                        pgCursor = psycopg2Connection.cursor()
                        #   Query the pg db for column headers with "list" in their name (ie column_list)
                        pgCursor.execute("SELECT column_name from information_schema.columns WHERE (table_name = '" +
                                        table_name + "') AND column_name SIMILAR TO '%l" + "ist%';")
                        columns = pgCursor.fetchall()

                        #   Retrieve the string value of every element under the TEXT "list" column
                        if (len(columns) > 0):
                            for column in columns:
                                tbl_name = table_name
                                col_name = column[0]
                                pgCursor.execute("SELECT " + col_name +
                                                " FROM " + tbl_name)
                                column_lists = pgCursor.fetchall()

                                #   Update all TEXT elements containing '[...]' to TEXT[] (array) friendly format '{...}'
                                for column_list in column_lists:
                                    sqr_br_list = column_list[0]
                                    cur_br_list = ""
                                    left_br_list = sqr_br_list.replace("[", '{')
                                    cur_br_list = left_br_list.replace("]", '}')
                                    pgCursor.execute("UPDATE " + tbl_name + " SET " + col_name + " = %(r0)s WHERE " +
                                                    col_name + " = (%(r1)s);", {"r0": cur_br_list, "r1": sqr_br_list})

                                #   Change the datatype of the list column from TEXT to TEXT[] and commit the changes
                                pgCursor.execute("ALTER TABLE " + tbl_name + " ALTER COLUMN " +
                                                col_name + " TYPE TEXT[] USING " + col_name + "::TEXT[];")
                                psycopg2Connection.commit()
                                psycopg2Connection.close()
                                print("SQLITE TO POSTGRES CONVERSION COMPLETE")
                    except Error as e:
                        print(e)
                        dbConnection.close()

    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
