"""Grype SCA and Container tool class"""
import shlex

from pydash import py_

from eze.core.enums import VulnerabilityType, VulnerabilitySeverityEnum, ToolType, SourceType, Vulnerability

from eze.utils.cli.run import run_async_cli_command, run_cli_command, CompletedProcess
from eze.core.tool import ToolMeta, ScanResult
from eze.utils.io.file import write_text, parse_json
from eze.utils.log import log_error
from eze.utils.cli.exe import exe_variable_interpolation_single


class GrypeTool(ToolMeta):
    """SCA and Container scanning tool Grype tool class"""

    TOOL_NAME: str = "anchore-grype"
    TOOL_URL: str = "https://hub.docker.com/r/anchore/grype/tags"  # Changed from github url to docker image url
    TOOL_TYPE: ToolType = ToolType.SCA
    SOURCE_SUPPORT: list = [
        SourceType.RUBY,
        SourceType.NODE,
        SourceType.JAVA,
        SourceType.PYTHON,
        SourceType.PHP,
        SourceType.CONTAINER,
    ]
    SHORT_DESCRIPTION: str = "opensource multi language SCA and container scanner"
    INSTALL_HELP: str = """In most cases all that is required to install grype via apt-get or docker
As of writing, no native windows 10 grype exists, can be run via wsl2"""
    MORE_INFO: str = """https://github.com/anchore/grype

Tips
===========================
- use slim versions of base images
- always create a application user for running entry_point and cmd commands
- read https://owasp.org/www-project-docker-top-10/

Common Gotchas
===========================
Worth mentioning vulnerability counts are quite high for official out the box docker images

trivy image node:slim
Total: 101 (UNKNOWN: 2, LOW: 67, MEDIUM: 8, HIGH: 20, CRITICAL: 4)

trivy image python:3.8-slim
Total: 112 (UNKNOWN: 2, LOW: 74, MEDIUM: 11, HIGH: 21, CRITICAL: 4)
"""
    # https://github.com/anchore/grype/blob/main/LICENSE
    LICENSE: str = """Apache-2.0"""

    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": str,
            "default": ".",
            "required": True,
            "help_text": """By default it is "." aka local folder
From grype help
Supports the following image sources:
    grype yourrepo/yourimage:tag     defaults to using images from a Docker daemon
    grype path/to/yourproject        a Docker tar, OCI tar, OCI directory, or generic filesystem directory
You can also explicitly specify the scheme to use:
    grype docker:yourrepo/yourimage:tag          explicitly use the Docker daemon
    grype docker-archive:path/to/yourimage.tar   use a tarball from disk for archives created from "docker save"
    grype oci-archive:path/to/yourimage.tar      use a tarball from disk for OCI archives (from Podman or otherwise)
    grype oci-dir:path/to/yourimage              read directly from a path on disk for OCI layout directories (from Skopeo or otherwise)
    grype dir:path/to/yourproject                read directly from a path on disk (any directory)
    grype sbom:path/to/syft.json                 read Syft JSON from path on disk
    grype registry:yourrepo/yourimage:tag        pull image directly from a registry (no container runtime required)""",
            "help_example": """python""",
        },
        "CONFIG_FILE": {
            "type": str,
            "default": None,
            "help_text": """Grype config file location, by default Empty, maps to grype argument
  -c, --config string     application config file""",
        },
        "GRYPE_IGNORE_UNFIXED": {
            "type": bool,
            "default": False,
            "help_text": """if true ignores state = "not-fixed""" "",
        },
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_grype-bom.json",
            "default_help_value": "<cwd>.eze/raw/_grype-bom.json",
            "help_text": "output report location",
        },
    }

    VERSION_CHECK: dict = {
        "FROM_EXE": "grype version",
        "FROM_DOCKER": {"DOCKER_COMMAND": {"IMAGE_NAME": "anchore/grype:v0.54.0", "BASE_COMMAND": "version"}},
        "IGNORED_ERR_MESSAGES": [],
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("grype -q -o=json"),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "IMAGE_NAME": "anchore/grype:v0.54.0",
                "BASE_COMMAND": "-q -o=json",
                "WORKING_FOLDER": "/src",
                "ENV_VARS": {"GRYPE_DB_CACHE_DIR": "/src/.eze/grype_db"},
            },
            # eze config fields -> arguments
            "TAIL_ARGUMENTS": ["SOURCE"],
            # eze config fields -> flags
            "FLAGS": {"CONFIG_FILE": "-c="},
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
        # WORKAROUND: grype crashes on async, using run_cli_command (jerkier but no crash)
        self.config["__FORCE_SYNC_CMD"] = True
        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], self.config, self.TOOL_NAME
        )
        report_text = completed_process.stdout
        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        write_text(report_local_filepath, report_text)
        report_events = parse_json(report_text)
        report = self.parse_report(report_events)
        if completed_process.stderr:
            report.warnings.append(completed_process.stderr)

        return report

    def grype_severity_to_cwe_severity(self, grype_severity: str) -> str:
        """convert grype severities into standard cvss severity

        as per
        https://semgrep.dev/docs/writing-rules/rule-syntax/#schema
        https://nvd.nist.gov/vuln-metrics/cvss"""
        grype_severity = grype_severity.lower()
        has_severity = hasattr(VulnerabilitySeverityEnum, grype_severity)
        if not has_severity:
            if grype_severity == "negligible":
                return VulnerabilitySeverityEnum.na.name
            log_error(f"unknown trivy severity '${grype_severity}', defaulting to na")
            return VulnerabilitySeverityEnum.na.name

        return VulnerabilitySeverityEnum[grype_severity].name

    def parse_report(self, parsed_json: list) -> ScanResult:
        """convert report json into ScanResult"""
        grype_matches = py_.get(parsed_json, "matches", [])
        vulnerabilities_list: list = []

        ignore_unfixed: bool = self.config["GRYPE_IGNORE_UNFIXED"]

        dup_key_list = {}

        for grype_match in grype_matches:
            is_unfixed: bool = py_.get(grype_match, "vulnerability.fix.state", "") == "not-fixed"
            if ignore_unfixed and is_unfixed:
                continue

            references = py_.get(grype_match, "vulnerability.urls", [])
            source_url = py_.get(grype_match, "vulnerability.dataSource", None)
            if source_url and source_url not in references:
                references.insert(0, source_url)

            grype_severity = py_.get(grype_match, "vulnerability.severity", [])
            severity = self.grype_severity_to_cwe_severity(grype_severity)
            vulnerable_package = py_.get(grype_match, "artifact.name", None)
            installed_version = py_.get(grype_match, "artifact.version", None)
            fixed_version = py_.get(grype_match, "vulnerability.fix.versions[0]", None)
            file_location: str = py_.get(grype_match, "artifact.locations[0].path", "unknown")

            recommendation = ""
            if fixed_version:
                recommendation = f"Update {vulnerable_package} ({installed_version}) to a non vulnerable version, fix version: {fixed_version}"
            identifiers = {}
            identifier_id = py_.get(grype_match, "vulnerability.id", None)
            if identifier_id.startswith("CVE"):
                identifiers["cve"] = identifier_id
            elif identifier_id.startswith("GHSA"):
                identifiers["ghsa"] = identifier_id
            overview = py_.get(grype_match, "vulnerability.description", [])
            related_vulnerability = py_.get(grype_match, "relatedVulnerabilities[0].id", None)
            if related_vulnerability and related_vulnerability == identifier_id and not recommendation:
                overview = py_.get(grype_match, "relatedVulnerabilities[0].description", None)
            unique_key: str = f"{vulnerable_package}_{severity}_{installed_version}_{file_location}"
            if dup_key_list.get(unique_key):
                continue
            dup_key_list[unique_key] = True
            vulnerability_raw = {
                "vulnerability_type": VulnerabilityType.dependency.name,
                "name": vulnerable_package,
                "version": installed_version,
                "overview": overview,
                "recommendation": recommendation,
                "severity": severity,
                "identifiers": identifiers,
                "file_location": {"path": file_location, "line": 1},
                "references": references,
                "metadata": None,
            }
            vulnerability = Vulnerability(vulnerability_raw)
            vulnerabilities_list.append(vulnerability)

        report = ScanResult(
            {
                "tool": self.TOOL_NAME,
                "vulnerabilities": vulnerabilities_list,
            }
        )
        return report
