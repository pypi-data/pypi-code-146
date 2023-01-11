from io import StringIO

import pytest
import yaml

from w.services.technical.filesystem_service import FilesystemService
from w.services.technical.yaml_service import YamlService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestYamlService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.data = {
            "a value": "a data",
            "a list": [1, 12, 13, "string"],
            "a dict": {
                "key": "value",
                "key2": ["value", "valuebis"],
                "key3": {"dictk": "value"},
            },
        }

    """
    dump_to_mem_file
    """

    def test_dump_to_mem_file_with_success_return_stringio(self):
        """Ensure dump_to_mem_file succeed"""
        with open(self.get_datasets_dir("yaml/example.yml")) as f:
            data = yaml.safe_load(f)
            actual = YamlService.dump_to_mem_file(data)
            assert isinstance(actual, StringIO)
            assert data == yaml.safe_load(actual)

    """
    dump_to_file
    """

    def test_dump_to_file_with_success_return_none(self):
        """Ensure method succeed"""
        filename = self.get_sandbox_dir("simple_dump.yml")
        assert YamlService.dump_to_file(self.data, filename) is None
        self.assert_file_exists(filename)
        self.assert_equals_resultset(FilesystemService.read_file(filename).split("\n"))

    """
    load
    """

    def test_load_with_file_not_exists_raise_runtime_error(self):
        """Ensure load unknown file raise RuntimeError"""
        with pytest.raises(RuntimeError, match="unknown.yml does not exists"):
            YamlService.load_from_file("unknown.yml")

    def test_load_with_success_return_dict(self):
        """Ensure load succeed"""
        self.assert_equals_resultset(
            YamlService.load_from_file(self.get_datasets_dir("yaml/example.yml"))
        )

    """
    check_is_valid
    """

    def test_check_is_valid_with_no_valid_yaml_raise_runtime_error(self):
        """Ensure check invalid yaml raise RuntimeError"""
        invalid_yaml = FilesystemService.read_file(
            self.get_datasets_dir("yaml/invalid_yaml.yml")
        )

        match = "Line 3, column 24: could not find expected ':'"
        with pytest.raises(RuntimeError, match=match):
            YamlService.check_is_valid(yaml_stream=invalid_yaml)

    def test_check_is_valid_with_success_return_dict(self):
        """Ensure check valid yaml, load yaml"""
        valid_yaml = FilesystemService.read_file(
            self.get_datasets_dir("yaml/example.yml")
        )

        self.assert_equals_resultset(YamlService.check_is_valid(yaml_stream=valid_yaml))

    def test_check_is_valid_with_invalid_date_raise_runtime_error(self):
        """Ensure check invalid date raises RuntimeError"""
        yaml_with_invalid_date = FilesystemService.read_file(
            self.get_datasets_dir("yaml/yaml_with_invalid_date.yml")
        )

        match = "month must be in 1..12"
        with pytest.raises(RuntimeError, match=match):
            YamlService.check_is_valid(yaml_stream=yaml_with_invalid_date)
