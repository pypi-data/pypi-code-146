"""JSON reporter class implementation"""

from eze.core.reporter import ReporterMeta
from eze.utils.io.file import write_json
from eze.utils.log import log
from eze.utils.cli.exe import exe_variable_interpolation_single


class JsonReporter(ReporterMeta):
    """Python report class for echoing all output into a json file"""

    REPORTER_NAME: str = "json"
    SHORT_DESCRIPTION: str = "json output file reporter"
    INSTALL_HELP: str = """inbuilt"""
    MORE_INFO: str = """inbuilt"""
    LICENSE: str = """inbuilt"""
    VERSION_CHECK: dict = {"FROM_EZE": True}
    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "default": ".eze/eze_report.json",
            "help_text": """report file location
By default set to eze_report.json""",
        }
    }

    async def run_report(self, scan_results: list):
        """Method for taking scans and turning then into report output"""
        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        json_location = write_json(report_local_filepath, scan_results, beatify_json=True)
        log(f"Written json report : {json_location}")
