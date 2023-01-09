"""Workers for handling task running on pods."""
from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
from sqlite3 import Connection
from typing import Any, List, Optional, Sequence, cast

import pandas as pd
import sqlvalidator

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import DataStructureError
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.authorisation_checkers import _AuthorisationChecker
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.monitoring.monitor import task_config_update
from bitfount.federated.pod_db_utils import (
    _map_task_to_hash_add_to_db,
    _save_results_to_db,
)
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseProtocolFactory,
)
from bitfount.federated.protocols.model_protocols.federated_averaging import (
    FederatedAveraging,
)
from bitfount.federated.transport.message_service import _BitfountMessageType
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import (
    SerializedAlgorithm,
    SerializedProtocol,
    _DataLessAlgorithm,
)
from bitfount.federated.utils import _PROTOCOLS
from bitfount.hub.api import BitfountHub
from bitfount.schemas.utils import bf_load
from bitfount.types import _JSONDict

logger = _get_federated_logger(__name__)


class _Worker:
    """Client worker which runs a protocol locally.

    Args:
        datasource: BaseSource object.
        mailbox: Relevant mailbox.
        bitfounthub: BitfountHub object.
        authorisation: AuthorisationChecker object.
        pod_identifier: Identifier of the pod the Worker is running in.
        serialized_protocol: SerializedProtocol dictionary that the Pod has received
            from the Modeller.
        pod_vitals: PodVitals object.
        pod_dp: DPPodConfig object.
        pod_db: Whether the pod has a databse associated with it. Defaults to False.
        show_datapoints_in_results_db: Whether the datasource records are shown
            in the results database. Defaults to True.
        project_id: The project id. Defaults to None.
        run_on_new_data_only: Whether to run on the whole dataset or only on
            new data. Defaults to False.
    """

    def __init__(
        self,
        datasource: BaseSource,
        mailbox: _WorkerMailbox,
        bitfounthub: BitfountHub,
        authorisation: _AuthorisationChecker,
        pod_identifier: str,
        serialized_protocol: SerializedProtocol,
        pod_vitals: Optional[_PodVitals] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_db: bool = False,
        show_datapoints_in_results_db: bool = True,
        project_id: Optional[str] = None,
        run_on_new_data_only: bool = False,
        **_kwargs: Any,
    ):
        self.datasource = datasource
        self.mailbox = mailbox
        self.hub = bitfounthub
        self.authorisation = authorisation
        self.pod_identifier = pod_identifier
        self.serialized_protocol = serialized_protocol
        self.pod_vitals = pod_vitals
        self._pod_dp = pod_dp
        self.project_id = project_id
        self._pod_db = (
            pod_db
            if project_id is not None
            and not isinstance(self.datasource, DatabaseSource)
            else False
        )
        self._show_datapoints_in_results_db = (
            show_datapoints_in_results_db if self._pod_db else False
        )
        self.run_on_new_data_only = run_on_new_data_only if self._pod_db else False
        # Compute task hash on ordered json dictionary
        self._task_hash = (
            hashlib.sha256(
                json.dumps(serialized_protocol, sort_keys=True).encode("utf-8")
            ).hexdigest()
            if self._pod_db
            else None
        )

    def _update_task_config(self) -> None:
        """Send task config update to monitor service."""
        # remove schema from task_config to limit request body size
        task_config = copy.deepcopy(self.serialized_protocol)
        for algorithm in task_config["algorithm"]:
            if not isinstance(algorithm, str):
                if model := algorithm["model"]:
                    if "schema" in model:
                        del model["schema"]
        task_config_update(dict(task_config))

    async def run(self) -> None:
        """Calls relevant training procedure and sends back weights/results."""
        # Send task to Monitor service. This is done regardless of whether or not
        # the task is accepted. This method is being run in a task monitor context
        # manager so no need to set the task monitor prior to sending.
        self._update_task_config()

        # Check authorisation with access manager
        authorisation_errors = await self.authorisation.check_authorisation()

        if authorisation_errors.messages:
            # Reject task, as there were errors
            await self.mailbox.reject_task(
                authorisation_errors.messages,
            )
            return

        # Accept task and inform modeller
        logger.info("Task accepted, informing modeller.")
        await self.mailbox.accept_task()
        # Wait for Modeller to give the green light to start the task
        await self.mailbox.get_task_start_update()

        # Update hub instance if BitfountModelReference
        algorithm = self.serialized_protocol["algorithm"]
        if not isinstance(self.serialized_protocol["algorithm"], list):
            algorithm = [cast(SerializedAlgorithm, algorithm)]

        algorithm = cast(List[SerializedAlgorithm], algorithm)
        for algo in algorithm:
            if model := algo.get("model"):
                if model["class_name"] == "BitfountModelReference":
                    logger.debug("Patching model reference hub.")
                    model["hub"] = self.hub

        # Deserialize protocol only after task has been accepted just to be safe
        protocol = cast(
            BaseProtocolFactory,
            bf_load(cast(_JSONDict, self.serialized_protocol), _PROTOCOLS),
        )
        # For FederatedAveraging, we return a dictionary of
        # validation metrics, which is incompatible with the database.
        if isinstance(protocol, FederatedAveraging):
            self._pod_db = False
        # Load data according to model datastructure if one exists.
        # For multi-algorithm protocols, we assume that all algorithm models have the
        # same datastructure.
        datastructure: Optional[DataStructure] = None
        algorithm_ = protocol.algorithm
        if not isinstance(algorithm_, Sequence):
            algorithm_ = [algorithm_]

        algorithm_ = cast(List[BaseCompatibleAlgoFactory], algorithm_)
        for algo_ in algorithm_:
            if isinstance(algo_, _BaseModelAlgorithmFactory):
                datastructure = algo_.model.datastructure

            if not isinstance(algo_, _DataLessAlgorithm):
                if self._pod_db:
                    con = sqlite3.connect(f"{self.project_id}.db")
                    cur = con.cursor()
                    cur.execute(
                        f"""CREATE TABLE IF NOT EXISTS "{self._task_hash}" (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""  # noqa: B950
                    )
                    table = self._load_data_for_worker(
                        datastructure=datastructure, con=con
                    )
                    # task_hash is set if pod_db is true, so it's safe to cast
                    _map_task_to_hash_add_to_db(
                        self.serialized_protocol, cast(str, self._task_hash), con
                    )
                else:
                    # We execute the query directly on the db connection,
                    # or load the data at runtime for a csv.
                    # TODO: [NO_TICKET: Reason] No ticket created yet. Add the private sql query algorithm here as well. # noqa: B950
                    self._load_data_for_worker(datastructure=datastructure)
        # Calling the `worker` method on the protocol also calls the `worker` method on
        # underlying objects such as the algorithm and aggregator. The algorithm
        # `worker` method will also download the model from the Hub if it is a
        # `BitfountModelReference`
        worker_protocol = protocol.worker(mailbox=self.mailbox, hub=self.hub)

        # If the algorithm is a model algorithm, then we need to pass the pod identifier
        # to the model so that it can extract the relevant information from the
        # datastructure the Modeller has sent. This must be done after the worker
        # protocol has been created, so that any model references have been converted
        # to models.
        for worker_algo in worker_protocol.algorithms:
            if isinstance(worker_algo, _BaseModelAlgorithm):
                worker_algo.model.set_pod_identifier(self.pod_identifier)

        results = await worker_protocol.run(
            datasource=self.datasource,
            pod_dp=self._pod_dp,
            pod_vitals=self.pod_vitals,
            pod_identifier=self.mailbox.pod_identifier,
        )
        if self._pod_db:
            # pod_db is always false for DatabaseSource,
            # which is the only datasource that accepts sqlquery
            # instead of table name, so we can cast
            # if pod_db is true, task_hash is a str,
            # so it's safe to cast
            if isinstance(results, list):
                _save_results_to_db(
                    results=results,
                    pod_identifier=self.pod_identifier,
                    task_hash=cast(str, self._task_hash),
                    table=cast(str, table),
                    datasource=self.datasource,
                    show_datapoints_in_results_db=self._show_datapoints_in_results_db,
                    run_on_new_data_only=self.run_on_new_data_only,
                    con=con,
                )
                con.close()
            else:
                logger.info(
                    "Results cannot be saved to pod database."
                    "Results can be only saved to database if "
                    "they are returned from the algorithm as a list, "
                    f"whereas the chosen protocol returns {type(results)}."
                )

        logger.info("Task complete.")
        self.mailbox.delete_all_handlers(_BitfountMessageType.LOG_MESSAGE)

    def _load_data_for_worker(
        self,
        datastructure: Optional[DataStructure] = None,
        con: Optional[Connection] = None,
    ) -> Optional[str]:
        """Load the data for the worker and returns table_name."""
        sql_query: Optional[str] = None
        table: Optional[str] = None
        kwargs = {}
        if datastructure:
            if datastructure.table:
                if isinstance(datastructure.table, dict):
                    if not (table := datastructure.table.get(self.pod_identifier)):
                        raise DataStructureError(
                            f"Table definition not found for {self.pod_identifier}. "
                            f"Table definitions provided in this DataStructure: "
                            f"{str(datastructure.table)}"
                        )
                    kwargs["table_name"] = table
                elif isinstance(datastructure.table, str):
                    table = datastructure.table
                    if not table == self.pod_identifier.split("/")[1]:
                        raise DataStructureError(
                            f"Table definition not found for {self.pod_identifier}. "
                            f"Table definitions provided in this DataStructure: "
                            f"{str(datastructure.table)}"
                        )
                    kwargs["table_name"] = datastructure.table
            elif datastructure.query:
                if isinstance(datastructure.query, dict):
                    if not (sql_query := datastructure.query.get(self.pod_identifier)):
                        raise DataStructureError(
                            f"Query definition not found for {self.pod_identifier}. "
                            f"Query definitions provided in this DataStructure: "
                            f"{str(datastructure.query)}"
                        )
                elif isinstance(datastructure.query, str):
                    sql_query = datastructure.query
                if sql_query and sqlvalidator.parse(sql_query).is_valid():
                    if not isinstance(self.datasource, DatabaseSource):
                        raise ValueError(
                            "Incompatible DataStructure, data source pair. "
                            "DataStructure is expecting the data source to "
                            "be a DatabaseSource."
                        )
                    kwargs["sql_query"] = sql_query
        # This call loads the data for a multi-table BaseSource as specified by the
        # Modeller/DataStructure.

        self.datasource.load_data(**kwargs)
        if self._pod_db and self.run_on_new_data_only:
            # pod database is incompatible with DatabaseSource,
            # which is the only datasource that supports
            # datastructure queries, so it's safe to cast
            # for the table name
            self.load_new_records_only_for_task(
                cast(Connection, con), table=cast(str, table)
            )
        return table

    def load_new_records_only_for_task(self, con: Connection, table: str) -> None:
        # Ignoring the security warning because the sql query is trusted and
        # the task_hash is calculated at __init__.
        task_data = pd.read_sql(
            f'SELECT "datapoint_hash" FROM "{self._task_hash}"', con  # nosec
        )
        # check hash in from static datasource table -
        pod_con = sqlite3.connect(f"{self.pod_identifier.split('/')[1]}.db")
        # Ignoring the security warning because the sql query is trusted and
        # the table is checked that it matches the datasource tables.
        data = pd.read_sql(f'SELECT * FROM "{table}"', pod_con)  # nosec
        # set datasource_data for specific task to only run on new records.
        new_records = data[~data["datapoint_hash"].isin(task_data["datapoint_hash"])]
        self.datasource._ignore_cols.append("datapoint_hash")
        self.datasource._data = new_records
        pod_con.close()
