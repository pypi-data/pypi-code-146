import pytest
from pathlib import Path
from akerbp.mlops.core.config import read_project_settings
from akerbp.mlops.core.exceptions import MissingMetadataError


def test_single_model_all_required_fields_no_exception_raised():
    yaml_file = Path("test/test_settings/single_model_all_required_fields.yaml")
    try:
        read_project_settings(yaml_file=yaml_file)
    except MissingMetadataError as exc:
        raise AssertionError(f"Settings file raised an exception {exc}") from None


def test_multiple_models_all_required_fields_no_exception_raised():
    yaml_file = Path("test/test_settings/multiple_models_all_required_fields.yaml")
    try:
        read_project_settings(yaml_file=yaml_file)
    except MissingMetadataError as exc:
        raise AssertionError(f"Settings file raised an exception {exc}") from None


def test_single_model_missing_field_throws_exception():
    yaml_file = Path("test/test_settings/single_model_missing_field.yaml")
    with pytest.raises(MissingMetadataError):
        read_project_settings(yaml_file=yaml_file)


def test_single_model_missing_petrel_field_throws_exception():
    yaml_file = Path("test/test_settings/single_model_missing_petrel_field.yaml")
    with pytest.raises(MissingMetadataError):
        read_project_settings(yaml_file=yaml_file)


def test_multiple_models_one_with_missing_field_throws_exception():
    yaml_file = Path("test/test_settings/multiple_models_missing_field.yaml")
    with pytest.raises(MissingMetadataError):
        read_project_settings(yaml_file=yaml_file)
