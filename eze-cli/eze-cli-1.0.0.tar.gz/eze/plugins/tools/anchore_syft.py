"""Syft SCA and Container SBOM tool class"""
import shlex

from eze.core.enums import ToolType, SourceType, LICENSE_CHECK_CONFIG, LICENSE_ALLOWLIST_CONFIG, LICENSE_DENYLIST_CONFIG
from eze.core.tool import ToolMeta, ScanResult
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import create_tempfile_path, get_filename, write_text, load_json
from eze.utils.scan_result import convert_sbom_into_scan_result
from eze.utils.cli.exe import exe_variable_interpolation_single


class SyftTool(ToolMeta):
    """Software and Container bill of materials generator tool (SBOM) Syft tool class"""

    TOOL_NAME: str = "anchore-syft"
    TOOL_URL: str = "https://github.com/anchore/syft"
    TOOL_TYPE: ToolType = ToolType.SBOM
    SOURCE_SUPPORT: list = [
        SourceType.RUBY,
        SourceType.NODE,
        SourceType.JAVA,
        SourceType.PYTHON,
        SourceType.GO,
        SourceType.CONTAINER,
    ]
    SHORT_DESCRIPTION: str = "opensource multi language and container bill of materials (SBOM) generation utility"
    INSTALL_HELP: str = """In most cases all that is two things
        
Syft required to installed via apt-get or docker
As of writing, no native windows 10 syft exists, can be run via wsl2

Also cyclonedx-cli tool for converting xml output into json
https://github.com/CycloneDX/cyclonedx-cli/releases
"""
    MORE_INFO: str = """https://github.com/anchore/syft
https://github.com/CycloneDX/cyclonedx-cli
https://owasp.org/www-project-cyclonedx/
https://cyclonedx.org/

This plugin uses syft to create a xml cyclonedx sbom
Then cyclone-cli to convert that isn't json cyclonedx sbom

Tips
===========================
- if scan running slow, try command locally to see what can be done to optimise the CONFIG_FILE
  (you can see command with --debug)
"""
    # https://github.com/anchore/syft/blob/main/LICENSE
    LICENSE: str = """Apache-2.0"""
    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": str,
            "default": ".",
            "help_example": "python:3.8-slim",
            "help_text": """By default it is "." aka local folder
From syft help
 Supports the following image sources:
    syft packages yourrepo/yourimage:tag     defaults to using images from a Docker daemon. If Docker is not present, the image is pulled directly from the registry.
    syft packages path/to/a/file/or/dir      a Docker tar, OCI tar, OCI directory, or generic filesystem directory

  You can also explicitly specify the scheme to use:
    syft packages docker:yourrepo/yourimage:tag          explicitly use the Docker daemon
    syft packages docker-archive:path/to/yourimage.tar   use a tarball from disk for archives created from "docker save"
    syft packages oci-archive:path/to/yourimage.tar      use a tarball from disk for OCI archives (from Skopeo or otherwise)
    syft packages oci-dir:path/to/yourimage              read directly from a path on disk for OCI layout directories (from Skopeo or otherwise)
    syft packages dir:path/to/yourproject                read directly from a path on disk (any directory)
    syft packages registry:yourrepo/yourimage:tag        pull image directly from a registry (no container runtime required)""",
        },
        "CONFIG_FILE": {
            "type": str,
            "help_text": """Syft config file location, by default Empty, maps to syft argument
-c, --config string     application config file""",
        },
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_syft-bom.json",
            "default_help_value": "<cwd>.eze/raw/_syft-bom.json",
            "help_text": "output report location",
        },
        "INTERMEDIATE_FILE": {
            "type": str,
            "default": "__TEMP_DIRECTORY__/tmp-syft-bom.xml",
            "default_help_value": "<tempdir>/.eze-temp/tmp-syft-bom.xml",
            "help_text": """file used to store xml cyclonedx from syft before conversion into final json format
(will default to tmp file otherwise)""",
        },
        "LICENSE_CHECK": LICENSE_CHECK_CONFIG.copy(),
        "LICENSE_ALLOWLIST": LICENSE_ALLOWLIST_CONFIG.copy(),
        "LICENSE_DENYLIST": LICENSE_DENYLIST_CONFIG.copy(),
    }
    VERSION_CHECK: dict = {
        "FROM_EXE": "syft --version",
        "FROM_DOCKER": {"DOCKER_COMMAND": {"IMAGE_NAME": "anchore/syft:v0.64.0", "BASE_COMMAND": "--version"}},
    }
    TOOL_CLI_CONFIG = {
        "CONVERSION_CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("cyclonedx-cli convert --output-format json"),
            # eze config fields -> flags
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/path",
                "INTERMEDIATE_FILE": "/data/tmp-syft-bom.xml",
                "FOLDERS": {f"/data/tmp-syft-bom.xml": str(create_tempfile_path("tmp-syft-bom.xml"))},
                "WORKING_FOLDER": "/path",
                "IMAGE_NAME": "cyclonedx/cyclonedx-cli:0.24.2",
                "BASE_COMMAND": "convert --output-format json",
            },
            "FLAGS": {"REPORT_FILE": "--output-file ", "INTERMEDIATE_FILE": "--input-file "},
        },
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("syft -q -o=cyclonedx-xml"),
            # eze config fields -> arguments
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/path",
                "WORKING_FOLDER": "/path",
                "IMAGE_NAME": "anchore/syft:v0.64.0",
                "BASE_COMMAND": "-q -o=cyclonedx-xml",
            },
            "TAIL_ARGUMENTS": ["SOURCE"],
            # eze config fields -> flags
            "FLAGS": {"CONFIG_FILE": "-c="},
        },
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

        # create xml cyclonedx using syft
        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], self.config, self.TOOL_NAME
        )
        report_text = completed_process.stdout
        intermediate_file_path = create_tempfile_path(get_filename(self.config["INTERMEDIATE_FILE"]))
        write_text(intermediate_file_path, report_text)

        # convert xml cyclonedx format into json cyclonedx format
        conversion_completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CONVERSION_CMD_CONFIG"], self.config, self.TOOL_NAME
        )

        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        cyclonedx_bom = load_json(report_local_filepath)
        report = self.parse_report(cyclonedx_bom)
        if completed_process.stderr:
            report.warnings.append(completed_process.stderr)
        if conversion_completed_process.stderr:
            report.warnings.append(conversion_completed_process.stderr)

        return report

    def parse_report(self, cyclonedx_bom: dict) -> ScanResult:
        """convert report json into ScanResult"""
        return convert_sbom_into_scan_result(self, cyclonedx_bom)
