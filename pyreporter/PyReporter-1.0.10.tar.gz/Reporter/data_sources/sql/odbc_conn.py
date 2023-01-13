import pyodbc
from .sql_query import SqlQuery
from .sql_conn import SQLConn


# ODBCConn: Wrapper to deal with ODBC connections
# Note: This is for a very basic ODBC connection
class ODBCConn(SQLConn):
    """
    A very basic ODBC connection assuming it only requires the dsn name

    Attributes
    ----------
    dsn_name: :class:`str`
        The name of the data source to connect to
    """

    def __init__(self, dsn_name: str):
        self.dsn = dsn_name
        super().__init__()


    # connect(): Connects to the server
    def _connect_db(self, **kwargs) -> pyodbc.Connection:
        return pyodbc.connect(f"DSN={self.dsn}")


    # _retrieve_cursor(): Retrieves the cursor for the connection
    def _retrieve_cursor(self, **kwargs) -> pyodbc.Cursor:
        return self.conn.cursor()


    # _close(): Closes the connection to the server
    def _close(self, **kwargs):
        self.cursor.close()


    # _execute_query(sql_query, **kwargs): Executes 'sql_query'
    def _execute_query(self, sql_query: str, **kwargs):
        self.cursor.execute(sql_query)
