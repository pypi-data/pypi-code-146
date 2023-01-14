from typing import Optional

from sqlalchemy.engine.url import URL

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.utils.missing_dependency import missing_dependency_exception


class BigQuerySourceImpl(BaseSQLSource):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[str] = None,
        location: Optional[str] = None,
        credentials_base64: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        try:
            import sqlalchemy_bigquery  # noqa
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")
        del sqlalchemy_bigquery  # unused

        BaseSQLSource.__init__(self, name=name)
        self.location = location or load_integration_variable(integration_name=name, name="BQ_LOCATION")
        self.dataset = dataset or load_integration_variable(integration_name=name, name="BQ_DATASET")
        self.project = project or load_integration_variable(integration_name=name, name="BQ_PROJECT")
        self.credentials_base64 = credentials_base64 or load_integration_variable(
            integration_name=name, name="BQ_CREDENTIALS_BASE64"
        )
        self.credentials_path = credentials_path or load_integration_variable(
            integration_name=name, name="BQ_CREDENTIALS_PATH"
        )

    def local_engine_url(self) -> URL:
        query = {
            k: v
            for k, v in {
                "location": self.location,
                "credentials_base64": self.credentials_base64,
                "credentials_path": self.credentials_path,
            }.items()
            if v is not None
        }
        return URL.create(drivername="bigquery", host=self.project, database=self.dataset, query=query)
