"""Provide scan CLI command."""

import argparse
import itertools
import json
import os
import re
import sys
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, cast

import pydantic.dataclasses
from colorama import Fore, Style
from junitparser import TestSuite, TestCase, Error, JUnitXml, JUnitXmlError, Attr
from pydantic.json import pydantic_encoder
from requests import JSONDecodeError

from spotter.api import ApiClient
from spotter.environment import Environment
from spotter.parsing import parse_ansible_artifacts, ParsingResult
from spotter.rewriting import Suggestion, update_files
from spotter.storage import Storage
from spotter.utils import prompt_yes_no_question


class DisplayLevel(Enum):
    """Enum that holds different levels/statuses for check result."""

    HINT = 1
    WARNING = 2
    ERROR = 3

    def __str__(self) -> str:
        """
        Convert DisplayLevel to lowercase string.

        :return: String in lowercase
        """
        return str(self.name.lower())

    @classmethod
    def from_string(cls, level: str) -> "DisplayLevel":
        """
        Convert string level to DisplayLevel object.

        :param level: Check result level
        :return: DisplayLevel object
        """
        try:
            return cls[level.upper()]
        except KeyError:
            print(f"Error: nonexistent check status display level: {level}, "
                  f"valid values are: {list(str(e) for e in DisplayLevel)}.")
            sys.exit(1)


@pydantic.dataclasses.dataclass
class TaskMetadata:
    """A container for task metadata originating from the original task."""

    file_name: str
    task_line: int
    task_column: int

    @classmethod
    def from_task_meta(cls, task_meta: Dict[str, Any]) -> "TaskMetadata":
        """
        Convert task metadata to TaskMetadata object for storing metadata for Ansible task.

        :param task_meta: Ansible task spotter_metadata content.
        :return: TaskMetadata object
        """
        file_name = task_meta.get("file", "")
        task_line = task_meta.get("line", "")
        task_column = task_meta.get("column", "")

        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        return cls(
            file_name=file_name,
            task_line=task_line,
            task_column=task_column
        )


@pydantic.dataclasses.dataclass
class ScanPayload:
    """A container for information about the scan payload/input."""

    environment: Environment
    tasks: List[Dict[str, Any]]
    playbooks: List[Dict[str, Any]]

    @classmethod
    def from_json_file(cls, import_path: Path) -> "ScanPayload":
        """
        Load ScanPayload object from JSON file.

        :param import_path: File path with JSON to import from
        :return: ScanPayload object holding input tuple (environment, tasks, playbooks)
        """
        try:
            if not import_path.exists():
                print(f"Error: import file at {import_path} does not exist.")
                sys.exit(1)

            with import_path.open("r") as import_file:
                scan_payload = json.load(import_file)
                environment_dict = scan_payload.get("environment", None)
                if environment_dict is not None:
                    environment = Environment(**environment_dict)
                else:
                    environment = Environment()

                return cls(
                    environment=environment,
                    tasks=scan_payload.get("tasks", []),
                    playbooks=scan_payload.get("playbooks", [])
                )
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

    @classmethod
    def from_args(cls, parsing_result: ParsingResult, environment: Environment, upload_metadata: bool,
                  import_payload: Path) -> "ScanPayload":
        """
        Convert CLI arguments to ScanPayload object.

        :param parsing_result: ParsingResult object
        :param environment: Environment object
        :param upload_metadata: Upload metadata (i.e., file names, line and column numbers)
        :param import_payload: Path to file where ScanPayload can be imported from
        :return: ScanPayload object
        """
        if import_payload:
            return cls.from_json_file(import_payload)

        return cls(
            environment=environment,
            tasks=parsing_result.tasks if upload_metadata else parsing_result.tasks_without_metadata(),
            playbooks=parsing_result.playbooks if upload_metadata else parsing_result.playbooks_without_metadata()
        )

    def to_json_file(self, export_path: Path) -> None:
        """
        Export scan payload to JSON file.

        :param export_path: File path to export to (will be overwritten if exists)
        """
        try:
            with export_path.open("w") as export_file:
                json.dump(pydantic_encoder(self), export_file, indent=2)
        except TypeError as e:
            print(f"Error: {str(e)}")
            sys.exit(1)


@pydantic.dataclasses.dataclass
class CheckCatalogInfo:
    """A container for information about the specific check in check catalog from the backend."""

    event_code: str
    event_value: str
    event_message: str
    check_class: str

    @classmethod
    def from_api_response_element(cls, element: Dict[str, Any]) -> "CheckCatalogInfo":
        """
        Convert element entry from scan API response to CheckCatalogInfo object.

        :param element: An 'element' JSON entry from scan API response
        :return: CheckCatalogInfo object
        """
        return cls(
            event_code=element.get("event_code", ""),
            event_value=element.get("event_value", ""),
            event_message=element.get("event_message", ""),
            check_class=element.get("check_class", "")
        )


@pydantic.dataclasses.dataclass
class CheckResult:
    """A container for parsed check results originating from the backend."""

    task_id: str
    original_task: Dict[str, Any]
    task_metadata: TaskMetadata
    catalog_info: CheckCatalogInfo
    level: DisplayLevel
    message: str
    suggestion: Optional[Suggestion]
    doc_url: Optional[str]

    def construct_output(self, disable_colors: bool = False, disable_docs_url: bool = False) -> str:
        """
        Construct CheckResult output using its properties.

        :param disable_colors: Disable output colors and styling
        :param disable_docs_url: Disable outputting URL to documentation
        :return: Formatted output for check result
        """
        task_metadata = self.task_metadata

        result_level = self.level.name.strip().upper()
        out_prefix = f"{task_metadata.file_name}:{task_metadata.task_line}:{task_metadata.task_column}: {result_level}"
        out_message = self.message.strip()
        if not disable_colors:
            if result_level == DisplayLevel.ERROR.name:
                out_prefix = Fore.RED + out_prefix + Fore.RESET
                out_message = re.sub(r"'([^']*)'", Style.BRIGHT + Fore.RED + r"\1" + Fore.RESET + Style.NORMAL,
                                     out_message)
            elif result_level == DisplayLevel.WARNING.name:
                out_prefix = Fore.YELLOW + out_prefix + Fore.RESET
                out_message = re.sub(r"'([^']*)'", Style.BRIGHT + Fore.YELLOW + r"\1" + Fore.RESET + Style.NORMAL,
                                     out_message)
            else:
                out_message = re.sub(r"'([^']*)'", Style.BRIGHT + r"\1" + Style.NORMAL, out_message)

        output = f"{out_prefix}: {out_message}".strip()
        if not output.endswith("."):
            output += "."
        if not disable_docs_url and self.doc_url:
            output = f"{output} View docs at {self.doc_url}."

        return output


@pydantic.dataclasses.dataclass
class ScanResult:
    """A container for scan result/output originating from the backend."""

    # TODO: Add more fields from scan response if we need them
    uuid: Optional[str]
    user: Optional[str]
    user_info: Optional[Dict[str, Any]]
    project: Optional[str]
    environment: Optional[Dict[str, Any]]
    scan_date: Optional[str]
    status: Optional[str]
    subscription: Optional[str]
    is_paid: Optional[bool]
    check_results: List[CheckResult]

    @staticmethod
    def parse_check_results(response_json: Dict[str, Any], input_tasks: List[Dict[str, Any]]) -> List[CheckResult]:
        """
        Parse result objects and map tasks with complete information.

        :param response_json: The backend API response in JSON format
        :param input_tasks: The scanned tasks with no information removed
        :return: A list of check results
        """
        check_results: List[CheckResult] = []
        for element in response_json.get("elements", []):
            task_id = element.get("task_id", "")
            suggestion = element.get("suggestion", "")

            # match the result task's ID to the original task (with complete information)
            original_task: Optional[Dict[str, Any]] = None
            for task in input_tasks:
                if task.get("task_id", None) == task_id:
                    original_task = task
                    break

            # guard against incomplete results where we don't match a task
            if original_task is None:
                print("Could not map task ID to its original task.")
                continue

            # guard against missing task args and metadata
            task_meta = original_task.get("spotter_metadata", None)

            if task_meta:
                task_metadata_object = TaskMetadata.from_task_meta(task_meta)
                suggestion_object: Optional[Suggestion] = None
                if suggestion:
                    suggestion_object = Suggestion.from_task(original_task, suggestion)

                check_results.append(
                    CheckResult(
                        task_id, original_task, task_metadata_object,
                        CheckCatalogInfo.from_api_response_element(element),
                        DisplayLevel.from_string(element.get("level", "")), element.get("message", ""),
                        suggestion_object, element.get("doc_url", "")
                    )
                )

        return check_results

    @classmethod
    def from_api_response(cls, response_json: Dict[str, Any], input_tasks: List[Dict[str, Any]]) -> "ScanResult":
        """
        Convert scan API response to ScanResult object.

        :param response_json: The backend API response in JSON format
        :param input_tasks: The scanned tasks with no information removed
        :return: A list of check results
        """
        return cls(
            uuid=response_json.get("id", ""),
            user=response_json.get("user", ""),
            user_info=response_json.get("user_info", {}),
            project=response_json.get("project", ""),
            environment=response_json.get("environment", {}),
            scan_date=response_json.get("scan_date", ""),
            status=response_json.get("status", ""),
            subscription=response_json.get("subscription", ""),
            is_paid=response_json.get("is_paid", ""),
            check_results=cls.parse_check_results(response_json, input_tasks)
        )

    def filter_check_results(self, threshold: DisplayLevel) -> None:
        """
        Filter a list of check results by only keeping tasks over a specified severity level.

        :param threshold: The DisplayLevel object as threshold (inclusive) of what level messages (and above) to keep
        """
        self.check_results = [cr for cr in self.check_results if cr.level.value >= threshold.value]

    def sort_check_results(self) -> None:
        """Sort a list of check results by filenames (alphabetically) and also YAML line and column numbers."""
        self.check_results.sort(key=lambda cr: (
            cr.task_metadata.file_name, int(cr.task_metadata.task_line), int(cr.task_metadata.task_column)
        ))

    def print_check_results(self, disable_colors: bool = False, disable_docs_url: bool = False) -> None:
        """
        Render a list of results into the console (assumes results are pre-filtered).

        :param disable_colors: Disable output colors and styling
        :param disable_docs_url: Disable outputting URL to documentation
        """
        for result in self.check_results:
            print(result.construct_output(disable_colors, disable_docs_url))

        if len(self.check_results) > 0:
            def level_sort_key(level: DisplayLevel) -> int:
                return cast(int, level.value)

            worst_level = max((cr.level for cr in self.check_results), key=level_sort_key)

            print("------------------------------------------------------------------------")

            overall_status_message = f"Overall status: {worst_level.name.upper()}"
            if not disable_colors:
                overall_status_message = Style.BRIGHT + overall_status_message
            print(overall_status_message)

    def export_check_results_junit_xml(self, export_path: Path, disable_docs_url: bool = False) -> None:
        """
        Render a list of results into the console (assumes results are pre-filtered).

        :param export_path: File path to export JUnit XML to (will be overwritten if exists)
        :param disable_docs_url: Disable outputting URL to documentation
        """
        try:
            # add custom attributes for JUnit XML schema
            TestCase.file = Attr("file")

            xml = JUnitXml()
            get_check_class = lambda res: res.catalog_info.check_class  # pylint: disable=unnecessary-lambda-assignment
            for check_class, check_results in itertools.groupby(sorted(self.check_results, key=get_check_class),
                                                                get_check_class):
                suite = TestSuite(check_class)
                check_count = 0

                for result in check_results:
                    test_case = TestCase(
                        f"{result.catalog_info.event_code}-{result.catalog_info.event_value}[{check_count}]",
                        check_class
                    )
                    test_case.id = result.catalog_info.event_code
                    test_case.file = result.task_metadata.file_name
                    test_case.result = [
                        Error(result.construct_output(True, disable_docs_url), result.level.name.upper())]

                    suite.append(test_case)
                    check_count += 1

                suite.tests = check_count
                suite.errors = check_count
                xml.add_testsuite(suite)

            xml.write(export_path)
        except JUnitXmlError as e:
            print(f"Error exporting JUnit XML: {e}.")
            sys.exit(1)

    def apply_check_result_suggestions(self, scan_paths: List[Path]) -> None:
        """
        Automatically apply suggestions.

        :param scan_paths: A list of original paths to Ansible artifacts provided for scanning
        """
        all_suggestions = [cr.suggestion for cr in self.check_results if cr.suggestion is not None]

        # TODO: Remove when we find a solution for accessing original paths to Ansible artifacts provided for scanning
        for suggestion in all_suggestions:
            suggestion.file_parent = suggestion.file.parent
            for scan_path in scan_paths:
                if scan_path in (scan_path / suggestion.file).parents:
                    suggestion.file_parent = scan_path
                    break

        update_files(all_suggestions)


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new scan command parser to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "scan", help="Initiate Ansible scan", description="Initiate Ansible scan"
    )
    parser.add_argument(
        "--project-id", "-t", type=str, help="UUID of an existing project (default project from "
                                             "personal organization will be used if not specified)",
    )
    parser.add_argument(
        "--config", "-c", type=lambda p: Path(p).absolute(), help="Configuration file (as JSON/YAML)"
    )
    parser.add_argument(
        "--option", "-o", type=lambda s: s.strip().split("="), action="append", default=[],
        help="Additional config variable as key=value pair, for example ansible_version=2.13"
    )
    parser.add_argument(
        "--upload-values", action="store_true",
        help="Parse and upload values from Ansible task parameters",
    )
    parser.add_argument(
        "--parse-values", "-p", dest="upload_values", action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--upload-metadata", action="store_true",
        help="Upload metadata (i.e., file names, line and column numbers) to portal",
    )
    parser.add_argument(
        "--rewrite", "-r", action="store_true", help="Rewrite files with fixes",
    )
    parser.add_argument(
        "--display-level", "-l", type=DisplayLevel.from_string,
        choices=list(DisplayLevel), default=DisplayLevel.HINT,
        help="Display only check results with specified level or greater "
             "(e.g., -l warning will show all warnings and errors, but suppress hints)"
    )
    parser.add_argument(
        "--no-docs-url", action="store_true", help="Disable outputting URL to documentation"
    )
    parser.add_argument(
        "--junit-xml", "-j", type=lambda p: Path(p).absolute(),
        help="Output file path to export the scan result to a file in JUnit XML format"
    )
    import_export_group = parser.add_mutually_exclusive_group()
    import_export_group.add_argument(
        "--import-payload", "-i", type=lambda p: Path(p).absolute(),
        help="Path to the previously exported file to be sent for scanning"
    )
    import_export_group.add_argument(
        "--export-payload", "-e", type=lambda p: Path(p).absolute(),
        help="Output file path to export the locally scanned data without sending anything for scanning at the server"
    )
    parser.add_argument(
        "path", type=lambda p: Path(p).absolute(), nargs="*", help="Path to Ansible artifact or directory",
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    # pylint: disable=too-many-branches,too-many-locals, too-many-statements
    """
    Execute callback for scan command.

    :param args: Argparse arguments
    """
    api_endpoint = os.environ.get("SPOTTER_ENDPOINT", "")
    storage_path = args.storage_path or Storage.DEFAULT_PATH
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")
    scan_paths = args.path

    if args.import_payload and scan_paths:
        print("Error: the --import-payload is mutually exclusive with positional arguments.")
        sys.exit(1)

    if args.export_payload and not scan_paths or (
            not args.export_payload and not args.import_payload and not scan_paths):
        print("Error: no paths provided for scanning.")
        sys.exit(1)

    # create and set environment
    # the order that we read configuration is the following (in each step we overwrite what the previous one has):
    # 1. local discovery (from user's current workspace)
    # 2. config file (JSON/YAML file provided after --config flag)
    # 3. options provided as key=value pairs to the scan command
    environment = Environment.from_local_discovery(scan_paths)
    if args.config:
        environment = environment.combine(Environment.from_config_file(args.config))
    if args.option:
        extra_vars = {}
        for key_value in args.option:
            if len(key_value) != 2:
                print(f"Error: '{'='.join(key_value)}' extra option is not specified as key=value.")
                sys.exit(1)
            else:
                extra_vars[key_value[0]] = key_value[1]

        environment = environment.combine(Environment.from_extra_vars(extra_vars))

    environment.cli_scan_args = {
        "parse_values": args.upload_values,  # deprecated - but currently mandatory on backend
        "upload_values": args.upload_values,
        "upload_metadata": args.upload_metadata,
        "rewrite": args.rewrite,
        "display_level": str(args.display_level)
    }

    parsing_result = parse_ansible_artifacts(scan_paths, parse_values=bool(args.upload_values))
    scan_payload = ScanPayload.from_args(parsing_result, environment, args.upload_metadata, args.import_payload)
    if args.export_payload:
        if not args.upload_metadata:
            print("Warning: exporting without the --upload-metadata won't allow you to properly import payload.")
            yes = prompt_yes_no_question(default_yes_response=False)
            if not yes:
                sys.exit(0)

        scan_payload.to_json_file(args.export_payload)

        file_name = str(args.export_payload)
        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        print(f"Scan data saved to {file_name}.\nNote: this operation is fully offline. No actual scan was executed.")
        sys.exit(0)
    else:
        scan_result = scan(api_endpoint, storage_path, username, password, scan_payload, parsing_result,
                           args.display_level, args.project_id)

        if args.junit_xml:
            scan_result.export_check_results_junit_xml(args.junit_xml, args.no_docs_url)
            print(f"Scan result exported to {args.junit_xml} in JUnit XML format.")
            sys.exit(0)
        else:
            scan_result.print_check_results(args.no_colors, args.no_docs_url)

            if args.rewrite:
                scan_result.apply_check_result_suggestions(scan_paths)

            if len(scan_result.check_results) > 0:
                sys.exit(1)


# pylint: disable=too-many-arguments
def scan(api_endpoint: str, storage_path: Path, username: Optional[str], password: Optional[str],
         scan_payload: ScanPayload, parsing_result: ParsingResult, display_level: DisplayLevel,
         project_id: Optional[str] = None) -> ScanResult:
    """
    Scan Ansible content and return scan result.

    :param api_endpoint: Steampunk Spotter API endpoint
    :param storage_path: Path to storage
    :param username: Steampunk Spotter username
    :param password: Steampunk Spotter password
    :param scan_payload: ScanPayload object
    :param parsing_result: ParsingResult object
    :param display_level: DisplayLevel object
    :param project_id: Project id
    :return: ScanResult object
    """
    storage = Storage(storage_path)

    # TODO: extract this to a separate configuration component along with other configuration file options
    if not api_endpoint:
        if storage.exists("spotter.json"):
            storage_configuration_json = storage.read_json("spotter.json")
            api_endpoint = storage_configuration_json.get("endpoint", ApiClient.DEFAULT_ENDPOINT)
        else:
            api_endpoint = ApiClient.DEFAULT_ENDPOINT

    api_client = ApiClient(api_endpoint, storage, username, password)

    if project_id:
        response = api_client.post(f"/v2/scans/?project={project_id}", payload=pydantic_encoder(scan_payload),
                                   timeout=120)
    else:
        response = api_client.post("/v2/scans/", payload=pydantic_encoder(scan_payload), timeout=120)

    try:
        response_json = response.json()
    except JSONDecodeError as e:
        print(f"Error: scan result cannot be converted to JSON: {str(e)}")
        sys.exit(1)

    scan_result = ScanResult.from_api_response(response_json, parsing_result.tasks)
    # TODO: Remove when scan API endpoint will be able to filter check results based on display level query param
    scan_result.filter_check_results(display_level)
    # TODO: figure out if we can sort returned check results by tasks line numbers and columns on the backend
    scan_result.sort_check_results()

    return scan_result
