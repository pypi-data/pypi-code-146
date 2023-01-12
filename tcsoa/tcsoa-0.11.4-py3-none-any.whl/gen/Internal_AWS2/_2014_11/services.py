from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2014_11.RequirementsManagement import GetTemplateInput, GetExportTemplateResponse
from typing import List
from tcsoa.base import TcService
from tcsoa.gen.Internal.AWS2._2014_11.Workflow import WorkflowGraphResponse, WorkflowGraphInput, WorkflowGraphLegendResponse


class WorkflowService(TcService):

    @classmethod
    def getWorkflowGraph(cls, input: List[WorkflowGraphInput]) -> WorkflowGraphResponse:
        """
        This operation returns the latest workflow associated with selected WorkspaceObjects.
        
        Use cases:
        An Active workspace user selects an ItemRevision and wants to see the currently running workflow associated
        with it.
        """
        return cls.execute_soa_method(
            method_name='getWorkflowGraph',
            library='Internal-AWS2',
            service_date='2014_11',
            service_name='Workflow',
            params={'input': input},
            response_cls=WorkflowGraphResponse,
        )

    @classmethod
    def getWorkflowGraphLegend(cls, viewName: str) -> WorkflowGraphLegendResponse:
        """
        This operation returns a localized list of objects and relation type names which are used to represent the
        task(s) and path(s) in a Workflow graph. This list of objects and relation type names is the filter which is
        applied during the graph navigation.
        
        Use cases:
        An Active Workspace user selects an object and opens the Workflow tab. System responds by returning the latest
        workflow associated with the selected object. The task(s) and the path(s) shown in the workflow will have the
        colors, shapes,edges as per the configutation.
        """
        return cls.execute_soa_method(
            method_name='getWorkflowGraphLegend',
            library='Internal-AWS2',
            service_date='2014_11',
            service_name='Workflow',
            params={'viewName': viewName},
            response_cls=WorkflowGraphLegendResponse,
        )


class RequirementsManagementService(TcService):

    @classmethod
    def getExportTemplates(cls, filter: List[GetTemplateInput]) -> GetExportTemplateResponse:
        """
        This operation retrieves export templates from database.These export templates are of type SpecTemplate and
        ExcelTemplate that are used to exporting Teamcenter objects to Office applications using the template option.
        The templates are retrieved based on the input filter.
        """
        return cls.execute_soa_method(
            method_name='getExportTemplates',
            library='Internal-AWS2',
            service_date='2014_11',
            service_name='RequirementsManagement',
            params={'filter': filter},
            response_cls=GetExportTemplateResponse,
        )
