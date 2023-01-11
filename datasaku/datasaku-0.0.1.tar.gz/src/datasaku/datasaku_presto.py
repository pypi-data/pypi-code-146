"""presto related module"""

#############################
###### import packages ######
#############################

import pandas as pd
from pyhive import presto
from sqlalchemy import create_engine

# import warnings

##############################
###### set the settings ######
##############################

# warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

#####################
###### packages #####
#####################

def presto_import(
        sqlcode: str
        , host: str
        , username: str
        , port: str
        ) -> pd.DataFrame:
    """
    function to import from presto or trino
    """

    # create a connection
    try:
        cnxn = presto.connect(
                        host = host
                        , port = port
                        , username = username
                        # , catalog = catalog
                        )
        cursor = cnxn.cursor()
    except presto.DatabaseError as err:
        print("Error: Could not make connection to Presto DB")
        print(err)

    # run query, extract column name, and close the connection
    cursor.execute(sqlcode)
    column = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns = column)
    cursor.close()
    cnxn.close()
    return df

def presto_import_multi(
        sqlcode: str
        , hosts: list
        , username: str
        , port: str
        ) -> pd.DataFrame:
    """
    function to import from presto from multiple host
    """
    # loop every host
    i = 1
    for host in hosts:
        # create a connection
        try:
            cnxn = presto.connect(
                            host = host
                            , port = port
                            , username = username
                            ) 
            cursor = cnxn.cursor() # make a cursor
        except presto.DatabaseError as err:
            print("Error: Could not make connection to Presto DB")
            print(err)

        # run query, extract column name, and close the connection
        cursor.execute(sqlcode)
        column = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns = column)
        cursor.close()
        cnxn.close()
        if i == 1:
            # if first itteration make a copy
            df_compile = df.copy()
        else:
            # compile if not the first itteration
            df_compile = pd.concat([df_compile, df], ignore_index = True)
        i = i+1
    return df_compile

def presto_store_data(host_var_def, username_var_def, df_var_def, catalog_name_var_def, schema_name_var_def, table_name_var_def):
    """function to store data in presto"""
    cnxn_def = create_engine(f"presto://{username_var_def}@{host_var_def}:8080/{catalog_name_var_def}")
    df_var_def.to_sql(name = table_name_var_def
                    , con = cnxn_def
                    , schema = schema_name_var_def
                    , index = False
                    , chunksize = 100000
                    ) # make a buffer file directly from the connection
    # cnxn_def.close() # closing the connection

def presto_store_data_multi(hosts_var_def, username_var_def, dfs_var_def, catalogs_name_var_def, schema_name_var_def, table_name_var_def):
    """function to store data in presto"""
    for host_var_def, catalog_name_def, df_var_def in zip(hosts_var_def, catalogs_name_var_def, dfs_var_def):
        cnxn_def = create_engine(f"presto://{username_var_def}@{host_var_def}:8080/{catalog_name_def}")
        df_var_def.to_sql(name = table_name_var_def
                        , con = cnxn_def
                        , schema = schema_name_var_def
                        , index = False
                        , chunksize = 100000
                        ) # make a buffer file directly from the connection
        print(f"Table is stored successfully in  {host_var_def}")
        # cnxn_def.close() # closing the connection

def presto_execute(sql_var_def, host_var_def, username_var_def):
    """function to execute in presto"""
    catalog_def = 'global' if host_var_def == 'presto-cross.taxibeat.com' else host_var_def.split('-')[1][:2] # split the catalogue
    try:
        cnxn_def = presto.connect(
                        host = host_var_def
                        , port = 8080
                        , username = username_var_def
                        , catalog = catalog_def
                        ) # create a connection
        cursor_def = cnxn_def.cursor() # make a cursor
    except presto.DatabaseError as err:
        print("Error: Could not make connection to Presto DB")
        print(err)
    cursor_def.execute(sql_var_def) # execute the sql
    temp_def = cursor_def.fetchall() # return of the fetch
    cnxn_def.close() # closing the connection
    cursor_def.close() # closing the cursor
    if temp_def[0][0] == 1:
        print("Command is executed successfully")

def presto_execute_multi(sql_var_def, hosts_var_def, username_var_def):
    """function to execute in presto"""
    i = 1
    for host_var_def in hosts_var_def:
        catalog_def = 'global' if host_var_def == 'presto-cross.taxibeat.com' else host_var_def.split('-')[1][:2] # split the catalogue
        market = list(map(host_var_map.get, [host_var_def]))[0] # change to market
        try:
            cnxn_def = presto.connect(
                            host = host_var_def
                            , port = 8080
                            , username = username_var_def
                            , catalog = catalog_def
                            ) # create a connection
            cursor_def = cnxn_def.cursor() # make a cursor
        except presto.DatabaseError as err:
            print("Error: Could not make connection to Presto DB")
            print(err)
        cursor_def.execute(sql_var_def) # execute the sql
        temp_def = cursor_def.fetchall() # return of the fetch
        cnxn_def.close() # closing the connection
        cursor_def.close() # closing the cursor
        if temp_def[0][0] == 1:
            print(f"Command {market} is executed successfully")
        i = i+1
