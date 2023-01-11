import datetime
from decimal import Decimal

import pytest

from w.services.technical.filesystem_service import FilesystemService
from w.services.technical.json_service import JsonService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestJsonService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.no_dumpable_data = {
            "str": "string",
            "int": 15,
            "float": 18.2,
            "decimal": Decimal(11.115),
            "datetime": datetime.datetime(2018, 7, 7, 12, 15, 35),
            "date": datetime.date(2018, 7, 7),
            "bytes": b"a bytes text a translate",
            "tuple": ("string", Decimal(11.5)),
            "list": [datetime.datetime(2018, 7, 7, 12, 15, 35), Decimal(11.115)],
        }

        cls.dumpable_data = {
            "a value": "a data",
            "a list": [1, 12, 13, "string"],
            "a dict": {"key": "value", "key2": ["value", "valuebis"]},
        }
        cls.valid_json = (
            '{"menu":{"id":"file","value":"File","popup":{"menuitem":[{"value":"New",'
            '"onclick":"CreateNewDoc()"},{"value":"Open","onclick":"OpenDoc()"},'
            '{"value":"Close","onclick":"CloseDoc()"}]}}}'
        )

    def setup_method(self):
        JsonService.clear()
        self.clean_sandbox()

    """
    to_json_dumpable
    """

    def test_json_dumpable_with_success_return_dict(self):
        """Ensure method succeed on dict"""
        self.assert_equals_resultset(
            JsonService.to_json_dumpable(self.no_dumpable_data)
        )

    """
    dump_to_file
    """

    def test_dump_to_file_with_success_return_none(self):
        """Ensure method succeed"""
        filename = self.get_sandbox_dir("simple_dump.json")
        assert JsonService.dump_to_file(self.dumpable_data, filename) is None
        self.assert_file_exists(filename)
        self.assert_equals_resultset(FilesystemService.read_file(filename))

    def test_dump_to_file_with_human_readable_return_none(self):
        """Ensure method succeed with human readable option"""
        filename = self.get_sandbox_dir("simple_dump.json")
        assert (
            JsonService.dump_to_file(self.dumpable_data, filename, human_readable=True)
            is None
        )
        self.assert_file_exists(filename)
        self.assert_equals_resultset(FilesystemService.read_file(filename))

    """
    load_from_file
    """

    def test_load_with_file_not_exists_raise_runtime_error(self):
        """Ensure load unknown file raise RuntimeError"""
        with pytest.raises(RuntimeError, match="unknown.json does not exists"):
            JsonService.load_from_file("unknown.json")

    def test_load_from_file_with_success_return_dict(self):
        """Ensure load json file succeed"""
        filename = self.get_datasets_dir("json/example.json")
        self.assert_equals_resultset(JsonService.load_from_file(filename))

    """
    load_from_str
    """

    def test_load_from_str_with_success_return_dict(self):
        """Ensure method succeed"""
        self.assert_equals_resultset(JsonService.load_from_str(self.valid_json))

    """
    is_valid
    """

    def test_is_valid_with_no_valid_json_return_false(self):
        data = "]invalid json}"
        assert not JsonService.is_valid(data)

    def test_is_valid_with_success_return_true(self):
        assert JsonService.is_valid(self.valid_json)
