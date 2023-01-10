from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Group, Signoff, ResourcePool, EPMAssignmentList, EPMTask, EPMSignoffProfile, EPMTaskTemplate, Role
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetResourcePoolOutput(TcBaseObj):
    """
    Structure containing the Resource Pool matching the GroupRoleRef and the ServiceData
    
    :var resourcePoolInfo: resourcePoolInfo
    :var serviceData: serviceData
    """
    resourcePoolInfo: List[ResourcePoolInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AssignmentLists(TcBaseObj):
    """
    Process Assignment Lists
    
    :var assignedLists: assignedLists
    :var ownedLists: ownedLists
    :var groupLists: groupLists
    :var otherLists: otherLists
    :var serviceData: Service data - returns index of the input vector if call on that fails
    """
    assignedLists: List[EPMAssignmentList] = ()
    ownedLists: List[EPMAssignmentList] = ()
    groupLists: List[EPMAssignmentList] = ()
    otherLists: List[EPMAssignmentList] = ()
    serviceData: ServiceData = None


@dataclass
class GroupRoleRef(TcBaseObj):
    """
    Structure containing the group and role info
    
    :var groupTag: groupTag
    :var roleTag: roleTag
    :var allowSubGroup: allowSubGroup
    :var isAllMembers: isAllMembers
    """
    groupTag: Group = None
    roleTag: Role = None
    allowSubGroup: int = 0
    isAllMembers: int = 0


@dataclass
class InstanceInfo(TcBaseObj):
    """
    Structure containing information related to the new process
    
    :var instanceKey: instanceKey. supported in future
    :var newProcessDepTask: newProcessDepTask. supported in future
    :var newProcessUrl: newProcessUrl. supported in future
    :var newProcessDepTaskUrl: newProcessDepTaskUrl. supported in future
    :var serviceData: serviceData containing the created process and errors if any
    """
    instanceKey: str = ''
    newProcessDepTask: str = ''
    newProcessUrl: str = ''
    newProcessDepTaskUrl: str = ''
    serviceData: ServiceData = None


@dataclass
class AttachmentInfo(TcBaseObj):
    """
    Structure containing list of attachments and the attachment types
    
    :var attachment: attachment
    :var attachmentType: attachmentType
    """
    attachment: List[BusinessObject] = ()
    attachmentType: List[int] = ()


@dataclass
class AuditFile(TcBaseObj):
    """
    Audit files
    
    :var auditFiles: auditFiles
    :var serviceData: serviceData
    """
    auditFiles: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class ProcessTemplates(TcBaseObj):
    """
    Process templates
    
    :var output: vector of DefinitionInfo objects
    :var serviceData: Service data contains any partial errors.
    """
    output: List[DefinitionInfo] = ()
    serviceData: ServiceData = None


@dataclass
class RemoveSignoffsInfo(TcBaseObj):
    """
    Structure containing signoffs to be removed
    
    :var task: task
    :var removeSignoffObjs: removeSignoffObjs
    """
    task: EPMTask = None
    removeSignoffObjs: List[Signoff] = ()


@dataclass
class ResourcePoolInfo(TcBaseObj):
    """
    Structure containing resource pool , group and role info
    
    :var groupRoleRef: groupRoleRef
    :var resourcePoolTag: resourcePoolTag
    """
    groupRoleRef: GroupRoleRef = None
    resourcePoolTag: ResourcePool = None


@dataclass
class Resources(TcBaseObj):
    """
    Structure containing the task template and the resources to be applied to the template
    
    :var taskTemplate: taskTemplate
    :var templateResources: templateResources
    :var profiles: profiles
    :var actions: actions
    :var revQuorum: revQuorum
    :var ackQuorum: ackQuorum
    """
    taskTemplate: EPMTaskTemplate = None
    templateResources: List[BusinessObject] = ()
    profiles: List[EPMSignoffProfile] = ()
    actions: List[int] = ()
    revQuorum: int = 0
    ackQuorum: int = 0


@dataclass
class Tasks(TcBaseObj):
    """
    Structure containing all the tasks in a process
    
    :var allTasks: allTasks
    :var serviceData: Service data contains any partial errors.
    """
    allTasks: List[EPMTask] = ()
    serviceData: ServiceData = None


@dataclass
class Templates(TcBaseObj):
    """
    structure containing workflow templates
    
    :var workflowTemplates: workflowTemplates
    :var serviceData: Service data contains any partial errors.
    """
    workflowTemplates: List[EPMTaskTemplate] = ()
    serviceData: ServiceData = None


@dataclass
class ChangeStateInputInfo(TcBaseObj):
    """
    Input to changeState operation
    
    :var state: state
    :var remoteProcessID: remoteProcessID
    """
    state: stateType = None
    remoteProcessID: str = ''


@dataclass
class ChangeStateOutput(TcBaseObj):
    """
    ChangeState operation output
    
    :var state: state
    :var remoteProcessID: remoteProcessID
    :var parentProcessID: parentProcessID
    :var serviceData: serviceData
    """
    state: stateType = None
    remoteProcessID: str = ''
    parentProcessID: str = ''
    serviceData: ServiceData = None


@dataclass
class ContextData(TcBaseObj):
    """
    Context-specific data required to create a process or a sub process at a local or a remote site.  Except the
    process template, the rest of the elements in the context data is optional. The optional elements        that are
    currently supported are attachmentCount,attachments,attachmentTypes and processAssignmentList.  The rest of the
    optional elements are defined to support        future workflow enhancements.
    
    :var processTemplate: Name of the process template.  must be a valid, existing process template
    :var processOwner: Login id of the process owner. supported in future
    :var dependencyTask: The path to the dependency task. This will be used to determine the dependency tasks in the
    processes that need to be returned in response.   The full path to the task in the template needs to be specified,
    e.g.       CMII Change Notice: Change Admin II (CN). supported in future
    :var subscribeToEvents: The flag to indicate if the observer needs to be notified about events that occur on the
    processes and the dependency tasks in the processes. supported in future
    :var subscriptionEventCount: Number of events to subscribe to
    :var subscriptionEventList: List of events for which subscription objects will be created so that the observer is
    notified when these events occur on the process and /or process dependency task. supported in future
    :var remoteParent: URI of the observer in the remote application. supported in future
    :var remoteParentAppguid: The Application ID of the application in which the observer resides. supported in future
    :var remoteParentUrl: The URL to the observer. supported in future
    :var attachmentCount: Count of attachment objects consisting of including both target        and reference
    attachments. If count is less than 1, no attachments are added
    :var attachments: List of atachments representing either target or reference objects that will be added at process
    creation time. List may consist of target attachments or reference attachments or a mixture of both. If NULL, no
    attachments are added
    :var attachmentTypes: Identifies the types of attachments listed in attachment.  Valid types include
    EPM_target_attachment (target attachment) and EPM_reference_attachment (reference attachment). There is a
    one-to-one correspondence between the attachment types on this list and the list of attachments.
    :var deadlineDate: A date in the form of yyyy-mm-dd hh-mm-ss GMT that will be applied as a due date for the
    processes. If GMT is not specified then the time will be interpreted as based on the local time zone of the server.
    If NULL or invalid date, no due date is applied. supported in future
    :var container: Identifies the object to which the processes should be attached using the relation_type specified.
    supported in future
    :var relationType: The name of the relation. If NULL, the default relation type for the container object will be
    used. supported in future
    :var processAssignmentList: Name of the process assignment list
    :var processResources: A list of comma-separated user login IDs that will be used to satisfy signoff profiles for
    each individual task. Any users that do not match a signoff profile within a task will be added as an adhoc user.
    supported in future
    """
    processTemplate: str = ''
    processOwner: str = ''
    dependencyTask: str = ''
    subscribeToEvents: bool = False
    subscriptionEventCount: int = 0
    subscriptionEventList: List[str] = ()
    remoteParent: str = ''
    remoteParentAppguid: str = ''
    remoteParentUrl: str = ''
    attachmentCount: int = 0
    attachments: List[str] = ()
    attachmentTypes: List[int] = ()
    deadlineDate: datetime = None
    container: str = ''
    relationType: str = ''
    processAssignmentList: str = ''
    processResources: List[str] = ()


@dataclass
class CreateSignoffInfo(TcBaseObj):
    """
    Structure containing information to add adhoc signoff or add signoff based on a profile
    
    :var signoffMember: signoffMember
    :var origin: origin
    :var signoffAction: signoffAction
    :var originType: originType
    """
    signoffMember: BusinessObject = None
    origin: BusinessObject = None
    signoffAction: SignoffAction = None
    originType: OriginType = None


@dataclass
class CreateSignoffs(TcBaseObj):
    """
    Structure containing information to add adhoc signoff or add signoff based on a profile
    
    :var task: task
    :var signoffInfo: signoffInfo
    """
    task: EPMTask = None
    signoffInfo: List[CreateSignoffInfo] = ()


@dataclass
class DefinitionInfo(TcBaseObj):
    """
    Structure containing process template information
    
    :var definitionkey: unique identifier of the process template
    :var name: name of the process template
    :var description: description of the process template
    :var version: version of the process template
    :var status: status of the process template. The values are 0 -obsolete,1 - under construction, 2- ready for use
    """
    definitionkey: str = ''
    name: str = ''
    description: str = ''
    version: str = ''
    status: int = 0


class AllOrAssigned(Enum):
    """
    AllOrAssigned
    """
    SOA_EPM_All = 'SOA_EPM_All'
    SOA_EPM_Assigned = 'SOA_EPM_Assigned'


class OriginType(Enum):
    """
    OriginType
    """
    SOA_EPM_ORIGIN_UNDEFINED = 'SOA_EPM_ORIGIN_UNDEFINED'
    SOA_EPM_SIGNOFF_ORIGIN_PROFILE = 'SOA_EPM_SIGNOFF_ORIGIN_PROFILE'
    SOA_EPM_SIGNOFF_ORIGIN_ADDRESSLIST = 'SOA_EPM_SIGNOFF_ORIGIN_ADDRESSLIST'


class SignoffAction(Enum):
    """
    SignoffAction
    """
    SOA_EPM_ACTION_UNDEFINED = 'SOA_EPM_ACTION_UNDEFINED'
    SOA_EPM_Review = 'SOA_EPM_Review'
    SOA_EPM_Acknowledge = 'SOA_EPM_Acknowledge'
    SOA_EPM_Notify = 'SOA_EPM_Notify'


class SoaEPMAction(Enum):
    """
    SoaEPMAction
    """
    SOA_EPM_assign_action = 'SOA_EPM_assign_action'
    SOA_EPM_start_action = 'SOA_EPM_start_action'
    SOA_EPM_remove_attachment_action = 'SOA_EPM_remove_attachment_action'
    SOA_EPM_approve_action = 'SOA_EPM_approve_action'
    SOA_EPM_reject_action = 'SOA_EPM_reject_action'
    SOA_EPM_promote_action = 'SOA_EPM_promote_action'
    SOA_EPM_demote_action = 'SOA_EPM_demote_action'
    SOA_EPM_refuse_action = 'SOA_EPM_refuse_action'
    SOA_EPM_assign_approver_action = 'SOA_EPM_assign_approver_action'
    SOA_EPM_notify_action = 'SOA_EPM_notify_action'
    SOA_EPM_no_action = 'SOA_EPM_no_action'
    SOA_EPM_fail_action = 'SOA_EPM_fail_action'
    SOA_EPM_complete_action = 'SOA_EPM_complete_action'
    SOA_EPM_skip_action = 'SOA_EPM_skip_action'
    SOA_EPM_suspend_action = 'SOA_EPM_suspend_action'
    SOA_EPM_resume_action = 'SOA_EPM_resume_action'
    SOA_EPM_undo_action = 'SOA_EPM_undo_action'
    SOA_EPM_abort_action = 'SOA_EPM_abort_action'
    SOA_EPM_perform_action = 'SOA_EPM_perform_action'
    SOA_EPM_add_attachment_action = 'SOA_EPM_add_attachment_action'


class SoaEPMSupportingValues(Enum):
    """
    SoaEPMSupportingValues
    """
    SOA_EPM_no_decision = 'SOA_EPM_no_decision'
    SOA_EPM_approve = 'SOA_EPM_approve'
    SOA_EPM_reject = 'SOA_EPM_reject'
    SOA_EPM_unset = 'SOA_EPM_unset'
    SOA_EPM_completed = 'SOA_EPM_completed'
    SOA_EPM_unable_to_complete = 'SOA_EPM_unable_to_complete'
    SOA_EPM_true = 'SOA_EPM_true'
    SOA_EPM_false = 'SOA_EPM_false'
    SOA_EPM_no_error = 'SOA_EPM_no_error'


class stateType(Enum):
    """
    stateType
    """
    open_notrunning = 'open_notrunning'
    open_notrunning_suspended = 'open_notrunning_suspended'
    open_running = 'open_running'
    closed_completed = 'closed_completed'
    closed_abnormalcompleted = 'closed_abnormalcompleted'
    closed_abnormalcompleted_terminated = 'closed_abnormalcompleted_terminated'
    closed_abnormalcompleted_aborted = 'closed_abnormalcompleted_aborted'
    open_notrunning_pending = 'open_notrunning_pending'
    open_running_started = 'open_running_started'
    open_running_failed = 'open_running_failed'
