"""helper functions for dealing with mvn and java issues"""

import re
import shlex

from eze.utils.io.file_scanner import find_files_by_name
from eze.utils.cli.run import run_async_cmd, CompletedProcess, has_missing_exe_output
from eze.utils.error import EzeExecutableNotFoundError
from eze.utils.cli.exe import exe_variable_interpolation_single
from eze.utils.io.file import normalise_windows_double_escape_file_path
from typing import Tuple

# TODO: handle multiple sdk versions
MAVEN_DOCKER_IMAGE: str = "maven:3.3-jdk-8"


def get_maven_projects() -> []:
    """give a list of maven projects"""
    pom_files: list = find_files_by_name("^pom.xml$")
    return pom_files


def is_groovy_errors(warning_text: str) -> bool:
    """detect https://issues.apache.org/jira/browse/GROOVY-8339 error messages"""
    return (
        not warning_text.startswith("WARNING: An illegal reflective access operation has occurred")
        and not warning_text.startswith("WARNING: Illegal reflective access by")
        and not warning_text.startswith("WARNING: Please consider reporting")
        and not warning_text.startswith("WARNING: All illegal access operations")
        and not warning_text.startswith("WARNING: Use --illegal-access=warn")
        and not re.match("^\\s*$", warning_text)
    )


def ignore_groovy_errors(warnings_text: str) -> list:
    """Ignore https://issues.apache.org/jira/browse/GROOVY-8339 error messages"""
    warnings = warnings_text.split("\n")
    without_groovy_warnings = [warning for warning in warnings if is_groovy_errors(warning)]
    return without_groovy_warnings


async def run_mvn_command(mvn_command: str, cwd: str) -> Tuple[CompletedProcess, bool]:
    """run dotnet local command with docker fallback"""
    try:
        completed_process: CompletedProcess = await run_async_cmd(shlex.split(mvn_command), True, cwd=cwd)
        output = completed_process.stdout
        if has_missing_exe_output(output):
            raise EzeExecutableNotFoundError("failed local mvn try docker")
        return completed_process, False
    except EzeExecutableNotFoundError as error:
        m2_filepath = exe_variable_interpolation_single("__ABSOLUTE_CWD__.eze/.m2")
        m2_filepath_normalised = normalise_windows_double_escape_file_path(m2_filepath)
        cwd_normalised: str = normalise_windows_double_escape_file_path(cwd)
        return (
            await run_async_cmd(
                shlex.split(
                    f"docker run --rm -v {m2_filepath_normalised}:/root/.m2 -v {cwd_normalised}:/src -w /src --rm {MAVEN_DOCKER_IMAGE} {mvn_command}"
                ),
                True,
                cwd=cwd,
            ),
            True,
        )
