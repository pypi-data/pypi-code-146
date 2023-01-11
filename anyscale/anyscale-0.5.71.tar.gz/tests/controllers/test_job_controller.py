import json
import os
from pathlib import Path
import tempfile
import time
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple, Type
from unittest.mock import MagicMock, Mock, mock_open, patch

from aiohttp import ClientResponseError, ClientSession, WSMsgType
from asynctest import CoroutineMock
import click
import pytest
import yaml

from anyscale.client.openapi_client.models.create_internal_production_job import (
    CreateInternalProductionJob,
)
from anyscale.client.openapi_client.models.log_filter import LogFilter
from anyscale.client.openapi_client.models.production_job_config import (
    ProductionJobConfig,
)
from anyscale.controllers.job_controller import (
    _working_dir_is_remote_uri,
    JobConfig,
    JobController,
    LogProvider,
    LogsLogger,
    MiniJobRun,
)
from anyscale.sdk.anyscale_client.models.compute_template import ComputeTemplate
from anyscale.util import PROJECT_NAME_ENV_VAR


CONDA_DICT = {"dependencies": ["pip", {"pip": ["pip-install-test==0.5"]}]}
PIP_LIST = ["requests==1.0.0", "pip-install-test"]
ENV_VARS_DICT = {"TEST_ENV_VAR": "test_value"}


class FakeLogger(LogsLogger):
    logs: List[str] = []

    def open_block(self, *args, **kwargs,) -> None:
        pass

    def log(self, msg: str):
        self.logs.append(msg)
        print(msg)


@pytest.fixture
def test_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir)
        subdir = path / "subdir"
        subdir.mkdir(parents=True)
        requirements_file = subdir / "requirements.txt"
        with requirements_file.open(mode="w") as f:
            print("\n".join(PIP_LIST), file=f)

        good_conda_file = subdir / "good_conda_env.yaml"
        with good_conda_file.open(mode="w") as f:
            yaml.dump(CONDA_DICT, f)

        bad_conda_file = subdir / "bad_conda_env.yaml"
        with bad_conda_file.open(mode="w") as f:
            print("% this is not a YAML file %", file=f)

        old_dir = os.getcwd()
        os.chdir(tmp_dir)
        yield subdir, requirements_file, good_conda_file, bad_conda_file
        os.chdir(old_dir)


@pytest.fixture
def patch_jobs_anyscale_api_client(base_mock_anyscale_api_client: Mock):
    base_mock_anyscale_api_client.get_cluster_environment_build = Mock(
        return_value=Mock(result=Mock(status="succeeded"))
    )
    with patch.multiple(
        "anyscale.cluster_env",
        get_auth_api_client=Mock(
            return_value=Mock(anyscale_api_client=base_mock_anyscale_api_client)
        ),
    ):
        yield


@pytest.mark.parametrize("workspace_id", [None, "test_workspace_id"])
def test_generate_config_from_entrypoint(
    mock_auth_api_client, workspace_id: Optional[str]
):
    mock_logger = Mock()
    job_controller = JobController(log=mock_logger)
    entrypoint = ["python", "test.py"]
    name = "test_name"
    description = "test_description"

    mock_get_default_cluster_compute = Mock(
        return_value=Mock(id="mock_compute_config_id")
    )

    mock_validate_successful_build = Mock()
    mock_get_default_cluster_env_build = Mock(return_value=Mock(id="mock_build_id"))
    with patch.multiple(
        "anyscale.controllers.job_controller",
        get_default_cluster_compute=mock_get_default_cluster_compute,
        validate_successful_build=mock_validate_successful_build,
        get_default_cluster_env_build=mock_get_default_cluster_env_build,
    ):
        job_config = job_controller.generate_config_from_entrypoint(
            entrypoint, name, description, workspace_id
        )

    assert job_config.entrypoint == "python test.py"
    assert job_config.name == name
    assert job_config.description == description
    assert job_config.workspace_id == workspace_id


@pytest.mark.parametrize(
    "config_dict",
    [
        {
            "entrypoint": "mock_entrypoint",
            "build_id": "mock_build_id",
            "compute_config_id": "cpt_123",
        },
        {
            "entrypoint": "mock_entrypoint",
            "cluster_env": "mock_cluster_env",
            "compute_config": "mock_compute_config",
        },
        {
            "entrypoint": "mock_entrypoint",
            "compute_config": {
                "cloud_id": "mock_cloud_id",
                "region": "mock_region",
                "head_node_type": {"name": "head", "instance_type": "m5.large"},
                "worker_node_types": [],
            },
        },
        {
            "entrypoint": "mock_entrypoint",
            "cluster_env": "mock_cluster_env",
            "cloud": "mock_cloud",
        },
        {"entrypoint": "mock_entrypoint", "cluster_env": "mock_cluster_env"},
        {"entrypoint": "mock_entrypoint", "cloud": "mock_cloud"},
        {"entrypoint": "mock_entrypoint"},
        {"entrypoint": "mock_entrypoint", "project_id": "specified_project_id"},
    ],
)
@pytest.mark.parametrize("use_default_project", [True, False])
def test_submit_job(
    mock_auth_api_client,
    config_dict: Dict[str, Any],
    use_default_project: bool,
    compute_template_test_data: ComputeTemplate,
) -> None:
    config_project_id = config_dict.get("project_id")
    mock_logger = Mock()
    job_controller = JobController(log=mock_logger)
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"

    def infer_project_id_mock(project_id: str, *args: Any):
        if project_id:
            return project_id
        elif use_default_project:
            return "mock_default_project_id"
        else:
            return "mock_project_id"

    mock_infer_project_id = Mock(side_effect=infer_project_id_mock)
    mock_get_build_from_cluster_env_identifier = Mock(
        return_value=Mock(id="mock_build_id")
    )
    job_controller.api_client.get_compute_template_api_v2_compute_templates_template_id_get = Mock(
        return_value=Mock(result=compute_template_test_data)
    )
    job_controller.api_client.search_compute_templates_api_v2_compute_templates_search_post = Mock(
        return_value=Mock(results=[compute_template_test_data])
    )
    mock_get_cluster_compute_from_name = Mock(return_value=compute_template_test_data)
    mock_get_default_cluster_compute = Mock(return_value=compute_template_test_data)
    mock_register_compute_template = Mock(return_value=compute_template_test_data)

    mock_validate_successful_build = Mock()
    mock_get_default_cluster_env_build = Mock(return_value=Mock(id="mock_build_id"))
    with patch(
        "builtins.open", mock_open(read_data=json.dumps(config_dict))
    ), patch.multiple(
        "anyscale.controllers.job_controller",
        infer_project_id=mock_infer_project_id,
        get_build_from_cluster_env_identifier=mock_get_build_from_cluster_env_identifier,
        get_cluster_compute_from_name=mock_get_cluster_compute_from_name,
        get_default_cluster_compute=mock_get_default_cluster_compute,
        register_compute_template=mock_register_compute_template,
        validate_successful_build=mock_validate_successful_build,
        get_default_cluster_env_build=mock_get_default_cluster_env_build,
    ), patch.object(
        JobController,
        "_get_maximum_uptime_output",
        return_value="mock maximum uptime output",
    ), patch.multiple(
        "os.path", exists=Mock(return_value=True)
    ):
        job_controller.submit(
            "mock_config_file", name="mock_name", description="mock_description"
        )
    mock_validate_successful_build.assert_called_once_with("mock_build_id")

    if config_project_id:
        final_project_id = config_project_id
    elif use_default_project:
        final_project_id = "mock_default_project_id"
    else:
        final_project_id = "mock_project_id"
    job_controller.api_client.create_job_api_v2_decorated_ha_jobs_create_post.assert_called_once_with(
        CreateInternalProductionJob(
            name="mock_name",
            description="mock_description",
            project_id=final_project_id,
            workspace_id=None,
            config=ProductionJobConfig(
                **{
                    "entrypoint": "mock_entrypoint",
                    "build_id": "mock_build_id",
                    "compute_config_id": compute_template_test_data.id,
                }
            ),
        )
    )
    assert mock_logger.info.call_count == 5
    if "cluster_env" not in config_dict and "build_id" not in config_dict:
        mock_get_default_cluster_env_build.assert_called_once_with()
    if "compute_config" in config_dict:
        compute_config = config_dict["compute_config"]
        if isinstance(compute_config, str):
            mock_get_cluster_compute_from_name.assert_called_with(compute_config)
        elif isinstance(compute_config, dict):
            mock_register_compute_template.assert_called_once_with(compute_config)
    elif "cloud" in config_dict:
        mock_get_default_cluster_compute.assert_called_once_with(
            config_dict["cloud"], None
        )
    elif "compute_config_id" in config_dict:
        mock_get_default_cluster_compute.assert_not_called()


@pytest.mark.parametrize("include_all_users", [False, True])
@pytest.mark.parametrize("name", ["mock_job_name", None])
@pytest.mark.parametrize("job_id", ["mock_job_id", None])
@pytest.mark.parametrize("project_id", ["mock_project_id", None])
@pytest.mark.parametrize(
    "is_service", [False, True]
)  # Whether command should list jobs or services
@pytest.mark.parametrize(
    "passed_service_id", [False, True]
)  # Whether `job_id` is id of job or service
@pytest.mark.parametrize("include_archived", [False, True])
def test_list_jobs(
    mock_auth_api_client,
    include_all_users: bool,
    name: Optional[str],
    job_id: Optional[str],
    project_id: Optional[str],
    is_service: bool,
    passed_service_id: bool,
    include_archived: bool,
) -> None:
    job_controller = JobController()
    job_controller.api_client.get_user_info_api_v2_userinfo_get = Mock(
        return_value=Mock(result=Mock(id="mock_user_id"))
    )
    job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get = Mock(
        return_value=Mock(
            results=[Mock(config=Mock(entrypoint=""))] * 10,
            metadata=Mock(next_paging_token="paging_token"),
        )
    )
    job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get = Mock(
        return_value=Mock(
            result=Mock(
                config=Mock(entrypoint="", is_service=passed_service_id),
                is_service=passed_service_id,
            )
        )
    )

    if is_service != passed_service_id and job_id is not None:
        # Raise error if trying to list id that is not valid for the command.
        # Eg: job_id providied for `anyscale service list`
        with pytest.raises(click.ClickException):
            job_controller.list(
                include_all_users=include_all_users,
                name=name,
                job_id=job_id,
                project_id=project_id,
                is_service=is_service,
                include_archived=include_archived,
                max_items=20,
            )
        return
    else:
        job_controller.list(
            include_all_users=include_all_users,
            name=name,
            job_id=job_id,
            project_id=project_id,
            is_service=is_service,
            include_archived=include_archived,
            max_items=20,
        )

    if job_id:
        job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get.assert_called_once_with(
            job_id
        )
        job_controller.api_client.get_user_info_api_v2_userinfo_get.assert_not_called()
        job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.assert_not_called()
    else:
        creator_id: Optional[str] = None
        if not include_all_users:
            creator_id = "mock_user_id"
            job_controller.api_client.get_user_info_api_v2_userinfo_get.assert_called_once()
        else:
            job_controller.api_client.get_user_info_api_v2_userinfo_get.assert_not_called()
        job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get.assert_not_called()
        job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.assert_any_call(
            creator_id=creator_id,
            name=name,
            project_id=project_id,
            type_filter="SERVICE" if is_service else "BATCH_JOB",
            archive_status="ALL" if include_archived else "NOT_ARCHIVED",
            count=10,
        )
        job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.assert_any_call(
            creator_id=creator_id,
            name=name,
            project_id=project_id,
            type_filter="SERVICE" if is_service else "BATCH_JOB",
            archive_status="ALL" if include_archived else "NOT_ARCHIVED",
            count=10,
            paging_token="paging_token",
        )
        assert (
            job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.call_count
            == 2
        )


@pytest.mark.parametrize(
    "is_service", [False, True]
)  # Whether command should list jobs or services
@pytest.mark.parametrize("name", ["mock_job_name", None])
@pytest.mark.parametrize("id", ["mock_job_id", None])
def test_terminate_job(
    mock_auth_api_client,
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    is_service: bool,
) -> None:
    job_controller = JobController()
    job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get = Mock(
        return_value=Mock(results=[Mock(id="mock_job_id")])
    )
    job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get = Mock(
        return_value=Mock(result=Mock(id="mock_job_id"))
    )
    if not name and not id:
        with pytest.raises(click.ClickException):
            job_controller.terminate(id, name, is_service)
        return
    else:
        job_controller.terminate(id, name, is_service)

    job_controller.api_client.terminate_job_api_v2_decorated_ha_jobs_production_job_id_terminate_post.assert_called_once_with(
        "mock_job_id"
    )
    if name is not None and id is None:
        job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.assert_called_once_with(
            name=name, type_filter="SERVICE" if is_service else "BATCH_JOB",
        )


@pytest.mark.parametrize("is_service", [False, True])
@pytest.mark.parametrize("name", ["mock_job_name", None])
@pytest.mark.parametrize("id", ["mock_job_id", None])
def test_archive_job(
    mock_auth_api_client,
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    is_service: bool,
) -> None:
    job_controller = JobController()
    job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get = Mock(
        return_value=Mock(results=[Mock(id="mock_job_id")])
    )
    job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get = Mock(
        return_value=Mock(result=Mock(id="mock_job_id"))
    )
    if not name and not id:
        with pytest.raises(click.ClickException):
            job_controller.archive(id, name, is_service)
        return
    else:
        job_controller.archive(id, name, is_service)

    job_controller.api_client.archive_job_api_v2_decorated_ha_jobs_production_job_id_archive_post.assert_called_once_with(
        "mock_job_id"
    )
    if name is not None and id is None:
        job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.assert_called_once_with(
            name=name, type_filter="SERVICE" if is_service else "BATCH_JOB",
        )


class TestValidateConda:
    def test_validate_conda_str(self, test_directory, patch_jobs_anyscale_api_client):
        """Tests the conda field is allowed to be a str. It represents an existing env name."""
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"conda": "env_name"},
        )
        assert jc.runtime_env["conda"] == "env_name"

    def test_validate_conda_invalid_path(self, patch_jobs_anyscale_api_client):
        """If a path to a YAML file is given, it should error if the path does not exist."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"conda": "../bad_path.yaml"},
            )

    @pytest.mark.parametrize("absolute_path", [True, False])
    def test_validate_conda_valid_file(
        self, test_directory, absolute_path, patch_jobs_anyscale_api_client
    ):
        _, _, good_conda_file, _ = test_directory

        if absolute_path:
            good_conda_file = good_conda_file.resolve()

        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"conda": str(good_conda_file)},
        )
        assert jc.runtime_env["conda"] == CONDA_DICT

    @pytest.mark.parametrize("absolute_path", [True, False])
    def test_validate_conda_invalid_file(
        self, test_directory, absolute_path, patch_jobs_anyscale_api_client
    ):
        """We should error if a .yml file with invalid YAML format is specified."""
        _, _, _, bad_conda_file = test_directory

        if absolute_path:
            bad_conda_file = bad_conda_file.resolve()

        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"conda": str(bad_conda_file)},
            )

    def test_validate_conda_valid_dict(self, patch_jobs_anyscale_api_client):
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"conda": CONDA_DICT},
        )
        assert jc.runtime_env["conda"] == CONDA_DICT


class TestValidatePip:
    def test_validate_pip_invalid_path(self, patch_jobs_anyscale_api_client):
        """If a path to a .txt file is given, it should error if the path does not exist."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"pip": "../bad_path.txt"},
            )

    @pytest.mark.parametrize("absolute_path", [True, False])
    def test_validate_pip_valid_file(
        self, test_directory, absolute_path, patch_jobs_anyscale_api_client
    ):
        _, requirements_file, _, _ = test_directory

        if absolute_path:
            requirements_file = requirements_file.resolve()

        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"pip": str(requirements_file)},
        )
        assert jc.runtime_env["pip"] == PIP_LIST

    def test_validate_pip_valid_list(self, patch_jobs_anyscale_api_client):
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"pip": PIP_LIST},
        )
        assert jc.runtime_env["pip"] == PIP_LIST


class TestValidateEnvVars:
    def test_validate_env_vars_valid_dict(self, patch_jobs_anyscale_api_client):
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"env_vars": ENV_VARS_DICT},
        )
        assert jc.runtime_env["env_vars"] == ENV_VARS_DICT

    def test_validate_env_vars_invalid_dict(self, patch_jobs_anyscale_api_client):
        """Error if env_vars is not a dict."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"env_vars": "not_a_dict"},
            )

    def test_validate_env_vars_not_dict_str(self, patch_jobs_anyscale_api_client):
        """Error if env_vars is not a Dict[str, str]."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"env_vars": {"key", 123}},
            )
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"env_vars": {"key": "value", 123: "value2"}},
            )


class TestValidateUploadPath:
    def test_reject_upload_path_without_local_dir(self, patch_jobs_anyscale_api_client):
        """If upload_path is specified, a local working_dir must also be specified."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"upload_path": "s3://some_bucket"},
            )

    def test_reject_non_s3_or_gs_upload_path(self, patch_jobs_anyscale_api_client):
        """If upload_path is specified, it must be an s3 or gs path."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"upload_path": "file://some_file"},
            )

    def test_accept_s3_upload_path(self, patch_jobs_anyscale_api_client):
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"working_dir": "./", "upload_path": "s3://some_bucket"},
        )
        assert jc.runtime_env["upload_path"] == "s3://some_bucket"

    def test_accept_gs_upload_path(self, patch_jobs_anyscale_api_client):
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"working_dir": "./", "upload_path": "gs://some_bucket"},
        )
        assert jc.runtime_env["upload_path"] == "gs://some_bucket"


class TestValidateWorkingDir:
    def test_working_dir_is_remote_uri(self):
        assert _working_dir_is_remote_uri("s3://some_bucket")
        assert _working_dir_is_remote_uri("s3://some_bucket/some/path")
        assert _working_dir_is_remote_uri("fake://some_bucket/some/path/")
        assert not _working_dir_is_remote_uri("/some/path")
        assert not _working_dir_is_remote_uri("some/path/")

    def test_reject_local_dir_without_upload_path(self, patch_jobs_anyscale_api_client):
        """If a local working_dir is specified, upload_path must also be specified."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"working_dir": "."},
            )

        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"working_dir": "/tmp/dir"},
            )

    def test_reject_remote_uri_with_upload_path(self, patch_jobs_anyscale_api_client):
        """If a working_dir is specified as a remote URI, upload_path cannot be specified."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"working_dir": "s3://test", "upload_path": "s3://another"},
            )

    def test_accept_local_dir_with_upload_path(self, patch_jobs_anyscale_api_client):
        JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"working_dir": ".", "upload_path": "s3://fake"},
        )

        JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"working_dir": ".", "upload_path": "gs://fake/dir"},
        )

    def test_reject_nonexistent_local_dir(self, patch_jobs_anyscale_api_client):
        """If a local working_dir is specified, it must exist."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={
                    "working_dir": "/does/not/exist",
                    "upload_path": "gs://fake",
                },
            )

    def test_accept_uri(self, patch_jobs_anyscale_api_client):
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"working_dir": "s3://path/to/archive.zip"},
        )
        assert jc.runtime_env["working_dir"] == "s3://path/to/archive.zip"


class TestValidatePyModules:
    def test_reject_local_dir(self, patch_jobs_anyscale_api_client):
        """Local directories are only supported using working_dir, not py_modules."""
        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"py_modules": ["."]},
            )

        with pytest.raises(click.ClickException):
            JobConfig(
                entrypoint="ls",
                build_id="123",
                compute_config_id="test",
                runtime_env={"py_modules": ["/tmp/dir"]},
            )

    def test_accept_uri(self, patch_jobs_anyscale_api_client):
        jc = JobConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"py_modules": ["s3://path/to/archive.zip"]},
        )
        assert jc.runtime_env["py_modules"] == ["s3://path/to/archive.zip"]


@pytest.mark.parametrize("project_id", [None, "proj_id"])
@pytest.mark.parametrize("project_name", [None, "proj_name"])
@pytest.mark.parametrize("project_name_env_var", [None, "proj_name_env"])
def test_validate_project_id_field(
    project_id: Optional[str],
    project_name: Optional[str],
    project_name_env_var: Optional[str],
):
    mock_get_proj_id_from_name = Mock(return_value="proj_id")
    mock_validate_successful_build = Mock()
    config_dict = {
        "entrypoint": "mock_entrypoint",
        "build_id": "mock_build_id",
        "compute_config_id": "mock_compute_config_id",
        "project_id": project_id,
        "project": project_name,
    }
    mock_os_dict = (
        {PROJECT_NAME_ENV_VAR: project_name_env_var} if project_name_env_var else {}
    )
    with patch.multiple(
        "anyscale.controllers.job_controller",
        get_proj_id_from_name=mock_get_proj_id_from_name,
        validate_successful_build=mock_validate_successful_build,
    ), patch.dict(os.environ, mock_os_dict):
        if project_id and project_name:
            with pytest.raises(click.ClickException):
                job_config = JobConfig.parse_obj(config_dict)
        else:
            job_config = JobConfig.parse_obj(config_dict)
            if project_name_env_var:
                assert job_config.project_id == "proj_id"
                mock_get_proj_id_from_name.assert_called_once_with(project_name_env_var)
            elif project_name:
                assert job_config.project_id == "proj_id"
                mock_get_proj_id_from_name.assert_called_once_with(project_name)
            else:
                assert job_config.project_id == project_id


def fake_log_provider(mode: str) -> Type[LogProvider]:
    class FakeLogProvider(LogProvider):
        def __init__(self, *args, **kwargs) -> None:
            self.constructed_at = int(time.time() * 1e9)
            self.page = -1
            self.query_count = 0

        def close(self):
            pass

        def query(
            self, start_timestamp_ns: int, end_timestamp_ns: int
        ) -> List[Tuple[int, str]]:
            # For typing
            empty_list: List[Tuple[int, str]] = []

            if mode == "empty":
                return empty_list
            if mode == "single":
                if start_timestamp_ns > self.constructed_at:
                    return []
                return [(start_timestamp_ns, "start"), (self.constructed_at, "end")]
            if mode == "paginate":
                self.page += 1
                return [
                    [(start_timestamp_ns, "entry-1")],
                    [(start_timestamp_ns + 1, "entry-2")],
                    empty_list,
                ][self.page]
            if mode == "follow":
                self.page += 1
                return [
                    # simulate no log
                    empty_list,
                    empty_list,
                    [(start_timestamp_ns, "finally")],
                ][self.page]
            if mode == "flush_success":
                self.page += 1
                return (
                    [
                        # simulate no log
                        empty_list,
                        empty_list,
                        [(start_timestamp_ns, "finally")],
                        empty_list,
                        # Simulate 30 steps of empty logs
                    ]
                    + [empty_list for _ in range(30)]
                )[self.page]
            if mode == "wait_for_running":
                self.page += 1
                return (
                    [
                        # simulate no log
                        empty_list,
                        empty_list,
                        [(start_timestamp_ns, "finally")],
                        empty_list,
                        # Simulate 30 steps of empty logs
                    ]
                    + [empty_list for _ in range(30)]
                )[self.page]

            raise Exception("unreachable")

    return FakeLogProvider


# For `async with a() as b:`
class MockAsyncContextManagerReturnValue(MagicMock):
    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, *args):
        return None


def test_stream_logs(mock_auth_api_client) -> None:
    job_controller = JobController(log=FakeLogger())
    prodjob_id = "prodjob_123"
    job_id = "job_123"
    job_controller._wait_for_a_job_run = Mock(return_value=job_id)  # type: ignore
    job_controller.api_client = Mock(
        get_job_logs_stream_api_v2_logs_job_logs_stream_job_id_get=Mock(
            return_value=Mock(result=Mock(stream_url="http://localhost:5000/stream",))
        )
    )
    mock_websocket = MockAsyncContextManagerReturnValue()
    # Test logs successfully streamed
    mock_websocket.receive = CoroutineMock(
        side_effect=[
            Mock(type=WSMsgType.TEXT, data=" abc "),
            Mock(type=WSMsgType.ERROR),
            Mock(type=WSMsgType.CLOSED),
        ]
    )
    with patch.object(
        ClientSession, ClientSession.ws_connect.__name__, return_value=mock_websocket
    ):
        job_controller.stream_logs(prodjob_id)
    job_controller._wait_for_a_job_run.assert_called_once_with(prodjob_id)
    job_controller.api_client.get_job_logs_stream_api_v2_logs_job_logs_stream_job_id_get.assert_called_once_with(
        job_id=job_id
    )
    assert mock_websocket.receive.call_count == 3
    assert job_controller.log.logs == ["abc"]  # type: ignore
    # Test job does not exist
    mock_job_run_not_found_exception = ClientResponseError(
        request_info=Mock(), history=Mock(), status=404
    )
    mock_websocket.receive = CoroutineMock(side_effect=mock_job_run_not_found_exception)
    with patch.object(
        ClientSession, ClientSession.ws_connect.__name__, return_value=mock_websocket
    ), pytest.raises(Exception) as e:
        job_controller.stream_logs(job_id)
    assert "Job run job_123 not found in cluster for current running job." in str(e)

    # Test other exception thrown
    mock_other_exception = ClientResponseError(
        request_info=Mock(), history=Mock(), status=400
    )
    mock_websocket.receive = CoroutineMock(side_effect=mock_other_exception)
    with patch.object(
        ClientSession, ClientSession.ws_connect.__name__, return_value=mock_websocket
    ), pytest.raises(Exception) as e:
        job_controller.stream_logs(job_id)


@pytest.mark.parametrize("cluster_id_found_in_last_job_run", [True, False])
def test_download_logs(
    mock_auth_api_client, cluster_id_found_in_last_job_run: bool
) -> None:
    prodjob_id = "prodjob_123"
    cluster_id = "session_123"
    job_controller = JobController(log=FakeLogger())
    if cluster_id_found_in_last_job_run:
        mock_prod_job = Mock(last_job_run=Mock(cluster_id=cluster_id), state=Mock())
    else:
        mock_prod_job = Mock(last_job_run=None, state=Mock(cluster_id=cluster_id))
    job_controller._get_latest_job_run = Mock(  # type: ignore
        return_value=mock_prod_job
    )
    mock_download_logs = Mock()
    job_controller.logs_controller.download_logs = mock_download_logs  # type: ignore
    job_controller.download_logs(prodjob_id)
    job_controller._get_latest_job_run.assert_called_once_with(prodjob_id)
    mock_download_logs.assert_called_once_with(
        filter=LogFilter(cluster_id=cluster_id, glob="/job-driver-"),
        write_to_stdout=True,
    )


@pytest.mark.parametrize(
    "mode",
    ["empty", "single", "paginate", "follow", "flush_success", "wait_for_running"],
)
def test_loki_logs(mock_auth_api_client, capsys, mode) -> None:
    job_controller = JobController(log=FakeLogger())
    fake_log_provider_cls = fake_log_provider(mode)

    state = {"flush_success": "SUCCESS", "wait_for_running": "PENDING"}.get(
        mode, "RUNNING"
    )

    job_controller._get_formatted_latest_job_run = Mock(  # type: ignore
        return_value=MiniJobRun(
            last_job_run_id="mock_job_id", job_state=state, error=None
        )
    )

    def reset(*args, **kwargs):
        job_controller._get_formatted_latest_job_run = Mock(  # type: ignore
            return_value=MiniJobRun(
                last_job_run_id="mock_job_id", job_state="SUCCESS", error=None
            )
        )

    job_controller._wait_for_job_running = Mock(side_effect=reset)  # type: ignore
    job_controller.anyscale_api_client.get_job_logs_query_info = Mock(
        return_value=Mock(
            result=Mock(
                loki_dns_name="abc.com",
                access_token="secret-key",
                loki_query="query-abc",
            )
        )
    )

    def do_loki_logs() -> None:
        job_controller.loki_logs(
            job_id="mock_job_id",
            should_follow=mode in ["follow", "flush_success", "wait_for_running"],
            log_provider_cls=fake_log_provider_cls,
        )

    if mode == "empty":
        do_loki_logs()
        assert capsys.readouterr().out.strip() == ""
    elif mode == "single":
        do_loki_logs()
        assert capsys.readouterr().out.strip() == "start\nend"
    elif mode == "paginate":
        do_loki_logs()
        assert capsys.readouterr().out.strip() == "entry-1\nentry-2"
    elif mode == "follow":
        with pytest.raises(IndexError):  # controller should continue to query
            do_loki_logs()
        out = capsys.readouterr().out.strip()
        assert out == "finally"
    elif mode == "flush_success":
        do_loki_logs()
        out = capsys.readouterr().out.strip()
        assert out == "finally"
    elif mode == "wait_for_running":
        with pytest.raises(IndexError):  # controller should continue to query
            do_loki_logs()
        assert job_controller._wait_for_job_running.call_count == 1
        out = capsys.readouterr().out.strip()
        assert out == "finally"
    else:
        raise Exception("unreachable")


def test_logs(mock_auth_api_client) -> None:
    job_controller = JobController()
    prod_job_id = "prodjob_123"
    job_controller._resolve_job_object = Mock(return_value=Mock(id=prod_job_id))  # type: ignore
    job_controller.stream_logs = mock_stream_logs = Mock()  # type: ignore
    job_controller.download_logs = mock_download_logs = Mock()  # type: ignore
    job_controller.loki_logs = mock_loki_logs = Mock()  # type: ignore

    def reset_mocks() -> None:
        for mock in [mock_download_logs, mock_stream_logs, mock_loki_logs]:
            mock.reset_mock()

    def do_assertions(
        called: Optional[List[Mock]] = None, not_called: Optional[List[Mock]] = None
    ) -> None:
        if not called:
            called = []
        if not not_called:
            not_called = []
        for mock in called:
            mock.assert_called_once_with(prod_job_id)
        for mock in not_called:
            mock.assert_not_called()

    # Test download logs by default
    job_controller.logs(job_id=prod_job_id)
    do_assertions(
        called=[mock_download_logs], not_called=[mock_stream_logs, mock_loki_logs]
    )

    # Test stream logs if follow specified
    reset_mocks()
    job_controller.logs(job_id=prod_job_id, should_follow=True)
    do_assertions(
        called=[mock_stream_logs], not_called=[mock_download_logs, mock_loki_logs]
    )

    # Test download if stream fails
    reset_mocks()
    job_controller.stream_logs.side_effect = Exception
    job_controller.logs(job_id=prod_job_id, should_follow=True)
    do_assertions(
        called=[mock_stream_logs, mock_download_logs], not_called=[mock_loki_logs]
    )

    # Test loki logs if both stream and download fails
    reset_mocks()
    job_controller.download_logs.side_effect = Exception
    job_controller.logs(job_id=prod_job_id, should_follow=True)
    do_assertions(called=[mock_stream_logs, mock_download_logs])
    mock_loki_logs.assert_called_once_with(prod_job_id, True)


def test_wait_for_job_running(mock_auth_api_client) -> None:
    job_controller = JobController(log=FakeLogger())
    i = 0

    def get_latest_job_run(*args, **kwargs):
        print("Called get_latest_job_run")
        nonlocal i
        i += 1
        ret = Mock()
        status = "RUNNING"
        if i < 3:
            status = "PENDING"
        elif i < 5:
            status = "AWAITING_CLUSTER_START"
        ret.state.current_state = status
        return ret

    job_controller._get_latest_job_run = Mock(side_effect=get_latest_job_run)  # type: ignore
    job_controller._wait_for_job_running("fake_job_id")
    assert i == 5


def test_job_submit_parse_logic(mock_auth_api_client) -> None:
    job_controller = JobController()
    job_controller.generate_config_from_entrypoint = Mock()  # type: ignore
    job_controller.generate_config_from_file = Mock()  # type: ignore
    job_controller.submit_from_config = Mock()  # type: ignore

    # We are not in a workspace, so entrypoint should not be allowed
    with pytest.raises(click.ClickException):
        job_controller.submit(
            "file", entrypoint=["entrypoint"], is_entrypoint_cmd=False
        )

    with pytest.raises(click.ClickException):
        job_controller.submit("file", entrypoint=["entrypoint"], is_entrypoint_cmd=True)

    with pytest.raises(click.ClickException):
        job_controller.submit(
            "file", entrypoint=["entrypoint", "commands"], is_entrypoint_cmd=True
        )

    # Simulate a workspace
    with patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "fake_workspace_id"}
    ):
        # Fails due to is_entrypoint_cmd being False
        with pytest.raises(click.ClickException):
            job_controller.submit(
                "file", entrypoint=["entrypoint"], is_entrypoint_cmd=False
            )

        mock_config = Mock()
        job_controller.generate_config_from_file.return_value = mock_config
        job_controller.submit("file", entrypoint=[], is_entrypoint_cmd=False)
        job_controller.generate_config_from_file.assert_called_once_with(
            "file", name=None, description=None, workspace_id="fake_workspace_id"
        )
        job_controller.submit_from_config.assert_called_once_with(mock_config)
        job_controller.generate_config_from_file.reset_mock()
        job_controller.submit_from_config.reset_mock()

        mock_config = Mock()
        job_controller.generate_config_from_entrypoint.return_value = mock_config
        job_controller.submit("file", entrypoint=["entrypoint"], is_entrypoint_cmd=True)
        job_controller.generate_config_from_entrypoint.assert_called_once_with(
            ["file", "entrypoint"], None, None, "fake_workspace_id"
        )
        job_controller.submit_from_config.assert_called_once_with(mock_config)


def test_job_wait(mock_auth_api_client) -> None:
    job_controller = JobController()
    job_controller.api_client = Mock()
    job_controller._resolve_job_object = Mock(return_value=SimpleNamespace(id="id"))  # type: ignore
    spin_mock = MagicMock()
    job_controller.log = MagicMock()
    job_controller.log.spinner.return_value.__enter__.return_value = spin_mock

    def get_job_state(states_to_return, mock_state=None):
        if mock_state is None:
            mock_state = Mock()

        mock_state.i = 0

        def g(*args, **kwargs):
            nonlocal mock_state
            state = states_to_return[mock_state.i]
            mock_state.i += 1
            mock_state.state = state
            return state

        return g, mock_state

    # Test the happy path
    states_to_return = ["PENDING", "AWAITING_CLUSTER_START", "SUCCESS"]
    job_controller._get_job_state, mock_state = get_job_state(states_to_return)  # type: ignore

    assert job_controller.wait("name")
    assert mock_state.i == 3
    assert mock_state.state == "SUCCESS"
    spin_mock.succeed.assert_called_once()

    # Test the failure case
    spin_mock.reset_mock()
    states_to_return = [
        "PENDING",
        "AWAITING_CLUSTER_START",
        "ERRORED",
        "OUT_OF_RETRIES",
    ]
    job_controller._get_job_state, mock_state = get_job_state(states_to_return)  # type: ignore

    with pytest.raises(click.ClickException):
        job_controller.wait("name")
    assert mock_state.i == 4
    assert mock_state.state == "OUT_OF_RETRIES"
    spin_mock.fail.assert_called_once()

    # Test the non default case
    spin_mock.reset_mock()
    states_to_return = [
        "PENDING",
        "AWAITING_CLUSTER_START",
        "ERRORED",
        "SHOULD_NOT_REACH",
        "SHOULD_NOT_REACH",
        "SHOULD_NOT_REACH",
    ]
    job_controller._get_job_state, mock_state = get_job_state(states_to_return)  # type: ignore

    assert job_controller.wait("name", target_state="ERRORED")
    assert mock_state.state == "ERRORED"
    assert mock_state.i == 3
    spin_mock.succeed.assert_called_once()

    # Test timeout logic
    spin_mock.reset_mock()
    states_to_return = [
        "PENDING",
        "AWAITING_CLUSTER_START",
        "ERRORED",
        "SHOULD_NOT_REACH",
        "SHOULD_NOT_REACH",
        "SHOULD_NOT_REACH",
    ]
    job_controller._get_job_state, mock_state = get_job_state(states_to_return)  # type: ignore

    with pytest.raises(click.ClickException):
        job_controller.wait("name", timeout_secs=0.00001)

    # Test parsing logic
    with pytest.raises(click.ClickException):
        job_controller.wait("name", target_state="FAKE_STATE")
