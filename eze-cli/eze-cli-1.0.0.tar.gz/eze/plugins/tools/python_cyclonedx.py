"""cyclonedx SBOM tool class"""
import re
import shlex

from pydash import py_

from eze.utils.log import log_debug

from eze.utils.io.file_scanner import find_files_by_name

from eze.core.enums import (
    ToolType,
    SourceType,
    LICENSE_CHECK_CONFIG,
    LICENSE_ALLOWLIST_CONFIG,
    LICENSE_DENYLIST_CONFIG,
    VulnerabilityType,
    Vulnerability,
    VulnerabilitySeverityEnum,
)
from eze.core.tool import ToolMeta, ScanResult
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import load_json
from eze.utils.scan_result import convert_multi_sbom_into_scan_result
from eze.utils.data.pypi import pypi_sca_sboms
from eze.utils.language.python import get_requirements_projects, get_poetry_projects, get_piplock_projects
from eze.utils.cli.exe import exe_variable_interpolation_single


class PythonCyclonedxTool(ToolMeta):
    """cyclonedx python bill of materials generator & vulnerability detection tool (SBOM/SCA) tool class"""

    TOOL_NAME: str = "python-cyclonedx"
    TOOL_URL: str = "https://cyclonedx.org/"
    TOOL_TYPE: ToolType = ToolType.SBOM
    SOURCE_SUPPORT: list = [SourceType.PYTHON]
    SHORT_DESCRIPTION: str = "opensource python bill of materials (SBOM) generation utility, also runs SCA via pypi"
    INSTALL_HELP: str = """In most cases all that is required is python and pip (version 3+), and cyclonedx installed via pip

pip install cyclonedx-bom"""
    MORE_INFO: str = """https://hub.docker.com/r/cyclonedx/cyclonedx-python
https://github.com/CycloneDX/cyclonedx-python
https://owasp.org/www-project-cyclonedx/
https://cyclonedx.org/

Will automatically run against any poetry, requirements.txt, and pipenv projects in the repo

Common Gotchas
===========================
requirements.txt Pip Freezing

A bill-of-material such as CycloneDX expects exact version numbers. Therefore requirements.txt must be frozen. 

This can be accomplished via:

$ pip freeze > requirements.txt
"""
    # https://github.com/CycloneDX/cyclonedx-python/blob/master/LICENSE
    LICENSE: str = """Apache-2.0"""
    EZE_CONFIG: dict = {
        "REQUIREMENTS_FILES": {
            "type": list,
            "default": [],
            "help_text": """surplus custom requirements.txt file
any requirements files named requirements.txt will be automatically collected (or requirements-dev.txt with INCLUDE_DEV=true flag)
gotcha: make sure it's a frozen version of the pip requirements""",
            "help_example": "[custom-requirements.txt]",
        },
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_python-cyclonedx-bom.json",
            "default_help_value": "<cwd>.eze/raw/_python-cyclonedx-bom.json",
            "help_text": "output report location",
        },
        "INCLUDE_DEV": {
            "type": bool,
            "default": False,
            "help_text": "Exclude development dependencies from the BOM, aka requirements-dev.txt",
        },
        "SCA_ENABLED": {
            "type": bool,
            "default": True,
            "help_text": "use pypi and nvd data feeds to Pypi detect vulnerabilities",
        },
        "LICENSE_CHECK": LICENSE_CHECK_CONFIG.copy(),
        "LICENSE_ALLOWLIST": LICENSE_ALLOWLIST_CONFIG.copy(),
        "LICENSE_DENYLIST": LICENSE_DENYLIST_CONFIG.copy(),
    }

    VERSION_CHECK: dict = {
        "FROM_EXE": "cyclonedx-py",
        "FROM_PIP": "cyclonedx-bom",
        "FROM_DOCKER_IMAGE": "cyclonedx/cyclonedx-python:3.10.1",
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("cyclonedx-py --format=json --force"),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "IMAGE_NAME": "cyclonedx/cyclonedx-python:3.10.1",
                "BASE_COMMAND": " --format=json --force",
            },
            # eze config fields -> flags
            "FLAGS": {
                "PACKAGE_FILE": "-i=",
                "REPORT_FILE": "-o=",
            },
            # eze config fields -> flags
            "SHORT_FLAGS": {"REQUIREMENTS_FILE": "-r", "PIPLOCK_FILE": "-pip", "POETRY_FILE": "-p"},
        }
    }

    def extract_unpinned_requirements(self, stdout_output: str, pip_project_file: str) -> dict:
        """Extract the unpinned requirement from stdout of python-cyclonedx"""
        if not "Some of your dependencies do not have pinned version" in stdout_output:
            return {"cyclonedx_components": [], "vulnerabilities": []}

        pattern = re.compile(r"(?<=->\s)(.*?)(?=\s*!!)")
        matches = pattern.finditer(stdout_output)

        cyclonedx_components: list = []
        vulnerabilities: list = []
        for match in matches:
            package: str = match.group()
            cyclonedx_components.append(
                {"type": "library", "name": package, "version": None, "purl": f"pkg:pypi/{package}"}
            )
            name: str = f"unpinned requirement '{package}' found"
            recommendation = (
                f"pin version with '{package}==xxx', or update to mature dependency system, aka poetry or pipenv"
            )
            vulnerabilities.append(
                Vulnerability(
                    {
                        "name": package,
                        "overview": name,
                        "identifiers": {
                            # external input (aka default latest package) can code what code is executed
                            "CWE": "CWE-470"
                        },
                        "vulnerability_type": VulnerabilityType.code.name,
                        "recommendation": recommendation,
                        "severity": VulnerabilitySeverityEnum.medium.name,
                        "file_location": {"path": pip_project_file, "line": 1},
                    }
                )
            )
        return {"cyclonedx_components": cyclonedx_components, "vulnerabilities": vulnerabilities}

    async def run_scan(self) -> ScanResult:
        """
        Run scan using tool multiple times against multiple boms

        typical steps
        1) find all the manifests aka "package.json"s
        2) setup config
        3) run tool against
        4) parse tool report & normalise into common format
        5) repeat

        :raises EzeError
        """
        # 1) find all the manifests
        warnings_list: list = []
        vulnerabilities_list: list = []
        sboms: dict = {}

        requirements_files: list = get_requirements_projects()
        if self.config["INCLUDE_DEV"]:
            requirements_files.extend(find_files_by_name("^requirements-dev.txt$"))
        requirements_files.extend(self.config["REQUIREMENTS_FILES"])
        poetry_files: list = get_poetry_projects()
        piplock_files: list = get_piplock_projects()

        has_found_packages: bool = False
        # 3) run tool against requirements_file
        for requirements_file in requirements_files:
            log_debug(f"run 'cyclonedx-py' on {requirements_file}")
            [warnings, cyclonedx_bom, completed_process_stdout] = await self.run_individual_scan(
                {
                    "PACKAGE_FILE": "__ABSOLUTE_CWD__" + requirements_file,
                    "REQUIREMENTS_FILE": True,
                    "REPORT_FILE": self.config["REPORT_FILE"],
                }
            )
            warnings_list.extend(warnings)
            sboms[requirements_file] = cyclonedx_bom
            has_found_packages = True
            # AB#1054: additional parsing for unpinned assets
            # add unpinned assets as vulnerabilities
            # append unpinned assets into cyclonedx
            unpinned_requirements = self.extract_unpinned_requirements(completed_process_stdout, requirements_file)
            vulnerabilities_list.extend(unpinned_requirements["vulnerabilities"])
            components = py_.get(sboms[requirements_file], "components") or []
            components.extend(unpinned_requirements["cyclonedx_components"])
            sboms[requirements_file]["components"] = components

        # 3) run tool against poetry_files
        for poetry_file in poetry_files:
            log_debug(f"run 'cyclonedx-py' on {poetry_file}")
            [warnings, cyclonedx_bom, completed_process_stdout] = await self.run_individual_scan(
                {
                    "PACKAGE_FILE": "__ABSOLUTE_CWD__" + poetry_file,
                    "POETRY_FILE": True,
                    "REPORT_FILE": self.config["REPORT_FILE"],
                }
            )
            warnings_list.extend(warnings)
            sboms[poetry_file] = cyclonedx_bom
            has_found_packages = True

        # 3) run tool against piplock_files
        for piplock_file in piplock_files:
            log_debug(f"run 'cyclonedx-py' on {piplock_file}")
            [warnings, cyclonedx_bom, completed_process_stdout] = await self.run_individual_scan(
                {
                    "PACKAGE_FILE": "__ABSOLUTE_CWD__" + piplock_file,
                    "PIPLOCK_FILE": True,
                    "REPORT_FILE": self.config["REPORT_FILE"],
                }
            )
            warnings_list.extend(warnings)
            sboms[piplock_file] = cyclonedx_bom
            has_found_packages = True

        if not has_found_packages:
            warnings_list.append("cyclonedx-py not ran, no python packages found")

        report = self.parse_report(sboms)
        report.warnings.extend(warnings_list)
        report.vulnerabilities.extend(vulnerabilities_list)

        return report

    async def run_individual_scan(self, settings) -> list:
        """run individual scan of cyclonedx"""
        warnings: list = []
        scan_config: dict = self.config.copy()
        scan_config = {**scan_config, **settings}

        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME
        )
        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        cyclonedx_bom = load_json(report_local_filepath)
        if completed_process.stderr:
            warnings.append(completed_process.stderr)
        return [warnings, cyclonedx_bom, completed_process.stdout]

    def parse_report(self, cyclonedx_boms: dict) -> ScanResult:
        """convert report json into ScanResult"""
        is_sca_enabled: bool = self.config.get("SCA_ENABLED", False)
        if is_sca_enabled:
            # When SCA_ENABLED get SCA vulnerabilities/warnings directly from PYPI
            [pypi_vulnerabilities, pypi_warnings] = pypi_sca_sboms(cyclonedx_boms)
            scan_result: ScanResult = convert_multi_sbom_into_scan_result(self, cyclonedx_boms)
            scan_result.vulnerabilities.extend(pypi_vulnerabilities)
            scan_result.warnings.extend(pypi_warnings)
        else:
            scan_result: ScanResult = convert_multi_sbom_into_scan_result(self, cyclonedx_boms)
        return scan_result
