"""Basic cli helpers utils

handles detecting versions of tools
"""
import asyncio
import re
from pathlib import Path

from eze.utils.cli.run import run_cmd, cmd_exists, has_missing_exe_output, build_cli_command, CompletedProcess
from eze.utils.semvar import is_semvar
from eze.utils.cli.docker import create_docker_config
from eze.utils.language.java import run_mvn_command


def extract_cmd_version(
    command: list, *, ignored_errors_list: list = None, combine_std_out_err: bool = False, allowed_stderr: bool = False
) -> str:
    """
    Run cmd and extract version number from output
    """
    completed_process: CompletedProcess = run_cmd(command, False)
    output: str = completed_process.stdout
    error_output: str = completed_process.stderr
    if has_missing_exe_output(output):
        return ""
    if combine_std_out_err:
        output += error_output
        error_output = ""
    version = _extract_version(output)
    is_acceptable_stderr = (
        not error_output or allowed_stderr or _contains_list_element(error_output, ignored_errors_list)
    )
    is_valid_version = is_semvar(version) or version != output
    if not is_valid_version or not is_acceptable_stderr:
        version = ""
    return version


def extract_version_from_maven(mvn_package: str) -> str:
    """
    Check maven package metadata and checks for Maven version
    """
    ignored_errors_list = ["WARNING: An illegal reflective access operation has occurred"]
    (completed_process, used_docker_mvn) = asyncio.run(
        run_mvn_command(f"mvn -B -Dplugin={mvn_package} help:describe", str(Path.cwd()))
    )
    output: str = completed_process.stdout
    version: str = _extract_maven_version(output)
    error_output = completed_process.stderr
    if used_docker_mvn:
        version = version + " (docker)"
    is_acceptable_stderr = not error_output or _contains_list_element(error_output, ignored_errors_list)
    if not version or not is_acceptable_stderr:
        version = ""
    return version


def detect_pip_executable_version(pip_package: str, cli_command: str) -> str:
    """Check pip package metadata and check for pip version"""
    # 1. detect tool on command line
    # 2. detect version via pip
    #
    # 1. detect if tool on command line
    executable_path = cmd_exists(cli_command)
    if not executable_path:
        return ""
    # 2. detect version via pip, to see what version is installed on cli
    version = _extract_version_from_pip(pip_package)
    if not version:
        return "Non-Pip version Installed"
    return version


def detect_docker_version(
    docker_to_check: dict,
    *,
    ignored_errors_list: list = None,
    combine_std_out_err: bool = False,
    allowed_stderr: bool = False,
) -> str:
    """Check docker package metadata"""
    # 1. detect tool on command line
    # 2. detect version via pip
    #
    # 1. detect if tool on command line
    executable_path = cmd_exists("docker")
    if not executable_path:
        return ""
    # 2. detect version via docker, to see what version is installed on cli
    command_list: list = _build_docker_command(docker_to_check, {})
    version: str = extract_cmd_version(
        command_list,
        ignored_errors_list=ignored_errors_list,
        combine_std_out_err=combine_std_out_err,
        allowed_stderr=allowed_stderr,
    )
    if version:
        version += " (docker)"
    return version


def extract_docker_image_version(docker_image: str) -> str:
    """Check docker package metadata"""
    version_match = re.match(".*[:]([0-9a-zA-Z-.]+)$", docker_image)
    if not version_match:
        return ""
    return version_match.group(1) + " (docker)"


def _extract_version(value: str) -> str:
    """Take output and check for common version patterns"""
    version_matcher = re.compile("[0-9]+[.]([0-9]+[.]?:?)+")
    version_str = re.search(version_matcher, value)
    if version_str:
        return value[version_str.start() : version_str.end()]
    return value


def _contains_list_element(text: str, element_list: list = None) -> bool:
    """checks if given text contains list element"""
    if not element_list:
        return False
    for element in element_list:
        if element in text:
            return True
    return False


def _build_docker_command(docker_config: dict, config: dict = None) -> list:
    """build command line docker command"""
    if not config:
        config = {}
    docker_config: dict = create_docker_config(docker_config, None)
    command_list: list = build_cli_command(docker_config, config)
    return command_list


def _extract_maven_version(value: str) -> str:
    """Take Maven output and checks for version patterns"""
    leading_number_regex = re.compile("Version: ([0-9].[0-9](.[0-9])?)")
    leading_number = re.search(leading_number_regex, value)
    if leading_number is None:
        return ""
    return leading_number.group(1)


def _extract_version_from_pip(pip_package: str) -> str:
    """Run pip for package and check for common version patterns"""
    pip_command = _detect_pip_command()
    return extract_cmd_version([pip_command, "show", pip_package])


def _detect_pip_command() -> str:
    """Run pip3 and pip to detect which is installed"""
    version = extract_cmd_version(["pip3", "--version"])
    if version:
        return "pip3"
    version = extract_cmd_version(["pip", "--version"])
    if version:
        return "pip"
    # unable to find pip, default to pip
    return "pip"
