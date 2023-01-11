from io import BytesIO
from pathlib import Path
import pickle
import requests

import tarfile
from typing import Any, List, Dict, Optional

from cinnaroll_internal.constants import (
    API_KEY_HEADER_KEY,
    BACKEND_BASE_URL,
)

from cinnaroll_internal.environment_check import get_api_key
from cinnaroll_internal import environment_info, constants
from cinnaroll_internal import rollout_config
from cinnaroll_internal.io_formats import JSON, FILE, IMG


INFER_FUNC_SOURCE_CODE_FILENAME = "infer"
REQUIREMENTS_FILENAME = "requirements"
MODEL_INPUT_SAMPLE_FILENAME = "model_input_sample"
INFER_FUNC_INPUT_SAMPLE_FILENAME = "infer_func_input_sample"


class SizeLimitExceededError(Exception):
    ...


MEGABYTE = 1024 * 1024

TEXT_MAX_LENGTH = 10000
BYTES_MAX_SIZE = round(10 * MEGABYTE)
ARTIFACT_MAX_SIZE = round(500 * MEGABYTE)


def check_size_limits(
    infer_py_file_content: str,
    model_input_sample: Any,
    infer_func_input_sample: str,
    infer_func_input_format: str,
) -> List[Exception]:

    errors: List[Exception] = []

    if len(infer_py_file_content) > TEXT_MAX_LENGTH:
        errors.append(
            SizeLimitExceededError(
                f"Infer function source code exceeds the current size limit of {TEXT_MAX_LENGTH} characters"
            )
        )

    if len(pickle.dumps(model_input_sample)) > BYTES_MAX_SIZE:
        errors.append(
            SizeLimitExceededError(
                f"Model input sample exceeds the current size limit of {BYTES_MAX_SIZE} bytes"
            )
        )

    if infer_func_input_format == JSON:
        if len(infer_func_input_sample) > TEXT_MAX_LENGTH:
            errors.append(
                SizeLimitExceededError(
                    f"Infer function input sample exceeds the current size limit of {TEXT_MAX_LENGTH} characters"
                )
            )
    elif infer_func_input_format in (FILE, IMG):
        if Path(infer_func_input_sample).stat().st_size > BYTES_MAX_SIZE:
            errors.append(
                SizeLimitExceededError(
                    f"Infer function input sample exceeds the current size limit of {BYTES_MAX_SIZE} bytes"
                )
            )

    return errors


def prepare_artifact(
    artifact_path: Path,
    model_path: Path,
    infer_func_source_code: str,
    infer_func_global_variables: Dict[str, Any],
    requirements: List[str],
    model_input_sample: Any,
    infer_func_input_sample: str,
    infer_func_input_format: str,
) -> List[Exception]:
    def _process_requirements(r: List[str]) -> str:
        """
        In requirements:
        * replace tensorflow-macos and tensorflow-cpu with tensorflow,
        * cut out cinnaroll.
        Return a string which can be written to a file.
        """
        cinnaroll_index: Optional[int] = None
        for index, x in enumerate(r):
            if "tensorflow-macos" in x:
                r[index] = x.replace("tensorflow-macos", "tensorflow")
            if "tensorflow-cpu" in x:
                r[index] = x.replace("tensorflow-cpu", "tensorflow")
            if "cinnaroll" in x:
                cinnaroll_index = index
        if cinnaroll_index:
            r.pop(cinnaroll_index)

        return "\n".join(r)

    errors: List[Exception] = []

    # We are working under the assumption that infer_func_input_sample is always a string. This can either be a
    # JSON-formatted string or a path to a file. Then:
    # - if input_format is "json", then we will save infer_func_input_sample string to a text file
    # with standardised name and extension .json
    # - if input_format is "img" or "file", then input_sample is a path to a file, and we will just copy that file
    # into the artifact, we give it a new standardised name, but we keep the original extension

    # key = filename, val = (content, content_type)
    files = {
        INFER_FUNC_SOURCE_CODE_FILENAME: (infer_func_source_code, "py"),
        constants.GLOBAL_VARS_DICT_FILENAME: (
            infer_func_global_variables,
            "pickle",
        ),
        REQUIREMENTS_FILENAME: (_process_requirements(requirements), "txt"),
        MODEL_INPUT_SAMPLE_FILENAME: (model_input_sample, "pickle"),
        INFER_FUNC_INPUT_SAMPLE_FILENAME: (
            infer_func_input_sample,
            infer_func_input_format,
        ),
    }

    with tarfile.open(artifact_path, "w:gz") as tar:
        tar.add(model_path, arcname=model_path.name)

        for key, val in files.items():
            if val[1] in (JSON, "py", "pickle", "txt"):
                if val[1] == "pickle":
                    file_obj = BytesIO(pickle.dumps(val[0]))
                else:
                    s = f"{val[0]}\n"
                    print(f"Length of string: {len(s)}")
                    file_obj = BytesIO(f"{val[0]}\n".encode("utf-8"))

                tar_info = tarfile.TarInfo(name=f"{key}.{val[1]}")
                tar_info.size = len(file_obj.getbuffer())
                print(f"{key}: {tar_info.size} B")
                tar.addfile(tarinfo=tar_info, fileobj=file_obj)
            elif val[1] in (FILE, IMG):
                tar.add(val[0], arcname=f"{key}{Path(val[0]).suffix}")

    if artifact_path.stat().st_size > ARTIFACT_MAX_SIZE:
        errors.append(
            SizeLimitExceededError(
                f"Prepared artifact exceeds the current size limit of {ARTIFACT_MAX_SIZE} bytes."
            )
        )

    return errors


def send_rollout_data(
    config: rollout_config.RolloutConfig,
    framework: str,
    user_environment_info: environment_info.EnvironmentInfo,
    model_metadata: Dict[str, str],
) -> requests.Response:

    rollout_data = {
        "projectId": config.project_id,
        "modelName": config.model_name,
        "framework": framework,
        "frameworkVersion": user_environment_info.framework_version,
        "pythonVersion": ".".join(map(str, user_environment_info.python_version[:3])),
        "metrics": config.metrics,
        "metadata": model_metadata,
        "inputFormat": config.infer_func_input_format,
        "outputFormat": config.infer_func_output_format,
    }

    url = f"{BACKEND_BASE_URL}/modelUploads/"
    headers = {API_KEY_HEADER_KEY: get_api_key()}
    res = requests.post(url, headers=headers, json=rollout_data)
    return res


def upload_artifact(artifact_path: Path, upload_url: str) -> requests.Response:
    with open(artifact_path, "rb") as f:
        data = f.read()
    res = requests.put(upload_url, data=data)
    return res


def notify_server(upload_id: str, status: str) -> requests.Response:
    url = f"{BACKEND_BASE_URL}/modelUploads/{upload_id}"
    headers = {API_KEY_HEADER_KEY: get_api_key()}
    res = requests.put(url, headers=headers, json={"status": status})
    return res
