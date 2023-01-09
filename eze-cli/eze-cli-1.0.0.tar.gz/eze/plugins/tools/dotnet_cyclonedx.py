"""cyclonedx SBOM tool class"""
import shlex
from pathlib import Path

from eze.core.enums import ToolType, SourceType, LICENSE_CHECK_CONFIG, LICENSE_ALLOWLIST_CONFIG, LICENSE_DENYLIST_CONFIG
from eze.core.tool import ToolMeta, ScanResult
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.log import log_debug
from eze.utils.scan_result import convert_multi_sbom_into_scan_result
from eze.utils.io.file import load_json
from eze.utils.language.dotnet import (
    get_deprecated_packages,
    get_vulnerable_packages,
    annotate_transitive_licenses,
    get_dotnet_projects,
    get_dotnet_solutions,
)
from eze.utils.cli.exe import exe_variable_interpolation_single


class DotnetCyclonedxTool(ToolMeta):
    """cyclonedx dot net bill of materials generator tool (SBOM) tool class"""

    TOOL_NAME: str = "dotnet-cyclonedx"
    TOOL_URL: str = "https://owasp.org/www-project-cyclonedx/"
    TOOL_TYPE: ToolType = ToolType.SBOM
    SOURCE_SUPPORT: list = [SourceType.DOTNET]
    SHORT_DESCRIPTION: str = "opensource C#/dotnet bill of materials (SBOM) generation utility"
    INSTALL_HELP: str = """In most cases all that is required is dotnet sdk 6+, and to install via nuget

dotnet tool install --global CycloneDX
"""
    MORE_INFO: str = """
https://github.com/CycloneDX/cyclonedx-dotnet
https://owasp.org/www-project-cyclonedx/
https://cyclonedx.org/
"""
    # https://github.com/CycloneDX/cyclonedx-node-module/blob/master/LICENSE

    LICENSE: str = """Apache-2.0"""

    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_dotnet-cyclonedx-bom",
            "default_help_value": "<cwd>.eze/raw/_dotnet-cyclonedx-bom/bom.json",
            "help_text": "output report directory location",
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

    VERSION_CHECK: dict = {
        "FROM_EXE": "dotnet CycloneDX --version",
        "FROM_DOCKER": {
            "DOCKER_COMMAND": {"IMAGE_NAME": "cyclonedx/cyclonedx-dotnet:2.7.0", "BASE_COMMAND": "--version"}
        },
    }

    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("dotnet CycloneDX --json"),
            # eze config fields -> arguments
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "IMAGE_NAME": "cyclonedx/cyclonedx-dotnet:2.7.0",
                "BASE_COMMAND": " --json",
            },
            "ARGUMENTS": ["INPUT_FILE"],
            # eze config fields -> flags
            "FLAGS": {"REPORT_FILE": "-o "},
            "SHORT_FLAGS": {"INCLUDE_DEV": "-d", "_INCLUDE_TEST": "-t"},
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
        sboms: dict = {}
        warnings: list = []
        vulns: list = []
        dotnet_projects = get_dotnet_projects()
        dotnet_solutions = get_dotnet_solutions()
        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        for dotnet_project_file in dotnet_projects + dotnet_solutions:
            log_debug(f"run 'dotnet-cyclonedx' on {dotnet_project_file}")
            project_folder = Path(dotnet_project_file).parent
            project_fullpath = Path.joinpath(Path.cwd(), project_folder)
            scan_config: dict = self.config.copy()
            scan_config["INPUT_FILE"] = "__ABSOLUTE_CWD__" + Path(dotnet_project_file).name
            scan_config["__THROW_ERROR_ON_STDERR"] = True
            scan_config["__FORCED_DOCKER_SOURCE_FOLDER"] = str(project_fullpath)
            completed_process: CompletedProcess = await run_async_cli_command(
                self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME, cwd=project_folder
            )
            sboms[dotnet_project_file] = load_json(Path(report_local_filepath) / "bom.json")
            if completed_process.stderr:
                warnings.append(f"Errored when parsing {dotnet_project_file}: {completed_process.stderr}")
                continue
            # annotate transitive packages
            # "properties"."transitive" not "dependency" as too complex to calculate
            await annotate_transitive_licenses(sboms[dotnet_project_file], project_folder)

            # annotate deprecated packages
            vulns.extend(await get_deprecated_packages(project_folder, dotnet_project_file))

            # annotate vulnerabilities packages
            vulns.extend(await get_vulnerable_packages(project_folder, dotnet_project_file))

        report = self.parse_report(sboms)
        # add all warnings
        report.warnings.extend(warnings)
        report.vulnerabilities.extend(vulns)

        return report

    def parse_report(self, sboms: dict) -> ScanResult:
        """convert report json into ScanResult"""
        return convert_multi_sbom_into_scan_result(self, sboms)

    def _parse_config(self, eze_config: dict) -> dict:
        """take raw config dict and normalise values"""
        parsed_config = super()._parse_config(eze_config)

        # ADDITION PARSING: replicate INCLUDE_DEV into INCLUDE_TEST(-d -t) flag
        parsed_config["_INCLUDE_TEST"] = parsed_config["INCLUDE_DEV"]

        return parsed_config
