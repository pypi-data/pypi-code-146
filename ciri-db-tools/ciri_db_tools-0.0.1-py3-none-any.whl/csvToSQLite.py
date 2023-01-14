"""
This script reads in CSV and EXCEL files,
converts them into pandas dataframes,
and then reads those dataframes into a SQLite database
Mandatory installations:
pip install pandas
pip install openpyxl
"""

import pandas as pd
import sqlite3
from sqlite3 import Error
import os

path = 'ciri_results_db/csvConverters/csvData'
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
except Error as e:
    print(e)
finally:
    print("Done [1]: Dataframe list complete")
    print("Start [2]: Reading dataframes to test SQLite database")
try:
    table_index = 0
    for table in table_list:
        dbname = "test"
        tbname = table_name_list[table_index]
        if '-' in table_name_list[table_index]:
            dbname = table_name_list[table_index].split('-')[0]
            tbname = table_name_list[table_index].split('-')[1]
        connection = sqlite3.connect("./ciri_results_db/csvConverters/" + dbname + ".db")
        sqliteCursor = connection.cursor()
        table_list[table_index].to_sql(tbname, connection, index=False)
        table_index+=1
except Error as e:
    print(e)
finally:
    print("Done [2]: Done reading dataframes to test SQLite database.")