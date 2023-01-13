import pandas as pd
from .sql_query import SqlQuery
from typing import Callable, Any, Union, TypeVar


Connection = TypeVar("Connection")
Cursor = TypeVar("Cursor")


class SQLConn():
    """
    An abstract connection to a database assuming it only requires the data source name

    Attributes
    ----------
    dsn_name: :class:`str`
        The name of the data source server you want to connect to

    conn:
        The connection to the server

        **On Initialization**: ``None``

    cursor:
        The cursor for the connection of the server

        **On Initialization**: ``None``
    """
    def __init__(self, dsn_name: str):
        self.dsn = dsn_name
        self.conn = None
        self.cursor = None


    # _connect_db(): Establish a connection with the server
    def _connect_db(self, **kwargs) -> Connection:
        pass


    # _retrieve_cursor(): Retrieves the cursor for the connection
    def _retrieve_cursor(self, **kwargs) -> Cursor:
        pass


    # _close(): Closes the connection to the server
    def _close(self, **kwargs):
        pass


    # _execute_query(sql_query, **kwargs): Executes 'sql_query'
    def _execute_query(self, sql_query: str, **kwargs):
        pass


    # connect(): Connects to the server
    # Effects: Modifies 'conn' and 'cursor'
    def connect(self, **kwargs):
        """
        Connects to the server
        """
        self.conn = self._connect_db(**kwargs)
        self.cursor = self._retrieve_cursor(**kwargs)


    # _reset_conns(): Reset the connection attributes
    def _reset_conns(self):
        self.conn = None
        self.cursor = None


    # close_conn(): Closes the connection to the server and reset
    #   all connections
    def close_conn(self, **kwargs):
        """
        Closes the connection to the server
        """
        self._close(**kwargs)
        self._reset_conns()


    # check_connect(func): Decorator to check if the server connection is specified
    def check_connect(func: Callable[..., Any]):
        """
        A decorator that helps with automatically connecting and closing the connection
            to the server

        Parameters
        ----------
        func: Callable[..., Any]
            the function that we want to connect to the server
        """
        def check_connect_helper(self, *args, **kwargs) -> Any:
            # establish the connection
            if (self.conn is None):
                self.connect()

            # this check is in case the connect function does not modify 'conn'
            if (self.conn is not None):
                return func(self, *args, **kwargs)

            self.close_conn()

        return check_connect_helper


    # execute(query): Executes sql queries to the server
    @check_connect
    def execute(self, query: Union[str, SqlQuery]) -> Cursor:
        """
        Executes an SQL query to the server

        Parameters
        ----------
        query: Union[:class:`str`, :class:`~Reporter.data_sources.sql.sql_query.SqlQuery`]
            the SQL query to be executed

        Returns
        -------
        The cursor that executed the query
        """
        sql_query = query
        if (isinstance(query, SqlQuery)):
            sql_query = query.parse()

        self._execute_query(sql_query)
        return self.cursor
