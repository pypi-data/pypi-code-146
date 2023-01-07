# Standard imports
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote

# Third-party imports
from ._sqlalchemy import SQLAlchemy


class PostgresClient(SQLAlchemy):

    def __init__(self, host: str, port: str, username: str, password: str, database: str, schema: str = None) -> None:
        """
            Creates and initializes a PostgreSQL engine instance that connects to the database

            Parameters:
                host (str): Host IP address
                port (str): Port number                
                username (str): Username for authentication/privileges
                password (str): Password for authentication
                database (str): Name of the database
        """
        super().__init__(engine = "postgresql", host = host, port = port, database = database, username = username, password = password)
        self.engine = create_engine(self.connection_string)


    @property
    def connection_string(self) -> str:
        """ Returns the connection string """
        return f"{self.engine}://{self.username}:%s@{self.host}:{self.port}/{self.database}" % urlquote(self.password)