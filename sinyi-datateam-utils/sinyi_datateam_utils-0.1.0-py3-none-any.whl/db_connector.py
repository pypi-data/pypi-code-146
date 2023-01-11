import os
from azure.keyvault.secrets import SecretClient
from azure.identity import EnvironmentCredential
from pathlib import Path
import sqlalchemy
from sqlalchemy.engine import URL
import base64
import requests

vault_url = os.environ['AZURE_VAULT_URL']
credential = EnvironmentCredential()
client = SecretClient(vault_url,credential=credential)

class MssqlConnector:
    driver = '{ODBC Driver 17 for SQL Server}'
    server = None
    database = None
    uid = None
    pwd = None

    def __init__(self) -> None:
        pass

    @classmethod
    def connector(cls, database=None):
        if cls.database and database == None:
            database = cls.database
        
        if cls.uid:
            connection_url = URL.create(
                    "mssql+pyodbc",
                    host= cls.server,  # plain (unescaped) text
                    password= cls.pwd,
                    username= cls.uid,
                    database= database,
                    query= dict(driver='ODBC Driver 17 for SQL Server')
                )
        else:
            connection_url = URL.create(
                    "mssql+pyodbc",
                    host= cls.server,  # plain (unescaped) text
                    password= cls.pwd,
                    username= cls.uid,
                    database= database,
                    query= {
                        'driver':'ODBC Driver 17 for SQL Server',
                        'authentication': 'ActiveDirectoryIntegrated',
                        'TrustServerCertificate':'yes'
                           
                           }
                )
            
        return sqlalchemy.create_engine(connection_url, fast_executemany=True)

    @classmethod
    def query(cls, query, database=None):
        connector = cls.connector(database= database)
        cnxn = connector.connect().execution_options(autocommit=True)
        count = cnxn.execute(query).rowcount
        print(str(count), 'rows affected')

        return None

class DW001Connector(MssqlConnector):
    server = client.get_secret('dw001-server').value
    uid = client.get_secret('dw001-uid').value
    pwd = client.get_secret('dw001-pwd').value

class AzureADSConnector(MssqlConnector):
    server = client.get_secret('azureADS-server').value
    database = 'ADS'
    uid = client.get_secret('azureADS-uid').value
    pwd = client.get_secret('azureADS-pwd').value

class AzureTMPConnector(MssqlConnector):
    server = client.get_secret('azureADS-server').value
    database = 'TMP'
    uid = client.get_secret('azureADS-uid').value
    pwd = client.get_secret('azureADS-pwd').value

    
