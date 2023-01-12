from __future__ import annotations

from tcsoa.gen.ImportExport._2017_11.FileImportExport import ExportToApplicationInputData3
from tcsoa.gen.ImportExport._2007_06.FileImportExport import ExportToApplicationResponse
from typing import List
from tcsoa.base import TcService


class FileImportExportService(TcService):

    @classmethod
    def exportToApplication(cls, inputs: List[ExportToApplicationInputData3]) -> ExportToApplicationResponse:
        """
        This operation is used for exporting Teamcenter objects to MSExcel. Each row in the MSExcel sheet can contain
        multiple Teamcener business objects and its properties. Teamcenter business objects should already be created
        so that the objects can be exported to MSExcel using the service operation.
        An MSExcel (.xlsm) file is generated at the server as a result of this operation. If the application format is
        "MSExcel" then the generated sheet is a static Excel spreadsheet. If the application format is "MSExcelLive"
        then the generated sheet is a Live Excel spreadsheet. "Live" sheet means that modifications done to the excel
        data will reflect to Teamcenter. If the export Option is "CheckOutObjects" then the objects will be checked out
        before exporting to Excel. Right now it only supports exporting to MSExcel, but we could support exporting to
        other application like MSWord in the future.
        
        Use cases:
        User can use this service operation to export 4GD objects from content pane to MSExcel. In the generated sheet,
        each row will contain multiple business objects and their properties. The properties can be edited from Excel
        and saved back to Teamcenter and vice versa.
        """
        return cls.execute_soa_method(
            method_name='exportToApplication',
            library='ImportExport',
            service_date='2017_11',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ExportToApplicationResponse,
        )
