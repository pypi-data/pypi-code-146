"""
tools for for local execution
"""
import re
from pathlib import Path

from eze.utils.io.file import create_absolute_path, create_tempfile_path, get_filename
from eze.utils.io.file_scanner import cache_workspace_into_tmp


def exe_variable_interpolation(command_list: list) -> list:
    """swap out variables for docker equivalents

    aka
    __ABSOLUTE_CWD__ - current working directory
    __TEMP_DIRECTORY__ - temporary directory
    __CACHED_WORKSPACE__ - path to working folder created by file_scanner::cache_workspace_into_tmp()
    """
    for index, value in enumerate(command_list):
        command_list[index] = exe_variable_interpolation_single(value)
    return command_list


def exe_variable_interpolation_single(command: str) -> str:
    """swap out variables for docker equivalents

    aka
    __ABSOLUTE_CWD__ - current working directory
    __TEMP_DIRECTORY__ - temporary directory
    __CACHED_WORKSPACE__ - path to working folder created by file_scanner::cache_workspace_into_tmp()
    """
    if not command:
        return command
    exe_variables: dict = {
        "__ABSOLUTE_CWD__": "CUSTOM_LOGIC",
        "__TEMP_DIRECTORY__": "CUSTOM_LOGIC",
        "__CACHED_WORKSPACE__": "CUSTOM_LOGIC",
    }
    for var_key, var_value in exe_variables.items():
        if var_key in command:
            if var_key == "__ABSOLUTE_CWD__":
                command = re.sub(
                    "__ABSOLUTE_CWD__(.*)$", lambda match: str(create_absolute_path(match.group(1))), command
                )
            if var_key == "__TEMP_DIRECTORY__":
                command = str(create_tempfile_path(get_filename(command)))
            if var_key == "__CACHED_WORKSPACE__":
                local_cached_path: Path = cache_workspace_into_tmp()
                command = re.sub(
                    "__CACHED_WORKSPACE__(.*)$",
                    lambda match: str(
                        Path.joinpath(local_cached_path / match.group(1)) if match.group(1) else local_cached_path
                    ),
                    command,
                )
            else:
                command = command.replace(var_key, var_value)
    return command


def _join_paths(part1: Path, part2: str) -> Path:
    if not part2:
        return part1
    return Path.joinpath(part1 / Path(part2))
