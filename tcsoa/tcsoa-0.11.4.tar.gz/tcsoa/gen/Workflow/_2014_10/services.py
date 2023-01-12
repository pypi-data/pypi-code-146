from __future__ import annotations

from tcsoa.gen.Workflow._2014_10.Workflow import CreateWkfInput, CreateWkfOutput, CreateRemoteWkfInput
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def createRemoteWorkflowAsync(cls, createRemoteWkfInput: CreateRemoteWkfInput) -> None:
        """
        This operation submits a request to the Teamcenter Integration Framework (TcIF) to create a workflow at the
        remote site. The request is accomplished by calling the TcIF Web Service operation to invoke the workflow
        groovy process.  The groovy process orchestrates the steps involved in the creation of the workflow process.
        
        Use cases:
        Use this operation to create a workflow process at a remote site based on a specific template and with specific
        attachments and attachment types. For example: When configuring the creation of workflow task from a schedule
        task, one can assign a remote privileged user and a remote workflow owner. When the creation of workflow is
        triggered from the schedule task, the request will be submitted to the Teamcenter Integration Framework (TcIF)
        to orchestrate the replication of attachments, creation of the workflow, creation of the workflow task proxy
        link and the schedule task proxy link.
        
        Exceptions:
        >Throws a service exception if TcGS login fails or if submitting a request to create a remote workflow fails.
        """
        return cls.execute_soa_method(
            method_name='createRemoteWorkflowAsync',
            library='Workflow',
            service_date='2014_10',
            service_name='Workflow',
            params={'createRemoteWkfInput': createRemoteWkfInput},
            response_cls=None,
        )

    @classmethod
    def createWorkflow(cls, input: CreateWkfInput) -> CreateWkfOutput:
        """
        This operation creates a workflow process given the  process template name, workflow owner, responsible party,
        attachments and attachment types.
        
        Use cases:
        Any client can use this operation to create a workflow process in Teamcenter given the process template name,
        workflow owner and the responsible party.  It can also provide the attachments to attach to the workflow
        process. For Example:  Teamcenter Integration Framework can call this operation by providing the process
        template name, workflow owner, responsible party, attachments, attachment types.  Workflow process will be
        created using the given workflow template. The responsibly party and the workflow owner will be assigned to the
        root task. The attachments will be attached using the given attachment relation types. 
        
        Exceptions:
        >Throws an expectation if an unhandled error is encountered during Workflow process creation.
        """
        return cls.execute_soa_method(
            method_name='createWorkflow',
            library='Workflow',
            service_date='2014_10',
            service_name='Workflow',
            params={'input': input},
            response_cls=CreateWkfOutput,
        )
