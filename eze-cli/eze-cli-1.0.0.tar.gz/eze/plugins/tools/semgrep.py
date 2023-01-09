"""SemGrep Python tool class"""
import shlex
import time

from pydash import py_

from eze.core.enums import VulnerabilityType, VulnerabilitySeverityEnum, ToolType, SourceType, Vulnerability
from eze.core.tool import (
    ToolMeta,
    ScanResult,
)
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import load_json
from eze.utils.log import log
from eze.utils.io.file_scanner import has_filetype

# TODO: IMPROVEMENT: speed up docker by mount the "cache_workspace_into_tmp" for scanning
from eze.utils.cli.exe import exe_variable_interpolation_single


class SemGrepTool(ToolMeta):
    """SemGrep Python tool class"""

    TOOL_NAME: str = "semgrep"
    TOOL_URL: str = "https://hub.docker.com/r/returntocorp/semgrep"
    TOOL_TYPE: ToolType = ToolType.SAST
    SOURCE_SUPPORT: list = [SourceType.ALL]
    SHORT_DESCRIPTION: str = "opensource multi language SAST scanner"
    INSTALL_HELP: str = """Only needs docker

You can run/install it locally with python and pip install*
pip install semgrep
semgrep --version

* currently running semgrep locally in windows outside of wsl2 is difficult"""
    MORE_INFO: str = """https://semgrep.dev/docs/cli-reference/
https://github.com/returntocorp/semgrep
https://github.com/returntocorp/semgrep-rules
https://semgrep.dev/explore

Language Support: https://semgrep.dev/docs/language-support/

Tips and Tricks
===============================
- As of 2021 windows support is limited, use eze inside wsl2 or linux to run semgrep, until support added
  https://github.com/returntocorp/semgrep/issues/1330
- tailor your configs to your products
- use PRINT_TIMING_INFO eze config flag to detect poor performing unnecessarily rules  
- only scan your source code, as test code can often use asserts or cli tools which can cause false positive security risks
- use "# nosemgrep" comments to ignore False positives
"""
    # https://github.com/returntocorp/semgrep/blob/develop/LICENSE
    LICENSE: str = """LGPL"""
    DEFAULT_SEVERITY = VulnerabilitySeverityEnum.high.name
    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": str,
            "default": ".",
            "required": True,
            "help_text": """SOURCE, space separated files and directories
defaults to cwd eze is running in maps to target.""",
        },
        "CONFIGS": {
            "type": list,
            "default": None,
            "default_help_value": "Automatically Detected",
            "help_text": """SemGrep config file to use. path to YAML configuration file, directory of YAML files
ending in .yml|.yaml, URL of a configuration file, or semgrep registry entry name.

See https://semgrep.dev/docs/writing-rules/rule-syntax for
information on configuration file format.

maps to --config""",
            "help_example": ["p/ci", "p/python"],
        },
        "INCLUDE": {
            "type": list,
            "default": [],
            "help_text": """array of list of paths (glob patterns supported) to include from scan

Filter files or directories by path. The argument is a glob-style pattern such as 'foo.*' that must match the path. This is an extra filter in
addition to other applicable filters. For example, specifying the language with '-l javascript' might preselect files 'src/foo.jsx' and
'lib/bar.js'. Specifying one of '--include=src', '--include=*.jsx', or '--include=src/foo.*' will restrict the selection to the single file
'src/foo.jsx'. A choice of multiple '--include' patterns can be specified. For example, '--include=foo.* --include=bar.*' will select both
'src/foo.jsx' and 'lib/bar.js'. Glob-style patterns follow the syntax supported by python, which is documented at
https://docs.python.org/3/library/glob.html

maps to semgrep flag
--include INCLUDE""",
            "help_example": ["PATH-TO-INCLUDE-FOLDER/.*", "PATH-TO-INCLUDE-FILE.js"],
        },
        "EXCLUDE": {
            "type": list,
            "default": [],
            "help_text": """Skip any file or directory that matches this pattern; --exclude='*.py' will ignore the following = foo.py, src/foo.py, foo.py/bar.sh.
--exclude='tests' will ignore tests/foo.py as well as a/b/tests/c/foo.py. Can add multiple times. Overrides includes.

maps to semgrep flag --exclude""",
            "help_example": ["PATH-TO-EXCLUDED-FOLDER/.*", "PATH-TO-EXCLUDED-FILE.js"],
        },
        "PRINT_TIMING_INFO": {
            "type": bool,
            "default": False,
            "help_text": """can be difficult to find which rules are running slowly, this outputs a small timing report""",
        },
        "USE_GIT_IGNORE": {
            "type": bool,
            "default": True,
            "help_text": """ignore files specified in .gitignore""",
        },
        "REPORT_FILE": {
            "type": str,
            "default": "__ABSOLUTE_CWD__.eze/raw/_semgrep-report.json",
            "default_help_value": "<cwd>.eze/raw/_semgrep-report.json",
            "help_text": "output report location",
        },
    }
    VERSION_CHECK: dict = {
        "FROM_EXE": "semgrep --version",
        "FROM_DOCKER": {
            "DOCKER_COMMAND": {"IMAGE_NAME": "returntocorp/semgrep", "BASE_COMMAND": "semgrep scan --version"}
        },
        # #100 - SEMGREP outputs updated version available strings randomly into stderr
        "IGNORED_ERR_MESSAGES": ["A new version of Semgrep is available"],
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("semgrep --json --metrics=off -q "),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "IMAGE_NAME": "returntocorp/semgrep",
                "BASE_COMMAND": "semgrep scan --json --metrics=off -q",
            },
            # eze config fields -> arguments
            "ARGUMENTS": ["SOURCE"],
            # eze config fields -> flags
            "FLAGS": {
                "CONFIGS": "-c ",
                "REPORT_FILE": "-o ",
                "INCLUDE": "--include ",
                "EXCLUDE": "--exclude ",
            },
            "SHORT_FLAGS": {"USE_GIT_IGNORE": "--use-git-ignore"},
        }
    }

    DEFAULT_TEST_PATTERNS = ["test_*.py", "*.test.js", "tests", "__tests__"]

    async def run_scan(self) -> ScanResult:
        """
        Run scan using tool

        typical steps
        1) setup config
        2) run tool
        3) parse tool report & normalise into common format

        :raises EzeError
        """
        tic: float = time.perf_counter()

        # 1) setup config
        scan_config: dict = self.config.copy()
        # make REPORT_FILE absolute in-case cwd changes
        scan_config["EXCLUDE"] = scan_config["EXCLUDE"].copy()
        scan_config["EXCLUDE"].extend(self.DEFAULT_TEST_PATTERNS)
        # 2) run tool
        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME
        )
        toc: float = time.perf_counter()
        total_time: float = toc - tic
        if total_time > 60:
            log(
                f"semgrep scan took a long time ({total_time:0.2f}s), "
                f"you can often speed up significantly by ignoring compiled assets and test/dependency folders"
            )
        # 3) parse report
        report_local_filepath: str = exe_variable_interpolation_single(self.config.get("REPORT_FILE", None))
        parsed_json: dict = load_json(report_local_filepath)
        report = self.parse_report(parsed_json, total_time)

        return report

    def parse_report(self, parsed_json: dict, total_time: int = 0) -> ScanResult:
        """convert report json into ScanResult"""

        time_info = parsed_json.get("time")
        if time_info and self.config["PRINT_TIMING_INFO"]:
            self.print_out_semgrep_timing_report(time_info, total_time)

        vulnerabilities_list: list = []

        report_events = parsed_json["results"]
        for report_event in report_events:
            path = report_event["path"]
            line = py_.get(report_event, "start.line", "")
            check_id = report_event["check_id"]
            short_link = py_.get(report_event, "extra.metadata.shortlink")

            name = f"{path}: {check_id}"
            summary = py_.get(report_event, "extra.message", name)

            semgrep_severity = py_.get(report_event, "extra.severity")
            cwe_severity = self.semgrep_severity_to_cwe_severity(semgrep_severity)

            recommendation = f"Investigate '{path}' on Line {line} for '{check_id}' strings. Read more at {short_link}"
            if cwe_severity in (VulnerabilitySeverityEnum.medium.name, VulnerabilitySeverityEnum.low.name):
                recommendation += " or use '# nosemgrep' if false positive"

            identifiers = self.extract_semgrep_identifiers(report_event)

            metadata = py_.get(report_event, "extra.metadata", {})
            references = metadata.pop("references", [])

            is_ignored = py_.get(report_event, "extra.is_ignored", False)

            vulnerabilities_list.append(
                Vulnerability(
                    {
                        "vulnerability_type": VulnerabilityType.code.name,
                        "name": name,
                        "version": None,
                        "overview": summary,
                        "recommendation": recommendation,
                        "language": "file",
                        "severity": cwe_severity,
                        "identifiers": identifiers,
                        "metadata": metadata,
                        "references": references,
                        "file_location": {"path": path, "line": line},
                        "is_ignored": is_ignored,
                    }
                )
            )

        report = ScanResult(
            {
                "tool": self.TOOL_NAME,
                "vulnerabilities": vulnerabilities_list,
                "warnings": self.extract_semgrep_warnings(parsed_json),
            }
        )
        return report

    def _parse_config(self, eze_config: dict) -> dict:
        """take raw config dict and normalise values"""
        parsed_config = super()._parse_config(eze_config)

        # ADDITION PARSING: CONFIGS
        # automatically detect and configure rules in semgrep
        if not parsed_config["CONFIGS"]:
            parsed_config["CONFIGS"] = ["p/ci"]
            if has_filetype("Dockerfile"):
                parsed_config["CONFIGS"].append("p/dockerfile")
            if has_filetype(".tf"):
                parsed_config["CONFIGS"].append("p/terraform")
            if has_filetype(".java"):
                parsed_config["CONFIGS"].append("p/java")
            if has_filetype(".py"):
                parsed_config["CONFIGS"].append("p/python")
            if has_filetype(".go"):
                parsed_config["CONFIGS"].append("p/golang")
            if has_filetype(".ml"):
                parsed_config["CONFIGS"].append("p/ocaml")
            if has_filetype(".cs"):
                parsed_config["CONFIGS"].append("p/csharp")
            if has_filetype(".rb"):
                parsed_config["CONFIGS"].append("p/ruby")
            if has_filetype(".js"):
                parsed_config["CONFIGS"].append("p/nodejs")
                parsed_config["CONFIGS"].append("p/javascript")
            if has_filetype(".ts"):
                parsed_config["CONFIGS"].append("p/typescript")
            if has_filetype(".yaml"):
                parsed_config["CONFIGS"].append("p/kubernetes")
            if has_filetype(".php"):
                parsed_config["CONFIGS"].append("p/phpcs-security-audit")
            if has_filetype(".conf") or has_filetype(".vhost"):
                parsed_config["CONFIGS"].append("p/nginx")
        return parsed_config

    @staticmethod
    def print_out_semgrep_timing_report(time_info: dict, total_time: int) -> dict:
        """prints out debug information for semgrep to identifier poorly performing rules"""
        rules = {}
        rules_index = []
        files = {}
        for rule in time_info["rules"]:
            rule_id = rule["id"]
            rules[rule_id] = {"name": rule_id, "time": 0}
            rules_index.append(rule_id)

        rule_parse_time = py_.get(time_info, "rule_parse_info", [])

        for rule_index, rule_parse_time in enumerate(rule_parse_time):
            rule_id = rules_index[rule_index]
            rules[rule_id]["time"] += rule_parse_time

        total_parse_time = 0
        total_match_time = 0
        total_run_time = 0
        for file_timings in time_info["targets"]:
            filename = file_timings["path"]
            file_time = 0
            for rule_index, file_parse_time in enumerate(file_timings["parse_times"]):
                rule_id = rules_index[rule_index]
                rules[rule_id]["time"] += file_parse_time
                file_time += file_parse_time
                total_parse_time += file_parse_time

            for rule_index, file_match_time in enumerate(file_timings["match_times"]):
                rule_id = rules_index[rule_index]
                rules[rule_id]["time"] += file_match_time
                file_time += file_match_time
                total_match_time += file_match_time

            v1_run_times = py_.get(file_timings, "run_times")
            if v1_run_times:
                for rule_index, file_run_time in enumerate(v1_run_times):
                    rule_id = rules_index[rule_index]
                    rules[rule_id]["time"] += file_run_time
                    file_time += file_run_time
                    total_run_time += file_run_time
            else:
                v2_run_time = py_.get(file_timings, "run_time", 0)
                file_time += v2_run_time
                total_run_time += v2_run_time

            files[filename] = {"name": filename, "time": file_time}
        rules = py_.sort_by(rules.values(), "time", reverse=True)
        files = py_.sort_by(files.values(), "time", reverse=True)
        log(
            f"""
Timing
======================
total time: {total_time}
accounted for time: {total_parse_time + total_match_time + total_run_time}
match time: {total_parse_time}
parse time: {total_match_time}
run time: {total_run_time}
"""
        )
        log(
            """
Top 10 slowest rules
======================"""
        )
        for rule in rules[0:10]:
            log(f" {rule['name']}: {rule['time']:0.2f}s")
        log(
            """
Top 10 slowest files
======================"""
        )
        for rule in files[0:10]:
            log(f" {rule['name']}: {rule['time']:0.2f}s")

        return {"rules": rules, "files": files}

    @staticmethod
    def semgrep_severity_to_cwe_severity(semgrep_severity: str) -> str:
        """convert semgrep severities into standard cvss severity

        as per
        https://semgrep.dev/docs/writing-rules/rule-syntax/#schema
        https://nvd.nist.gov/vuln-metrics/cvss"""
        semgrep_severity = semgrep_severity.lower()
        if semgrep_severity == "error":
            return VulnerabilitySeverityEnum.high.name
        if semgrep_severity == "warning":
            return VulnerabilitySeverityEnum.medium.name
        if semgrep_severity == "info":
            return VulnerabilitySeverityEnum.low.name

        return VulnerabilitySeverityEnum.low.name

    @staticmethod
    def extract_semgrep_identifiers(report_event: dict) -> dict:
        """extract semgrep identifiers"""
        metadata = py_.get(report_event, "extra.metadata", {})
        identifiers = {}
        for key in metadata:
            value = metadata[key]
            if key in ("cve", "cwe", "owasp", "bandit-code") and isinstance(value, str):
                identifiers[key] = value
        return identifiers

    @staticmethod
    def extract_semgrep_warnings(parsed_json: dict) -> list:
        """extract semgrep warnings"""
        warnings = []
        errors = parsed_json.get("errors", [])
        for error in errors:
            error_text = f"{error['level']}:{error['type']}"

            error_message_txt = error.get("long_msg")
            if error_message_txt:
                error_text += f": {error_message_txt}"
            else:
                error_message_txt = error.get("message")
                if error_message_txt:
                    error_text += f": {error_message_txt}"

            error_help_txt = error.get("help")
            if error_help_txt:
                error_text += f", {error_help_txt}"

            warnings.append(error_text)
        return warnings
