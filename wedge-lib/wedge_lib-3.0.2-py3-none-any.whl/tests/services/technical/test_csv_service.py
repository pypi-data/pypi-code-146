import copy

import pytest
import pandas
from w.services.technical.csv_service import CsvService
from w.services.technical.models.csv_options import CsvOptions
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestCsvService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.filename = cls.get_datasets_dir("csv/simple.csv")
        cls.filename_with_semi_colon_separator = cls.get_datasets_dir(
            "csv/simple_with_semi_colon.csv"
        )
        cls.mapping = {"colA": "columnA", "colB": "columnB", "colC": "columnC"}
        cls.rows_to_dump = [
            {
                "colA": "row 1 data, columnA",
                "colB": "row 1 data; columnB",
                "colC": "row 1 data\tcolumnC éàç",
            },
            {
                "colA": "row 2 data, columnA",
                "colB": "row 2 data, columnB",
                "colC": "row 2 data, columnC",
            },
        ]

    """
    is_csv
    """

    def test_is_csv_with_no_csv_file_return_false(self):
        """Ensure method return False on no csv file"""
        files = ["toto.txt", "csv.txt", "csv.csv.gz"]
        for file in files:
            assert CsvService.is_csv(file) is False

    def test_is_csv_with_success_return_true(self):
        """Ensure method return True on csv file"""
        files = ["toto.csv", "csv.csv"]
        for file in files:
            assert CsvService.is_csv(file) is True

    """
    load
    """

    def test_load_with_invalid_csv_raise_runtime_error(self):
        """Ensure method raise runtime error if file is not csv"""
        filename = self.get_datasets_dir("excel/Excel2007File.xlsx")
        match = "Excel2007File.xlsx is not a csv file"
        options = CsvOptions(self.mapping)
        with pytest.raises(RuntimeError, match=match):
            CsvService.load(filename, options)

    def test_load_with_invalid_header_raise_runtime_error(self):
        """Ensure method raise runtime error if header is false"""
        mapping = self.mapping.copy()
        mapping["colWrongA"] = mapping.pop("colA")
        match = (
            "incorrect or missing header, expected 'colB,colC,colWrongA'"
            " got 'colA,colB,colC'"
        )
        options = CsvOptions(mapping)
        with pytest.raises(RuntimeError, match=match):
            CsvService.load(self.filename, options)

    def test_load_with_none_options_return_attribute_error(self):
        """Ensure method raise error if no options passed"""
        match = "NoneType' object has no attribute 'field_delimiter"
        with pytest.raises(AttributeError, match=match):
            CsvService.load(self.filename_with_semi_colon_separator, None)

    def test_load_with_different_delimiter_return_list(self):
        """Ensure method succeed with separator different from comma"""
        options = CsvOptions(self.mapping, ";")
        self.assert_equals_resultset(
            CsvService.load(self.filename_with_semi_colon_separator, options)
        )

    def test_load_with_success_return_list(self):
        """Ensure method succeed"""
        options = CsvOptions(self.mapping)
        self.assert_equals_resultset(CsvService.load(self.filename, options))

    """
    dump
    """

    @staticmethod
    def _assert_line_terminator(filename: str, expected: str):
        with open(filename) as f:
            next(f)
            assert f.newlines == expected

    @staticmethod
    def _assert_columns(dataframe: pandas.DataFrame, expected: list):
        assert list(dataframe.columns) == expected

    @staticmethod
    def _assert_rows(dataframe: pandas.DataFrame, expected: list):
        for index, row in enumerate(expected):
            assert list(dataframe.values[index])

    def test_dump_with_empty_rows_raise_runtime_error(
        self,
    ):
        """Ensure method raises a RuntimeError exception if provided rows is an empty
        list"""
        self.clean_sandbox()
        filename = self.get_sandbox_dir("test_dump.csv")
        match = "Unable to dump data to csv file : invalid provided rows"
        with pytest.raises(RuntimeError, match=match):
            CsvService.dump(filename, [])

    def test_dump_with_invalid_items_in_rows_raise_runtime_error(
        self,
    ):
        """Ensure method raises a RuntimeError exception if provided rows is a list
        containing at least one item with an unexpected type"""
        self.clean_sandbox()
        filename = self.get_sandbox_dir("test_dump.csv")
        rows = copy.deepcopy(self.rows_to_dump)
        rows.insert(1, "invalid item")
        match = "Unable to dump data to csv file : invalid provided rows"
        with pytest.raises(RuntimeError, match=match):
            CsvService.dump(filename, rows)

    def test_dump_with_invalid_file_path_raise_runtime_error(
        self,
    ):
        """Ensure method raises a RuntimeError exception if provided filename cannot be
        created as path does not exist"""
        self.clean_sandbox()
        # filename = self.get_sandbox_dir("test_dump.csv")
        filename = "/tmp/non-existent_dir/test_dump.csv"
        match = "/non-existent_dir does not exist"
        with pytest.raises(RuntimeError, match=match):
            CsvService.dump(filename, self.rows_to_dump)

    def test_dump_with_semicolon_delimiter_and_mapping_columns_success_return_none(
        self,
    ):
        """Ensure method succeeds and actually uses a semicolon to delimiter fields in
        each row and uses provided mapping columns to rename columns"""
        self.clean_sandbox()
        filename = self.get_sandbox_dir("test_dump.csv")
        options = CsvOptions(self.mapping, ";")
        CsvService.dump(filename, self.rows_to_dump, options)
        dataframe = pandas.read_csv(filename, sep=";")
        self._assert_line_terminator(filename, "\n")
        self._assert_columns(dataframe, list(self.mapping.values()))
        self._assert_rows(dataframe, self.rows_to_dump)

    def test_dump_with_default_comma_delimiter_and_mapping_columns_success_return_none(
        self,
    ):
        """Ensure method succeeds and actually uses the default character (a comma) to
        delimiter fields in each row and uses provided mapping columns to rename
        columns"""
        self.clean_sandbox()
        filename = self.get_sandbox_dir("test_dump.csv")
        options = CsvOptions(self.mapping)
        CsvService.dump(filename, self.rows_to_dump, options)
        dataframe = pandas.read_csv(filename, sep=",")
        self._assert_line_terminator(filename, "\n")
        self._assert_columns(dataframe, list(self.mapping.values()))
        self._assert_rows(dataframe, self.rows_to_dump)

    def test_dump_with_default_options_success_return_none(
        self,
    ):
        """Ensure method succeeds and actually uses the default character (a comma) to
        delimiter fields in each row and does not rename columns"""
        self.clean_sandbox()
        filename = self.get_sandbox_dir("test_dump.csv")
        # doesn't really make sense but... robustness !
        options = CsvOptions()
        CsvService.dump(filename, self.rows_to_dump, options)
        dataframe = pandas.read_csv(filename, sep=",")
        self._assert_line_terminator(filename, "\n")
        self._assert_columns(dataframe, list(self.rows_to_dump[0].keys()))
        self._assert_rows(dataframe, self.rows_to_dump)

    def test_dump_with_no_options_success_return_none(
        self,
    ):
        """Ensure method succeeds and actually uses the default character (a comma) to
        delimiter fields in each row and does not rename columns"""
        self.clean_sandbox()
        filename = self.get_sandbox_dir("test_dump.csv")
        CsvService.dump(filename, self.rows_to_dump)
        dataframe = pandas.read_csv(filename, sep=",")
        self._assert_line_terminator(filename, "\n")
        self._assert_columns(dataframe, list(self.rows_to_dump[0].keys()))
        self._assert_rows(dataframe, self.rows_to_dump)

    def test_dump_with_specific_line_terminator_success_return_none(
        self,
    ):
        """Ensure method succeeds and actually uses the specified line terminator"""
        self.clean_sandbox()
        filename = self.get_sandbox_dir("test_dump.csv")
        line_terminator = "\r\n"
        options = CsvOptions(line_terminator=line_terminator)
        CsvService.dump(filename, self.rows_to_dump, options)
        dataframe = pandas.read_csv(filename, sep=",")
        self._assert_line_terminator(filename, line_terminator)
        self._assert_columns(dataframe, list(self.rows_to_dump[0].keys()))
        self._assert_rows(dataframe, self.rows_to_dump)
