from __future__ import annotations

from tcsoa.gen.Workflow._2013_05.Workflow import GetWorkflowTemplatesInputInfo, GetWorkflowTemplatesResponse
from typing import List
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def getWorkflowTemplates(cls, input: List[GetWorkflowTemplatesInputInfo]) -> GetWorkflowTemplatesResponse:
        """
        This operation gets the list of workflow templates based on input criteria. The criteria includes the target
        objects for the workflow or the types of the target objects. User can also specify if the under construction
        templates should to be returned and if the filtered list of templates is required.
        The filtered list of templates are returned based on the users group and the target objects. The filter rules
        can also be customized using the user exits.
        """
        return cls.execute_soa_method(
            method_name='getWorkflowTemplates',
            library='Workflow',
            service_date='2013_05',
            service_name='Workflow',
            params={'input': input},
            response_cls=GetWorkflowTemplatesResponse,
        )
