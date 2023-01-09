import pandas as pd
import sqlalchemy as sa
import pyodbc

def pushdb(data,tablename,server,database,schema):
    
    connection_string = 'DRIVER={{ODBC Driver 17 for SQL Server}};' \
                        'SERVER={server};' \
                        'DATABASE={database};' \
                        'Trusted_Connection=yes'.format(server=server, database=database)

    connection_url=sa.engine.URL.create("mssql+pyodbc",query=dict(odbc_connect=connection_string))

    engine=sa.create_engine(connection_url,fast_executemany=True)

    data.to_sql(tablename,engine,schema=schema,if_exists="fail",index=False)