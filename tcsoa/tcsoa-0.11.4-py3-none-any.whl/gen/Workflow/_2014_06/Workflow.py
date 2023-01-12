from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, User
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApplySignatureInput(TcBaseObj):
    """
    Structure represents the parameters required to apply digital signature on target objects.
    
    :var object: The target object whose digital signature will be applied.
    :var base64String: The Base64 string containing signed information.
    """
    object: BusinessObject = None
    base64String: str = ''


@dataclass
class PerformActionInputInfo(TcBaseObj):
    """
    Structure represents the parameters required to perform an action on an EPMTask or Signoff.
    
    :var clientId: Input string to uniquely identify the input, used primarily for error handling and output mapping.
    
    :var actionableObject: The EPMTask or Signoff on which the action needs to be performed.
    :var action: Action to be performed on EPMTask or Signoff.
    
    Possible values for action are as follows.
    
                    Action                        Description
    
    "SOA_EPM_assign_action"- Assign task or delegate a signoff
    "SOA_EPM_start_action"- Start task
    "SOA_EPM_complete_action"- Mark the task as Complete
    "SOA_EPM_skip_action"- Skip task
    "SOA_EPM_suspend_action"- Suspend task
    "SOA_EPM_resume_action"    - Resume task
    "SOA_EPM_undo_action"- Undo task
    "SOA_EPM_abort_action"- Abort task
    "SOA_EPM_perform_action"- Perform task
    "SOA_EPM_approve_action"- Approve a Review Task
    "SOA_EPM_reject_action"- Reject a Review Task
    "SOA_EPM_promote_action"- Promote task
    "SOA_EPM_demote_action"- Demote task
    "SOA_EPM_assign_approver_action"- This action is not used. Use addSignoffs operations to add users to
    select-signoff-team task
    "SOA_EPM_notify_action"- Notify
    "SOA_EPM_no_action"- No action, results in the comments being set without triggering state change on the task.
    "SOA_EPM_fail_action"- Fail the task
    "SOA_EPM_claim_action"- Claim the task
    :var password: The password for a secure Task. The value of this parameter is ignored for non-secure Task.
    
    :var supportingValue: This argument can be used to send in decision value or result.  If the task is
    perform-signoff task, possible values for decision are:
    - "SOA_EPM_no_decision"
    - "SOA_EPM_approve"
    - "SOA_EPM_reject"
    
    
    
    Following are the result values applicable for different tasks:
    
    - "SOA_EPM_unset"- Do Task, Review Task, Route Task, Ackowledge Task, EPMTask, Condition Task (Auto/Manual),
    select-signoff-team task, Validate Task
    - "SOA_EPM_completed"- Do Task, EPMTask, select-signoff-team task
    - "SOA_EPM_unable_to_complete"- Do Task, EPMTtask, Condition Task (Manual)
    - "SOA_EPM_true"- Condition Task (Auto/Manual)
    - "SOA_EPM_false"- Condition Task (Auto/Manual)
    - "SOA_EPM_no_error"- Validate Task
    
    
    :var supportingObject: If the action is assign, provide a User or ResourcePool to assign the task.
    :var propertyNameValues: Property name and values map that will contain all property names and corresponding string
    values that needs to be saved. e.g. comments can be set on the EPMTask/Signoff by adding it to this map.
    :var signatures: List of ApplySignatureInput objects, each representing target object and its corresponding Base64
    string.
    """
    clientId: str = ''
    actionableObject: BusinessObject = None
    action: str = ''
    password: str = ''
    supportingValue: str = ''
    supportingObject: BusinessObject = None
    propertyNameValues: NameValuePair = None
    signatures: List[ApplySignatureInput] = ()


@dataclass
class SetActiveSurrogateInputInfo(TcBaseObj):
    """
    Structure represents the parameters required to set/unset the logged in user as an active surrogate on the EPMTask
    or Signoff objects and transfer the checkout of the target objects to/from the original user.
    
    :var taskOrSignoffTag: The EPMTask or Signoff business object for which the current user needs to be set/unset as
    an active surrogate.
    :var releaseStandIn: Logged in user is set as an active surrogate on EPMTask or Signoff when value of this
    parameter is false and is released as an active surrogate from the EPMTask or Signoff when value of this parameter
    is true.
    :var transferCheckouts: During Stand-In operation, if the value of this parameter is true, the transfer of checkout
    of the target object(s) from the original user to the current user is performed. During Release operation, if the
    value of this  parameter is true, the transfer of checkout of the target object(s) from the current user to the
    original user is performed. If the value of the parameter is false, transfer of checkout of the target object(s) is
    not performed during Stand-In or Release operation.
    """
    taskOrSignoffTag: BusinessObject = None
    releaseStandIn: bool = False
    transferCheckouts: bool = False


@dataclass
class SurrogateInput(TcBaseObj):
    """
    This operation sets or unsets the surrogate resource for a given User effective for a given date range.
    
    :var unset: If true, remove surrogate; if false, set surrogate.
    :var fromResource: The user for whom the surrogate will be set/unset.
    :var toResource: The surrogate user.
    :var startDate: The date at which the surrogate setting is to take effect.
    :var endDate: The date at which the surrogate setting ceases to be in effect.
    """
    unset: bool = False
    fromResource: User = None
    toResource: User = None
    startDate: datetime = None
    endDate: datetime = None


"""
This map holds property name and vector of property values. This is a generic container that contains the property name as string and the value is the string representation of the property value.
"""
NameValuePair = Dict[str, List[str]]
