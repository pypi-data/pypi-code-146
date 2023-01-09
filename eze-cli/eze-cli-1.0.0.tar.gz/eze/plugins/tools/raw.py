"""Raw Python tool class"""

from eze.core.enums import ToolType, SourceType
from eze.core.tool import ToolMeta, ScanResult
from eze.utils.io.file import load_json
from eze.utils.error import EzeFileAccessError
from eze.utils.cli.exe import exe_variable_interpolation_single


class RawTool(ToolMeta):
    """Raw Python tool class for manually in passing previous or generated scan json report"""

    TOOL_NAME: str = "raw"
    TOOL_URL: str = "https://github.com/RiverSafeUK/eze-cli"
    TOOL_TYPE: ToolType = ToolType.MISC
    SOURCE_SUPPORT: list = [SourceType.ALL]
    SHORT_DESCRIPTION: str = "input for saved eze json reports"
    INSTALL_HELP: str = """inbuilt"""
    LICENSE: str = """inbuilt"""
    VERSION_CHECK: dict = {"FROM_EZE": True}
    MORE_INFO: str = "Tool for ingesting off line and air gapped eze json reports"
    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "required": True,
            "help_text": """Eze report file to ingest
normally REPORT_FILE: eze_report.json""",
            "help_example": "eze_report.json",
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
        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        try:
            # get first scan in json
            scan_result = load_json(report_local_filepath)[0]
            report = ScanResult(scan_result)
            return report
        except EzeFileAccessError:
            raise EzeFileAccessError(f"""Eze Raw tool can not find 'REPORT_FILE' {report_local_filepath}""")
