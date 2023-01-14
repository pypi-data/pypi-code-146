"""
This script reads in CSV and EXCEL files,
converts them into pandas dataframes,
and then reads those dataframes to a remote Postgres database (The Heroku Metadata DB)
Mandatory installations:
pip install pandas
pip install openpyxl
pip install sqlalchemy
"""

import pandas as pd
from sqlite3 import Error
import os
from sqlalchemy import create_engine

PG_CONN = 'postgresql://postgres:cmpt276@localhost:5432/schematest2'
path = './csvData'

table_list = []
table_name_list = []
try:
    print("Start [1]: Initializing and constructing list of dataframes")
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            fullpath = path + "/" + filename
            pdCsv = pd.read_csv(fullpath, encoding="ISO-8859-1")
            table_list.append(pdCsv)
            table_name_list.append(filename.split(".")[0])
        if filename.endswith(".xlsx"):
            fullpath = path + "/" + filename
            pdExcel = pd.read_excel(fullpath)
            table_list.append(pdExcel)
            table_name_list.append(filename.split(".")[0])
    connection = create_engine(PG_CONN)

except Error as e:
    print(e)
finally:
    print("Done [1]: Dataframe list complete")
    print("Start [2]: Reading dataframes to metadata Postgres database")
try:
    table_index = 0
    for table in table_list:
        table_list[table_index].to_sql(table_name_list[table_index], connection, index=False)
        table_index+=1
except Error as e:
    print(e)
finally:
    print("Done [2]: Done reading dataframes to metadata Postgres database.")