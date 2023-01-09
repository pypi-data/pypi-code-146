"""Tests for the sql query algorithm."""
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import Mock, create_autospec

from _pytest.logging import LogCaptureFixture
from _pytest.tmpdir import TempPathFactory
import numpy as np
import pandas as pd
from pytest import fixture
from pytest_mock import MockerFixture
import sqlalchemy

from bitfount import DatabaseConnection
from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datasources.dataframe_source import DataFrameSource
from bitfount.data.datasources.excel_source import ExcelSource
from bitfount.data.datasources.intermine_source import IntermineSource
from bitfount.federated.algorithms.base import (
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
    _BaseAlgorithm,
)
from bitfount.federated.algorithms.sql_query import SqlQuery, _ModellerSide, _WorkerSide
from bitfount.federated.modeller import _Modeller
from bitfount.federated.utils import _ALGORITHMS
from bitfount.hub import BitfountHub
from bitfount.schemas.utils import bf_dump, bf_load
from tests.utils.helper import (
    create_dataset,
    create_datasource,
    integration_test,
    unit_test,
)


class TestSqlQuery:
    """Test SqlQuery algorithm."""

    @fixture
    def datasource(self) -> BaseSource:
        """Fixture for datasource."""
        return create_datasource(classification=True)

    @fixture(scope="class")
    def multi_table_excel_source(self, multi_table_excel_file: Path) -> ExcelSource:
        """Multi Table ExcelSource."""
        source = ExcelSource(multi_table_excel_file, sheet_name=["Sheet1", "Sheet2"])
        assert source.multi_table
        return source

    @fixture(scope="class")
    def multi_table_excel_file(self, tmp_path_factory: TempPathFactory) -> Path:
        """Path to multi table excel file."""
        dataframe = create_dataset()
        tmp_path = tmp_path_factory.mktemp("temp_excel")
        filename = tmp_path / "test.xlsx"
        with pd.ExcelWriter(filename) as writer:  # type: ignore[abstract] # Reason: This is the documented usage. # noqa: B950
            dataframe.to_excel(writer, index=False, sheet_name="Sheet1")
            dataframe.to_excel(writer, index=False, sheet_name="Sheet2")

        return filename

    @unit_test
    def test_modeller_types(self) -> None:
        """Test modeller method."""
        algorithm_factory = SqlQuery(query="SELECT * from `df`")
        algorithm = algorithm_factory.modeller()
        for type_ in [
            _BaseAlgorithm,
            BaseModellerAlgorithm,
        ]:
            assert isinstance(algorithm, type_)

    @unit_test
    def test_worker_types(self) -> None:
        """Test worker method."""
        algorithm_factory = SqlQuery(query="SELECT * from `df`")
        algorithm = algorithm_factory.worker(
            hub=create_autospec(BitfountHub, instance=True)
        )
        for type_ in [
            _BaseAlgorithm,
            BaseWorkerAlgorithm,
        ]:
            assert isinstance(algorithm, type_)

    @unit_test
    def test_worker_init_datasource(self, datasource: DataFrameSource) -> None:
        """Test worker method."""
        algorithm_factory = SqlQuery(query="SELECT * from `df`")
        algorithm_factory.worker().initialise(datasource=datasource)

    @unit_test
    def test_modeller_init(self) -> None:
        """Test worker method."""
        algorithm_factory = SqlQuery(query="SELECT * from `df`")
        algorithm_factory.modeller().initialise()

    @unit_test
    def test_bad_sql_no_table(
        self, caplog: LogCaptureFixture, datasource: DataFrameSource
    ) -> None:
        """Test that having no data raises an error."""
        algorithm_factory = SqlQuery(query="SELECT MAX(G) AS MAX_OF_G", table="df")
        worker = algorithm_factory.worker()
        worker.datasource = datasource
        worker.datasource.load_data()
        worker.run()
        err_msg = "The default table for single table datasource is the pod"
        assert err_msg in caplog.text

    @unit_test
    def test_bad_sql_query_statement(
        self, caplog: LogCaptureFixture, datasource: DataFrameSource
    ) -> None:
        """Test that a bad operator in SQL query errors out."""
        algorithm_factory = SqlQuery(query="SELECTOR MAX(G) AS MAX_OF_G FROM df")
        worker = algorithm_factory.worker()
        worker.datasource = datasource
        worker.datasource.load_data()
        worker.run()
        assert "ERROR" in caplog.text

    @unit_test
    def test_bad_sql_query_column(
        self, caplog: LogCaptureFixture, datasource: DataFrameSource
    ) -> None:
        """Test that an invalid column in SQL query errors out."""
        algorithm_factory = SqlQuery(
            query="SELECT MAX(BITFOUNT_TEST) AS MAX_OF_BITFOUNT_TEST FROM `df`",
            table="df",
        )
        worker = algorithm_factory.worker()
        worker.datasource = datasource
        worker.run()
        assert "ERROR" in caplog.text

    @unit_test
    def test_bad_sql_no_from_df(
        self, caplog: LogCaptureFixture, datasource: DataFrameSource
    ) -> None:
        """Test that an invalid query errors out."""
        algorithm_factory = SqlQuery(query="mock", table="df")
        worker = algorithm_factory.worker()
        worker.datasource = datasource
        worker.run()
        err_msg = "The default table for single table datasource is the pod"
        assert err_msg in caplog.text

    @unit_test
    def test_worker_gets_sql_results(self, datasource: DataFrameSource) -> None:
        """Test that a SQL query returns correct result."""
        algorithm_factory = SqlQuery(
            query="SELECT MAX(G) AS MAX_OF_G FROM `df`",
        )
        worker = algorithm_factory.worker()
        worker.initialise(datasource=datasource, pod_identifier="user/df")
        assert worker.table == "df"
        results = worker.run()
        assert np.isclose(results.MAX_OF_G[0], 0.9997870068530033, atol=1e-4)

    @unit_test
    def test_worker_run_no_table_error(
        self, caplog: LogCaptureFixture, multi_table_excel_source: ExcelSource
    ) -> None:
        """Test that a SQL query returns correct result."""
        algorithm_factory = SqlQuery(
            query="SELECT MAX(G) AS MAX_OF_G FROM `df`",
        )
        worker = algorithm_factory.worker()
        worker.initialise(datasource=multi_table_excel_source, pod_identifier="user/df")
        worker.run()
        err_msg = "No table specified on which to execute the query on. "
        assert err_msg in caplog.text

    @unit_test
    def test_modeller_gets_sql_results(self, datasource: DataFrameSource) -> None:
        """Test that a SQL query returns a result."""
        algorithm_factory = SqlQuery(
            query="SELECT MAX(G) AS MAX_OF_G FROM `df`", table="df"
        )
        modeller = algorithm_factory.modeller()
        data = {"MAX_OF_G": [0.9997870068530033]}
        results = {"pod1": pd.DataFrame(data)}
        returned_results = modeller.run(results=results)
        assert np.isclose(
            returned_results["pod1"]["MAX_OF_G"], results["pod1"]["MAX_OF_G"], atol=1e-4
        )

    @integration_test
    def test_sql_algorithm_db_connection_multitable(
        self,
        db_session: sqlalchemy.engine.base.Engine,
    ) -> None:
        """Test sql algorithm on multitable db connection."""
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DatabaseSource(db_conn, seed=420)
        algorithm_factory = SqlQuery(
            query='SELECT MAX("A") AS MAX_OF_A FROM dummy_data', table="dummy_data"
        )
        worker = algorithm_factory.worker()
        worker.datasource = ds
        res = worker.run()
        assert res["max_of_a"] is not None

    @unit_test
    def test_sql_output_duplicate_cols_error(
        self,
        caplog: LogCaptureFixture,
        datasource: DataFrameSource,
        mocker: MockerFixture,
    ) -> None:
        """Test that an error is raised if query output has a duplicated column name."""
        algorithm_factory = SqlQuery(query="SELECT * FROM `df`", table="df")
        worker = algorithm_factory.worker()
        dataset = pd.DataFrame({"A": [1], "B": [2]})
        dataset.columns = ["A", "A"]
        worker.datasource = datasource
        mocker.patch("pandasql.sqldf", return_value=dataset)
        worker.run()
        err_msg = "The following column names are duplicated in the output"
        assert err_msg in caplog.text

    @unit_test
    def test_sql_execute(
        self, mock_bitfount_session: Mock, mocker: MockerFixture
    ) -> None:
        """Test execute syntactic sugar."""
        query = SqlQuery(query="SELECT * FROM `df`")
        pod_identifiers = ["username/pod-id"]

        mock_modeller_run_method = mocker.patch.object(_Modeller, "run")
        query.execute(pod_identifiers=pod_identifiers)
        mock_modeller_run_method.assert_called_once_with(
            pod_identifiers=pod_identifiers, require_all_pods=False, project_id=None
        )

    @unit_test
    def test_sql_algorithm_intermine(self, mocker: MockerFixture) -> None:
        """Test sql algorithm on Intermine data source."""
        service_url = "https://fake_url"

        mock_service = mocker.patch(
            "bitfount.data.datasources.intermine_source.Service"
        )
        ds = IntermineSource(service_url, token=None)
        mocker.patch.object(ds, "get_data", return_value=create_dataset())
        algorithm_factory = SqlQuery(
            query="SELECT * FROM `Gene_Protein`", table="Gene_Protein"
        )
        worker = algorithm_factory.worker()
        worker.datasource = ds
        res = worker.run()

        mock_service.assert_called_once_with(service_url, token=None)
        assert not res.empty


@unit_test
class TestMarshmallowSerialization:
    """Test Marshmallow Serialization for sql query algorithm."""

    def test_serialization(self) -> None:
        """Test Marshmallow Serialization for sql query algorithm."""
        algorithm_factory = SqlQuery(query="SELECT * FROM `df`")
        dumped = bf_dump(algorithm_factory)
        loaded = bf_load(dumped, _ALGORITHMS)
        assert isinstance(loaded, SqlQuery)
        assert algorithm_factory.__dict__ == loaded.__dict__


# Static tests for algorithm-protocol compatibility
if TYPE_CHECKING:
    from typing import cast

    from bitfount.federated.protocols.results_only import (
        _ResultsOnlyCompatibleAlgoFactory_,
        _ResultsOnlyCompatibleModellerAlgorithm,
        _ResultsOnlyDataIncompatibleWorkerAlgorithm,
    )

    # Check compatible with ResultsOnly
    _algo_factory: _ResultsOnlyCompatibleAlgoFactory_ = SqlQuery(
        query=cast(str, object()), pretrained_file=cast(str, object())
    )
    _modeller_side: _ResultsOnlyCompatibleModellerAlgorithm = _ModellerSide()
    _worker_side: _ResultsOnlyDataIncompatibleWorkerAlgorithm = _WorkerSide(
        query=cast(str, object()), table=cast(str, object())
    )
