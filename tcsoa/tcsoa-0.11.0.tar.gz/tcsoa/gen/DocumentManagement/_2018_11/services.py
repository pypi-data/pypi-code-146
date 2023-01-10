from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.DocumentManagement._2018_11.PrintOrRender import ContainsRenderableFilesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class PrintOrRenderService(TcService):

    @classmethod
    def containsRenderableFiles(cls, selectedObjects: List[BusinessObject], renderFormat: str) -> ContainsRenderableFilesResponse:
        """
        Checks to see if 'selectedObjects' contains any files that can be rendered to the 'renderFormat' using the
        Dispatcher Render Management translator.
        
        Use cases:
        This operation is intended to be called to determine the visibility of commands such as the "Generate PDF"
        one-step command.
        
        Generate PDF (one-step command): The user selects one or more Dataset or ItemRevision (or sub-type) objects in
        Active Workspace.  The 'containsRenderableFiles' operation is called by the Active Workspace client framework
        to determine if there are any files within 'selectedObjects' that can be rendered to pdf.  If any renderable
        files are found, then the "Generate PDF" command becomes visible.  If no renderable files are found, then the
        "Generate PDF" command remains hidden.
        """
        return cls.execute_soa_method(
            method_name='containsRenderableFiles',
            library='DocumentManagement',
            service_date='2018_11',
            service_name='PrintOrRender',
            params={'selectedObjects': selectedObjects, 'renderFormat': renderFormat},
            response_cls=ContainsRenderableFilesResponse,
        )

    @classmethod
    def renderFilesSubmitRequest(cls, selectedObjects: List[BusinessObject], renderFormat: str, saveRenderedFiles: bool) -> ServiceData:
        """
        Submits a Render Management Dispatcher request to render the files within the selected objects to the specified
        file format without requiring any Item Revision Document Control (IRDC) forms to be defined in Business Modeler
        Integrated Development Environment (BMIDE).
        
        Use cases:
        Generate PDF:
        The user selects one or more Dataset or ItemRevision (or sub-type) objects in Active Workspace.  The
        'containsRenderableFiles' operation is called to determine if there are any files in the selected objects that
        can be rendered to pdf.  If any renderable files are found, the "Generate PDF" one-step command becomes
        visible.  If the user clicks on the "Generate PDF" command, the 'renderFilesSubmitRequest' operation is called
        to submit a Render Management Dispatcher request to render the valid files within the selected objects to pdf. 
        When the files have been rendered, an alert notification will be sent to inform the user that the rendering is
        complete.
        """
        return cls.execute_soa_method(
            method_name='renderFilesSubmitRequest',
            library='DocumentManagement',
            service_date='2018_11',
            service_name='PrintOrRender',
            params={'selectedObjects': selectedObjects, 'renderFormat': renderFormat, 'saveRenderedFiles': saveRenderedFiles},
            response_cls=ServiceData,
        )
