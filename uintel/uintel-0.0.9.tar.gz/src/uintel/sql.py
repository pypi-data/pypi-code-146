"""
Connect (or create) databases on postgreSQL servers, as well as upload DataFrames to a database
"""

__all__ = ["connect", "write_dataframe_to_sql"]

import io, sqlalchemy, sqlalchemy_utils, psycopg2, pandas
from uintel import config

def connect(database_name: str) -> dict:
    """
    Connect to the given database (e.g. 'chap'), using the stored credentials for SQL. If the database does not exist, then a new database is created with this databse_name.
    """

    db = config['SQL'].copy()
    db['engine'] = sqlalchemy.create_engine(f"postgresql+psycopg2://postgres:{db['password']}@{db['host']}/{database_name}?port={db['port']}")
    db['address'] = f"host={db['host']} dbname={database_name} user=postgres password='{db['password']}' port={str(db['port'])}"

    exists = sqlalchemy_utils.database_exists(db['engine'].url)
    if not exists:
        sqlalchemy_utils.create_database(db['engine'].url)

    db['con'] = psycopg2.connect(db['address'])

    if not exists:
        db['con'].cursor().execute("CREATE EXTENSION postgis;")
        db['con'].commit()

    return db


def write_dataframe_to_sql(df: pandas.DataFrame, table_name: str, db: dict, if_exists="replace") -> None:
    """
    Writes a Pandas Dataframe object to a SQL table called *table_name*. Based on code from https://stackoverflow.com/a/47984180/5890574.
    """

    # Truncates the table and sends the column names to sql
    df.head(0).to_sql(table_name, db['engine'], if_exists=if_exists, index=False) 
    
    # Open connection to sql
    conn = db['engine'].raw_connection()
    cur = conn.cursor()
    
    # Send dataframe to stringio
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    
    # Send stringio to sql
    output.seek(0)
    cur.copy_from(output, table_name, null="") # null values become ''
    conn.commit()