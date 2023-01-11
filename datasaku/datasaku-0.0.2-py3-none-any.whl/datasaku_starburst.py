"""starburst related module"""

#############################
###### import packages ######
#############################

import pandas as pd
from pyhive import trino
from sqlalchemy import create_engine
from requests.auth import HTTPBasicAuth

import urllib3
urllib3.disable_warnings()

# import warnings

##############################
###### set the settings ######
##############################

# warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

#####################
###### packages #####
#####################

def starburst_import(
        sqlcode: str
        , host: str
        , username: str
        , password: str
        , port: str
        ) -> pd.DataFrame:
    """
    function to import from trino
    """

    # create a connection
    try:
        cnxn = trino.connect(
                        host = host
                        , port = port
                        , username = username
                        , protocol='https'
                        , requests_kwargs={'auth': HTTPBasicAuth(username, password), 'verify':False}
                    )
        cursor = cnxn.cursor()
    except trino.DatabaseError as err:
        print("Error: Could not make connection to Starburst DB")
        print(err)

    # run query, extract column name, and close the connection
    cursor.execute(sqlcode)
    column = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns = column)
    cursor.close()
    cnxn.close()
    return df