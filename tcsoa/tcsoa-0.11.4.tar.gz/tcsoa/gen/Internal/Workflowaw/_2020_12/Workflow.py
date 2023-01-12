from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, EPMSignoffProfile, EPMAssignmentList
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class TaskAssignmentsInput(TcBaseObj):
    """
    This is the input structure for getWorkflowTaskAssignments SOA.
    
    :var taskOrTemplate: EPMTask or the EPMTaskTemplate for which the assignments data is required.
    :var pal: The EPMAssignmentList from which the data needs to be fetched. Either the taskOrTemplate or this
    parameter would exist.
    :var operationMode: Criteria on which the tasks for assignments are filtered. Value 1 indicates all tasks and 2 for
    future tasks.
    :var startIndex: Index of the start element of the response data. If this is not given, it will be considered as 0.
    :var maxToLoad: Maximum elements to load and be returned in the response data. If negative, all of the found
    objects are loaded.
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var additionalData: A map (string, list of string) of filter and sort criteria. The keys for this map are:
     "sort_criteria"  = "task_name", "origin" or "assignee". 
     "filter_criteria" = "task_name", "origin" or "assignee".
    """
    taskOrTemplate: BusinessObject = None
    pal: EPMAssignmentList = None
    operationMode: int = 0
    startIndex: int = 0
    maxToLoad: int = 0
    clientId: str = ''
    additionalData: KeyValuePair = None


@dataclass
class TaskAssignmentsOutput(TcBaseObj):
    """
    This structure represents EPMTask assignment information associated with the EPMJob.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with input structure.
    :var outData: A list of task data that contains information about the task assignments, assignment types and their
    origin.
    :var dpData: A list of dynamic Participant objects . The key is a specific dynamic Participant type.
    :var additionalData: A map (string, list of strings) of dynamic Participant type name as key and the value is the
    list of tasks (EPMTask) or (Signoff) that refers it.
    """
    clientId: str = ''
    outData: List[TaskData] = ()
    dpData: DynamicParticipantsPair = None
    additionalData: KeyValuePair = None


@dataclass
class TaskAssignmentsResponse(TcBaseObj):
    """
    This structure represents response for getWorkflowTaskAssignments SOA.
    
    :var output: A list of TaskAssignmentsOutput structure.
    :var serviceData: The service data.
    """
    output: List[TaskAssignmentsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class TaskData(TcBaseObj):
    """
    This structure contains all the assignment information related to task or task template.
    
    :var task: The task (EPMTask) or task template (EPMTaskTemplate)  for which the assigments are to be updated.
    :var assigmentData: A map (string, list of AssignmentData)  of task assignment type string as the key. The types of
    task assigments include "Reviewers", "Acknowledgers", "Notifiers" and "Assignee". The value is list of
    AssignmentData.
    :var additionalData: A map (string, list of strings) that has sources from which the assignees are referred by the
    EPMTask. For example, dynamic Participants. The key to this map is same like the assignmentData map above. The
    value is the list of origins. For example, if the Reviewer of the EPMTask is from Participant types:
    "ProposedReviewes" and "ChangeSpecialist", then the key to this map is "Reviewers" and it points to a list
    containing two values: "ProposedReviewers" and "ChangeSpecialist". 
    
    "Reviewers" = list of participant types
    "Acknowledgers" = list of participant types
    "Assignee" = participant type
    "Notifiers" = list of participant types
    """
    task: BusinessObject = None
    assigmentData: TaskAssignmentsMap = None
    additionalData: KeyValuePair = None


@dataclass
class UpdateTaskAssignmentsInput(TcBaseObj):
    """
    This structure contains information about the task and dynamic participants assignments.
    
    Note: Values for either taskData or dpData will be present in this structure at a time. For task data updates, this
    will have taskData details present and dpData would be NULL. For updating the dpData details, the taskData values
    will point to NULL.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var taskData: A task and the assignees that needs to be updated. It can also contain Signoff data. The assignment
    data for each task is grouped as "Reviewers", "Assignee", "Notifiers" and "Acknowledgers".
    :var dpData: A Participant data that contains details about the type and the new list of assignees to be updated.
    :var additionalData: A map (string, list of strings) of details about task assignments. The keys and the values are
    :
    " task_bypass"= "yes" or "no"
    " late_task" = "yes" or "no"
    " task_pal_resource" = list indicating the name of EPMAssignmentList objects.
    """
    clientId: str = ''
    taskData: TaskData = None
    dpData: DynamicParticipantsData = None
    additionalData: KeyValuePair = None


@dataclass
class UpdateTaskAssignmentsOutput(TcBaseObj):
    """
    This structure contains information about the successfully updated objects.
    
    :var clientId: The clientID received to uniquely identify this task.
    :var taskOrDP: The EPMTask or Participant that has been successfully updated.
    """
    clientId: str = ''
    taskOrDP: BusinessObject = None


@dataclass
class UpdateTaskAssignmentsReponse(TcBaseObj):
    """
    This structure contains the list of sucessfully updated objects.
    
    :var outData: A list of EPMTask  or Participant objects.
    :var serviceData: The service data that may also contain errors.
    """
    outData: List[UpdateTaskAssignmentsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class AssignmentData(TcBaseObj):
    """
    This represent all the assignment information like origin, signoff profile and decision is required or not.
    
    :var member: The task assignment. Supported types are: User, GroupMember or Resourcepool.
    :var origin: The origin source of the member. For example EPMAssignmentList, Participant Type, TcProject,
    Resourcepool and ImanAliasList .
    :var signoffProfile: The signoff profile if the member is part of one.
    :var isRequired: If true, the decision on the Signoff is mandatory, otherwise not.
    :var additionalData: A map (string, list of strings) that has details related to EPMTask or Signoff. 
        "task_comments" = User added comments for task.
        "signoff_comments" = User added comments for signoff.
    """
    member: BusinessObject = None
    origin: BusinessObject = None
    signoffProfile: EPMSignoffProfile = None
    isRequired: bool = False
    additionalData: KeyValuePair = None


@dataclass
class DynamicParticipantsData(TcBaseObj):
    """
    This structure represent all the information related to particular Participant Type which is being used in task or
    process template.
    
    :var primaryObject: A source object to which Participant is attached to. It is WorkspaceObject either a workflow
    target or process (EPMJob) itself.
    :var internalName: The internal name of the Participant type.
    :var displayName: The display name of the Participant type.
    :var allowMultipleAssignee: Identifies if the Participant type supports multiple assignees or it is a single
    assignee. If true, multiple assignees can be added otherwise this it supports single assignee.
    :var assigneeList: A list of all assignees for this Participant type that are applicable to the workflow.
    :var additionalData: A map (string, list of strings) of eligibility criteria name for the Participant and the
    supported list of values . The supported key and values are:
     "participant_used_on_obj_type" = list of WorkspaceObjects that this Participant type supports.
     "participant_eligibility" = list of group::role criteria for assigning Participant type.
    """
    primaryObject: BusinessObject = None
    internalName: str = ''
    displayName: str = ''
    allowMultipleAssignee: bool = False
    assigneeList: List[BusinessObject] = ()
    additionalData: KeyValuePair = None


"""
This map will be used to pass additonal information.
"""
KeyValuePair = Dict[str, List[str]]


"""
This map will store task assignment information such as "Assignee", "Reviewers", "Acknowledgers" and "Notifiers" etc.
"""
TaskAssignmentsMap = Dict[str, List[AssignmentData]]


"""
This map will contain key as Partcipant Type name and value will DynamicParticipantsData structure which have all information related to that Participant Type.
"""
DynamicParticipantsPair = Dict[str, DynamicParticipantsData]
