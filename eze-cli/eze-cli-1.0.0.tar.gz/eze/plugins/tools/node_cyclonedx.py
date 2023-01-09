"""cyclonedx SBOM tool class"""
import shlex
from pathlib import Path


from eze.core.enums import ToolType, SourceType, LICENSE_CHECK_CONFIG, LICENSE_ALLOWLIST_CONFIG, LICENSE_DENYLIST_CONFIG
from eze.core.tool import ToolMeta, ScanResult
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.language.node import install_npm_in_path, annotate_transitive_licenses, get_npm_projects
from eze.utils.log import log_debug
from eze.utils.error import EzeExecutableError
from eze.utils.scan_result import convert_multi_sbom_into_scan_result
from eze.utils.io.file import load_json
from eze.utils.cli.exe import exe_variable_interpolation_single


class NodeCyclonedxTool(ToolMeta):
    """cyclonedx node bill of materials generator tool (SBOM) tool class"""

    TOOL_NAME: str = "node-cyclonedx"
    TOOL_URL: str = "https://owasp.org/www-project-cyclonedx/"
    TOOL_TYPE: ToolType = ToolType.SBOM
    SOURCE_SUPPORT: list = [SourceType.NODE]
    SHORT_DESCRIPTION: str = "opensource node bill of materials (SBOM) generation utility"
    INSTALL_HELP: str = """In most cases all that is required is node and npm (version 6+), and cyclonedx installed via npm
        
npm install -g @cyclonedx/bom
"""
    MORE_INFO: str = """
https://github.com/CycloneDX/cyclonedx-node-module
https://owasp.org/www-project-cyclonedx/
https://cyclonedx.org/

Common Gotchas
===========================
NPM Installing

A bill-of-material such as CycloneDX expects exact version numbers. 
Therefore the dependencies in node_modules needs installed

This can be accomplished via:

$ npm install

This will be ran automatically, if npm install fails this tool can't be run
"""
    # https://github.com/CycloneDX/cyclonedx-node-module/blob/master/LICENSE
    LICENSE: str = """Apache-2.0"""
    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_node-cyclonedx-bom.json",
            "default_help_value": "<cwd>.eze/raw/_node-cyclonedx-bom.json",
            "help_text": "output report location",
        },
        "INCLUDE_DEV": {
            "type": bool,
            "default": False,
            "help_text": "Include development dependencies from the SCA",
        },
        "LICENSE_CHECK": LICENSE_CHECK_CONFIG.copy(),
        "LICENSE_ALLOWLIST": LICENSE_ALLOWLIST_CONFIG.copy(),
        "LICENSE_DENYLIST": LICENSE_DENYLIST_CONFIG.copy(),
    }

    VERSION_CHECK: dict = {
        "FROM_EXE": "cyclonedx-bom --version",
        "FROM_DOCKER": {
            "DOCKER_COMMAND": {"IMAGE_NAME": "cyclonedx/cyclonedx-node:3.10.6", "BASE_COMMAND": "--version"}
        },
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("cyclonedx-bom"),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "IMAGE_NAME": "cyclonedx/cyclonedx-node:3.10.6",
                "BASE_COMMAND": "",
            },
            # eze config fields -> flags
            "FLAGS": {"REPORT_FILE": "-o "},
            # eze config fields -> flags
            "SHORT_FLAGS": {"INCLUDE_DEV": "--include-dev"},
        }
    }

    @staticmethod
    def get_process_fatal_errors(completed_process) -> str:
        """Take output and check for common errors"""
        if "node_modules does not exist." in completed_process.stdout:
            return completed_process.stdout
        if "Error: Cannot find module" in completed_process.stdout:
            return completed_process.stdout
        return None

    async def run_scan(self) -> ScanResult:
        """
        Run scan using tool

        typical steps
        1) find all the manifests aka "package.json"s
        2) setup config
        3) run tool against
        4) parse tool report & normalise into common format
        5) repeat

        :raises EzeError
        """
        sboms: dict = {}
        warnings: list = []
        npm_package_jsons: list = get_npm_projects()
        scan_config: dict = self.config.copy()
        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        scan_config["__THROW_ERROR_ON_STDERR"] = True
        for npm_package in npm_package_jsons:
            log_debug(f"run 'cyclonedx-bom' on {npm_package}")
            npm_project = Path(npm_package).parent
            npm_project_fullpath = Path.joinpath(Path.cwd(), npm_project)
            await install_npm_in_path(npm_project)
            scan_config["__FORCED_DOCKER_SOURCE_FOLDER"] = str(npm_project_fullpath)
            completed_process: CompletedProcess = await run_async_cli_command(
                self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME, cwd=npm_project_fullpath
            )
            fatal_errors = self.get_process_fatal_errors(completed_process)
            if fatal_errors:
                raise EzeExecutableError(fatal_errors)
            sboms[npm_package] = load_json(report_local_filepath)
            if completed_process.stderr:
                warnings.append(completed_process.stderr)
            # mark node-cyclonedx transitive packages
            # "properties"."transitive" not "dependency" as too complex to calculate
            await annotate_transitive_licenses(sboms[npm_package], npm_project_fullpath, self.config["INCLUDE_DEV"])

        report = self.parse_report(sboms)
        # add all warnings
        report.warnings.extend(warnings)

        return report

    def parse_report(self, sboms: dict) -> ScanResult:
        """convert report json into ScanResult"""
        return convert_multi_sbom_into_scan_result(self, sboms)
