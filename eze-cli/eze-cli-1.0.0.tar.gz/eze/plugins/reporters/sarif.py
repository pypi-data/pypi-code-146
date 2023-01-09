"""Sarif reporter class implementation"""

from typing import List
import uuid
import textwrap
from pydash import py_
from eze.core.reporter import ReporterMeta
from eze.core.enums import Vulnerability
from eze.core.tool import ScanResult
from eze.utils.io.file import write_json
from eze.utils.log import log
from eze.utils.io.print import truncate
from eze.utils.cli.exe import exe_variable_interpolation_single
from typing import Tuple


class SarifReporter(ReporterMeta):
    """Python report class for echoing all output into a sarif file"""

    REPORTER_NAME: str = "sarif"
    SHORT_DESCRIPTION: str = "sarif output file reporter"
    INSTALL_HELP: str = """inbuilt"""
    MORE_INFO: str = """SBOM plugins will not be exported by this reporter"""
    LICENSE: str = """inbuilt"""
    VERSION_CHECK: dict = {"FROM_EZE": True}
    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "default": ".eze/eze_report.sarif",
            "help_text": """report file location
By default set to eze_report.sarif""",
        }
    }

    async def run_report(self, scan_results: list):
        """Method for taking scans and turning them into report output"""
        sarif_dict: dict = await self._build_sarif_dict(scan_results)
        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        sarif_location: str = write_json(report_local_filepath, sarif_dict, beatify_json=True)
        log(f"Written sarif report : {sarif_location}")

    async def _build_sarif_dict(self, scan_results: list):
        """
        Method for parsing the scans results into sarif format
        https://github.com/microsoft/sarif-tutorials/blob/main/docs/1-Introduction.md
        http://docs.oasis-open.org/sarif/sarif/v2.0/csprd01/sarif-v2.0-csprd01.html
        """
        sarif_schema: str = (
            "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
        )
        schema_version: str = "2.1.0"
        # TODO: SBOM cannot be handled by this reporter

        sarif_dict: dict = {"$schema": sarif_schema, "version": schema_version, "runs": []}
        for scan_result in scan_results:
            rules, results = self._create_sarif_rules_and_results(scan_result.vulnerabilities)
            tool: dict = self._create_sarif_tool(scan_result, rules)
            single_run = {"tool": tool, "results": results, "taxonomies": []}
            sarif_dict["runs"].append(single_run)
        return sarif_dict

    def _has_printable_vulnerabilities(self, scan_result: ScanResult) -> bool:
        """True if any vulnerabilities to print"""
        if len(scan_result.vulnerabilities) <= 0:
            return False
        return True

    def _create_sarif_rules_and_results(self, vulnerabilities: List[Vulnerability]) -> tuple:
        """Method for summarizing vulnerabilities and grouping into rules"""
        if len(vulnerabilities) <= 0:
            return [], []

        rules: list = []
        results: list = []

        for vulnerability_index, vulnerability in enumerate(vulnerabilities):
            rule_id: str = str(uuid.uuid4())
            rule: dict = self._create_sarif_rule(vulnerability, rule_id)
            rules.append(rule)

            result: dict = self._create_sarif_result(vulnerability, rule_id, vulnerability_index)
            results.append(result)

        return rules, results

    def _create_sarif_tool(self, scan_result: ScanResult, rules: list) -> dict:
        """
        create sarif tool block
        http://docs.oasis-open.org/sarif/sarif/v2.0/csprd01/sarif-v2.0-csprd01.html#_Toc517435985
        """
        run_details: dict = scan_result.run_details
        tool_name: str = py_.get(run_details, "tool_name", "unknown")
        tool_type: str = py_.get(run_details, "tool_type", "unknown")
        tool: dict = {
            "driver": {"name": tool_name, "version": "unknown", "fullName": tool_type + ":" + tool_name, "rules": rules}
        }
        if py_.get(run_details, "tool_url"):
            tool["driver"]["informationUri"] = py_.get(run_details, "tool_url")
        return tool

    def _create_sarif_rule(self, vulnerability: Vulnerability, rule_id: str) -> dict:
        """
        create sarif rule block
        http://docs.oasis-open.org/sarif/sarif/v2.0/csprd01/sarif-v2.0-csprd01.html#_Toc517436204
        """
        rule: dict = {
            "id": rule_id,
            "name": vulnerability.name,
            "shortDescription": {"text": truncate(vulnerability.overview, 70, "...")},
            "fullDescription": {
                "text": " ".join(textwrap.wrap(vulnerability.overview + " " + vulnerability.recommendation, width=140))
            },
        }
        return rule

    def _create_sarif_result(self, vulnerability: Vulnerability, rule_id: str, vulnerability_index: str) -> dict:
        """
        create sarif result block
        http://docs.oasis-open.org/sarif/sarif/v2.0/csprd01/sarif-v2.0-csprd01.html#_Toc517436058
        """
        vulnerability_level = self._convert_vulnerability_sarif_level(vulnerability)
        message: str = " ".join(textwrap.wrap(vulnerability.recommendation, width=130))
        uri: str = py_.get(vulnerability, "file_location.path", "unknown")
        start_line: int = int(py_.get(vulnerability, "file_location.line") or "1")
        result: dict = {
            "ruleId": rule_id,
            "ruleIndex": vulnerability_index,
            "level": vulnerability_level,
            "message": {"text": message},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": uri},
                        "region": {"startLine": start_line},
                    }
                }
            ],
        }
        return result

    def _convert_vulnerability_sarif_level(self, vulnerability: Vulnerability) -> str:
        vulnerability_level: str = ""
        if (
            vulnerability.severity == "critical"
            or vulnerability.severity == "high"
            or vulnerability.severity == "medium"
        ):
            vulnerability_level = "error"
        elif vulnerability.severity == "low":
            vulnerability_level = "warning"
        elif vulnerability.severity == "none" or vulnerability.severity == "na":
            vulnerability_level = "none"
        return vulnerability_level
