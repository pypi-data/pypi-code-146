"""SQL query algorithm."""
from __future__ import annotations

from typing import Any, ClassVar, Dict, Mapping, Optional, cast

from marshmallow import fields
import pandas as pd
import pandasql

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.exceptions import DuplicateColumnError
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.mixins import _ModellessAlgorithmMixIn
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.types import _DataLessAlgorithm
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import delegates

logger = _get_federated_logger(__name__)


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the SqlQuery algorithm."""

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the SqlQuery algorithm."""

    def __init__(
        self, *, query: str, table: Optional[str] = None, **kwargs: Any
    ) -> None:
        self.datasource: BaseSource
        self.query = query
        self.table = table
        super().__init__(**kwargs)

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.datasource = datasource
        if (
            self.table is None
            and pod_identifier is not None
            and not self.datasource.multi_table
        ):
            self.table = pod_identifier.split("/")[1]

    def run(self) -> pd.DataFrame:
        """Executes the query on the data source and returns a dataframe."""
        logger.info("Executing query...")
        if self.datasource.multi_table and isinstance(self.datasource, DatabaseSource):
            # Connect to the db directly if you are working with a multitable.
            conn = self.datasource.con.connect()
            output = pd.read_sql(sql=self.query, con=conn)
        elif self.datasource.multi_table and self.table is None:
            raise ValueError(
                "No table specified on which to execute the query on. "
                "Please specify the table on which to execute the query "
                "in the algorithm definition."
            )
        else:
            # For SQL queries on a dataframe/ single table.
            self.datasource.load_data(table_name=self.table)
            df = self.datasource.data
            if (f"from `{self.table}`" not in self.query) and (
                f"FROM `{self.table}`" not in self.query
            ):
                err_msg = """The default table for single table datasource is the pod
                    identifier without the username, in between backticks(``).
                    Please ensure your SQL query operates on that table. The
                    table name should be put inside backticks(``) in the
                    query statement, to make sure it is correctly parsed."""
                logger.error(err_msg)
                raise ValueError(err_msg)
            # Table name should be set by this point for single
            # table datasource, so it's safe to cast
            self.table = cast(str, self.table)
            # We need to remove hyphens as pandasql errors out if
            # they are included in the table name and query.
            query = self.query.split("`")
            query[query.index(self.table)] = query[query.index(self.table)].replace(
                "-", ""
            )
            table_name = self.table.replace("-", "")
            try:
                # Now for the actual query.
                output = pandasql.sqldf("".join(query), {table_name: df})
            except pandasql.PandaSQLException as ex:
                raise ValueError(
                    f"Error executing SQL query: [{self.query}], got error [{ex}]"
                )

        if any(output.columns.duplicated()):
            raise DuplicateColumnError(
                f"The following column names are duplicated in the output "
                f"dataframe: {output.columns[output.columns.duplicated()]}. "
                f"Please rename them in the query, and try again."
            )
        return cast(pd.DataFrame, output)


@delegates()
class SqlQuery(BaseAlgorithmFactory, _ModellessAlgorithmMixIn, _DataLessAlgorithm):
    r"""Simple algorithm for running a SQL query on a table.

    :::info

    The default table for single-table datasources is the pod identifier without the
    username, in between backticks(\`\`). Please ensure your SQL query operates on
    that table. The table name should be put inside backticks(\`\`) in the query
    statement, to make sure it is correctly parsed e.g. ``SELECT MAX(G) AS MAX_OF_G
    FROM `df` ``. This is the standard quoting mechanism used by MySQL (and also
    included in SQLite).

    :::

    :::info

    If you are using a multi-table datasource, ensure that your SQL query syntax matches
    the syntax required by the Pod database backend.

    :::

    Args:
        query: The SQL query to execute.
        table: The target table name. For single table pod datasources,
            this will default to the pod name.

    Attributes:
        query: The SQL query to execute.
        table: The target table name. For single table pod datasources,
            this will default to the pod name.

    """

    def __init__(self, *, query: str, table: Optional[str] = None, **kwargs: Any):
        super().__init__()
        self.query = query
        self.table = table

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "query": fields.Str(required=True),
        "table": fields.Str(allow_none=True),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the SqlQuery algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the SqlQuery algorithm."""
        return _WorkerSide(query=self.query, table=self.table, **kwargs)
