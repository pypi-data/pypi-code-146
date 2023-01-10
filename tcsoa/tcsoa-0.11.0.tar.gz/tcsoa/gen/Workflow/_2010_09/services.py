from __future__ import annotations

from tcsoa.gen.Workflow._2010_09.Workflow import ApplyTemplateInput, ApplyTemplateResponse
from typing import List
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def applyTemplateToProcesses(cls, applyTemplateInput: List[ApplyTemplateInput], processingMode: int) -> ApplyTemplateResponse:
        """
        Apply the specified templates to all active workflow processes that are based on earlier versions of the
        templates
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='applyTemplateToProcesses',
            library='Workflow',
            service_date='2010_09',
            service_name='Workflow',
            params={'applyTemplateInput': applyTemplateInput, 'processingMode': processingMode},
            response_cls=ApplyTemplateResponse,
        )

    @classmethod
    def applyTemplateToProcessesAsync(cls, applyTemplateInput: List[ApplyTemplateInput]) -> None:
        """
        Apply the specified templates to all active workflow processes that are based on earlier versions of the
        template.
        """
        return cls.execute_soa_method(
            method_name='applyTemplateToProcessesAsync',
            library='Workflow',
            service_date='2010_09',
            service_name='Workflow',
            params={'applyTemplateInput': applyTemplateInput},
            response_cls=None,
        )
