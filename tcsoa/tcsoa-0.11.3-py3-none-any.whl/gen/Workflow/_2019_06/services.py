from __future__ import annotations

from tcsoa.gen.Workflow._2019_06.Workflow import CreateOrUpdatePALResponse, CreateOrUpdateHandlerResponse, CreateUpdateHandlerInput, GetRegisteredHandlerResponse, CreateUpdateTemplateInput, CreateUpdatePALInput, CreateOrUpdateTemplateResponse
from typing import List
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def getRegisteredHandlers(cls) -> GetRegisteredHandlerResponse:
        """
        This operation returns the list of names of registered workflow handlers. The names returned by this operation 
        are used as an input for creating the handler instance(s).
        
        Use cases:
        In Active Workspace Client, this operation will be used in a Workflow Designer sub-location for following cases:
        
        1.    Creating a new workflow handler instance (EPMHandler) for specified workflow template (EPMTaskTemplate).
        Here user will use the name of the handler (shown as the dropdown list) returned from this service operation.
        """
        return cls.execute_soa_method(
            method_name='getRegisteredHandlers',
            library='Workflow',
            service_date='2019_06',
            service_name='Workflow',
            params={},
            response_cls=GetRegisteredHandlerResponse,
        )

    @classmethod
    def createOrUpdateHandler(cls, input: List[CreateUpdateHandlerInput]) -> CreateOrUpdateHandlerResponse:
        """
        Creates a new instance or updates an existing instance of workflow handler(s). User can add a new workflow
        handler or update existing handler added on a workflow template in a Workflow Designer application.
        
        Use cases:
        In Active Workspace Client, this operation can be used in a Workflow Designer sub-location for following cases:
        
        1.    Creating a new workflow handler instance (EPMHandler) for specified workflow template (EPMTaskTemplate).
        2.    Modifying the exisitng workflow handler instance (EPMHandler) for specified workflow template
        (EPMTaskTemplate).
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateHandler',
            library='Workflow',
            service_date='2019_06',
            service_name='Workflow',
            params={'input': input},
            response_cls=CreateOrUpdateHandlerResponse,
        )

    @classmethod
    def createOrUpdatePAL(cls, input: List[CreateUpdatePALInput]) -> CreateOrUpdatePALResponse:
        """
        Creates or updates or deep copies EPMAssignmentList objects - PAL (Process Assignment List). Newly created
        EPMAssignmentList objects reference a workflow template. These EPMAssignmentList objects can then be used by
        workflow handlers to assign tasks during workflow execution. In Active Workspace, EPMAssignmentList objects can
        be used for assignments in &lsquo;Assignments&rsquo; tab. The &lsquo;Submit to workflow&rsquo; panel can be
        used to perform assignment using EPMAssignmentList configured in the workflow.
        
        Use cases:
        In Active Workspace Client, this operation can be used in &lsquo;Assignment List&rsquo; panel for following
        cases:
        
        1.    Creating new process assignment list (EPMAssignmentList) for specified workflow template
        (EPMTaskTemplate).
        2.    Modifiying resource assignments for a process assignment list object (EPMAssignmentList) . 
        3.    Create new process assignment list(EPMAssignmentList) based on an existing assignment list.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdatePAL',
            library='Workflow',
            service_date='2019_06',
            service_name='Workflow',
            params={'input': input},
            response_cls=CreateOrUpdatePALResponse,
        )

    @classmethod
    def createOrUpdateTemplate(cls, input: List[CreateUpdateTemplateInput]) -> CreateOrUpdateTemplateResponse:
        """
        Creates a new instance or updates an existing instance of workflow task template ( EPMTaskTemplate ). User can
        add a new workflow task template or update an existing task template in a workflow template in Workflow
        Designer application.
        
        Use cases:
        In Active Workspace Client, this operation can be used in a Workflow Designer sub-location for following cases:
        
        1.    Creating a new workflow task template instance (EPMTaskTemplate).
        2.    Modifying the existng workflow task template instance (EPMTaskTemplate) for specified workflow template
        (EPMTaskTemplate).
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateTemplate',
            library='Workflow',
            service_date='2019_06',
            service_name='Workflow',
            params={'input': input},
            response_cls=CreateOrUpdateTemplateResponse,
        )
