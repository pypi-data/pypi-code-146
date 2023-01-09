import os

import pytest

from bluewave.compare_pdfs import compare_pdf_files, get_version
from bluewave.tests.constants import (
    EXPECTED_OUTPUT_1,
    EXPECTED_OUTPUT_2,
    EXPECTED_OUTPUT_3,
)
from pathlib import Path


@pytest.mark.parametrize(
    "filenames, expected_output",
    [
        (
            ["sample_file_1.pdf", "sample_file_1.pdf"],
            EXPECTED_OUTPUT_1,
        ),
        (
            ["sample_file_2.pdf", "sample_file_2.pdf"],
            EXPECTED_OUTPUT_2,
        ),
        (
            ["sample_file_1.pdf", "sample_file_2.pdf"],
            EXPECTED_OUTPUT_3,
        ),
    ],
)
def test_compare_pdf_files(filenames, expected_output):
    """Test Compare pdf files"""
    package_dir = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
    sample_files_folder_path = os.path.join(package_dir, "sample_files")
    filenames = [
        os.path.join(sample_files_folder_path, filename) for filename in filenames
    ]
    actual_output = compare_pdf_files(filenames, regen_cache=True, pretty_print=True)
    keys_to_pop = ["time", "elapsed_time_sec", "pages_per_second"]
    for key in keys_to_pop:
        actual_output.pop(key, None)
    for index, file in enumerate(actual_output["files"]):
        file.pop("path_to_file")
        actual_output["files"][index] = file
    assert actual_output == expected_output


def test_get_version():
    """Test get version"""
    actual_output = get_version()
    assert actual_output != ""
