"""TruffleHog v3 Python tool class"""
import json
import re
import shlex
import time
from pathlib import Path

from pydash import py_

from eze.core.enums import VulnerabilityType, VulnerabilitySeverityEnum, ToolType, SourceType, Vulnerability
from eze.core.tool import (
    ToolMeta,
    ScanResult,
)
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import (
    write_json,
)
from eze.utils.log import log

from eze.utils.io.file_scanner import cache_workspace_into_tmp
from eze.utils.cli.exe import exe_variable_interpolation_single
from eze.utils.git import get_compiled_gitignore_regexes, is_file_gitignored
from typing import List


def extract_leading_number(value: str) -> str:
    """Take output and check for common version patterns"""
    leading_number_regex = re.compile("^[0-9.]+")
    leading_number = re.search(leading_number_regex, value)
    if leading_number:
        return value[leading_number.start() : leading_number.end()]
    return ""


class TruffleHogTool(ToolMeta):
    """TruffleHog v3 Python tool class"""

    MAX_REASON_SIZE: int = 1000

    TOOL_NAME: str = "trufflehog-v3"
    TOOL_URL: str = "https://trufflesecurity.com/"
    TOOL_TYPE: ToolType = ToolType.SECRET
    SOURCE_SUPPORT: list = [SourceType.ALL]
    SHORT_DESCRIPTION: str = "opensource secret scanner"
    INSTALL_HELP: str = """Only needs docker
https://hub.docker.com/r/trufflesecurity/trufflehog/

Local GO exe can be installed, instructions on github
https://github.com/trufflesecurity/trufflehog
"""
    MORE_INFO: str = """https://github.com/trufflesecurity/trufflehog/

Tips
===============================
- false positives can be individually omitted with post fixing line with "# nosecret" and "// nosecret"
"""

    LICENSE: str = """GPL"""

    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": list,
            "default": ".",
            "required": True,
            "help_text": """TruffleHog v3 list of source folders to scan for secrets""",
        },
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_truffleHog-v3-report.json",
            "default_help_value": "<cwd>.eze/raw/_truffleHog-v3-report.json",
            "help_text": "output report location",
        },
        "USE_GIT_IGNORE": {
            "type": bool,
            "default": True,
            "help_text": """.gitignore ignore files specified added to EXCLUDE""",
        },
        "EXCLUDE": {
            "type": list,
            "default": [],
            "help_text": """array of regex str of folders/files to exclude from scan for secrets in .gitignore format
eze will automatically normalise folder separator "/" to os specific versions, "/" for unix, "\\\\" for windows""",
            "help_example": ["PATH-TO-EXCLUDED-FOLDER/**", ".secret"],
        },
    }
    DEFAULT_SEVERITY = VulnerabilitySeverityEnum.high.name

    VERSION_CHECK: dict = {
        "FROM_EXE": "trufflehog --version",
        "FROM_DOCKER": {
            "DOCKER_COMMAND": {"IMAGE_NAME": "trufflesecurity/trufflehog:3.21.0", "BASE_COMMAND": "--version"}
        },
        # #104 - TRUFFLEHOG outputs version string into stderr
        "COMBINE_STD_OUT_ERR": True,
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix.
            "BASE_COMMAND": shlex.split("trufflehog filesystem --directory=__CACHED_WORKSPACE__ --json"),
            "DOCKER_COMMAND": {
                "FOLDERS": {"/tmp/cached_workspace": "__CACHED_WORKSPACE__"},
                "FOLDER_NAME": "/src",
                "WORKING_FOLDER": "/tmp/cached_workspace",
                "IMAGE_NAME": "trufflesecurity/trufflehog:3.21.0",
                "BASE_COMMAND": "filesystem --directory=__CACHED_WORKSPACE__ --json",
            },
            # eze config fields -> flags
        }
    }

    async def run_scan(self) -> ScanResult:
        """
        Run scan using tool

        typical steps
        1) setup config
        2) run tool
        3) parse tool report & normalise into common format

        :raises EzeError
        """

        tic = time.perf_counter()

        scan_config = self.config.copy()
        cwd = cache_workspace_into_tmp()
        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME, cwd=cwd
        )

        toc = time.perf_counter()
        total_time = toc - tic
        if total_time > 10:
            log(
                f"trufflehog v3 scan took a long time ({total_time:0.2f}s), "
                f"you can often speed up trufflehog significantly by excluding dependency or binary folders like node_modules or sbin"
            )

        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        parsed_json: list = self._convert_json_lines_into_json_list(completed_process.stdout)
        write_json(report_local_filepath, parsed_json)
        report = self.parse_report(parsed_json)
        if completed_process.stderr:
            report.warnings.append(completed_process.stderr)

        return report

    def _convert_json_lines_into_json_list(self, json_strings_textblock: str) -> list:
        """given string of jsons on newlines, convert into python list of json objects"""
        return json.loads("[" + ",\n".join(json_strings_textblock.strip().split("\n")) + "]")

    def parse_report(self, parsed_json: list) -> ScanResult:
        """convert report json into ScanResult"""
        report_events = parsed_json
        vulnerabilities_list: list = []
        for report_event in report_events:
            if report_event != {}:
                vulnerability = self._trufflehog_line(report_event)
                vulnerabilities_list.append(vulnerability)
        vulnerabilities_list = self._remove_excluded_secrets(vulnerabilities_list)
        report: ScanResult = ScanResult(
            {
                "tool": self.TOOL_NAME,
                "vulnerabilities": vulnerabilities_list,
                "warnings": [],
            }
        )
        return report

    def _trufflehog_line(self, report_event):
        """trufflehog format parse support"""
        path: str = py_.get(report_event, "SourceMetadata.Data.Git.file")
        if not path:
            path = py_.get(report_event, "SourceMetadata.Data.Filesystem.file", "unknown")
        # normalise paths to be relative
        if path:
            local_cached_path: Path = cache_workspace_into_tmp()
            path = path.replace(str(local_cached_path), "")
            docker_cached_path: str = "/tmp/cached_workspace/"
            path = path.replace(docker_cached_path, "")
        line: str = py_.get(report_event, "SourceMetadata.Data.Git.line") or "1"
        location_str = path if line is None else path + ":" + str(line)
        detector_name = py_.get(report_event, "DetectorName", "")
        reason = f"Sensitive {detector_name}"

        name = f"Found Hardcoded '{reason}' Pattern"
        summary = f"Found Hardcoded '{reason}' Pattern in {path}"
        recommendation = (
            f"Investigate '{location_str}' for '{reason}' strings. (add '# nosecret' to line if false positive)"
        )

        line_containing_secret = report_event["Redacted"]
        if len(line_containing_secret) > self.MAX_REASON_SIZE:
            recommendation += f" Full Match: <on long line ({len(line_containing_secret)} characters)>"
        else:
            recommendation += " Full Match: " + line_containing_secret

        # TODO: assume medium as no severity is provided
        severity = "MEDIUM"

        return Vulnerability(
            {
                "vulnerability_type": VulnerabilityType.secret.name,
                "name": name,
                "version": None,
                "overview": summary,
                "recommendation": recommendation,
                "language": "file",
                "severity": severity,
                "identifiers": {},
                "metadata": None,
                "file_location": {"path": path, "line": line},
            }
        )

    def _remove_excluded_secrets(self, vulnerabilities_list: List[Vulnerability]) -> List[Vulnerability]:
        exclude_config: tuple = None
        if self.config["USE_GIT_IGNORE"]:
            exclude_config = get_compiled_gitignore_regexes(extra_paths=self.config["EXCLUDE"])

        def _is_secret_excluded(vulnerability: Vulnerability) -> bool:
            filepath: str = py_.get(vulnerability, "file_location.path")
            if self.config["USE_GIT_IGNORE"] and filepath:
                if is_file_gitignored(filepath, exclude_config):
                    return False
            return True

        return list(filter(_is_secret_excluded, vulnerabilities_list))
