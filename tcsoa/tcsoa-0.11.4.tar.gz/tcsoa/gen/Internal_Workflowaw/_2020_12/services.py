from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Workflowaw._2020_12.Workflow import UpdateTaskAssignmentsReponse, TaskAssignmentsInput, TaskAssignmentsResponse, UpdateTaskAssignmentsInput
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def getWorkflowTaskAssignments(cls, inData: List[TaskAssignmentsInput]) -> TaskAssignmentsResponse:
        """
        Get the assigments for all tasks or future tasks of the process (EPMJob) for which input EPMTask or
        EPMTaskTemplate belongs to.The assignments may be for EPMTask responsible party (User or ResourcePool) or for
        Signoffs (GroupMember or ResourcePool). These are presented as Reviewers, Acknowlegers, Notifiers (for Signoff)
        or Assignees (for task responsible party) on individual tasks.It also contains information about the origin of
        the task assigments. For example, EPMSignoffProfile, ResourcePool or Participant object.
        
        Use cases:
        Details provided by this operation are be displayed in the assignments panel to get an overview of the task
        assignments of all tasks for a workflow.
        """
        return cls.execute_soa_method(
            method_name='getWorkflowTaskAssignments',
            library='Internal-Workflowaw',
            service_date='2020_12',
            service_name='Workflow',
            params={'inData': inData},
            response_cls=TaskAssignmentsResponse,
        )

    @classmethod
    def updateWorkflowTaskAssignments(cls, inData: List[UpdateTaskAssignmentsInput]) -> UpdateTaskAssignmentsReponse:
        """
        Updates the assigments for all the tasks sent as input parameter. The assignments may be for EPMTask
        responsible party (User or ResourcePool) or for Signoffs (GroupMember or User or ResourcePool. These are
        presented as Reviewers, Acknowlegers, Notifiers (for Signoff) or Assignees (for EPMTask responsible party) on
        individual tasks. Apart from task assignments, it also contains the assignees of dynamic Participant and\or
        members of the signoff profile (EPMSignoffProfile) that are changed and that needs to be updated.
        
        Use cases:
        This operation provides details to update the task assignments , members of the signoff profiles
        (EPMSignoffProfile) and the dynamic participant (Participant) assignees.
        """
        return cls.execute_soa_method(
            method_name='updateWorkflowTaskAssignments',
            library='Internal-Workflowaw',
            service_date='2020_12',
            service_name='Workflow',
            params={'inData': inData},
            response_cls=UpdateTaskAssignmentsReponse,
        )
