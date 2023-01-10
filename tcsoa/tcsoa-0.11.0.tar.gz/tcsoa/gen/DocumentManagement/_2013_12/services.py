from __future__ import annotations

from typing import List
from tcsoa.gen.DocumentManagement._2013_12.PrintOrRender import PrinterDefinitionResponse, RenderSubmitRequestInfo, PrintSubmitRequestInfo, SubmitRequestResponse
from tcsoa.base import TcService


class PrintOrRenderService(TcService):

    @classmethod
    def printSubmitRequest(cls, input: List[PrintSubmitRequestInfo]) -> SubmitRequestResponse:
        """
        This operation submits print requests for batch printing.
        
        Use cases:
        The client can call this operation to do batch printing. Batch printing lets you select workspace objects, such
        as Item, ItemRevision, or Dataset objects, and print the associated documents with system stamps and watermarks.
        """
        return cls.execute_soa_method(
            method_name='printSubmitRequest',
            library='DocumentManagement',
            service_date='2013_12',
            service_name='PrintOrRender',
            params={'input': input},
            response_cls=SubmitRequestResponse,
        )

    @classmethod
    def renderSubmitRequest(cls, input: List[RenderSubmitRequestInfo]) -> SubmitRequestResponse:
        """
        This operation submits render requests for rendering.
        
        Use cases:
        The client can call this operation to do the rendering on ItemRevision objects. When you render an ItemRevision
        object containing a dataset, you translate the associated file to an alternate format.
        """
        return cls.execute_soa_method(
            method_name='renderSubmitRequest',
            library='DocumentManagement',
            service_date='2013_12',
            service_name='PrintOrRender',
            params={'input': input},
            response_cls=SubmitRequestResponse,
        )

    @classmethod
    def getPrinterDefinitions(cls) -> PrinterDefinitionResponse:
        """
        This operation returns Print Definition information from the PrintConfiguration objects defined in Teamcenter.
        
        Use cases:
        The client wants to get the information required for the Batch Print operation printSubmitRequest.
        """
        return cls.execute_soa_method(
            method_name='getPrinterDefinitions',
            library='DocumentManagement',
            service_date='2013_12',
            service_name='PrintOrRender',
            params={},
            response_cls=PrinterDefinitionResponse,
        )
