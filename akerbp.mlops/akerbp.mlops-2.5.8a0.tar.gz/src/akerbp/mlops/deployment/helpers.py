# helpers.py
import sys
import shutil
import os
import subprocess
import venv
import json
import re
from importlib import resources as importlib_resources
from pathlib import Path
from typing import Dict, Any, Tuple
from cognite.client import CogniteClient
import logging
from logging import config as logging_config
from akerbp.mlops import __version__
from akerbp.mlops.core import config
from akerbp.mlops.core.config import ServiceSettings
from akerbp.mlops.core.exceptions import (
    DeploymentError,
    TestError,
    VirtualEnvironmentError,
)
from akerbp.mlops.deployment import platforms
from akerbp.mlops.cdf import helpers as cdf

from akerbp.mlops.core.logger_config import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.captureWarnings(True)


env = config.envs.env
service_name = config.envs.service_name
platform_methods = platforms.get_methods()


def is_unix() -> bool:
    """Checks whether the working OS is unix-based or not

    Returns:
        bool: True if os is unix-based
    """
    return os.name == "posix"


def get_repo_origin() -> str:
    """Get origin of the git repo

    Returns:
        (str): origin
    """
    origin = subprocess.check_output(
        ["git", "remote", "get-url", "--push", "origin"], encoding="UTF-8"
    ).rstrip()
    return origin


def replace_string_file(s_old: str, s_new: str, file: Path) -> None:
    """
    Replaces all occurrences of s_old with s_new in a specifyied file

    Args:
        s_old (str): old string
        s_new (str): new string
        file (Path): file to replace the string in
    """
    with file.open() as f:
        s = f.read()
        if s_old not in s:
            logger.warning(f"Didn't find '{s_old}' in {file}")

    with file.open("w") as f:
        s = s.replace(s_old, s_new)
        f.write(s)


def set_mlops_import(req_file: Path) -> None:
    """Set correct package version in requirements.txt

    Args:
        req_file (Path): path to requirements.txt for the model to deploy
    """
    package_version = __version__
    replace_string_file("MLOPS_VERSION", package_version, req_file)
    logger.info(f"Set akerbp.mlops=={package_version} in requirements.txt")


def to_folder(path: Path, folder_path: Path) -> None:
    """
    Copy folders, files or package data to a given folder.
    Note that if target exists it will be overwritten.

    Args:
        path: supported formats
            - file/folder path (Path): e,g, Path("my/folder")
            - module file (tuple/list): e.g. ("my.module", "my_file"). Module
            path has to be a string, but file name can be a Path object.
        folder_path (Path): folder to copy to
    """
    if isinstance(path, (tuple, list)):
        module_path, file = path
        file = str(file)
        if importlib_resources.is_resource(module_path, file):
            with importlib_resources.path(module_path, file) as file_path:
                shutil.copy(file_path, folder_path)
        else:
            raise ValueError(f"Didn't find {path[1]} in {path[0]}")
    elif path.is_dir():
        shutil.copytree(path, folder_path / path, dirs_exist_ok=True)
    elif path.is_file():
        shutil.copy(path, folder_path)
    else:
        raise ValueError(f"{path} should be a file, folder or package resource")


def get_deployment_folder_content(deployment_folder: Path) -> Dict:
    """Logs the content of the deployment folder as a dictionary with keys being
    directory/subdirectory, and values the corresponding content

    Args:
        deployment_folder (Path): path to deployment folder

    Returns:
        Dict: content of deployment folder
    """
    dirwalk = os.walk(deployment_folder)
    content = {}
    for tup in dirwalk:
        if "__pycache__" in tup[0].split("/"):
            continue
        if (
            len(tup[1]) > 0 and "__pycache__" not in tup[1]
        ):  # includes subdirectories, skip pycache
            content[tup[0]] = tup[1] + tup[-1]
        else:
            content[tup[0]] = tup[-1]
    return content


def copy_to_deployment_folder(lst: Dict, deployment_folder: Path) -> None:
    """
    Copy a list of files/folders to a deployment folder

    Args:
        lst (dict): key is the nickname of the file/folder (used for
        logger) and the value is the path (see `to_folder` for supported
        formats)
        deployment_folder (Path): Path object for the deployment folder

    """
    for k, v in lst.items():
        if v:
            logger.debug(f"{k} => deployment folder")
            to_folder(v, deployment_folder)
        else:
            logger.warning(f"{k} has no value")


def update_pip(venv_dir: str, **kwargs) -> None:
    is_unix_os = kwargs.get("is_unix_os", True)
    setup_venv = kwargs.get("setup_venv", True)
    if setup_venv:
        if is_unix_os:
            sys.executable = os.path.join(venv_dir, "bin", "python")
            c = [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip",
            ]
        else:
            sys.executable = os.path.join(venv_dir, "Scripts", "python")
            c = [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip",
            ]
    else:
        c = ["python", "-m", "pip", "install", "--upgrade", "pip"]
    logger.info("Updating pip")
    subprocess.run(c)


def install_requirements(req_file: str, venv_dir: str, **kwargs) -> None:
    """install model requirements

    Args:
        req_file (str): path to requirements file
    """
    with_deps = kwargs.get("with_deps", True)
    setup_venv = kwargs.get("setup_venv", False)
    logger.info(f"Install python requirement file {req_file}")
    is_unix_os = is_unix()
    update_pip(
        venv_dir=venv_dir,
        is_unix_os=is_unix_os,
        setup_venv=setup_venv,
    )
    if with_deps:
        if setup_venv:
            if is_unix_os:
                sys.executable = os.path.join(venv_dir, "bin", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.abspath(req_file),
                ]
            else:
                sys.executable = os.path.join(venv_dir, "Scripts", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.abspath(req_file),
                ]
        else:
            c = ["pip", "install", "-r", os.path.abspath(req_file)]
    else:
        if setup_venv:
            if is_unix_os:
                sys.executable = os.path.join(venv_dir, "bin", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "-r",
                    os.path.abspath(req_file),
                ]
            else:
                sys.executable = os.path.join(venv_dir, "Scripts", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.abspath(req_file),
                ]
        else:
            c = ["pip", "install", "--no-deps", "-r", os.path.abspath(req_file)]
    subprocess.run(c)


def create_venv(venv_name: str) -> str:
    venv_dir = os.path.join(os.getcwd(), venv_name)
    logger.info(f"Creating virtual environment {venv_name}")
    venv.create(venv_dir, with_pip=True)
    if os.path.isdir(venv_dir):
        logger.info(f"Sucsessfully created virtual environment {venv_name}")
    else:
        raise VirtualEnvironmentError("Virtual environment was not created")
    return venv_dir


def delete_venv(venv_name: str) -> None:
    logger.info(f"Deleting virtual environment {venv_name}")
    subprocess.run(["rm", "-rf", os.path.abspath(venv_name)])
    if not os.path.isdir(os.path.abspath(venv_name)):
        logger.info(f"Virtual environment {venv_name} sucsessfully deleted")
    else:
        raise VirtualEnvironmentError("Virtual environment not deleted")


def set_up_requirements(c: ServiceSettings, **kwargs) -> str:
    """
    Set up a "requirements.txt" file at the top of the deployment folder
    (assumed to be the current directory), update config and install
    dependencies (unless in dev)

    Args:
        c (ServiceSettings): service settings a specified in the config file

    Keyword Args:
        install (bool): Whether to install the dependencies, defaults to True
    """
    logger.info("Create requirement file")
    install_reqs = kwargs.get("install", True)
    with_deps = kwargs.get("with_deps", True)
    unit_testing = kwargs.get("unit_testing", False)
    venv_name = kwargs.get("venv_name", "mlops-venv")
    setup_venv = kwargs.get("setup_venv", False)
    if setup_venv:
        venv_dir = create_venv(venv_name=venv_name)
    else:
        venv_dir = str(os.getcwd())

    set_mlops_import(c.req_file)
    if not unit_testing:
        shutil.copyfile(c.req_file, "requirements.txt")
        c.req_file = "requirements.txt"

    if env != "dev" or install_reqs:
        install_requirements(
            c.req_file, venv_dir=venv_dir, with_deps=with_deps, setup_venv=setup_venv
        )
    else:
        logger.info("Skipping installation of requirements.txt")
    return venv_dir  # type: ignore


def deployment_folder_path(model: str) -> Path:
    """Generate path to deployment folder, which is on the form "mlops_<model>"

    Args:
        model (str): model name

    Returns:
        Path: path to the deployment folder
    """
    return Path(f"mlops_{model}")


def rm_deployment_folder(model: str) -> None:
    logger.info("Deleting deployment folder")
    deployment_folder = deployment_folder_path(model)
    if deployment_folder.exists():
        shutil.rmtree(deployment_folder)


def run_tests(c: ServiceSettings, **kwargs) -> Any:
    """Helper function that runs unit tests and returns a test payload
    if run during deployment

    Args:
        c (ServiceSettings): Service settings object containing model settings

    Keyword Args:
        setup_venv (bool): whether to setup an ephemeral virtual environment.
            Defaults to False
    Raises:
        TestError: If unit tests are failing

    Returns:
        Union[Dict[str, Any], None]: Return test payload if test file is specified in 'mlops_settings.yaml'
    """
    if c.test_file:
        setup_venv = kwargs.get("setup_venv", False)
        if setup_venv:
            logger.info("Setting up ephemeral virtual environment")
            venv_dir = set_up_requirements(
                c,
                install=True,
                setup_venv=setup_venv,
            )
            is_unix_os = is_unix()
            if is_unix_os:
                sys.executable = os.path.join(venv_dir, "bin", "python")
            else:
                sys.executable = os.path.join(venv_dir, "Scripts", "python")
        else:
            set_up_requirements(c, install=True)
        config.store_service_settings(c)
        test_command = [
            sys.executable,
            "-m",
            "akerbp.mlops.services.test_service",
        ]
        logger.info(f"Running tests for model {c.model_name}")
        failed_test = False
        try:
            output = subprocess.check_output(test_command, encoding="UTF-8")
        except subprocess.CalledProcessError as e:
            output = e.output
            failed_test = True
        model_input = None
        for log_line in output.splitlines():  # type: ignore
            if log_line == "":
                continue
            elif log_line == "warnings.warn(":
                continue
            elif log_line.startswith('{"input": ['):
                # Extract payload for downstream testing of deployed model
                model_input = json.loads(log_line)
                logger.info("Payload for downstream logging of deployed model obtained")
                continue
            else:
                # Remove the date and time from piped log
                log_line = re.sub(
                    "\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2} -",
                    "",
                    log_line,
                )
                logger.info(log_line)
        if failed_test:
            raise TestError("Unit tests failed :( See the above traceback")
        if model_input is None:
            raise TestError(
                "Test was not able to extract the payload for downstream testing of deployed model"
            )
        if setup_venv:
            delete_venv(venv_name=venv_dir.split("/")[-1])
            logger.info("Ephemeral virtual environment deleted")
        logger.info("Unit tests passed :)")

        return model_input
    else:
        logger.warning(
            "No test file specified in 'mlops_settings.yaml', skipping tests"
        )
        return {}


def deploy_model(
    c: ServiceSettings,
    env: str,
    service_name: str,
    function_name: str,
    test_payload: Any,
    platform_methods: Dict = platform_methods,
) -> Tuple[str, int, int]:
    deploy_function, _, test_function = platform_methods[c.platform]
    logger.info(f"Starting deployment of model {c.model_name} to {env}")
    latest_artifact_version = cdf.get_latest_artifact_version(external_id=function_name)
    if c.artifact_version is None:
        logger.info(f"Latest artifact version in {env} is {latest_artifact_version}")
        artifact_version = latest_artifact_version
    else:
        artifact_version = c.artifact_version

    external_id = function_name + "-" + str(artifact_version)

    logger.info(
        f"Deploying function {c.human_friendly_model_name} with external id {external_id} to {c.platform}"
    )
    try:
        deploy_function(
            c.human_friendly_model_name, external_id, info=c.info[service_name]
        )
    except Exception as e:
        raise DeploymentError(f"Deployment failed with message: \n{str(e)}") from e
    if c.test_file:
        logger.info(f"Make a test call to function with external id {external_id}")
        try:
            test_function(external_id, test_payload)
        except Exception as e:
            raise TestError(
                f"Test of deployed model failed with message: \n{str(e)}"
            ) from e
    else:
        logger.warning(
            f"No test file was set up. End-to-end test skipped for function {external_id}"
        )
    return external_id, artifact_version, latest_artifact_version


def redeploy_model_with_predictable_external_id(
    c: ServiceSettings,
    external_id: str,
    predictable_external_id: str,
    test_payload: Any,
    platform_methods: Dict = platform_methods,
) -> None:
    _, redeploy_function, test_function = platform_methods[c.platform]
    (
        name,
        file_id,
        description,
        metadata,
        owner,
    ) = cdf.get_arguments_for_redeploying_latest_model_version(external_id=external_id)

    try:
        redeploy_function(
            name,
            predictable_external_id,
            file_id,
            description,
            metadata,
            owner,
        )
    except Exception as e:
        raise DeploymentError(
            f"Redeployment of latest model failed with message:  \n{str(e)}"
        ) from e

    if c.test_file:
        try:
            test_function(predictable_external_id, test_payload)
        except Exception as e:
            raise TestError(
                f"Testing the newly redeployed latest model failed with message: \n{str(e)}"
            ) from e
    else:
        logger.warning("No test file was specified in the settings, skipping tests")


def garbage_collection(
    c: ServiceSettings, function_name: str, env: str, client: CogniteClient
) -> None:
    models_to_keep = c.models_to_keep
    keep_all_models = c.keep_all_models
    if models_to_keep is None:
        if keep_all_models is True:
            logger.info("Keeping all models alive as specified in the settings file")
        else:
            logger.info("Number of models to keep alive not specified in settings file")
            logger.info("Setting number of models to keep to 3 (default)")
            models_to_keep = 3
    else:
        logger.info(
            f"Number of models to keep alive inferred from settings file ({models_to_keep})"
        )
        models_to_keep = int(models_to_keep)

    alive_models_with_version_number = client.functions.list(
        external_id_prefix=function_name + "-"
    )

    external_ids = [func.external_id for func in alive_models_with_version_number]

    if models_to_keep >= len(external_ids):
        logger.info(
            f"Number of alive models ({len(external_ids)}) fewer than/equal to the number of models to keep alive ({models_to_keep}). Skipping garbage collection."
        )
    elif keep_all_models is True:
        logger.info(
            f"Keeping all model versions ({len(external_ids)}) alive in {env} as specified in the settings file"
        )
    else:
        logger.info(
            f"Starting garbage collection of model {c.human_friendly_model_name} in {env}"
        )

        external_ids_sorted = [
            function_name + "-" + str(v)
            for v in sorted(
                [int(external_id.split("-")[-1]) for external_id in external_ids]
            )
        ]

        num_models_to_delete = len(external_ids) - models_to_keep
        external_ids_to_delete = external_ids_sorted[:num_models_to_delete]

        for external_id in external_ids_to_delete:
            version = external_id.split("-")[-1]
            logger.info(f"Deleting version {version} of model {c.model_name} in {env}")
            cdf.delete_function(function_name=external_id, confirm=False)


def setup_schedule_for_latest_model_in_prod(
    c: ServiceSettings, predictable_external_id: str, client: CogniteClient
) -> None:
    schedules = client.functions.schedules.list(
        function_external_id=predictable_external_id,
    )
    if len(schedules) > 0:
        logger.info("A schedule already exist and will be overwritten")
        for schedule in schedules:
            schedule_id = schedule.id
            client.functions.schedules.delete(id=schedule_id)

    _ = client.functions.schedules.create(
        name="Keep warm schedule",
        description="Keep the function warm by calling it with an empty payload every 30 minutes during extended working hours on weekdays",
        cron_expression="*/30 5-17 * * 1-5",
        function_external_id=predictable_external_id,
        data={},
    )
    logger.info("Schedule created")
