"""Markdown reporter class implementation"""

from eze.core.reporter import ReporterMeta
from eze.utils.io.file import write_text
from eze.utils.log import log

from eze.utils.markdown_print import (
    scan_results_as_markdown,
)
from eze.utils.cli.exe import exe_variable_interpolation_single


class MarkdownReporter(ReporterMeta):
    """Python report class for echoing output into a markdown report"""

    REPORTER_NAME: str = "markdown"
    SHORT_DESCRIPTION: str = "markdown output file formatter"
    INSTALL_HELP: str = """inbuilt"""
    MORE_INFO: str = """inbuilt"""
    LICENSE: str = """inbuilt"""
    VERSION_CHECK: dict = {"FROM_EZE": True}
    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "default": ".eze/eze_report.md",
            "help_text": """report file location
By default set to eze_report.md""",
        },
        "PRINT_TRANSITIVE_PACKAGES": {
            "type": bool,
            "default": False,
            "environment_variable": "PRINT_TRANSITIVE_PACKAGES",
            "help_text": """print out non top level packages""",
        },
    }

    async def run_report(self, scan_results: list):
        """Method for taking scans and turning then into report output for markdown format"""

        report_str = scan_results_as_markdown(scan_results, self.config["PRINT_TRANSITIVE_PACKAGES"])
        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        file_location = write_text(report_local_filepath, report_str)
        log(f"Written markdown report : {file_location}")
