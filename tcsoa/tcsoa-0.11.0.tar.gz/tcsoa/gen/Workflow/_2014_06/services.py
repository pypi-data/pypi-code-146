from __future__ import annotations

from tcsoa.gen.Workflow._2014_06.Workflow import SurrogateInput, ApplySignatureInput, PerformActionInputInfo, SetActiveSurrogateInputInfo
from tcsoa.gen.BusinessObjects import BusinessObject, User, EPMTask
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from datetime import datetime


class WorkflowService(TcService):

    @classmethod
    def performAction3(cls, input: List[PerformActionInputInfo]) -> ServiceData:
        """
        This operation performs an action on an EPMTask or Signoff. This operation also allows user to digitally sign
        the target objects in a workflow.
         
        Note:
        The Teamcenter session should be configured with HTTPS as the password in the input structure is not encrypted.
        
        Following actions are supported on EPMTask.
        
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
        
        
        
        Following action is supported on Signoff.
        
        - Assign
        
        
        This action will delegate a Signoff to a different GroupMember or ResourcePool and records the comments
        supplied while performing delegate operation in the audit log. User may use workflowService.getResourcePool
        method To get the ResourcePool business object from only group or only role or both.
        
        Use cases:
        Use Case 1: User can perform a workflow task.
        Description: User can perform an EPMTask from worklist folder in rich or thin client. Similarly EPMTask can be
        performed or signed-off using office client as well. This operation can be used to perform or signoff the
        workflow tasks.
        
        Use Case 2: User can assign or delegate a Signoff to a different GroupMember or ResourcePool and provide
        optional comments while performing delegate operation.
        Description: When a user delegates a Signoff to a different GroupMember or ResourcePool,  the comments provided
        while performing delegate operation gets recorded in the audit log.
        """
        return cls.execute_soa_method(
            method_name='performAction3',
            library='Workflow',
            service_date='2014_06',
            service_name='Workflow',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def performActionWithSignature(cls, task: EPMTask, action: str, comments: str, password: str, supportingValue: str, supportingObject: BusinessObject, signatures: List[ApplySignatureInput]) -> ServiceData:
        """
        This operation performs an action on workflow task. The following actions are supported.
        
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
        User can perform a workflow task from worklist folder in rich or thin client. Similarly, workflow tasks
        can be performed or signed-off using office client as well.This operation can be used to perfrom or sign-off
        the workflow tasks.
        """
        return cls.execute_soa_method(
            method_name='performActionWithSignature',
            library='Workflow',
            service_date='2014_06',
            service_name='Workflow',
            params={'task': task, 'action': action, 'comments': comments, 'password': password, 'supportingValue': supportingValue, 'supportingObject': supportingObject, 'signatures': signatures},
            response_cls=ServiceData,
        )

    @classmethod
    def setActiveSurrogate(cls, input: List[SetActiveSurrogateInputInfo]) -> ServiceData:
        """
        This operation sets/unsets the logged in user as an active surrogate on a given EPMTask or Signoff. It
        transfers checkout of the target object(s) to/from the logged in user from/to the original user.
        
        Use cases:
        Use Case 1: User can Stand In for an EPMTask or Signoff with Transfer Check-Out(s).
        Description: When a user is set as a surrogate and wants to perform received task in the original user's inbox
        while allowing the original user to retain control, user can Stand-In for the EPMTask or Signoff. The transfer
        of checkout of the target object(s) from the original user is done when the boolean input parameter
        transferCheckouts is set to true. 
        
        Use Case 2: User is released from EPMTask or Signoff with Transfer Check-Out(s).
        Description: Releases current user as an active surrogate for a EPMTask or Signoff. The transfer of checkout of
        the target object(s) from the current user to the original user is done when the boolean input parameter
        transferCheckouts is set to true.
        
        Use Case 3: User can Stand-In for an EPMTask or Signoff without Transfer Check-Out(s).
        Description: When a user is set as a surrogate and wants to perform the task in the original user's inbox while
        allowing the original user to retain control, user can Stand-In for the EPMTask or Signoff. The target
        object(s) will remain checked out to the original user if they were checked out before the Stand-In operation
        was performed.
        
        Use Case 4: User is released for EPMTask or Signoff without Transfer Check-Out(s).
        Description: Releases current user as an active surrogate for an EPMTask or Signoff. The target object(s) will
        remain checked out to the current user if the transfer of checkout(s) was done while Stand-In operation was
        performed.
        """
        return cls.execute_soa_method(
            method_name='setActiveSurrogate',
            library='Workflow',
            service_date='2014_06',
            service_name='Workflow',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def setOutOfOffice(cls, fromResource: User, toResource: BusinessObject, startDate: datetime, endDate: datetime) -> ServiceData:
        """
        This operation sets/unsets Out of Office resource for a given user. The Out of Office resource can be a User or
        a ResourcePool. The Out of Office setting is effective for the specified date range. 
        
        Use cases:
        Use Case 1: User sets Out of Office
        Description: When a user is going to be out of the office and wants to have someone receive the tasks during
        his/her absence then user sets Out of Office. If the end date is not provided then all the future tasks will be
        delegated indefinitely. 
        
        Use Case 2: System Administrator sets Out of Office for another user
        Description: When a user is out of the office but does not have Out of Office setting then System Administrator
        can set Out of Office for the user. Also, group administrators will only be able to set the Out of Office for
        users within their group.
        
        Use Case 3:  User modifies Out of Office settings
        Description: When a user has set Out of Office and during this period if the Out of Office resource is also
        going to be out of the office then System Administrator can modify the Out of Office settings of the user 
        
        Use Case 4:  User unsets Out of Office settings
        Description: When a user who has set Out of Office is back before the specified end date then he/she can unset
        the current Out of Office setting. The startDate and endDate parameters will be set to null and the toResource
        paramenter will be set to an empty object.
        """
        return cls.execute_soa_method(
            method_name='setOutOfOffice',
            library='Workflow',
            service_date='2014_06',
            service_name='Workflow',
            params={'fromResource': fromResource, 'toResource': toResource, 'startDate': startDate, 'endDate': endDate},
            response_cls=ServiceData,
        )

    @classmethod
    def setSurrogate(cls, requests: List[SurrogateInput]) -> ServiceData:
        """
        This operation sets or unsets the surrogate resource for a given User effective for a given date range.
        """
        return cls.execute_soa_method(
            method_name='setSurrogate',
            library='Workflow',
            service_date='2014_06',
            service_name='Workflow',
            params={'requests': requests},
            response_cls=ServiceData,
        )
