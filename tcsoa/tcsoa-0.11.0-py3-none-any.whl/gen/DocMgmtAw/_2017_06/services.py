from __future__ import annotations

from tcsoa.gen.DocMgmtAw._2017_06.DocMgmt import PrinterDefinitionResponse
from tcsoa.base import TcService


class DocMgmtService(TcService):

    @classmethod
    def getPrinterDefinitions(cls) -> PrinterDefinitionResponse:
        """
        This operation returns Print Configuration definition information from the PrintConfiguration object defined in
        Teamcenter.
        
        Use cases:
        The client wants to get the print configuration information required for the Batch Printing action in Active
        Workspace.
        """
        return cls.execute_soa_method(
            method_name='getPrinterDefinitions',
            library='DocMgmtAw',
            service_date='2017_06',
            service_name='DocMgmt',
            params={},
            response_cls=PrinterDefinitionResponse,
        )
