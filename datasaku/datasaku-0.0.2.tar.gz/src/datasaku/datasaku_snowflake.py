"""snowflake related module"""

#############################
###### import packages ######
#############################

import snowflake.connector
import pandas as pd

# import warnings

##############################
###### set the settings ######
##############################

# warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

#####################
###### packages #####
#####################

def snowflake_import(sql_var_def, username_var_def, warehouse_var_def):
    """function to import from snowflake"""
    try:
        # Connecting to Snowflake using SAML 2.0-compliant IdP federated authentication
        cnxn_def = snowflake.connector.connect(
                        user = username_var_def # your email address
                        , account = 'rma76667.us-east-1'
                        , authenticator='externalbrowser'
                        , warehouse = warehouse_var_def # your warehouse such as WH_DNA_ANALYTICS
                        , database = 'DNA_PROD'
                        , schema = 'CORE'
                        , role = 'ROLE_DNA_READER'
                        ) # create a connection
        cursor_def = cnxn_def.cursor() # make a cursor
    except:
        print("fail to make snowflake connection")
    cursor_def.execute(sql_var_def) # execute the connection
    column_def = [desc[0] for desc in cursor_def.description] # create the column
    buffer_def = pd.DataFrame(cursor_def.fetchall(), columns = column_def) # fetch data with column
    cursor_def.close() # closing the cursor
    cnxn_def.close() # closing the connection
    return buffer_def # return the dataframe

def snowflake_execute(sql_var_def, username_var_def, warehouse_var_def):
    """function to import from snowflake"""
    try:
        # Connecting to Snowflake using SAML 2.0-compliant IdP federated authentication
        cnxn_def = snowflake.connector.connect(
                        user = username_var_def # your email address
                        , account = 'rma76667.us-east-1'
                        , authenticator='externalbrowser'
                        , warehouse = warehouse_var_def # your warehouse such as WH_DNA_ANALYTICS
                        , database = 'DNA_PROD'
                        , schema = 'CORE'
                        , role = 'ROLE_DNA_READER'
                        ) # create a connection
        cursor_def = cnxn_def.cursor() # make a cursor
    except:
        print("fail to make snowflake connection")
    cursor_def.execute(sql_var_def) # execute the connection
    temp_def = cursor_def.fetchall() # return of the fetch
    cursor_def.close() # closing the cursor
    cnxn_def.close() # closing the connection
    if temp_def[0][0] == 1:
        print("Command is executed successfully")