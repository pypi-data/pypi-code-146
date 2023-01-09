"""Outdated Python tool class"""

import shlex
from datetime import datetime

from eze.core.enums import (
    VulnerabilityType,
    VulnerabilitySeverityEnum,
    ToolType,
    SourceType,
    Vulnerability,
    LICENSE_CHECK_CONFIG,
    LICENSE_ALLOWLIST_CONFIG,
    LICENSE_DENYLIST_CONFIG,
)
from eze.core.tool import (
    ToolMeta,
    ScanResult,
)
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.error import EzeError
from eze.utils.io.file_scanner import find_files_by_name
from eze.utils.log import log_debug
from eze.utils.io.http import request_json
from eze.utils.io.file import load_json
from pydash import py_
from eze.utils.language.python import get_poetry_projects, get_piplock_projects, get_requirements_projects
from eze.utils.cli.exe import exe_variable_interpolation_single


class PythonOutdatedTool(ToolMeta):
    """Python Outdated tool class"""

    TOOL_NAME: str = "python-outdated"
    TOOL_URL: str = "https://pip.pypa.io/en/stable/cli/"
    TOOL_TYPE: ToolType = ToolType.SCA
    SOURCE_SUPPORT: list = [SourceType.PYTHON]
    SHORT_DESCRIPTION: str = "inbuilt python outdated dependency scanner"
    INSTALL_HELP: str = """This is an Eze in-built tool, so no installation needed."""
    MORE_INFO: str = """By using the native pip with the command list we can retrive the info of your dependencies, and verify they aren't old and out of date.
This is important as old dependencies won't necessarily be actively supported
and can contain hidden vulnerabilities.

Common Gotchas
===========================
Pip Freezing

A Outdated expects exact version numbers. Therefore requirements.txt must be frozen. 

This can be accomplished via:

$ pip freeze > requirements.txt
"""
    # https://github.com/CycloneDX/cyclonedx-python/blob/master/LICENSE
    LICENSE: str = """Apache-2.0"""
    VERSION_CHECK: dict = {
        "FROM_EXE": "cyclonedx-py",
        "FROM_PIP": "cyclonedx-bom",
        "FROM_DOCKER_IMAGE": "cyclonedx/cyclonedx-python:3.10.1",
    }

    EZE_CONFIG: dict = {
        "REQUIREMENTS_FILES": {
            "type": list,
            "default": [],
            "help_text": """surplus custom requirements.txt file
        any requirements files named requirements.txt or requirements-dev.txt will be automatically collected
        gotcha: make sure it's a frozen version of the pip requirements""",
            "help_example": "[custom-requirements.txt]",
        },
        "HIGH_SEVERITY_AGE_THRESHOLD": {
            "type": int,
            "default": 1095,
            "help_text": """number of days before a out of date dependency is moved to High Risk
        default 1095 (three years)""",
        },
        "MEDIUM_SEVERITY_AGE_THRESHOLD": {
            "type": int,
            "default": 730,
            "help_text": """number of days before a out of date dependency is moved to Medium Risk
        default 730 (two years)""",
        },
        "LOW_SEVERITY_AGE_THRESHOLD": {
            "type": int,
            "default": 182,
            "help_text": """number of days before a out of date dependency is moved to Low Risk
        default is 182 (half a year)""",
        },
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_python-outdated-report.json",
            "default_help_value": "<cwd>.eze/raw/_python-outdated-report.json",
            "help_text": "output report location",
        },
        "INCLUDE_DEV": {
            "type": bool,
            "default": False,
            "help_text": "Exclude test / development dependencies from the BOM",
        },
        "LICENSE_CHECK": LICENSE_CHECK_CONFIG.copy(),
        "LICENSE_ALLOWLIST": LICENSE_ALLOWLIST_CONFIG.copy(),
        "LICENSE_DENYLIST": LICENSE_DENYLIST_CONFIG.copy(),
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("cyclonedx-py --format=json --force"),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "IMAGE_NAME": "cyclonedx/cyclonedx-python:3.10.1",
                "BASE_COMMAND": "--format=json --force",
            },
            "FLAGS": {
                "PACKAGE_FILE": "-i=",
                "REPORT_FILE": "-o=",
            },
            # eze config fields -> flags
            "SHORT_FLAGS": {"REQUIREMENTS_FILE": "-r", "PIPLOCK_FILE": "-pip", "POETRY_FILE": "-p"},
        }
    }

    def extract_name_and_version(self, cyclonedx_components: list) -> list:
        return [{"name": x["name"], "version": x["version"]} for x in cyclonedx_components]

    async def run_individual_scan(self, settings) -> list:
        """run individual scan of cyclonedx"""
        warnings = []
        scan_config = self.config.copy()
        scan_config = {**scan_config, **settings}

        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME
        )
        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        cyclonedx_bom: dict = load_json(report_local_filepath)
        if completed_process.stderr:
            warnings.append(completed_process.stderr)
        return [warnings, self.extract_name_and_version(py_.get(cyclonedx_bom, "components", []))]

    async def run_scan(self) -> ScanResult:
        """
        Run scan using tool

        typical steps
        1) setup config
        2) run tool
        3) parse tool report & normalise into common format

        :raises EzeError
        """
        requirements_files: list = get_requirements_projects()
        if self.config["INCLUDE_DEV"]:
            requirements_files.extend(find_files_by_name("^requirements-dev.txt$"))
        requirements_files.extend(self.config["REQUIREMENTS_FILES"])
        poetry_files = get_poetry_projects()
        piplock_files = get_piplock_projects()
        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])

        components = []
        warnings_list: list = []

        for requirements_file in requirements_files:
            [warnings, file_components] = await self.run_individual_scan(
                {
                    "PACKAGE_FILE": "__ABSOLUTE_CWD__" + requirements_file,
                    "REQUIREMENTS_FILE": True,
                    "REPORT_FILE": self.config["REPORT_FILE"],
                }
            )
            components.extend([{**component, "file": requirements_file} for component in file_components])
            warnings_list.extend(warnings)

        for poetry_file in poetry_files:
            log_debug(f"run 'cyclonedx-py' on {poetry_file}")
            [warnings, file_components] = await self.run_individual_scan(
                {"PACKAGE_FILE": poetry_file, "POETRY_FILE": True, "REPORT_FILE": self.config["REPORT_FILE"]}
            )
            warnings_list.extend(warnings)
            components.extend([{**component, "file": poetry_file} for component in file_components])

        for piplock_file in piplock_files:
            log_debug(f"run 'cyclonedx-py' on {piplock_file}")
            [warnings, file_components] = await self.run_individual_scan(
                {"PACKAGE_FILE": piplock_file, "PIPLOCK_FILE": True, "REPORT_FILE": self.config["REPORT_FILE"]}
            )
            warnings_list.extend(warnings)
            components.extend([{**component, "file": piplock_file} for component in file_components])

        report = self.parse_report(components, warnings_list)

        return report

    def get_recommendation_by_age(
        self, outdated_package: str, installed_version: str, latest_version: str, package_outdated_in_days: int
    ):
        """get recommendation to update a package by number of days out current version is"""
        recommendation = f"{outdated_package} ({installed_version}) {package_outdated_in_days} days out of date. Update to a newer version, latest version: {latest_version}"
        return recommendation

    def get_severity_by_age(self, package_outdated_in_days: int):
        """get the severity by number of days out current version is"""
        if (
            self.config["HIGH_SEVERITY_AGE_THRESHOLD"]
            and self.config["HIGH_SEVERITY_AGE_THRESHOLD"] <= package_outdated_in_days
        ):
            return VulnerabilitySeverityEnum.high.name
        if (
            self.config["MEDIUM_SEVERITY_AGE_THRESHOLD"]
            and self.config["MEDIUM_SEVERITY_AGE_THRESHOLD"] <= package_outdated_in_days
        ):
            return VulnerabilitySeverityEnum.medium.name
        if (
            self.config["LOW_SEVERITY_AGE_THRESHOLD"]
            and self.config["LOW_SEVERITY_AGE_THRESHOLD"] <= package_outdated_in_days
        ):
            return VulnerabilitySeverityEnum.low.name
        return ""

    def get_dependency_data_from_api(self, dependency_name, current):
        """call the api to extract the data (published date) of a given dependency"""

        warnings = []
        pypi_dep_url = f"https://pypi.org/pypi/{dependency_name}/json"
        dependency_data = {}

        try:
            log_debug(f"api request for dependency {dependency_name}")
            dependency_data = request_json(pypi_dep_url, method="GET")
        except EzeError as error:
            warnings.append(f"unable to get dependency data for {dependency_name}, Error: {error}")

        current_date = self.get_version_data(current, dependency_data, dependency_name)["upload_time"]
        latest_version = py_.get(dependency_data["info"], "version", None)
        latest_date = self.get_version_data(latest_version, dependency_data, dependency_name)["upload_time"]

        return current_date, latest_date, latest_version

    def get_version_data(self, version, dependency_data: dict, dependency_name: str) -> dict:
        """extract the information for a specific version given the dependency data"""
        releases: dict = dependency_data["releases"]
        if version not in releases and version[-2:] == ".0":
            version = version[:-2]
        if version not in releases:
            raise Exception(
                f"'{dependency_name}' version {version} does not exist. Possible versions are: {list(releases.keys())}"
            )
        return py_.get(releases[version], 0, None)

    def parse_report(self, dependencies: list, warnings: list) -> ScanResult:
        """convert report json into ScanResult"""

        vulnerabilities_list: list = []
        for dependency in dependencies:
            try:
                outdated_package = py_.get(dependency, "name")
                installed_version = py_.get(dependency, "version", "")
                file_location = py_.get(dependency, "file", "")
                installed_version_date, latest_version_date, latest_version = self.get_dependency_data_from_api(
                    outdated_package, installed_version
                )

                package_outdated_in_days = abs(
                    (
                        datetime.strptime(installed_version_date, "%Y-%m-%dT%H:%M:%S")
                        - datetime.strptime(latest_version_date, "%Y-%m-%dT%H:%M:%S")
                    ).days
                )

                age_severity = self.get_severity_by_age(package_outdated_in_days)
                if age_severity:
                    age_recommendation = self.get_recommendation_by_age(
                        outdated_package, installed_version, latest_version, package_outdated_in_days
                    )
                    vulnerability_raw = {
                        "vulnerability_type": VulnerabilityType.dependency.name,
                        "name": outdated_package,
                        "version": installed_version,
                        "overview": f"package: {outdated_package} is out of date",
                        "recommendation": age_recommendation,
                        "severity": age_severity,
                        "file_location": {"path": file_location},
                        "identifiers": {},
                        "metadata": {},
                    }
                    vulnerability = Vulnerability(vulnerability_raw)
                    vulnerabilities_list.append(vulnerability)
            except Exception as error:
                warnings.append(str(error))

        report = ScanResult(
            {
                "tool": self.TOOL_NAME,
                "vulnerabilities": vulnerabilities_list,
                "warnings": warnings,
            }
        )

        return report
