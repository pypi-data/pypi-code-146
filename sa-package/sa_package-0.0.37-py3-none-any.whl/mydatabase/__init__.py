import pandas as pd

from sqlalchemy.engine import URL
from sqlalchemy import create_engine


def get_engine(dbms:str, username:str, password:str, host:str, port:int, database:str):

    """
    Parameter
    ----------
    dbms : {"mysql", "postgres"}
    """

    assert dbms in ["mysql", "postgresql"], "available dbms values are mysql and postgresql only"

    if dbms == "mysql":
        
        connection_url = URL.create(
            "mssql+pyodbc",
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            query={
                "driver": "ODBC Driver 18 for SQL Server",
                "TrustServerCertificate": "yes",
                "authentication": "ActiveDirectoryIntegrated",
            },
        )

        engine = create_engine(connection_url)
        
    elif dbms == "postgresql":

        connection_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_url)
        
    return engine
