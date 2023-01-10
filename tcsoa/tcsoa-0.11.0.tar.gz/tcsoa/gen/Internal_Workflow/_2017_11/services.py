from __future__ import annotations

from tcsoa.gen.Internal.Workflow._2017_11.Workflow import CreateWorkflowInput
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def createWorkflowAsync(cls, inputData: CreateWorkflowInput) -> None:
        """
        Operation to create a workflow process in an asynchrous fashion. A workflow process is the running instance of
        a workflow template. This operation can be used to create a workflow process or sub process at a local or a
        remote site from a given workflow template in an asynchrous fashion.
        
        Use cases:
        Creating a workflow process in asynchronous mode improves the performance of the workflow creation by
        submitting the create request for background processing. This is especially useful when workflow is created
        from a very large workflow template. Creating a workflow using a large workflow template can take long time,
        since it involves creation of many objects, such as: tasks (EPMTask), signoff objects (Signoff),  and process
        instance (EPMJob). So, for cases that use large workflow templates, this SOA can be used to submit the workflow
        creation in background to improve performance.
        """
        return cls.execute_soa_method(
            method_name='createWorkflowAsync',
            library='Internal-Workflow',
            service_date='2017_11',
            service_name='Workflow',
            params={'inputData': inputData},
            response_cls=None,
        )
