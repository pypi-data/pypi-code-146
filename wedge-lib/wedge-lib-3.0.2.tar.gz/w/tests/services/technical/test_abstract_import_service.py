import pytest
import re

from w.services.technical.abstract_import_service import AbstractImportService
from w.tests.helpers import service_test_helper
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestAbstractImportService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.mock_abstract_methods = [
            {
                "service": AbstractImportService,
                "method_name": "_list_mapping_columns",
                "return_value": None,
            },
            {
                "service": AbstractImportService,
                "method_name": "_validate",
                "return_value": ("validated_datas", "validation_errors"),
            },
            {
                "service": AbstractImportService,
                "method_name": "_import",
                "return_value": None,
            },
            {
                "service": AbstractImportService,
                "method_name": "_get_import_report",
                "return_value": "import_report",
            },
        ]
        cls.csv_mapping = {"colA": "columnA", "colB": "columnB", "colC": "columnC"}
        cls.excel_mapping = {"header1": "colA", "header2": "colB", "header3": "colC"}

    """
    import_file
    """

    def test_import_file_with_unsupported_format_raise_runtime_exception(self):
        """Ensure we cannot import unsupported file format"""
        match = "Format file1.txt not supported"
        with pytest.raises(RuntimeError, match=match):
            AbstractImportService.import_file(
                self.get_datasets_dir("filesystem/dir1/file1.txt")
            )

    def test_import_file_with_csv_return_data(self):
        """Ensure we can import csv file"""
        self.mock_abstract_methods[0]["return_value"] = self.csv_mapping
        with service_test_helper.mock_services(self.mock_abstract_methods) as m:
            import_report = AbstractImportService.import_file(
                self.get_datasets_dir("csv/simple.csv")
            )
        assert import_report == "import_report"
        self.assert_equals_resultset(self.get_mock_calls(m))

    def test_import_file_with_csv_and_bad_format_delimiter_return_runtime_error(self):
        """Ensure method raise error if a bad delimiter is passed"""
        self.mock_abstract_methods[0]["return_value"] = self.csv_mapping
        match = re.escape(
            "incorrect or missing header, expected 'colA,colB,colC' got 'colA;colB;colC'"  # noqa
        )
        with service_test_helper.mock_services(self.mock_abstract_methods):
            with pytest.raises(RuntimeError, match=match):
                AbstractImportService.import_file(
                    self.get_datasets_dir("csv/simple_with_semi_colon.csv")
                )

    def test_import_file_with_csv_and_specific_delimiter_return_data(self):
        """Ensure we can import csv file with specific delimiter"""
        self.mock_abstract_methods[0]["return_value"] = self.csv_mapping
        with service_test_helper.mock_services(self.mock_abstract_methods) as m:
            import_report = AbstractImportService.import_file(
                self.get_datasets_dir("csv/simple_with_semi_colon.csv"), delimiter=";"
            )
        assert import_report == "import_report"
        self.assert_equals_resultset(self.get_mock_calls(m))

    def test_import_file_with_excel_return_data(self):
        """Ensure we can import csv file"""
        self.mock_abstract_methods[0]["return_value"] = self.excel_mapping
        with service_test_helper.mock_services(self.mock_abstract_methods) as m:
            import_report = AbstractImportService.import_file(
                self.get_datasets_dir("excel/Excel2010.xlsx"),
                context={"context_key_1": "context_value_1"},
            )
        assert import_report == "import_report"
        self.assert_equals_resultset(self.get_mock_calls(m))

    def test_import_file_with_sheet_name_return_data(self):
        """Ensure we can import Excel file with specific sheet name"""
        excel_mapping = {
            "header1_sheet2": "columnA",
            "header2_sheet2": "columnB",
            "header3_sheet2_with_space": "columnC",
        }

        self.mock_abstract_methods[0]["return_value"] = excel_mapping
        with service_test_helper.mock_services(self.mock_abstract_methods) as m:
            AbstractImportService.sheet_name = "Sheet_2"
            import_report = AbstractImportService.import_file(
                self.get_datasets_dir("excel/Excel2010.xlsx")
            )
        assert import_report == "import_report"
        self.assert_equals_resultset(self.get_mock_calls(m))
