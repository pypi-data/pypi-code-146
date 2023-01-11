# type: ignore

import os
from unittest.mock import Mock, mock_open, patch

import boto3
import smart_open

import anyscale
from anyscale.utils.runtime_env import override_runtime_env_for_local_working_dir


def test_override_no_workspace():
    local_test_zip_path = "file://test.zip"
    runtime_env = {"working_dir": local_test_zip_path}
    modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
    assert modified_runtime_env["working_dir"] == local_test_zip_path


def test_override_upload_no_workspace():
    runtime_env = {
        "working_dir": "job-services-cuj-examples",
        "upload_path": "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job",
    }
    boto_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.multiple(
        os, makedirs=Mock()
    ), patch("builtins.open", mock_open()), patch.multiple(
        boto3, client=boto_mock
    ), patch.multiple(
        smart_open, open=Mock()
    ):
        modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
        assert modified_runtime_env["working_dir"].startswith(
            "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job"
        )
        assert modified_runtime_env["working_dir"].endswith(".zip")


def test_override_upload_with_workspace():
    runtime_env = {
        "working_dir": "job-services-cuj-examples",
        "upload_path": "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job",
    }
    boto_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ,
        {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "Test_workspace_id"},
        clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "builtins.open", mock_open()
    ), patch.multiple(
        boto3, client=boto_mock
    ), patch.multiple(
        smart_open, open=Mock()
    ):
        modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
        assert modified_runtime_env["working_dir"].startswith("file:///efs/jobs")
        assert modified_runtime_env["working_dir"].endswith(".zip")


def test_runtime_env_override_to_efs_workspace():
    runtime_env = {"working_dir": "file://test.zip"}
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ,
        {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "Test_workspace_id"},
        clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "urllib.request", urlretrieve=Mock()
    ), patch(
        "builtins.open", mock_open()
    ):
        modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
        assert modified_runtime_env["working_dir"].startswith("file:///efs")


def test_local_runtime_env_override_to_efs_job():
    runtime_env = {"working_dir": "file://test.zip"}
    test_job_id = "Test_job_id"
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID": test_job_id}, clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "urllib.request", urlretrieve=Mock()
    ), patch(
        "builtins.open", mock_open()
    ):
        modified_runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        assert (
            modified_runtime_env["working_dir"]
            == f"/efs/jobs/{test_job_id}/working_dir.zip"
        )


def test_s3_runtime_env_override_to_efs_job():
    runtime_env = {
        "working_dir": "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job/_anyscale_pkg_00216a215e75dff900a133c9ac9c764a.zip"
    }
    test_job_id = "Test_job_id"
    boto_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID": test_job_id}, clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "builtins.open", mock_open()
    ), patch.multiple(
        boto3, client=boto_mock
    ):
        modified_runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        boto_mock.assert_called_once_with("s3")
        assert (
            modified_runtime_env["working_dir"]
            == f"/efs/jobs/{test_job_id}/working_dir.zip"
        )


def test_https_runtime_env_override_to_efs_job():
    runtime_env = {
        "working_dir": "https://github.com/anyscale/docs_examples/archive/refs/heads/main.zip"
    }
    test_job_id = "Test_job_id"
    urlretrieve_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID": test_job_id}, clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "builtins.open", mock_open()
    ), patch.multiple(
        "urllib.request", urlretrieve=urlretrieve_mock
    ):
        modified_runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        urlretrieve_mock.assert_called_once()
        assert (
            modified_runtime_env["working_dir"]
            == f"/efs/jobs/{test_job_id}/working_dir.zip"
        )
