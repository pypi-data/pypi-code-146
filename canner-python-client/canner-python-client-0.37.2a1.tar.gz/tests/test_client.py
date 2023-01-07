import csv
import pytest
import logging
import json_lines
import numpy as np
import pandas as pd
from PIL.PngImagePlugin import PngImageFile
from canner.client import Client
from .config import TestConfig
from uuid import uuid4

logger = logging.getLogger("test_client")


logger.info(
    {
        "endpoint": TestConfig.ENDPOINT,
        "workspaceId": TestConfig.WORKSPACE_ID,
        "secret": TestConfig.JUPYTER_SECRET,
        "token": TestConfig.PERSONAL_ACCESS_TOKEN,
    }
)


def test_should_find_file_when_list_after_put_file_to_remote(
    canner_client: Client, binary_filename: str
):
    # The list_file response will include directory '/'
    expected = f"/{binary_filename}"
    canner_client.put_binary(binary_filename, "")
    files = canner_client.list_file()
    assert expected in files, f"{expected} should exist in remote files when list"


def test_should_find_filepath_when_list_after_put_filepath_to_remote(
    canner_client: Client, binary_filepaths: str
):
    expected = set(binary_filepaths)
    # Act
    for file in binary_filepaths:
        canner_client.put_binary(file, "")
    files = canner_client.list_file()
    # Assert
    assert set(files) == expected, f"{expected} should exist in remote files when list"


def test_should_be_empty_after_delete_existed_file(canner_client: Client):
    random_filename = str(uuid4().hex)
    expected = f"/{random_filename}"
    canner_client.put_binary(random_filename, "")
    canner_client.delete_file(random_filename)
    files = canner_client.list_file()
    assert expected not in files, f"should not exist any files in remote when list"


@pytest.mark.parametrize(
    "input_file_sample",
    [
        (TestConfig.SAMPLE_01_MBCS_CP950_CSV),
        (TestConfig.SAMPLE_02_UTF8_BOM_CSV),
        (TestConfig.SAMPLE_03_CP950_CSV),
        (TestConfig.SAMPLE_04_UTF8_CSV),
    ],
)
def test_should_upload_success_when_put_binary(
    canner_client: Client, binary_filename: str, input_file_sample: str
):
    with open(input_file_sample, "rb") as file:
        data = file.read()
        result = canner_client.put_binary(binary_filename, data)
        assert result is True, "Should upload file"


@pytest.mark.parametrize(
    "input_file_sample",
    [
        (TestConfig.SAMPLE_01_MBCS_CP950_CSV),
        (TestConfig.SAMPLE_02_UTF8_BOM_CSV),
        (TestConfig.SAMPLE_03_CP950_CSV),
        (TestConfig.SAMPLE_04_UTF8_CSV),
    ],
)
def test_should_data_correct_when_get_binary(
    canner_client: Client, binary_filename: str, input_file_sample: str
):
    with open(input_file_sample, "rb") as file:
        data = file.read()
        canner_client.put_binary(binary_filename, data)
        binary = canner_client.get_binary(binary_filename)
        assert binary == data, "Uploaded file should be same as file"


@pytest.mark.parametrize(
    "input_file_sample,encoding",
    [
        (TestConfig.SAMPLE_01_MBCS_CP950_CSV, "cp950"),
        (TestConfig.SAMPLE_02_UTF8_BOM_CSV, "utf8"),
        (TestConfig.SAMPLE_03_CP950_CSV, "cp950"),
        (TestConfig.SAMPLE_04_UTF8_CSV, "utf8"),
    ],
)
def test_should_upload_success_when_put_csv(
    canner_client: Client, csv_filename: str, input_file_sample: str, encoding: str
):
    with open(input_file_sample, encoding=encoding) as file:
        spamreader = csv.reader(file)
        uploaded_csv = [row for row in spamreader]
        result = canner_client.put_csv(csv_filename, uploaded_csv)
        assert result is True, "Should upload csv"


@pytest.mark.parametrize(
    "input_file_sample, encoding",
    [
        (TestConfig.SAMPLE_01_MBCS_CP950_CSV, "cp950"),
        (TestConfig.SAMPLE_02_UTF8_BOM_CSV, "utf8"),
        (TestConfig.SAMPLE_03_CP950_CSV, "cp950"),
        (TestConfig.SAMPLE_04_UTF8_CSV, "utf8"),
    ],
)
def test_should_data_correct_when_get_csv(
    canner_client: Client, csv_filename: str, input_file_sample: str, encoding: str
):
    with open(input_file_sample, encoding=encoding) as file:
        spamreader = csv.reader(file)
        uploaded_csv = [row for row in spamreader]
        canner_client.put_csv(csv_filename, uploaded_csv)
        downloaded_csv = canner_client.get_csv(csv_filename)
        assert type(downloaded_csv) is list, "csv should be a list"
        assert uploaded_csv == downloaded_csv, "Uploaded file should be same as file"


@pytest.mark.parametrize(
    "input_file_sample,encoding",
    [
        (TestConfig.SAMPLE_01_MBCS_CP950_CSV, "cp950"),
        (TestConfig.SAMPLE_02_UTF8_BOM_CSV, "utf8"),
        (TestConfig.SAMPLE_03_CP950_CSV, "cp950"),
        (TestConfig.SAMPLE_04_UTF8_CSV, "utf8"),
    ],
)
def test_should_data_correct_when_get_panda_csv(
    canner_client: Client, csv_filename: str, input_file_sample: str, encoding: str
):
    uploaded_csv = pd.read_csv(input_file_sample, encoding=encoding)
    canner_client.put_csv(csv_filename, uploaded_csv)
    downloaded_csv = canner_client.get_pandas_csv(csv_filename)
    assert isinstance(downloaded_csv, pd.DataFrame), "should get data frame"
    assert uploaded_csv.equals(downloaded_csv), "Uploaded file should be same as file"


def test_should_upload_success_when_put_json(
    canner_client: Client, json_filename: str
):
    with open(TestConfig.SAMPLE_JSON) as file:
        spamreader = json_lines.reader(file)
        upload_json = [row for row in spamreader]
        result = canner_client.put_json(json_filename, upload_json)
        assert result is True, "Should upload json"


def test_should_data_correct_when_get_json(
    canner_client: Client, json_filename: str
):
    with open(TestConfig.SAMPLE_JSON) as file:
        spamreader = json_lines.reader(file)
        upload_json = [row for row in spamreader]
        canner_client.put_json(json_filename, upload_json)
        downloaded_json = canner_client.get_json(json_filename)
        assert type(downloaded_json) is list, "json should be a list"
        assert upload_json == downloaded_json, "Uploaded file should be same as file"


def test_should_be_correct_size_when_get_pil_image(
    canner_client: Client, png_filename: str
):
    with open(TestConfig.SAMPLE_IMAGE, "rb") as file:
        data = file.read()
        canner_client.put_binary(png_filename, data)

        pil_image = canner_client.get_pil_image(png_filename)
        assert isinstance(pil_image, PngImageFile), "Should be PngImageFile"
        assert pil_image.height is 256, "height should be 256"
        assert pil_image.width is 256, "width should be 256"


def test_should_be_correct_size_when_get_np_image(
    canner_client: Client, png_filename: str
):
    with open(TestConfig.SAMPLE_IMAGE, "rb") as file:
        data = file.read()
        canner_client.put_binary(png_filename, data)

        np_image = canner_client.get_np_image(png_filename)
        assert isinstance(np_image, np.ndarray), "Should be ndarray"
        assert np_image.shape[0] is 256, "height should be 256"
        assert np_image.shape[1] is 256, "width should be 256"
