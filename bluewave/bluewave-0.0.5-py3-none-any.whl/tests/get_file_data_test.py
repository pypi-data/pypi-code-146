import pytest

from bluewave.compare_pdfs import get_version
from bluewave.src.get_file_data import (
    page_skip_conditions,
    block_skip_conditions,
    is_compatible,
    get_file_data,
)
import os
from pathlib import Path


@pytest.mark.parametrize(
    "text, expected_output",
    [
        ("", False),
        ("FORM FDA ", True),
        ("Safety Data Sheet", True),
        ("PAPERWORK REDUCTION ACT", True),
    ],
)
def test_page_skip_conditions(text, expected_output):
    """Test Page Skip Conditions"""
    actual_output = page_skip_conditions(text)
    assert any(actual_output) == expected_output


@pytest.mark.parametrize(
    "text, expected_output",
    [("", True), ("510(k)", True), ("Fax:", True), ("phone", False)],
)
def test_block_skip_conditions(text, expected_output):
    """Test Block Skip Conditions"""
    actual_output = block_skip_conditions(text)
    assert any(actual_output) == expected_output


@pytest.mark.parametrize(
    "text_1, text_2, expected_output",
    [("1.1.1", "1.1.1", True), ("1.1.1", "1.2.1", False)],
)
def test_is_compatible(text_1, text_2, expected_output):
    """Test is compatible"""
    actual_output = is_compatible(text_1, text_2)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "file_name, regen_cache_flag",
    [
        ("sample_file_1.pdf", True),
        ("sample_file_1.pdf", False),
        ("sample_file_2.pdf", True),
        ("sample_file_2.pdf", False),
    ],
)
def test_get_file_data(file_name, regen_cache_flag):
    """Test get file data"""
    package_dir = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
    sample_files_folder_path = os.path.join(package_dir, "sample_files")
    file_name = os.path.join(sample_files_folder_path, file_name)
    actual_output = get_file_data(file_name, regen_cache_flag, get_version())
    assert "blocks" in actual_output
    assert "full_text" in actual_output
    assert "image_hashes" in actual_output
    assert "n_pages" in actual_output
    assert "path_to_file" in actual_output
    assert "filename" in actual_output
