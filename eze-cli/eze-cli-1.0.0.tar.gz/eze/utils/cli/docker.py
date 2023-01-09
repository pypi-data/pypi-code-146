"""
tools for docker execution

NORMAL COMMAND CLI
=================================
{
    # tool command prefix
    "BASE_COMMAND": shlex.split("semgrep --optimizations all --json --timeout --disable-metrics -q "),
    # eze config fields -> arguments
    "ARGUMENTS": ["SOURCE"],
    # eze config fields -> flags
    "FLAGS": {
        "CONFIGS": "--config ",
        "REPORT_FILE": "--output ",
        "INCLUDE": "--include ",
        "EXCLUDE": "--exclude ",
    },
    "SHORT_FLAGS": {"USE_GIT_IGNORE": "--use-git-ignore"},
}


DOCKER COMMAND CLI
=================================
{
    # tool command prefix
    "DOCKER_COMMAND": {
        "ENV_VARS": {
            'xxx': 'foo'
        }
        "FOLDERS": {
            '/xxx': '__ABSOLUTE_CWD__.xxx/xxx'
        }
        "FOLDER_NAME": "/src",
        "WORKING_FOLDER": "/src",
        "IMAGE_NAME": "returntocorp/semgrep",
        "BASE_COMMAND": "semgrep scan --json --quiet ."
    },
    # eze config fields -> arguments
    "ARGUMENTS": ["SOURCE"],
    # eze config fields -> flags
    "FLAGS": {
        "CONFIGS": "--config ",
        "REPORT_FILE": "--output ",
        "INCLUDE": "--include ",
        "EXCLUDE": "--exclude ",
    },
    "SHORT_FLAGS": {"USE_GIT_IGNORE": "--use-git-ignore"},
}

COMBINED COMMAND CLI
=================================
{
    # tool command prefix
    "BASE_COMMAND": shlex.split("semgrep --optimizations all --json --timeout --disable-metrics -q "),
    "DOCKER_COMMAND": {
        "FOLDERS": {
            '/xxx': '__ABSOLUTE_CWD__.xxx/xxx'
        }
        "FOLDER_NAME": "/src",
        "WORKING_FOLDER": "/src",
        "IMAGE_NAME": "returntocorp/semgrep",
        "BASE_COMMAND": "semgrep scan --json --quiet ."
    },
    # eze config fields -> arguments
    "ARGUMENTS": ["SOURCE"],
    # eze config fields -> flags
    "FLAGS": {
        "CONFIGS": "--config ",
        "REPORT_FILE": "--output ",
        "INCLUDE": "--include ",
        "EXCLUDE": "--exclude ",
    },
    "SHORT_FLAGS": {"USE_GIT_IGNORE": "--use-git-ignore"},
}

"""

import shlex
from copy import deepcopy

from pydash import py_

from eze.utils.log import log_error
from eze.utils.io.file import normalise_linux_file_path, normalise_windows_double_escape_file_path
from eze.utils.cli.exe import exe_variable_interpolation_single


def create_docker_config(cli_config: dict, source_folder: str = None):
    """this will take a cli config, and convert it to run the docker command contained"""
    docker_config = deepcopy(cli_config)
    if "DOCKER_COMMAND" not in docker_config:
        return None
    base_command: str = "docker run --rm"
    # mount folders
    if "FOLDERS" in docker_config["DOCKER_COMMAND"]:
        for docker_path, local_path_expression in docker_config["DOCKER_COMMAND"]["FOLDERS"].items():
            local_path = exe_variable_interpolation_single(local_path_expression)
            local_path_normalised: str = normalise_windows_double_escape_file_path(local_path)
            base_command += f" -v {local_path_normalised}:{docker_path}"
    # add enviornment variables
    if "ENV_VARS" in docker_config["DOCKER_COMMAND"]:
        for key, value in docker_config["DOCKER_COMMAND"]["ENV_VARS"].items():
            base_command += f" -e {key}={value}"
    # mount folder name
    if "FOLDER_NAME" in docker_config["DOCKER_COMMAND"]:
        base_command += f" -v {source_folder}:{docker_config['DOCKER_COMMAND']['FOLDER_NAME']}"
    # set working folder name
    if "WORKING_FOLDER" in docker_config["DOCKER_COMMAND"]:
        base_command += f" -w {docker_config['DOCKER_COMMAND']['WORKING_FOLDER']}"
    # add docker image
    if "IMAGE_NAME" in docker_config["DOCKER_COMMAND"]:
        base_command += f" {docker_config['DOCKER_COMMAND']['IMAGE_NAME']}"
    else:
        log_error("IMAGE_NAME is missing !")
    if "BASE_COMMAND" in docker_config["DOCKER_COMMAND"]:
        base_command += f" {docker_config['DOCKER_COMMAND']['BASE_COMMAND']}"
    docker_config["BASE_COMMAND"] = shlex.split(base_command)
    docker_config.pop("DOCKER_COMMAND")
    return docker_config


def docker_variable_interpolation(command_list: list, docker_config: dict) -> list:
    """swap out variables for docker equivalents

    aka
    __ABSOLUTE_CWD__
    __TEMP_DIRECTORY__
    """
    for index, value in enumerate(command_list):
        command_list[index] = docker_variable_interpolation_single(value, docker_config)
    return command_list


def docker_variable_interpolation_single(command: str, docker_config: dict) -> str:
    """swap out variables for docker equivalents

    aka
    __ABSOLUTE_CWD__
    __TEMP_DIRECTORY__
    __CACHED_WORKSPACE__ path to docker's mounted working folder created by file_scanner::cache_workspace_into_tmp()
                         expected to be mounted to /tmp/cached_workspace/
    """
    docker_variables: dict = {
        "__ABSOLUTE_CWD__": "CUSTOM_LOGIC",
        "__TEMP_DIRECTORY__": "CUSTOM_LOGIC",
        "__CACHED_WORKSPACE__": "CUSTOM_LOGIC",
    }
    for var_key, var_value in docker_variables.items():
        if var_key in command:
            if var_key == "__ABSOLUTE_CWD__":
                docker_cwd: str = py_.get(docker_config, "DOCKER_COMMAND.FOLDER_NAME", "") + "/"
                command = command.replace(var_key, docker_cwd)
                command = normalise_linux_file_path(command)
            if var_key == "__TEMP_DIRECTORY__":
                intermediate_file_path: str = py_.get(docker_config, "DOCKER_COMMAND.INTERMEDIATE_FILE", "")
                command = normalise_linux_file_path(intermediate_file_path)
            if var_key == "__CACHED_WORKSPACE__":
                docker_cwd: str = "/tmp/cached_workspace/"
                command = command.replace(var_key, docker_cwd)
                command = normalise_linux_file_path(command)
            else:
                command = command.replace(var_key, var_value)
    return command
