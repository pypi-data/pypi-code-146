"""
test_service.py

Generic test for services (training or prediction). Set up the service folder
(copy model code, download model artifact if necessary), install model
dependencies and set current working directory to service folder, then run:
python -m akerbp.mlops.services.test_service
"""
import json
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from typing import Union, Tuple, Dict, Any
import logging
from logging import config as logging_config
from akerbp.mlops.core import config
from akerbp.mlops.core.logger_config import LOGGING_CONFIG

service_name = config.envs.service_name

logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.captureWarnings(True)

api_keys = config.api_keys


def mock_saver(*args, **kwargs):
    pass


def run_tests(test_path: Union[Path, str], path_type: str = "file") -> None:
    """
    Run tests with pytest. Raises exception subprocess.CalledProcessError
    if pytest fails.

    Input
      - test_path: path to tests with pytest (string or a list of strings) All
        should have the same format (see next parameter)
      - path_type: either 'file' (test_path refers then to files/folders) or
        'module' (test_path refers then to modules)

    """
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--quiet",
        "-o",
        "log_cli=true",
        "--color=no",
        "-W ignore:numpy.ufunc size changed",
    ]
    if path_type == "module":
        command.append("--pyargs")
    if isinstance(test_path, str) or isinstance(test_path, Path):
        command.append(str(test_path))
    elif isinstance(test_path, list):
        command += test_path
    else:
        raise ValueError("Input should be string or list of strings")
    logger.info(f"Run tests: {test_path}")
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command exited with error {e.stdout}") from e


def get_model_test_data(test_import_path: str) -> Tuple[Dict, bool]:
    """
    Read input and validation function from the model test file
    """
    service_test = import_module(test_import_path).ServiceTest()
    input = getattr(service_test, f"{service_name}_input")
    check = getattr(service_test, f"{service_name}_check")
    return input, check


def test_service(input: Dict, check: Any) -> None:
    """
    Generic service test. Call service with the model's test input data and
    validate the output.
    """
    logger.info(f"Test {service_name} service")
    service = import_module(f"akerbp.mlops.services.{service_name}").service

    if service_name == "training":
        response = service(data=input, secrets=api_keys, saver=mock_saver)
    elif service_name == "prediction":
        response = service(data=input, secrets=api_keys)
    else:
        raise Exception("Unknown service name")

    assert response["status"] == "ok"
    # assert check(response[service_name])


if __name__ == "__main__":
    logging_config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name="akerbp.mlops.services.test_service.py")
    logging.captureWarnings(True)

    c = config.read_service_settings()
    run_tests(c.test_file)
    input, check = get_model_test_data(c.test_import_path)
    test_service(input, check)
    # Share input with main process:
    print(json.dumps(input))
