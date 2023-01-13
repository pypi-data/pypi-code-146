import pyodbc
import pandas as pd
from .sql_conn import SQLConn
from ..df_processor import DFProcessor
from ..abs_source import AbsSource
from .sql_query import SqlQuery
from ...events import SqlQueryCheckEvent
from typing import Union, Optional


# SQLSource: Source table from SQL
# Requires: 'query' selects a table from the server
class SQLSource(AbsSource):
    """
    A source to retrieve data from tables in SQL

    Attributes
    ----------
    sql_conn: :class:`~Reporter.data_sources.sql.SQLConn`
        The connection to the server

    query: Union[:class:`str`, :class:`~Reporter.data_sources.sql.sql_query.SqlQuery`]
        The SQL query to be executed for retrieving the needed data

    post_processor: Optional[Union[Dict[str, :class:`~Reporter.data_sources.df_processor.DFProcessor`], :class:`~Reporter.data_sources.df_processor.DFProcessor`]]
        the processors used to transform the raw imported table

        **Default**: ``None``
    """

    def __init__(self, sql_conn: SQLConn, query: Union[str, SqlQuery], post_processor: Optional[DFProcessor] = None):
        super().__init__(post_processor)
        self.sql_conn = sql_conn
        self._parse_query(query)


    # parse_query(): Converts the SQL query to a string
    def _parse_query(self, query):
        if (isinstance(query, SqlQuery)):
            self.query= query.parse()
        else:
            self.query = query


    # import_data(): Imports the sql table
    async def import_data(self) -> pd.DataFrame:
        # notifies the SQL query for the source
        self.notify(SqlQueryCheckEvent(self.name, self.nav.dsn, self.query))

        if (self.sql_conn.conn is not None):
            self.sql_conn.connect()

        result = pd.read_sql(self.query, self.nav.conn)

        self.sql_conn.close_conn()
        return result
