from __future__ import annotations

from typing import List
from tcsoa.gen.Workflow._2020_01.Workflow import SupportedHandlerArgumentsInput, SupportedHandlerArgumentsReponse
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def getSupportedHandlerArguments(cls, input: List[SupportedHandlerArgumentsInput]) -> SupportedHandlerArgumentsReponse:
        """
        Get hints from <handler_name>.json file placed in TC_DATA/workflow_handlers location which is helpful for
        handler creation in Workflow Designer. The following hints are supported by this service operation.
        &bull;    Mandatory arguments.
        &bull;    Optional arguments.
        &bull;    Mutex arguments.
        &bull;    Dependent arguments.
        &bull;    Nullable arguments.
        &bull;    Required one of arguments.
        &bull;    And argument values which allow only particular set of values for eg: list of object types, status,
        relations, LOVs etc.
        
        For detailed information, please refer to Teamcenter Active Workspace Documentation link:
        https://docs.plm.automation.siemens.com/tdoc/aw/4.3/aw_html_collection#uid:xid1284832:index_Configuration:xid1567004:xid1760071
        This link points to Active Workspace documentation path ( applicable Active Workspace 4.3 onwards ): 
        Home > Deployment and Configuration > Configuration and Extensibility > Working with platform customizations >
        Enable your custom workflow handler in Active Workspace
        
        Use cases:
        Data provided by this operation will be used by Workflow Designer in Active Workspace to simplify handler
        configuration in templates.
        """
        return cls.execute_soa_method(
            method_name='getSupportedHandlerArguments',
            library='Workflow',
            service_date='2020_01',
            service_name='Workflow',
            params={'input': input},
            response_cls=SupportedHandlerArgumentsReponse,
        )
