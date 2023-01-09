"""Tests datasource.py."""
import datetime
from functools import partial
from pathlib import Path
import platform
import re
from typing import Any, Callable, Dict, cast
from unittest.mock import Mock, PropertyMock

from _pytest.logging import LogCaptureFixture
from _pytest.tmpdir import TempPathFactory
from intermine.webservice import Service
import numpy as np
import pandas as pd
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
import pytest
from pytest import fixture
from pytest_mock import MockerFixture
import sqlalchemy
from sqlalchemy.exc import ArgumentError

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.csv_source import CSVSource
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datasources.dataframe_source import DataFrameSource
from bitfount.data.datasources.dicom_source import (
    DICOMSource,
    OphthalmologyDataSourceArgs,
)
from bitfount.data.datasources.excel_source import ExcelSource
from bitfount.data.datasources.intermine_source import IntermineSource
from bitfount.data.exceptions import (
    DataNotLoadedError,
    DataSourceError,
    ExcelSourceError,
)
from bitfount.data.types import DataPathModifiers
from bitfount.data.utils import DatabaseConnection, _hash_str
from tests.utils import PytestRequest
from tests.utils.helper import (
    DATASET_ROW_COUNT,
    create_dataset,
    integration_test,
    unit_test,
)


@fixture(scope="module")
def dataframe() -> pd.DataFrame:
    """Dataframe fixture."""
    return create_dataset()


@unit_test
class TestBaseSource:
    """Tests core BaseSource functionality with a CSV file."""

    @fixture(scope="function", params=["pandas", "image"])
    def datasource_generator(
        self, request: PytestRequest
    ) -> Callable[..., DataFrameSource]:
        """Dataset loader for use in tests."""
        image = False
        if request.param == "image":
            image = True
        data = create_dataset(image=image)
        if image:
            return partial(DataFrameSource, data, seed=420)

        return partial(DataFrameSource, data, seed=420)

    def test_get_data_dtypes(self) -> None:
        """Tests _get_data_dtypes."""
        df = pd.DataFrame(
            {
                "int_column": [1, 2, 3],
                "float_column": [1.0, 2.0, 3.0],
                "str_column": ["1", "2", "3"],
            }
        )
        df["date"] = datetime.date(2020, 1, 1)
        df["datetime"] = datetime.datetime(2020, 1, 1, 0, 0)
        dtypes = BaseSource._get_data_dtypes(df)

        # Check that the correct columns are returned
        assert isinstance(dtypes, dict)
        assert sorted(list(dtypes)) == sorted(df.columns)
        # Check that the types are as expected
        assert dtypes["date"] == object
        assert dtypes["date"] != pd.StringDtype()
        assert dtypes["datetime"] != object
        assert dtypes["datetime"] == pd.StringDtype()

    def test_tabular_datasource_errors(self) -> None:
        """Checks BaseSource object errors via wrong first argument."""
        with pytest.raises(TypeError):
            DataFrameSource("test1", seed=420)  # type: ignore[arg-type] # Reason: purpose of test # noqa: B950

        with pytest.raises(TypeError):
            test_path = Path("/my/root/directory")
            DataFrameSource(test_path, seed=420)  # type: ignore[arg-type] # Reason: purpose of test # noqa: B950

    def test_datasource_modifiers_path_prefix(self, dataframe: pd.DataFrame) -> None:
        """Tests functionality for providing image path prefix."""
        dataframe["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"prefix": "/path/to/"})}
        datasource = DataFrameSource(dataframe, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image"].unique()) == 1
        assert datasource.data["image"].unique()[0] == "/path/to/image_file_name"

    def test_image_datasource_ext_suffix(self, dataframe: pd.DataFrame) -> None:
        """Tests functionality for finding images by file extension."""
        dataframe["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"suffix": ".jpeg"})}
        datasource = DataFrameSource(dataframe, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image"].unique()) == 1
        assert datasource.data["image"].unique()[0] == "image_file_name.jpeg"

    def test_image_datasource_ext_prefix_suffix(self, dataframe: pd.DataFrame) -> None:
        """Tests functionality for finding images by file extension."""
        dataframe["image"] = "image_file_name"
        modifiers = {
            "image": DataPathModifiers({"prefix": "/path/to/", "suffix": ".jpeg"})
        }
        datasource = DataFrameSource(dataframe, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image"].unique()) == 1
        assert datasource.data["image"].unique()[0] == "/path/to/image_file_name.jpeg"

    def test_multiple_img_datasource_modifiers(self) -> None:
        """Tests functionality for finding multiple images by file extension."""
        data = create_dataset(multiimage=True, img_size=1)
        data["image1"] = "image1_file_name"
        data["image2"] = "image2_file_name"
        modifiers = {
            "image1": DataPathModifiers({"prefix": "/path/to/"}),
            "image2": DataPathModifiers({"suffix": ".jpeg"}),
        }
        datasource = DataFrameSource(data, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image1"].unique()) == 1
        assert datasource.data["image1"].unique()[0] == "/path/to/image1_file_name"
        assert len(datasource.data["image2"].unique()) == 1
        assert datasource.data["image2"].unique()[0] == "image2_file_name.jpeg"

    def test_tabular_datasource_read_csv_correctly(
        self, dataframe: pd.DataFrame, tmp_path: Path
    ) -> None:
        """Tests CSVSource loading from csv."""
        file_path = tmp_path / "tabular_data_test.csv"
        dataframe.to_csv(file_path)
        ds = CSVSource(file_path)
        ds.load_data()
        assert ds.data is not None

    def test_ignored_cols_list_excluded_from_df(self, dataframe: pd.DataFrame) -> None:
        """Tests that a list of ignore_cols are ignored in the data."""
        dataframe["image"] = "image_file_name"
        ignore_cols = ["N", "O", "P"]
        datasource = DataFrameSource(
            dataframe,
            seed=420,
            ignore_cols=ignore_cols,
        )
        datasource.load_data()
        assert not any(item in datasource.data.columns for item in ignore_cols)

    def test_ignored_single_col_list_excluded_from_df(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Tests that a str ignore_cols is ignored in the data."""
        dataframe["image"] = "image_file_name"
        ignore_cols = "N"
        datasource = DataFrameSource(
            dataframe,
            seed=420,
            ignore_cols=ignore_cols,
        )
        datasource.load_data()
        assert ignore_cols not in datasource.data.columns

    def test_hash(
        self,
        datasource_generator: Callable[..., DataFrameSource],
        mocker: MockerFixture,
    ) -> None:
        """Tests hash is called on the dtypes."""
        datasource = datasource_generator()
        expected_hash = f"hash_{id(datasource._table_hashes)}"
        mock_hash_function: Mock = mocker.patch(
            "bitfount.data.datasources.base_source._generate_dtypes_hash",
            return_value=expected_hash,
            autospec=True,
        )
        datasource.get_dtypes()

        actual_hash = datasource.hash

        # Check hash is expected return and how it was called
        assert actual_hash == _hash_str(str([expected_hash]))
        mock_hash_function.assert_called_once()

    def test_get_dtypes_ignores_cols(
        self,
        datasource_generator: Callable[..., DataFrameSource],
        mocker: MockerFixture,
    ) -> None:
        """Tests get_dtypes drops _ignore_cols."""
        datasource = datasource_generator()
        datasource._ignore_cols = ["A"]
        assert "A" in datasource.get_data().columns

        result = datasource.get_dtypes()

        assert "A" not in result.keys()

    def test_get_column_applies_modifiers(
        self,
        datasource_generator: Callable[..., DataFrameSource],
        mocker: MockerFixture,
    ) -> None:
        """Tests get_column applies modifiers."""
        datasource = datasource_generator()
        prefix = "/path/to/"
        datasource._modifiers = {"A": DataPathModifiers({"prefix": prefix})}
        expected_result = prefix + datasource.get_data()["A"].astype(str)

        result = datasource.get_column("A")

        assert all(result == expected_result)

    def test_get_data_failes(self, mock_engine: Mock) -> None:
        """Test data raises error when data not set."""
        db_conn = DatabaseConnection(mock_engine)
        datasource = DatabaseSource(db_conn)
        with pytest.raises(
            DataNotLoadedError,
            match="Data is not loaded yet. Please call `load_data` first.",
        ):
            datasource.data


class TestDatabaseSource:
    """Tests DatabaseSource."""

    @unit_test
    @pytest.mark.parametrize(
        "params, result",
        [
            ({"table_names": ["dummy_data"]}, "SELECT * FROM dummy_data"),
            ({"query": "SELECT * FROM dummy_data"}, "SELECT * FROM dummy_data"),
        ],
    )
    def test_query(
        self, mock_engine: Mock, params: Dict[Any, Any], result: Any
    ) -> None:
        """Test query returns correct result."""
        db_conn = DatabaseConnection(mock_engine, **params)
        datasource = DatabaseSource(db_conn, seed=420)
        assert datasource.query == result

    @unit_test
    def test_query_datastructure_query(self, mock_engine: Mock) -> None:
        """Test query returns datastructure query."""
        db_conn = DatabaseConnection(
            mock_engine,
        )
        datastructure_query = "SELECT * FROM dummy_data"
        datasource = DatabaseSource(db_conn, seed=420)
        datasource.datastructure_query = datastructure_query
        assert datasource.query == datastructure_query

    @unit_test
    def test_hash_multitable_raises_value_error(self, mock_engine: Mock) -> None:
        """Tests hash function raises `DataNotLoadedError` if data is not loaded."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        datasource = DatabaseSource(db_conn, seed=420)
        with pytest.raises(DataNotLoadedError):
            datasource.hash

    @unit_test
    def test_value_error_raised_if_no_table_name_provided_for_multitable_datasource(
        self, mock_engine: Mock
    ) -> None:
        """Test ValueError raised if no table_name for multi-table DatabaseSource."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DatabaseSource(db_conn, seed=420)
        ds.load_data()
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            ds.get_dtypes()

    @unit_test
    def test_value_error_raised_if_table_not_found_for_multitable_datasource(
        self, mock_engine: Mock
    ) -> None:
        """Tests ValueError raised if table missing for multi-table DatabaseSource."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DatabaseSource(db_conn, seed=420)
        ds.load_data()
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Table name not_a_table not found in the data. "
                + "Available tables: ['dummy_data', 'dummy_data_2']"
            ),
        ):
            ds.get_dtypes(table_name="not_a_table")

    @unit_test
    def test_invalid_connection_string_errors(self) -> None:
        """Test DatabaseSource errors with invalid conn string."""
        invalid_connection_str = "random_str"
        with pytest.raises(
            ArgumentError,
            match=(
                f"Invalid db_conn. db_conn: {invalid_connection_str} "
                "must be sqlalchemy compatible database url, see: .*"
            ),
        ):
            DatabaseSource(invalid_connection_str)

    @integration_test
    def test_instantiation_works_with_db_conn_as_string(
        self, db_session: sqlalchemy.engine.base.Engine
    ) -> None:
        """Test DataSource can be created with valid connection string."""
        expected_table_names = ["dummy_data", "dummy_data_2"]
        connection_str = str(db_session.url)
        assert isinstance(connection_str, str)
        ds = DatabaseSource(connection_str)

        # Correctly read table from connection string
        assert ds.table_names == expected_table_names

    @integration_test
    def test_mock_get_dtypes_reads_and_returns_table_schema(
        self, db_session: sqlalchemy.engine.base.Engine
    ) -> None:
        """Tests that the `get_dtypes` method returns a dictionary.

        Also checks that the dtypes hash is added appropriately.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DatabaseSource(db_conn, seed=420)

        assert len(ds._table_hashes) == 0
        assert isinstance(ds.get_dtypes(table_name="dummy_data"), dict)
        assert len(ds._table_hashes) == 1

    @integration_test
    def test_get_dtypes_reads_and_returns_table_schema(
        self, db_session: sqlalchemy.engine.base.Engine
    ) -> None:
        """Tests that the `get_dtypes` method returns a dictionary.

        Also checks that the dtypes hash is added appropriately.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DatabaseSource(db_conn, seed=420)
        assert len(ds._table_hashes) == 0
        table = ds.get_dtypes(table_name="dummy_data")
        assert isinstance(table, dict)
        assert len(ds._table_hashes) == 1

    @unit_test
    def test_get_column(self, mock_engine: Mock, mocker: MockerFixture) -> None:
        """Test get_column returns column."""
        # Creates a multitable DatabaseConnection object
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        datasource = DatabaseSource(db_conn)
        col_name = "A"
        mock_table: Mock = mocker.patch(
            "bitfount.data.datasources.database_source.Table",
            autospec=True,
        )
        mock_table.return_value.columns = {col_name: None}
        mock_session: Mock = mocker.patch(
            "bitfount.data.datasources.database_source.Session",
            autospec=True,
        )
        mock_result = [(1,), (2,), (3,)]
        mock_session.return_value.__enter__.return_value.query.return_value = (
            mock_result
        )

        result = datasource.get_column(col_name=col_name, table_name="dummy_data")

        assert all(result == pd.Series([1, 2, 3]))
        mock_table.assert_called_once()
        mock_session.assert_called_once()

    @unit_test
    def test_len_magic_method_multi_table(
        self, mock_engine: Mock, mocker: MockerFixture
    ) -> None:
        """Tests that __len__ magic method returns correct row count."""
        # Mocks `execute` method on the SQLAlchemy connection object and the
        # `scalar_one` method on the resulting cursor result to return the
        # dataset row count
        mock_db_connection = Mock()
        mock_result = Mock()
        mock_result.scalar_one.return_value = DATASET_ROW_COUNT
        mock_db_connection.execute.return_value = mock_result
        mock_engine.execution_options.return_value = mock_engine

        # Creates a multitable DatabaseConnection object
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        # Mocks `connect` method and resulting context manager on SQLAlchemy Engine
        mocker.patch.object(
            db_conn.con, "connect"
        ).return_value.__enter__.return_value = mock_db_connection
        loader = DatabaseSource(db_conn)

        # Calls __len__ method on loader
        dataset_length = len(loader)

        # Makes assertions on call stack in order
        # Ignoring mypy errors because `connect` has been patched to return a Mock
        db_conn.con.connect.assert_called_once()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        db_conn.con.connect.return_value.__enter__.assert_called_once()  # type: ignore[attr-defined]  # Reason: see above # noqa: B950
        mock_db_connection.execute.assert_called_once()
        mock_result.scalar_one.assert_called_once()

        # Makes assertion on final result
        assert dataset_length == DATASET_ROW_COUNT

    @unit_test
    def test_len_magic_method_single_table_preloaded(self, mock_engine: Mock) -> None:
        """Test `len()` works as expected with one already loaded table."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data"],
        )
        datasource = DatabaseSource(db_conn, seed=420)
        datasource.data = pd.DataFrame({"A": [1, 2, 3]})
        assert len(datasource) == 3

    @unit_test
    def test_len_magic_method_single_table(
        self, mock_engine: Mock, mock_pandas_read_sql_query: None
    ) -> None:
        """Test `len()` works as expected with one table."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data"],
        )
        datasource = DatabaseSource(db_conn, seed=420)
        assert len(datasource) == DATASET_ROW_COUNT

    @unit_test
    def test_get_dtypes_raises_value_error_if_table_name_is_none(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if there is no table name provided."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        datasource = DatabaseSource(db_conn)
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            datasource.get_dtypes(table_name=None)

    @unit_test
    def test_get_column_raises_value_error_if_table_name_is_none(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if there is no table name provided."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        datasource = DatabaseSource(db_conn)
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            datasource.get_column(col_name="col", table_name=None)

    @unit_test
    def test_get_values_raises_value_error_if_table_name_is_none(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if there is no table name provided."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        datasource = DatabaseSource(db_conn)
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            datasource.get_values(table_name=None, col_names=["col1", "col2"])

    @unit_test
    def test_validate_table_name_raises_value_error_if_tables_dont_exist(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if there are no tables."""
        db_conn = DatabaseConnection(
            mock_engine,
            query="DUMMY QUERY",
        )
        loader = DatabaseSource(db_conn)
        with pytest.raises(
            ValueError, match="Database Connection is not aware of any tables."
        ):
            loader._validate_table_name("dummy_data")

    @unit_test
    def test_validate_table_name_raises_value_error_if_table_name_not_found(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if the table name is not found."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        loader = DatabaseSource(db_conn)
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Table name blah not found in the data. "
                "Available tables: ['dummy_data', 'dummy_data_2']",
            ),
        ):
            loader._validate_table_name("blah")


@unit_test
class TestCSVSource:
    """Tests CSVSource."""

    @fixture
    def csv_source(self, dataframe: pd.DataFrame, tmp_path: Path) -> CSVSource:
        """CSVSource."""
        file_path = tmp_path / "tabular_data_test.csv"
        dataframe.to_csv(file_path, index=False)
        datasource = CSVSource(file_path, read_csv_kwargs={"parse_dates": ["Date"]})
        return datasource

    def test_len(self, csv_source: CSVSource) -> None:
        """Tests that __len__ magic method returns correct row count."""
        assert len(csv_source) == DATASET_ROW_COUNT

    def test_get_data(self, csv_source: CSVSource, dataframe: pd.DataFrame) -> None:
        """Test get_data returns dataframe."""
        dataframe["Date"] = pd.to_datetime(dataframe["Date"])
        result = csv_source.get_data()
        pd.testing.assert_frame_equal(dataframe, result, check_dtype=False)

    def test_get_column(self, csv_source: CSVSource, dataframe: pd.DataFrame) -> None:
        """Test get_column returns column."""
        column = "A"
        result = csv_source.get_column(column)
        assert all(dataframe[column] == result)

    def test_get_dtypes(self, csv_source: CSVSource, dataframe: pd.DataFrame) -> None:
        """Test get_dtypes works."""
        result = csv_source.get_dtypes()
        assert isinstance(result, dict)
        for col in dataframe.columns:
            assert col in result.keys()

    def test_multitable(self, csv_source: CSVSource) -> None:
        """Test multi_table for CSVSource."""
        assert not csv_source.multi_table


@unit_test
class TestDataFrameSource:
    """Tests DataFrameSource."""

    def test_len(self, dataframe: pd.DataFrame) -> None:
        """Tests that __len__ magic method returns correct row count."""
        loader = DataFrameSource(dataframe)
        assert len(loader) == DATASET_ROW_COUNT


@unit_test
class TestIntermineSource:
    """Tests IntermineSource."""

    @fixture
    def intermine_source(
        self, dataframe: pd.DataFrame, mocker: MockerFixture
    ) -> IntermineSource:
        """IntermineSource."""
        service_url = "https://beta.humanmine.org/humanmine"
        mock_service = mocker.patch(
            "bitfount.data.datasources.intermine_source.Service"
        )
        mock_service.get_template_by_user.return_value = Service(
            "https://beta.humanmine.org/humanmine"
        ).get_template("Gene_Protein")
        datasource = IntermineSource(service_url, None)
        mocker.patch.object(
            IntermineSource, "table_names", PropertyMock(return_value=["table_name"])
        )
        mocker.patch.object(IntermineSource, "_template_to_df", return_value=dataframe)

        datasource.template_to_user_map = {"table_name": "user1"}
        return datasource

    def test_len(self, intermine_source: IntermineSource) -> None:
        """Tests that __len__ magic method returns correct row count."""
        intermine_source.load_data(table_name="table_name")
        assert len(intermine_source) == DATASET_ROW_COUNT

    def test_get_data(self, intermine_source: IntermineSource) -> None:
        """Test get_data returns dataframe."""
        result = intermine_source.get_data(table_name="table_name")
        assert isinstance(result, pd.DataFrame)

    def test__validate_table_name_no_table_name(
        self, intermine_source: IntermineSource
    ) -> None:
        """Test get_data raises ValueError when no table_name specified."""
        with pytest.raises(
            ValueError, match="No table name provided for Intermine service."
        ):
            intermine_source._validate_table_name()

    def test_get_data_service_with_no_templates(
        self, intermine_source: IntermineSource, mocker: MockerFixture
    ) -> None:
        """Test get_data raises ValueError the service has no templates."""
        mock_table_names = PropertyMock(return_value=[])
        mocker.patch.object(IntermineSource, "table_names", mock_table_names)
        with pytest.raises(
            ValueError, match="Service .* did not return any templates."
        ):
            intermine_source.get_data(table_name="table_name")

    def test_get_data_service_with_invalid_table_name(
        self, intermine_source: IntermineSource
    ) -> None:
        """Test get_data raises ValueError with invalid table name."""
        with pytest.raises(
            ValueError,
            match=(
                "Template name invalid_table_name not found in service: .*. "
                "Available tables: .*"
            ),
        ):
            intermine_source.get_data(table_name="invalid_table_name")

    def test_get_column(self, intermine_source: IntermineSource) -> None:
        """Test get_column returns column."""
        column = "A"
        result = intermine_source.get_column(column, table_name="table_name")
        assert isinstance(result, pd.Series)

    def test_get_column_no_table_name(self, intermine_source: IntermineSource) -> None:
        """Test get_column raises ValueError when no table_name specified."""
        column = "Gene.symbol"
        with pytest.raises(ValueError, match="Expected parameter: table_name."):
            intermine_source.get_column(column)

    def test_get_dtypes(self, intermine_source: IntermineSource) -> None:
        """Test get_dtypes works."""
        result = intermine_source.get_dtypes(table_name="table_name")
        assert isinstance(result, dict)

    def test_get_values(self, intermine_source: IntermineSource) -> None:
        """Test get_values works."""
        result = intermine_source.get_values(col_names=["A"], table_name="table_name")
        assert isinstance(result, dict)

    def test_multitable(
        self, intermine_source: IntermineSource, mocker: MockerFixture
    ) -> None:
        """Test multi_table for IntermineSource."""
        mock_table_names = PropertyMock(return_value=["table_1", "table_2"])
        mocker.patch.object(IntermineSource, "table_names", mock_table_names)
        assert intermine_source.multi_table

    def test_multitable_false_for_single_template(
        self, intermine_source: IntermineSource
    ) -> None:
        """Test multi_table for single table IntermineSource."""
        assert not intermine_source.multi_table

    def test__check_duplicate_templates(self, mocker: MockerFixture) -> None:
        """Test ValueError raised when there are duplicate template names."""
        service_url = "https://beta.humanmine.org/humanmine"
        mock_service = mocker.patch(
            "bitfount.data.datasources.intermine_source.Service"
        )
        duplicate_table_names = ["table_name"] * 2
        mocker.patch.object(
            IntermineSource,
            "table_names",
            PropertyMock(return_value=duplicate_table_names),
        )
        expected_err = (
            "Duplicated template name: 'table_name', found in service. "
            "Template names must have unique names."
        )
        with pytest.raises(ValueError, match=expected_err):
            IntermineSource(service_url, None)
        mock_service.assert_called_once_with(service_url, token=None)


@unit_test
class TestExcelSource:
    """Tests ExcelSource."""

    @fixture(scope="class")
    def single_table_excel_file(
        self, tmp_path_factory: TempPathFactory, dataframe: pd.DataFrame
    ) -> Path:
        """Path to single table excel file."""
        tmp_path = tmp_path_factory.mktemp("temp_excel")
        filename = tmp_path / "test.xlsx"
        dataframe.to_excel(filename, index=False, sheet_name="Sheet1")
        return filename

    @fixture(scope="class")
    def multi_table_excel_file(
        self, tmp_path_factory: TempPathFactory, dataframe: pd.DataFrame
    ) -> Path:
        """Path to multi table excel file."""
        tmp_path = tmp_path_factory.mktemp("temp_excel")
        filename = tmp_path / "test.xlsx"
        with pd.ExcelWriter(filename) as writer:  # type: ignore[abstract] # Reason: This is the documented usage. # noqa: B950
            dataframe.to_excel(writer, index=False, sheet_name="Sheet1")
            dataframe.to_excel(writer, index=False, sheet_name="Sheet2")

        return filename

    @fixture(scope="class")
    def single_table_excel_source(self, single_table_excel_file: Path) -> ExcelSource:
        """Single Table ExcelSource."""
        source = ExcelSource(single_table_excel_file, sheet_name="Sheet1")
        assert not source.multi_table
        return source

    @fixture(scope="class")
    def multi_table_excel_source(self, multi_table_excel_file: Path) -> ExcelSource:
        """Multi Table ExcelSource."""
        source = ExcelSource(multi_table_excel_file, sheet_name=["Sheet1", "Sheet2"])
        assert source.multi_table
        return source

    def test_excel_source_raises_type_error_if_wrong_file_extension(self) -> None:
        """Test ExcelSource raises TypeError if wrong file extension."""
        with pytest.raises(
            TypeError, match="Please provide a Path or URL to an Excel file."
        ):
            ExcelSource("test.txt")

    def test_multi_table_excel_source_raises_value_error_if_column_names_provided(
        self, multi_table_excel_file: Path
    ) -> None:
        """Test Multi Table ExcelSource raises ValueError if column names provided."""
        with pytest.raises(
            ValueError,
            match="Column names can only be provided if a single sheet name is provided.",  # noqa: B950
        ):
            ExcelSource(
                multi_table_excel_file,
                sheet_name=["Sheet1", "Sheet2"],
                column_names=["A"],
            )

    @pytest.mark.parametrize("multi_table", [True, False])
    def test_excel_source_raises_value_error_if_referenced_sheets_are_missing(
        self,
        multi_table: bool,
        multi_table_excel_file: Path,
        single_table_excel_file: Path,
    ) -> None:
        """Test ExcelSource raises ValueError if referenced sheets are missing."""
        with pytest.raises(
            ValueError,
            match=re.escape("Sheet(s) Sheet3 were not found in the Excel file."),
        ):
            if multi_table:
                ExcelSource(
                    multi_table_excel_file,
                    sheet_name=["Sheet1", "Sheet2", "Sheet3"],  # Sheet3 is missing
                )
            else:
                ExcelSource(
                    single_table_excel_file,
                    sheet_name=["Sheet3"],  # Sheet3 is missing
                )

    def test_column_names_override_the_ones_in_the_excel_file(
        self, single_table_excel_file: Path
    ) -> None:
        """Test column names override the ones in the excel file."""
        new_column_names = [str(i) for i in range(16)]
        datasource = ExcelSource(
            single_table_excel_file,
            column_names=new_column_names,
            read_excel_kwargs={"skiprows": 1},
        )

        df = datasource.get_data()
        assert df is not None
        assert list(df.columns) == new_column_names

    def test_multi_table_get_data_raises_value_error_if_table_name_not_recognised(
        self, multi_table_excel_source: ExcelSource
    ) -> None:
        """Test Multi-Table ExcelSource raises ValueError if table name not recognised."""  # noqa: B950
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Table name Table3 not found in the data. "
                "Available tables: Sheet1, Sheet2"
            ),
        ):
            multi_table_excel_source.get_data(table_name="Table3")

    @pytest.mark.parametrize("multi_table", [True, False])
    def test_get_values(
        self,
        multi_table: bool,
        multi_table_excel_source: ExcelSource,
        single_table_excel_source: ExcelSource,
    ) -> None:
        """Test get_values method works as expected."""
        if multi_table:
            values = multi_table_excel_source.get_values(["A"], "Sheet1")
        else:
            values = single_table_excel_source.get_values(["A"])

        assert isinstance(values, dict)
        assert len(values["A"]) == len(set(values["A"]))  # type: ignore[arg-type] # Reason: Len methods is available. # noqa: B950

    @pytest.mark.parametrize("multi_table", [True, False])
    def test_get_column(
        self,
        multi_table: bool,
        multi_table_excel_source: ExcelSource,
        single_table_excel_source: ExcelSource,
    ) -> None:
        """Test get_column method works as expected."""
        if multi_table:
            values = multi_table_excel_source.get_column("A", "Sheet1")
        else:
            values = single_table_excel_source.get_column("A")

        assert isinstance(values, pd.Series)
        assert len(values) == DATASET_ROW_COUNT

    @pytest.mark.parametrize("multi_table", [True, False])
    def test_get_dtypes(
        self,
        multi_table: bool,
        multi_table_excel_source: ExcelSource,
        single_table_excel_source: ExcelSource,
    ) -> None:
        """Test get_dtypes method works as expected."""
        if multi_table:
            dtypes = multi_table_excel_source.get_dtypes("Sheet1")
        else:
            dtypes = single_table_excel_source.get_dtypes()

        assert isinstance(dtypes, dict)

    def test_multitable_get_dtypes_error_no_table(
        self,
        multi_table_excel_source: ExcelSource,
    ) -> None:
        """Test that error is raised when no table is provided."""
        with pytest.raises(ExcelSourceError):
            multi_table_excel_source.get_dtypes()

    @pytest.mark.parametrize("multi_table", [True, False])
    def test_len_magic_method(
        self,
        multi_table: bool,
        multi_table_excel_source: ExcelSource,
        single_table_excel_source: ExcelSource,
    ) -> None:
        """Test len magic method works as expected."""
        if multi_table:
            with pytest.raises(
                ValueError, match="Can't ascertain length of multi-table Excel dataset."
            ):
                len(multi_table_excel_source)

            multi_table_excel_source.load_data(table_name="Sheet1")
            length = len(multi_table_excel_source)
        else:
            length = len(single_table_excel_source)

        assert length == DATASET_ROW_COUNT

    @unit_test
    def test_get_values_raises_value_error_if_table_name_is_none(
        self, multi_table_excel_source: ExcelSource
    ) -> None:
        """Tests that ValueError is raised if there is no table name provided."""
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            multi_table_excel_source.get_values(
                table_name=None, col_names=["col1", "col2"]
            )

    @unit_test
    def test_get_column_raises_value_error_if_table_name_is_none(
        self, multi_table_excel_source: ExcelSource
    ) -> None:
        """Tests that ValueError is raised if there is no table name provided."""
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            multi_table_excel_source.get_column(table_name=None, col_name="col1")


@unit_test
class TestDICOMSource:
    """Tests DICOMSource."""

    def dicom_files_2d(self, tmp_path: Path, filename: str = "dicom_file") -> None:
        """Generates five 2d dicom files for testing."""
        for i in range(5):
            filepath = tmp_path / f"{filename}_{i}.dcm"
            pixel_arr = np.random.randint(0, 255, (100, 100))
            file_meta = FileMetaDataset()
            ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.PatientName = f"Patient {i}"
            ds.PatientID = f"ID {i}"
            ds.StudyDate = f"{i}"
            ds.StudyTime = f"{i}"
            ds.StudyDescription = "Test"
            ds.PixelData = pixel_arr.tobytes()
            ds.NumberOfFrames = "1"
            ds.BitsAllocated = 8
            ds.SamplesPerPixel = 1
            ds.Rows = 100
            ds.Columns = 100
            ds.PhotometricInterpretation = "RGB"
            ds.PixelRepresentation = 0
            ds.BitsStored = 8
            ds.file_meta = FileMetaDataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian  # type: ignore[attr-defined] # Reason: pydicom has that attr and we only use it for testing. # noqa: B950
            ds.is_little_endian = False
            ds.is_implicit_VR = False
            ds.save_as(filepath)

    def dicom_files_2d_window(
        self, tmp_path: Path, filename: str = "dicom_file"
    ) -> None:
        """Generates five 2d dicom files for testing."""
        for i in range(5):
            filepath = tmp_path / f"{filename}_{i}.dcm"
            pixel_arr = np.random.randint(0, 255, (100, 100))
            file_meta = FileMetaDataset()
            ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.WindowWidth = 400
            ds.WindowCenter = 40
            ds.PatientName = f"Patient {i}"
            ds.PatientID = f"ID {i}"
            ds.StudyDate = f"{i}"
            ds.StudyTime = f"{i}"
            ds.StudyDescription = "Test"
            ds.PixelData = pixel_arr.tobytes()
            ds.NumberOfFrames = "1"
            ds.BitsAllocated = 16
            ds.SamplesPerPixel = 1
            ds.Rows = 100
            ds.Columns = 100
            ds.ImageType = ["ORIGINAL", "PRIMARY", "AXIAL"]
            ds.PhotometricInterpretation = "RGB"
            ds.PixelRepresentation = 0
            ds.BitsStored = 8
            ds.file_meta = FileMetaDataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian  # type: ignore[attr-defined] # Reason: pydicom has that attr and we only use it for testing. # noqa: B950
            ds.is_little_endian = False
            ds.is_implicit_VR = False
            ds.save_as(filepath)

    def dicom_files_3d(self, tmp_path: Path, filename: str = "OCT") -> None:
        """Generates five 2d dicom files for testing."""
        for i in range(5):
            filepath = tmp_path / f"{filename}_3d_{i}.dcm"
            pixel_arr = np.random.randint(0, 255, (100, 100))
            file_meta = FileMetaDataset()
            ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.PatientName = f"Patient {i}"
            ds.PatientID = f"ID {i}"
            ds.StudyDate = f"{i}"
            ds.StudyTime = f"{i}"
            ds.StudyDescription = "Test"
            ds.PixelData = pixel_arr.tobytes()
            ds.LanguageCodeSequence = [pydicom.Dataset(), pydicom.Dataset()]
            ds.NumberOfFrames = "5"
            ds.BitsAllocated = 8
            ds.SamplesPerPixel = 1
            if platform.system() == "Windows":
                ds.Rows = 80
            else:
                ds.Rows = 100
            ds.Columns = 100
            ds.PhotometricInterpretation = "RGB"
            ds.PixelRepresentation = 0
            ds.BitsStored = 8
            ds.file_meta = FileMetaDataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian  # type: ignore[attr-defined] # Reason: pydicom has that attr and we only use it for testing. # noqa: B950
            ds.is_little_endian = False
            ds.is_implicit_VR = False
            ds.save_as(filepath)

    def dicom_files_3d_3_samples(self, tmp_path: Path, filename: str = "OCT") -> None:
        """Generates five 3d dicom files for testing."""
        for i in range(5):
            filepath = tmp_path / f"{filename}_3d_{i}.dcm"
            if platform.system() == "Windows":
                pixel_arr = np.random.randint(0, 255, (180, 100))
            else:
                pixel_arr = np.random.randint(0, 255, (90, 100))
            file_meta = FileMetaDataset()
            ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.PatientName = f"Patient {i}"
            ds.PatientID = f"ID {i}"
            ds.StudyDate = f"{i}"
            ds.StudyTime = f"{i}"
            ds.StudyDescription = "Test"
            ds.PixelData = pixel_arr.tobytes()
            ds.LanguageCodeSequence = [pydicom.Dataset(), pydicom.Dataset()]
            ds.NumberOfFrames = "5"
            ds.BitsAllocated = 8
            ds.SamplesPerPixel = 3
            ds.Rows = 100
            ds.PlanarConfiguration = 0
            ds.Columns = 48
            ds.PhotometricInterpretation = "RGB"
            ds.PixelRepresentation = 0
            ds.add_new(0x00280006, "US", 0)
            ds.BitsStored = 8
            ds.file_meta = FileMetaDataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian  # type: ignore[attr-defined] # Reason: pydicom has that attr and we only use it for testing. # noqa: B950
            ds.is_little_endian = False
            ds.is_implicit_VR = False
            ds.save_as(filepath)

    def dicom_files_3d_wrong_pixel_config(
        self, tmp_path: Path, filename: str = "OCT"
    ) -> None:
        """Generates five 2d dicom files for testing."""
        for i in range(5):
            filepath = tmp_path / f"{filename}_3d_{i}.dcm"
            pixel_arr = np.random.randint(0, 255, (10, 100, 100))
            file_meta = FileMetaDataset()
            ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.PatientName = f"Patient {i}"
            ds.PatientID = f"ID {i}"
            ds.StudyDate = f"{i}"
            ds.StudyTime = f"{i}"
            ds.StudyDescription = "Test"
            ds.PixelData = pixel_arr.tobytes()
            ds.LanguageCodeSequence = [pydicom.Dataset(), pydicom.Dataset()]
            ds.NumberOfFrames = "5"
            ds.BitsAllocated = 8
            ds.SamplesPerPixel = 5
            ds.Rows = 100
            ds.PlanarConfiguration = 0
            ds.Columns = 100
            ds.PhotometricInterpretation = "RGB"
            ds.PixelRepresentation = 0
            ds.add_new(0x00280006, "US", 0)
            ds.BitsStored = 8
            ds.file_meta = FileMetaDataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian  # type: ignore[attr-defined] # Reason: pydicom has that attr and we only use it for testing. # noqa: B950
            ds.is_little_endian = False
            ds.is_implicit_VR = False
            ds.save_as(filepath)

    @fixture
    def dicom_2dsource(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_2d(tmp_path)
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        return datasource

    @fixture
    def dicom_2dsource_window(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_2d_window(tmp_path)
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        return datasource

    @fixture
    def dicom_3dsource(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_3d(tmp_path)
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        return datasource

    @fixture
    def dicom_3dsource_wrong(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_3d_wrong_pixel_config(tmp_path)
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        return datasource

    @fixture
    def dicom_3dsource_3samples(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_3d_3_samples(tmp_path)
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        return datasource

    @fixture
    def dicom_3dsource_slo(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_2d(tmp_path, "SLO_IR_3d")
        self.dicom_files_3d(tmp_path, "OCT")
        datasource = DICOMSource(
            path=tmp_path,
            output_path=tmp_path,
            ophthalmology_args=OphthalmologyDataSourceArgs(),
        )
        return datasource

    @fixture
    def dicom_2d_3dsource(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_2d(tmp_path)
        self.dicom_files_3d(tmp_path)
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        return datasource

    def test_no_dicom_files_logs_warning(
        self, caplog: LogCaptureFixture, tmp_path: Path
    ) -> None:
        """Test warning is raised with no dcm files."""
        DICOMSource(path=tmp_path)
        assert (
            "Didn't detect any DICOM files in the provided directory that matched the "
            "provided criteria." in caplog.text
        )

    def test_get_data_unhashable_type(
        self, caplog: LogCaptureFixture, mocker: MockerFixture, tmp_path: Path
    ) -> None:
        """Test that get_data with unhashable type logs warning."""
        ds = DICOMSource(path=tmp_path)
        df = pd.DataFrame()
        df["test_col"] = [[1, 2, 3], [3, 4, 5]]
        mock_data = mocker.patch.object(DICOMSource, "_get_data")
        mock_data.return_value = df
        ds.get_values(["test_col"])
        assert "Found unhashable value type, skipping column test_col." in caplog.text

    def test_len(self, dicom_2dsource: DICOMSource) -> None:
        """Tests that __len__ magic method returns correct row count."""
        assert len(dicom_2dsource) == 5

    def test_get_data_2d_only(self, dicom_2dsource: DICOMSource) -> None:
        """Test get_data returns dataframe."""
        result = dicom_2dsource.get_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 14
        assert "Pixel Data" in result.columns
        assert len(result) == 5
        assert result["Number of Frames"].unique() == np.array([1])

    def test_get_data_2d_window(self, dicom_2dsource_window: DICOMSource) -> None:
        """Test get_data returns dataframe."""
        result = dicom_2dsource_window.get_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 17
        assert "Pixel Data" in result.columns
        assert len(result) == 5
        assert result["Number of Frames"].unique() == np.array([1])

    def test_get_data_3d_3samples(self, dicom_3dsource_3samples: DICOMSource) -> None:
        """Test get_data returns dataframe."""
        result = dicom_3dsource_3samples.get_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 19
        assert "Pixel Data 3" in result.columns
        assert len(result) == 5

    def test_get_data_wrong_no_bits_raisese_error(
        self, dicom_3dsource_wrong: DICOMSource
    ) -> None:
        """Test get_data raises error on wrong number of bits."""
        with pytest.raises(TypeError):
            dicom_3dsource_wrong.get_data()

    def test_get_data_3d_only(
        self, caplog: LogCaptureFixture, dicom_3dsource: DICOMSource
    ) -> None:
        """Test get_data returns dataframe."""
        result = dicom_3dsource.get_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 18  # 13 cols + 5 pixel arrays
        assert "Pixel Data 3" in result.columns
        assert len(result) == 5
        assert result["Number of Frames"].unique() == np.array([5])
        assert "Language Code Sequence" not in result.columns
        assert (
            "Cannot process sequence data, ignoring column Language Code Sequence"
            in caplog.text
        )

    def test_get_data_3d_w_slo(
        self, caplog: LogCaptureFixture, dicom_3dsource_slo: DICOMSource
    ) -> None:
        """Test get_data returns dataframe."""
        result = dicom_3dsource_slo.get_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 19  # 13 cols + 5 pixel arrays + slo column
        assert "Pixel Data 3" in result.columns
        assert len(result) == 5
        assert result["Number of Frames"].unique() == np.array([5])
        assert "Language Code Sequence" not in result.columns
        assert "SLO Image Data" in result.columns
        assert (
            "Cannot process sequence data, ignoring column Language Code Sequence"
            in caplog.text
        )

    def test_get_data_3d_only_include_slo_true_missing_slo(
        self, caplog: LogCaptureFixture, dicom_3dsource: DICOMSource
    ) -> None:
        """Test get_data returns dataframe."""
        dicom_3dsource.ophthalmology_args = OphthalmologyDataSourceArgs()
        result = dicom_3dsource.get_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 18  # 13 cols + 5 pixel arrays
        assert "Pixel Data 3" in result.columns
        assert len(result) == 5
        assert result["Number of Frames"].unique() == np.array([5])
        assert "Language Code Sequence" not in result.columns
        assert "SLO Image Data" not in result.columns
        assert (
            "Cannot process sequence data, ignoring column Language Code Sequence"
            in caplog.text
        )
        assert (
            "`include_slo` was set to True, but no corresponding SLO file found. "
            in caplog.text
        )

    def test_get_data_2d_3d_mix_error(self, dicom_2d_3dsource: DICOMSource) -> None:
        """Test get_data returns dataframe."""
        with pytest.raises(DataSourceError):
            dicom_2d_3dsource.get_data()

    def test_get_column(self, dicom_2dsource: DICOMSource) -> None:
        """Test get_column returns column."""
        result = cast(pd.Series, dicom_2dsource.get_column("Patient ID"))
        result = result.sort_values(ignore_index=True)
        for i in range(5):
            assert result[i] == f"ID {i}"

    def test_get_values(self, dicom_2dsource: DICOMSource) -> None:
        """Test get_column returns column."""
        result = cast(
            pd.Series,
            dicom_2dsource.get_values(
                ["Study Description", "Bits Stored", "Number of Frames"]
            ),
        )
        assert result["Bits Stored"] == np.array([8])
        assert result["Study Description"] == np.array(["Test"])
        assert result["Number of Frames"] == np.array([1])

    def test_get_dtypes(self, dicom_2dsource: DICOMSource) -> None:
        """Test get_dtypes works."""
        result = dicom_2dsource.get_dtypes()
        assert isinstance(result, dict)
        assert result["Samples per Pixel"] == pd.Int64Dtype()
        assert result["Number of Frames"] == pd.Int64Dtype()
        assert result["Rows"] == pd.Int64Dtype()
        assert result["Columns"] == pd.Int64Dtype()

    def test_multitable(self, dicom_2dsource: DICOMSource) -> None:
        """Test multi_table for DICOMSource."""
        assert not dicom_2dsource.multi_table

    def test_yield_data_2d(self, dicom_2dsource: DICOMSource) -> None:
        """Test yield_data for DICOMSource."""
        dicom_2dsource.partition_size = 2
        # There are 5 rows in the test data, so we should get 3 partitions
        for i, partition in enumerate(dicom_2dsource.yield_data()):
            # Asserting that the partition is a dataframe
            assert isinstance(partition, pd.DataFrame)
            if i == 2:  # Last partition
                # Asserting that the last partition has 1 row
                assert len(partition) == 1
            else:
                # Asserting that the other partitions have 2 rows
                assert len(partition) == 2

    def test_yield_data_cleanup_3d(self, dicom_3dsource: DICOMSource) -> None:
        """Test yield_data for DICOMSource with 3D images.

        3D images should be split into 2D images and cleaned up.
        """
        dicom_3dsource.partition_size = 2
        out_path = dicom_3dsource.out_path
        # There are 5 rows in the test data, so we should get 3 partitions
        for i, partition in enumerate(dicom_3dsource.yield_data()):
            # Asserting that the 5 3D images always remain and are untouched
            assert len([f for f in Path(out_path).iterdir() if f.is_file()]) == 5
            # Asserting that the partition is a dataframe
            assert isinstance(partition, pd.DataFrame)
            # Asserting that the number of temporary directories corresponds to the
            # number of rows in each partition. These are cleaned up after each
            # partition.
            num_temp_directories = len(
                [f for f in Path(out_path).iterdir() if not f.is_file()]
            )
            if i == 2:  # Last partition
                assert len(partition) == 1
                assert num_temp_directories == 1
            else:
                assert len(partition) == 2
                assert num_temp_directories == 2

        # Once the generator is exhausted, all temporary directories should be
        # cleaned up and we are left with just the 5 3D images.
        assert len([f for f in Path(out_path).iterdir()]) == 5

    def test_yield_data_raises_value_error(self, tmp_path: Path) -> None:
        """Test yield_data for DICOMSource when there is no data."""
        dicom_source = DICOMSource(path=tmp_path, out_path=tmp_path)
        with pytest.raises(ValueError, match="No files found to yield data from."):
            next(dicom_source.yield_data())

    def test_get_data_with_more_files_added(self, tmp_path: Path) -> None:
        """Tests the `get_data` method when more files are added to the source.

        This test is to ensure that the `get_data` method does not cache the
        source files and instead always returns the latest data.
        """
        self.dicom_files_2d(tmp_path)
        for path in tmp_path.iterdir():
            if path.is_file():
                path.rename(tmp_path / f"_{path.name}")
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        datasource.load_data()
        assert len(datasource.data) == 5
        # Add more files to the source
        self.dicom_files_2d(tmp_path)
        datasource.load_data()  # Reload the data
        assert len(datasource.data) == 10

    @pytest.mark.parametrize(
        "method", ["get_column", "get_data", "get_dtypes", "get_values"]
    )
    def test_data_is_not_reloaded_if_it_hasnt_changed(
        self, dicom_2dsource: DICOMSource, method: str, mocker: MockerFixture
    ) -> None:
        """Tests that the data is not reloaded if it hasn't changed.

        This test is to ensure that the `get_column`, `get_data`, `get_dtypes` and
        `get_values` methods do not reload the data if it is already loaded and
        hasn't changed.
        """
        dicom_2dsource.load_data()
        mock_get_data: Mock = mocker.patch.object(dicom_2dsource, "_get_data")
        kwargs: Dict[str, Any] = {}
        method_callable = getattr(dicom_2dsource, method)
        if method == "get_values":
            kwargs["col_names"] = ["Study Description"]
        elif method == "get_column":
            kwargs["col_name"] = "Study Description"

        method_callable(**kwargs)
        mock_get_data.assert_not_called()
