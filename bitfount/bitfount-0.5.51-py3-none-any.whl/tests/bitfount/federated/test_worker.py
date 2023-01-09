"""Tests worker.py."""
import hashlib
import json
import os
import platform
import sqlite3
from typing import Any, Mapping, Union, cast
from unittest.mock import AsyncMock, Mock, PropertyMock, create_autospec

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
import pandas as pd
import pytest
from pytest import fixture
from pytest_mock import MockerFixture
import sqlalchemy

from bitfount import BitfountSchema, DataStructure
from bitfount.backends.pytorch import PyTorchTabularClassifier
from bitfount.data.datasets import _IterableBitfountDataset
from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datasources.intermine_source import IntermineSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.exceptions import DataStructureError
from bitfount.data.types import DataSplit, SchemaOverrideMapping
from bitfount.data.utils import DatabaseConnection
from bitfount.federated.aggregators.base import _BaseAggregatorFactory
from bitfount.federated.aggregators.base import _registry as aggregator_registry
from bitfount.federated.algorithms.base import BaseAlgorithmFactory
from bitfount.federated.algorithms.base import _registry as algorithm_registry
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
)
from bitfount.federated.algorithms.model_algorithms.inference import ModelInference
from bitfount.federated.authorisation_checkers import (
    _AuthorisationChecker,
    _LocalAuthorisation,
)
from bitfount.federated.monitoring.types import (
    AdditionalMonitorMessageTypes,
    MonitorRecordPrivacy,
)
from bitfount.federated.protocols.base import BaseProtocolFactory
from bitfount.federated.protocols.base import _registry as protocol_registry
from bitfount.federated.protocols.model_protocols.federated_averaging import (
    FederatedAveraging,
)
from bitfount.federated.protocols.results_only import ResultsOnly, _WorkerSide
from bitfount.federated.types import (
    SerializedAggregator,
    SerializedAlgorithm,
    SerializedProtocol,
)
from bitfount.federated.utils import _DISTRIBUTED_MODELS
from bitfount.federated.worker import _Worker
from bitfount.types import DistributedModelProtocol, _JSONDict
from tests.utils.helper import (
    create_dataset,
    create_datasource,
    integration_test,
    unit_test,
)


@unit_test
class TestWorker:
    """Tests Worker class."""

    @fixture
    def dummy_protocol(self) -> FederatedAveraging:
        """Returns a FederatedAveraging instance."""
        protocol = Mock(algorithm=Mock(spec=_BaseModelAlgorithmFactory))
        protocol.class_name = "FederatedAveraging"
        protocol.algorithm.class_name = "FederatedModelTraining"
        protocol.aggregator.class_name = "Aggregator"
        protocol.algorithm.model = Mock()
        protocol.algorithm.model.datastructure = create_autospec(DataStructure)
        protocol.algorithm.model.schema = create_autospec(BitfountSchema)
        protocol.worker.return_value = AsyncMock(algorithm=protocol.algorithm)
        return protocol

    @fixture
    def dummy_fed_avg(self) -> FederatedAveraging:
        """Returns a FederatedAveraging instance."""
        model = create_autospec(PyTorchTabularClassifier)
        model.steps = 2
        model.datastructure = Mock()
        protocol_factory = FederatedAveraging(
            algorithm=FederatedModelTraining(model=model, modeller_checkpointing=False),
            steps_between_parameter_updates=2,
        )
        return protocol_factory

    @fixture
    def dummy_res_only(self) -> ResultsOnly:
        """Returns a ResultsOnly instance."""
        model = create_autospec(PyTorchTabularClassifier)
        model.datastructure = DataStructure(table={"user/testpod": "testpod"})
        model.steps = 2
        protocol_factory = ResultsOnly(
            algorithm=ModelInference(model=model, modeller_checkpointing=False),
            steps_between_parameter_updates=2,
        )
        return protocol_factory

    @fixture
    def dummy_serializable_protocol(self) -> FederatedAveraging:
        """Returns a serializable FederatedAveraging instance."""
        mock_protocol_factory: Mock = create_autospec(FederatedAveraging, instance=True)
        dump_return_value = {
            "class_name": "bitfount.FederatedAveraging",
            "algorithm": {
                "class_name": "bitfount.FederatedModelTraining",
                "model": {
                    "class_name": "bitfount.PyTorchTabularClassifier",
                    "datastructure": create_autospec(DataStructure),
                    "schema": create_autospec(BitfountSchema),
                },
            },
            "aggregator": {"class_name": "bitfount.Aggregator"},
        }
        mock_protocol_factory.dump.return_value = dump_return_value
        return mock_protocol_factory

    @fixture
    def authoriser(self) -> _AuthorisationChecker:
        """An AuthorisationChecker object.

        An instance of LocalAuthorisation is returned because AuthorisationChecker
        cannot itself be instantiated.
        """
        return _LocalAuthorisation(
            Mock(),
            SerializedProtocol(
                class_name="bitfount.FederatedAveraging",
                algorithm=SerializedAlgorithm(
                    class_name="bitfount.FederatedModelTraining"
                ),
                aggregator=SerializedAggregator(class_name="bitfount.SecureAggregator"),
            ),
        )

    @fixture
    def mock_aggregator_cls_name(self) -> str:
        """Registry name for mock aggregator class."""
        return "mock_aggregator_cls"

    @fixture
    def mock_aggregator_cls_in_registry(
        self, mock_aggregator_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock aggregator class in relevant registry."""
        mock_aggregator_cls: Mock = create_autospec(_BaseAggregatorFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            aggregator_registry,
            mock_aggregator_cls_name,
            cast(Any, mock_aggregator_cls),
        )
        return mock_aggregator_cls

    @fixture
    def mock_algorithm_cls_name(self) -> str:
        """Registry name for mock algorithm class."""
        return "mock_algorithm_cls"

    @fixture
    def mock_algorithm_cls_in_registry(
        self, mock_algorithm_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock algorithm class in relevant registry."""
        mock_algorithm_cls: Mock = create_autospec(BaseAlgorithmFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            algorithm_registry, mock_algorithm_cls_name, cast(Any, mock_algorithm_cls)
        )
        return mock_algorithm_cls

    @fixture
    def mock_model_cls_name(self) -> str:
        """Registry name for mock model class."""
        return "mock_model_cls"

    @fixture
    def mock_model_cls_in_registry(
        self, mock_model_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock model class in relevant registry."""
        mock_model_cls: Mock = create_autospec(DistributedModelProtocol)
        mock_model_cls.Schema = Mock()
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            _DISTRIBUTED_MODELS, mock_model_cls_name, cast(Any, mock_model_cls)
        )
        return mock_model_cls

    @fixture
    def mock_protocol_cls_name(self) -> str:
        """Registry name for mock protocol class."""
        return "mock_protocol_cls"

    @fixture
    def mock_protocol_cls_in_registry(
        self, mock_protocol_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock protocol class in relevant registry."""
        mock_protocol_cls: Mock = create_autospec(BaseProtocolFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            protocol_registry, mock_protocol_cls_name, cast(Any, mock_protocol_cls)
        )
        return mock_protocol_cls

    @fixture
    def serialized_protocol_modelless(
        self, mock_algorithm_cls_name: str, mock_protocol_cls_name: str
    ) -> _JSONDict:
        """Serialized protocol dict without model."""
        return {
            "algorithm": {
                "class_name": mock_algorithm_cls_name,
            },
            "class_name": mock_protocol_cls_name,
        }

    @fixture
    def serialized_protocol_with_model(
        self,
        mock_aggregator_cls_name: str,
        mock_algorithm_cls_name: str,
        mock_model_cls_name: str,
        mock_protocol_cls_name: str,
    ) -> _JSONDict:
        """Serialized protocol dict with model (and aggregator)."""
        return {
            "algorithm": {
                "class_name": mock_algorithm_cls_name,
                "model": {
                    "class_name": mock_model_cls_name,
                    "schema": "mock_schema",
                    "datastructure": {"table": "testpod"},
                },
            },
            "aggregator": {"class_name": mock_aggregator_cls_name},
            "class_name": "FederatedAveraging",
        }

    @fixture
    def mock_worker(self) -> Mock:
        """Mock Worker instance to use in `self` arg."""
        mock_worker = Mock(spec=_Worker, hub=Mock())
        return mock_worker

    async def test_worker_run_method_waits_for_task_start_message(
        self,
        authoriser: _AuthorisationChecker,
        dummy_protocol: FederatedAveraging,
        mocker: MockerFixture,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Tests that the worker waits for the TASK_START message to come through."""
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        mailbox = AsyncMock()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier="dummy_id",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
        )
        await worker.run()
        # Check that the worker awaits on the TASK_START message
        mailbox.get_task_start_update.assert_awaited_once()

    async def test_worker_run_protocol_with_model_loads_datastructure_schema(
        self,
        authoriser: _AuthorisationChecker,
        dummy_protocol: FederatedAveraging,
        dummy_serializable_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the datastructure and schema are taken from model."""
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        worker = _Worker(
            Mock(),
            AsyncMock(),
            Mock(),
            authoriser,
            pod_identifier="dummy_id",
            serialized_protocol=dummy_serializable_protocol.dump(),
        )
        mock_data = mocker.patch.object(worker, "_load_data_for_worker")
        await worker.run()
        mock_data.assert_called_once_with(
            datastructure=dummy_protocol.algorithm.model.datastructure,
        )

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    async def test_worker_run_fed_avg_with_pod_db(
        self,
        authoriser: _AuthorisationChecker,
        dummy_fed_avg: FederatedAveraging,
        mocker: MockerFixture,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Tests that pod_db is False for FederatedAveraging.."""
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_fed_avg)
        mailbox = AsyncMock()
        mailbox.pod_identifier = "user/testpod"
        con = sqlite3.connect("testpod.db")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS "datasource" ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""  # noqa: B950
        )
        con.commit()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier="dummy_id",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
            project_id="someId",
        )
        assert (
            worker._task_hash
            == hashlib.sha256(
                json.dumps(serialized_protocol_with_model, sort_keys=True).encode(
                    "utf-8"
                )
            ).hexdigest()
        )
        mocker.patch.object(worker, "_load_data_for_worker")
        mock_map_task = mocker.patch(
            "bitfount.federated.worker._map_task_to_hash_add_to_db"
        )
        mock_save_results = mocker.patch(
            "bitfount.federated.worker._save_results_to_db"
        )
        await worker.run()
        assert worker._pod_db is False
        mock_map_task.assert_not_called()
        mock_save_results.assert_not_called()
        con.close()
        os.remove("testpod.db")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    async def test_worker_run_fed_avg_with_pod_db_no_projectid(
        self,
        authoriser: _AuthorisationChecker,
        dummy_fed_avg: FederatedAveraging,
        serialized_protocol_with_model: _JSONDict,
        mocker: MockerFixture,
    ) -> None:
        """Tests that pod_db is False for FederatedAveraging.."""
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_fed_avg)
        mailbox = AsyncMock()
        mailbox.pod_identifier = "user/testpod"
        con = sqlite3.connect("testpod.db")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS "datasource" ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""  # noqa: B950
        )
        con.commit()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier="dummy_id",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
        )
        assert worker._task_hash is None

        mocker.patch.object(worker, "_load_data_for_worker")
        mock_map_task = mocker.patch(
            "bitfount.federated.worker._map_task_to_hash_add_to_db"
        )
        mock_save_results = mocker.patch(
            "bitfount.federated.worker._save_results_to_db"
        )
        await worker.run()
        assert worker._pod_db is False
        mock_map_task.assert_not_called()
        mock_save_results.assert_not_called()
        con.close()
        os.remove("testpod.db")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    async def test_worker_run_w_pod_db(
        self,
        authoriser: _AuthorisationChecker,
        dummy_res_only: ResultsOnly,
        serialized_protocol_with_model: _JSONDict,
        mocker: MockerFixture,
    ) -> None:
        """Tests that pod database works with ResultsOnly protocol."""
        pod_name = "testpod"
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_res_only)
        mailbox = AsyncMock()
        mailbox.pod_identifier = f"user/{pod_name}"
        con = sqlite3.connect(f"{pod_name}.db")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{pod_name}" ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""  # noqa: B950
        )
        con.commit()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier=f"user/{pod_name}",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
            project_id="someid",
        )
        mock_map_task = mocker.patch(
            "bitfount.federated.worker._map_task_to_hash_add_to_db"
        )
        mock_save_results = mocker.patch(
            "bitfount.federated.worker._save_results_to_db"
        )
        assert (
            worker._task_hash
            == hashlib.sha256(
                json.dumps(serialized_protocol_with_model, sort_keys=True).encode(
                    "utf-8"
                )
            ).hexdigest()
        )
        mock_proto_run = mocker.patch.object(_WorkerSide, "run")
        mock_proto_run.side_effect = AsyncMock(return_value=[])
        await worker.run()
        mock_proto_run.assert_awaited_once()
        mock_map_task.assert_called_once()
        mock_save_results.assert_called_once()
        con.close()
        os.remove(f"{pod_name}.db")
        os.remove("someid.db")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    async def test_worker_run_w_pod_db_no_projectid(
        self,
        authoriser: _AuthorisationChecker,
        dummy_res_only: ResultsOnly,
        serialized_protocol_with_model: _JSONDict,
        mocker: MockerFixture,
    ) -> None:
        """Tests that pod database works with ResultsOnly protocol."""
        pod_name = "testpod"
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_res_only)
        mailbox = AsyncMock()
        mailbox.pod_identifier = f"user/{pod_name}"
        pod_con = sqlite3.connect(f"{pod_name}.db")
        cur = pod_con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{pod_name}" ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""  # noqa: B950
        )
        pod_con.commit()
        pod_con.close()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier=f"user/{pod_name}",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
        )
        mock_map_task = mocker.patch(
            "bitfount.federated.worker._map_task_to_hash_add_to_db"
        )
        mock_save_results = mocker.patch(
            "bitfount.federated.worker._save_results_to_db"
        )
        assert worker._task_hash is None

        mock_proto_run = mocker.patch.object(_WorkerSide, "run")
        mock_proto_run.side_effect = AsyncMock(return_value=[])
        await worker.run()
        mock_proto_run.assert_awaited_once()
        mock_map_task.assert_not_called()
        mock_save_results.assert_not_called()
        os.remove(f"{pod_name}.db")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    async def test_worker_run_w_pod_db_results_dict(
        self,
        authoriser: _AuthorisationChecker,
        caplog: LogCaptureFixture,
        dummy_res_only: ResultsOnly,
        mocker: MockerFixture,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Tests that results are not saved if returned as a dict."""
        pod_name = "testpod"
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_res_only)
        mailbox = AsyncMock()
        mailbox.pod_identifier = f"user/{pod_name}"
        pod_con = sqlite3.connect(f"{pod_name}.db")
        cur = pod_con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{pod_name}" ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""  # noqa: B950
        )
        pod_con.commit()
        pod_con.close()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier=f"user/{pod_name}",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
            project_id="someid",
        )
        con = sqlite3.connect("someid.db")
        mock_map_task = mocker.patch(
            "bitfount.federated.worker._map_task_to_hash_add_to_db"
        )
        mock_save_results = mocker.patch(
            "bitfount.federated.worker._save_results_to_db"
        )
        task_hash = hashlib.sha256(
            json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
        ).hexdigest()
        assert worker._task_hash == task_hash
        mock_proto_run = mocker.patch.object(_WorkerSide, "run")
        mock_proto_run.side_effect = AsyncMock(return_value={})
        await worker.run()
        data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
        assert sorted(set(data.columns)) == ["datapoint_hash", "results", "rowID"]
        mock_proto_run.assert_awaited_once()
        mock_map_task.assert_called_once()
        mock_save_results.assert_not_called()
        assert (
            "Results cannot be saved to pod database.Results "
            "can be only saved to database if they are returned "
            "from the algorithm as a list, whereas the chosen "
            "protocol returns <class 'dict'>" in caplog.text
        )
        con.close()
        os.remove("testpod.db")
        os.remove("someid.db")

    async def test_worker_run_protocol_without_model_no_datastructure(
        self,
        authoriser: _AuthorisationChecker,
        dummy_protocol: FederatedAveraging,
        dummy_serializable_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the datastructure and schema are None if no model."""
        dummy_protocol.algorithm = Mock()
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        worker = _Worker(
            Mock(),
            AsyncMock(),
            Mock(),
            authoriser,
            pod_identifier="dummy_id",
            serialized_protocol=dummy_serializable_protocol.dump(),
        )
        mock_data = mocker.patch.object(worker, "_load_data_for_worker")
        await worker.run()
        mock_data.assert_called_once_with(datastructure=None)

    def test__load_data_for_worker(
        self,
        dummy_res_only: ResultsOnly,
        mocker: MockerFixture,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Tests that the worker loads the data."""
        datasource = create_datasource(classification=True)
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_res_only)

        worker = _Worker(
            datasource,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier="user/testpod",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
            project_id="someId",
        )

        def mock_load_data(self_: BaseSource, **kwargs: Any) -> None:
            self_._data_is_loaded = True
            self_.data = Mock(spec=pd.DataFrame)

        mocker.patch(
            "bitfount.federated.worker.BaseSource.load_data",
            autospec=True,
            side_effect=mock_load_data,
        )
        mock_load_new_records = mocker.patch.object(
            worker, "load_new_records_only_for_task"
        )

        # Assert that a datasource is returned is constructed
        worker._load_data_for_worker()
        assert worker.datasource is not None
        assert isinstance(worker.datasource, BaseSource)
        mock_load_new_records.assert_not_called()

    def test__load_new_data_only_for_worker(
        self,
        dummy_res_only: ResultsOnly,
        mocker: MockerFixture,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Tests that the worker loads the new data only."""
        datasource = create_datasource(classification=True)
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_res_only)

        worker = _Worker(
            datasource,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier="user/testpod",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
            project_id="someId",
            run_on_new_data_only=True,
        )

        def mock_load_data(self_: BaseSource, **kwargs: Any) -> None:
            self_._data_is_loaded = True
            self_.data = Mock(spec=pd.DataFrame)

        mocker.patch(
            "bitfount.federated.worker.BaseSource.load_data",
            autospec=True,
            side_effect=mock_load_data,
        )
        mock_load_new_records = mocker.patch.object(
            worker, "load_new_records_only_for_task"
        )

        # Assert that a datasource is returned is constructed
        worker._load_data_for_worker()
        assert worker.datasource is not None
        assert isinstance(worker.datasource, BaseSource)
        mock_load_new_records.assert_called_once()

    def test__load_data_for_worker_no_projectid(
        self,
        dummy_res_only: ResultsOnly,
        serialized_protocol_with_model: _JSONDict,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the worker loads the data with no project id."""
        datasource = create_datasource(classification=True)
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_res_only)

        worker = _Worker(
            datasource,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier="dummy_id",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
        )

        def mock_load_data(self_: BaseSource, **kwargs: Any) -> None:
            self_._data_is_loaded = True
            self_.data = Mock(spec=pd.DataFrame)

        mocker.patch(
            "bitfount.federated.worker.BaseSource.load_data",
            autospec=True,
            side_effect=mock_load_data,
        )
        mock_load_new_records = mocker.patch.object(
            worker, "load_new_records_only_for_task"
        )

        # Assert that a datasource is returned is constructed
        worker._load_data_for_worker()
        assert worker.datasource is not None
        assert isinstance(worker.datasource, BaseSource)
        mock_load_new_records.assert_not_called()

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    async def test_worker_load_new_records_only_for_task(
        self,
        authoriser: _AuthorisationChecker,
        caplog: LogCaptureFixture,
        dummy_res_only: ResultsOnly,
        mocker: MockerFixture,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Tests that only new records are loaded for task."""
        pod_name = "testpod"
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_res_only)
        mailbox = AsyncMock()
        mailbox.pod_identifier = f"user/{pod_name}"
        pod_con = sqlite3.connect(f"{pod_name}.db")
        cur = pod_con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{pod_name}"
            ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""
        )
        pod_con.commit()
        pod_con.close()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier=f"user/{pod_name}",
            serialized_protocol=cast(
                SerializedProtocol, serialized_protocol_with_model
            ),
            pod_db=True,
            project_id="someId",
        )
        mock_map_task = mocker.patch(
            "bitfount.federated.worker._map_task_to_hash_add_to_db"
        )
        mocker.patch("bitfount.federated.worker._save_results_to_db", autospec=True)
        task_hash = hashlib.sha256(
            json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
        ).hexdigest()
        assert worker._task_hash == task_hash
        mock_proto_run = mocker.patch.object(_WorkerSide, "run")
        mock_proto_run.side_effect = AsyncMock(return_value=[])
        await worker.run()
        con = sqlite3.connect("someId.db")
        data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
        assert sorted(set(data.columns)) == ["datapoint_hash", "results", "rowID"]
        mock_proto_run.assert_awaited_once()
        mock_map_task.assert_called_once()
        worker.load_new_records_only_for_task(con, table=pod_name)
        assert worker.datasource._data is not None
        con.close()
        os.remove(f"{pod_name}.db")
        os.remove("someId.db")

    @pytest.mark.parametrize(
        "sql_query, schema_types_override",
        [
            (
                'SELECT "Date", "TARGET" FROM dummy_data',
                {"categorical": [{"TARGET": {"0": 0, "1": 1}}], "text": ["Date"]},
            ),
            (
                """SELECT d1."Date", d2."A" from dummy_data d1
            JOIN dummy_data_2 d2
            ON d1."Date" = d2."Date"
            """,
                {"continuous": ["A"], "text": ["Date"]},
            ),
        ],
    )
    def test__load_data_for_worker_table_as_query_pod_id(
        self,
        dummy_protocol: FederatedAveraging,
        mock_engine: sqlalchemy.engine.base.Engine,
        mocker: MockerFixture,
        schema_types_override: SchemaOverrideMapping,
        sql_query: str,
    ) -> None:
        """Tests sql query provided by datastructure is applied to datasource."""
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        pod_id = "dummy_pod_id"

        ds = DatabaseSource(db_conn, seed=420)
        datastructure = DataStructure(
            query={pod_id: sql_query},  # dictionary of pod_id to sql query
            schema_types_override={pod_id: schema_types_override},
        )
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        worker._load_data_for_worker(
            datastructure=datastructure,
        )

    @pytest.mark.parametrize(
        "sql_query, schema_types_override",
        [
            (
                'SELECT "Date", "TARGET" FROM dummy_data',
                {"categorical": [{"TARGET": {"0": 0, "1": 1}}], "text": ["Date"]},
            ),
            (
                """SELECT d1."Date", d2."A" from dummy_data d1
            JOIN dummy_data_2 d2
            ON d1."Date" = d2."Date"
            """,
                {"continuous": ["A"], "text": ["Date"]},
            ),
        ],
    )
    def test__load_data_for_worker_table_as_query(
        self,
        dummy_protocol: FederatedAveraging,
        mock_engine: sqlalchemy.engine.base.Engine,
        mocker: MockerFixture,
        schema_types_override: SchemaOverrideMapping,
        sql_query: str,
    ) -> None:
        """Tests sql query provided by datastructure is applied to datasource."""
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        pod_id = "dummy_pod_id"

        ds = DatabaseSource(db_conn, seed=420)
        datastructure = DataStructure(
            query=sql_query,  # standalone sql query
            schema_types_override=schema_types_override,
        )
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        worker._load_data_for_worker(
            datastructure=datastructure,
        )

    @pytest.mark.parametrize(
        "table", ["dummy_pod_id", {"user/dummy_pod_id": "dummy_pod_id"}]
    )
    def test__load_data_for_worker_single_table(
        self,
        dummy_protocol: FederatedAveraging,
        mock_engine: sqlalchemy.engine.base.Engine,
        mock_pandas_read_sql_query: None,
        mocker: MockerFixture,
        table: Union[dict, str],
    ) -> None:
        """Tests table name provided by datastructure is applied to datasource."""
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        db_conn = DatabaseConnection(mock_engine, table_names=["dummy_data"])
        pod_id = "user/dummy_pod_id"

        ds = DatabaseSource(db_conn, seed=420)
        datastructure = DataStructure(table=table)
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
            pod_db=True,
        )
        assert worker._pod_db is False
        worker._load_data_for_worker(
            datastructure=datastructure,
        )

        assert worker.datasource.data is not None
        assert isinstance(worker.datasource.data, pd.DataFrame)

    def test__load_data_for_worker_intermine(self, mocker: MockerFixture) -> None:
        """Tests table name provided by datastructure is applied to datasource."""
        pod_id = "user/dummy_pod_id"
        table_name = "dummy_pod_id"
        service_url = "https://fake_url"
        mocker.patch("bitfount.federated.worker.bf_load")
        mock_service = mocker.patch(
            "bitfount.data.datasources.intermine_source.Service"
        )
        ds = IntermineSource(service_url, token=None)
        mocker.patch.object(
            IntermineSource, "table_names", PropertyMock(return_value=[table_name])
        )
        mocker.patch.object(
            IntermineSource, "_template_to_df", return_value=create_dataset()
        )
        datastructure = DataStructure(table={pod_id: table_name})
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        worker._load_data_for_worker(
            datastructure=datastructure,
        )

        assert worker.datasource.data is not None
        mock_service.assert_called_once_with(service_url, token=None)
        assert isinstance(worker.datasource.data, pd.DataFrame)

    def test__load_data_for_worker_errors_wrong_pod_id_query(
        self,
        dummy_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Test error raised if DataStructure has no map for workers pod id."""
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        sql_query = 'SELECT "Date", "TARGET" FROM dummy_data'
        worker_pod_id = "worker_pod_id"
        query = {"different_pod_id": sql_query}
        schema_override: Mapping[str, SchemaOverrideMapping]
        schema_override = {"different_pod_id": {"text": ["Date", "TARGET"]}}
        ds = create_datasource(classification=True)
        datastructure = DataStructure(
            query=query, schema_types_override=schema_override
        )
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=worker_pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        with pytest.raises(DataStructureError):
            worker._load_data_for_worker(datastructure=datastructure)

    def test__load_data_for_worker_errors_wrong_pod_id_table(
        self,
        dummy_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Test error raised if DataStructure has no map for workers pod id."""
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        worker_pod_id = "worker_pod_id"
        ds_table = {"different_pod_id": "table_name"}
        ds = create_datasource(classification=True)
        datastructure = DataStructure(table=ds_table)
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=worker_pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        with pytest.raises(DataStructureError):
            worker._load_data_for_worker(datastructure=datastructure)

    def test__load_data_for_worker_errors_incompatiable_ds(
        self,
        dummy_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Test error raised with incompatible DataStructure and DatabaseSource.

        If the datastructure table is given as a SQL query but the datasource
        is a dataframe an ValueError should be raised.
        """
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        sql_query = 'SELECT "Date", "TARGET" FROM dummy_data'
        pod_id = "dummy_pod_id"
        schema_override: Mapping[str, SchemaOverrideMapping]
        schema_override = {pod_id: {"continuous": ["a", "b", "c"]}}
        ds = create_datasource(classification=True)
        datastructure = DataStructure(
            query={pod_id: sql_query},
            schema_types_override=schema_override,
        )
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        with pytest.raises(ValueError):
            worker._load_data_for_worker(datastructure=datastructure)

    async def test_worker_adds_hub_instance_to_serialized_bitfount_model_reference(
        self,
        authoriser: _AuthorisationChecker,
        caplog: LogCaptureFixture,
        dummy_protocol: FederatedAveraging,
        dummy_serializable_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the worker adds hub to serialized bitfount model reference.

        The worker should add the hub instance to the serialized bitfount model
        reference because the hub is not serialized as part of the protocol but is
        required to retrieve the custom model from the hub.
        """
        caplog.set_level("DEBUG")
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        protocol_with_bitfount_model_reference = dummy_serializable_protocol.dump()
        serialized_algorithm = cast(
            SerializedAlgorithm, protocol_with_bitfount_model_reference["algorithm"]
        )
        serialized_algorithm["model"]["class_name"] = "BitfountModelReference"
        worker = _Worker(
            Mock(),
            AsyncMock(),
            Mock(),
            authoriser,
            pod_identifier="dummy_id",
            serialized_protocol=protocol_with_bitfount_model_reference,
        )
        mocker.patch.object(worker, "_load_data_for_worker")
        await worker.run()
        assert "Patching model reference hub." in [i.message for i in caplog.records]

    async def test_worker_run_sends_task_config_to_monitor_service(
        self,
        authoriser: _AuthorisationChecker,
        dummy_protocol: FederatedAveraging,
        dummy_serializable_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the worker sends task config to monitor service."""
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        mocker.patch("bitfount.federated.worker.bf_load", return_value=dummy_protocol)
        mock_monitor = Mock()
        mocker.patch(
            "bitfount.federated.monitoring.monitor._get_task_monitor",
            return_value=mock_monitor,
        )
        mailbox = AsyncMock()
        worker = _Worker(
            Mock(),
            mailbox,
            Mock(),
            authoriser,
            pod_identifier="dummy_id",
            serialized_protocol=dummy_serializable_protocol.dump(),
        )
        await worker.run()
        mock_monitor.send_to_monitor_service.assert_called_once_with(
            event_type=AdditionalMonitorMessageTypes.TASK_CONFIG,
            privacy=MonitorRecordPrivacy.OWNER_MODELLER,
            metadata=worker.serialized_protocol,
        )


@integration_test
class TestWorkerDatabaseConnection:
    """Tests Worker class with an underlying database connection."""

    @pytest.mark.parametrize(
        "sql_query, schema_types_override",
        [
            (
                'SELECT "Date", "TARGET" FROM dummy_data',
                {"categorical": [{"TARGET": {"0": 0, "1": 1}}], "text": ["Date"]},
            ),
            (
                """SELECT d1."Date", d2."A" from dummy_data d1
            JOIN dummy_data_2 d2
            ON d1."Date" = d2."Date"
            """,
                {"continuous": ["A"], "text": ["Date"]},
            ),
        ],
    )
    def test__load_data_for_worker_table_as_query_pod_id(
        self,
        db_session: sqlalchemy.engine.base.Engine,
        mocker: MockerFixture,
        schema_types_override: SchemaOverrideMapping,
        sql_query: str,
    ) -> None:
        """Tests sql query provided by datastructure is applied to datasource."""
        mocker.patch("bitfount.federated.worker.bf_load")
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        pod_id = "dummy_pod_id"
        expected_output = pd.read_sql(sql_query, con=db_conn.con)
        ds = DatabaseSource(db_conn, seed=420, data_splitter=PercentageSplitter(0, 0))
        datastructure = DataStructure(
            query={pod_id: sql_query},  # dictionary of pod_id to sql query
            schema_types_override={pod_id: schema_types_override},
        )
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        worker._load_data_for_worker(
            datastructure=datastructure,
        )

        cumulative_len = 0

        mocker.patch.object(_IterableBitfountDataset, "_set_column_name_attributes")
        dataset = _IterableBitfountDataset(ds, Mock(), Mock(), Mock(), Mock())

        for df in dataset.yield_dataset_split(DataSplit.TRAIN):
            assert list(df.columns) == list(expected_output.columns)
            cumulative_len += len(df)

        assert cumulative_len == len(expected_output)

    @pytest.mark.parametrize(
        "sql_query, schema_types_override",
        [
            (
                'SELECT "Date", "TARGET" FROM dummy_data',
                {"categorical": [{"TARGET": {"0": 0, "1": 1}}], "text": ["Date"]},
            ),
            (
                """SELECT d1."Date", d2."A" from dummy_data d1
            JOIN dummy_data_2 d2
            ON d1."Date" = d2."Date"
            """,
                {"continuous": ["A"], "text": ["Date"]},
            ),
        ],
    )
    def test__load_data_for_worker_table_as_query(
        self,
        db_session: sqlalchemy.engine.base.Engine,
        mocker: MockerFixture,
        schema_types_override: SchemaOverrideMapping,
        sql_query: str,
    ) -> None:
        """Tests sql query provided by datastructure is applied to datasource."""
        mocker.patch("bitfount.federated.worker.bf_load")
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        pod_id = "dummy_pod_id"
        expected_output = pd.read_sql(sql_query, con=db_conn.con)
        ds = DatabaseSource(db_conn, seed=420, data_splitter=PercentageSplitter(0, 0))
        datastructure = DataStructure(
            query=sql_query,  # standalone sql query
            schema_types_override=schema_types_override,
        )
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        worker._load_data_for_worker(
            datastructure=datastructure,
        )
        cumulative_len = 0

        mocker.patch.object(_IterableBitfountDataset, "_set_column_name_attributes")
        dataset = _IterableBitfountDataset(ds, Mock(), Mock(), Mock(), Mock())

        for df in dataset.yield_dataset_split(DataSplit.TRAIN):
            assert list(df.columns) == list(expected_output.columns)
            cumulative_len += len(df)

        assert cumulative_len == len(expected_output)

    @pytest.mark.parametrize(
        "table", ["dummy_pod_id", {"user/dummy_pod_id": "dummy_data"}]
    )
    def test__load_data_for_worker_single_table(
        self,
        db_session: sqlalchemy.engine.base.Engine,
        mocker: MockerFixture,
        table: Union[dict, str],
    ) -> None:
        """Tests table name provided by datastructure is applied to datasource."""
        mocker.patch("bitfount.federated.worker.bf_load")
        pod_id = "user/dummy_pod_id"
        db_conn = DatabaseConnection(db_session, table_names=["dummy_data"])
        expected_output = pd.read_sql_table(table_name="dummy_data", con=db_conn.con)
        ds = DatabaseSource(db_conn, seed=420, data_splitter=PercentageSplitter(0, 0))
        datastructure = DataStructure(table=table)
        worker = _Worker(
            ds,
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier=pod_id,
            serialized_protocol=Mock(spec=SerializedProtocol),
        )
        worker._load_data_for_worker(
            datastructure=datastructure,
        )

        cumulative_len = 0

        mocker.patch.object(_IterableBitfountDataset, "_set_column_name_attributes")
        dataset = _IterableBitfountDataset(ds, Mock(), Mock(), Mock(), Mock())

        for df in dataset.yield_dataset_split(DataSplit.TRAIN):
            assert list(df.columns) == list(expected_output.columns)
            cumulative_len += len(df)

        assert cumulative_len == len(expected_output)
