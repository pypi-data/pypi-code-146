from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, EPMTask
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def performAction2(cls, task: EPMTask, action: str, comments: str, password: str, supportingValue: str, supportingObject: BusinessObject) -> ServiceData:
        """
        This operation performs an action on a workflow task. The following actions are supported: 
        - Assign
        - Start
        - Complete
        - Skip
        - Suspend
        - Resume
        - Undo
        - Perform
        - Approve
        - Reject
        - Promote
        - Demote
        - Claim
        
        
        
        Use cases:
        User can perform a workflow task from worklist folder in rich or thin client. Similarly, workflow tasks can be
        performed or signed-off using office client as well. This operation can be used to perform or sign-off the
        workflow tasks.
        """
        return cls.execute_soa_method(
            method_name='performAction2',
            library='Workflow',
            service_date='2012_10',
            service_name='Workflow',
            params={'task': task, 'action': action, 'comments': comments, 'password': password, 'supportingValue': supportingValue, 'supportingObject': supportingObject},
            response_cls=ServiceData,
        )
