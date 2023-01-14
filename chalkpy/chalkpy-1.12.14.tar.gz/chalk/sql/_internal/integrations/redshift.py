from typing import Optional

from sqlalchemy.engine.url import URL

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource


class RedshiftSourceImpl(BaseSQLSource):
    def __init__(
        self,
        host: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.host = host or load_integration_variable(name="REDSHIFT_HOST", integration_name=name)
        self.db = db or load_integration_variable(name="REDSHIFT_DB", integration_name=name)
        self.user = user or load_integration_variable(name="REDSHIFT_USER", integration_name=name)
        self.password = password or load_integration_variable(name="REDSHIFT_PASSWORD", integration_name=name)
        BaseSQLSource.__init__(self, name=name)

    def local_engine_url(self) -> URL:
        return URL.create(
            drivername="redshift+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.db,
        )
