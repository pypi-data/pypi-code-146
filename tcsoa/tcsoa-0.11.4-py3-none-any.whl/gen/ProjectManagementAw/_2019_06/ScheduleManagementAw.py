from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.BusinessObjects import ScheduleTask, ResourcePool
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssignedTasksInfo(TcBaseObj):
    """
    Contains information about the assigned ScheduleTask objects  to the logged in User.
    
    :var state: State of the SchduleTask. Valid values are: "not_started","in_progress","complete", "closed" and
    "aborted".
    :var status: Status of the SchduleTask. Valid values are: "not_started", "in_progress", "needs_attention", "late",
    "completed", "abandoned" and "aborted".
    :var loadedTasks: A list of loaded Schedule Task objects assigned to the logged in User.
    :var foundTasks: The foundTasks will be populated if loadOptions  is set  to "populateFoundTasksUIDs = "true" in
    LoadAssignedTaskInfo structure. If "false", foundTasks will not be populated.
    :var nFoundTasks: The number of Schedule Task objects found for the logged in User.
    """
    state: str = ''
    status: str = ''
    loadedTasks: List[ScheduleTask] = ()
    foundTasks: List[str] = ()
    nFoundTasks: int = 0


@dataclass
class LoadAssignedTasksInfo(TcBaseObj):
    """
    Information to fetch the ScheduleTask objects assigned to the logged in User.
    
    :var state: State of the SchduleTask. Valid values are: "not_started","in_progress","complete", "closed" and
    "aborted".
    :var status: Status of the SchduleTask. Valid values are: "not_started", "in_progress", "needs_attention", "late",
    "completed", "abandoned" and "aborted".
    :var startIndex: Pagination value. User can specify the the start index of the next chunk of objects to return. For
    example: This operation loads 100 ScheduleTask objects. User want to get first 50 loaded objects. So here the
    startIndex would be 0. For next chunk of loaded objects this input would be 51. Note Value for this input should be
    a positive integer. If the value is negative number then it is considered as 0.
    :var maxToLoad: The maximum number of found ScheduleTask objects to load. Note: Value for this input should be a
    positive integer. If the value is 0 or negative number then this input will be ignored and all the found
    ScheuleTask objects will be loaded.
    :var loadOptions: A map( sttring, string) of options for loading a ScheduleTask objects. Valid options (key :
    value) are:
    "populateFoundTasksUIDs" : "true" or "false".  If "true", foundTasks element in AssignedTasksInfo structure will be
    populated with the UIDs of all schedule tasks assigned to the logged in user. If "false", foundTasks will not be
    populated.
    """
    state: str = ''
    status: str = ''
    startIndex: int = 0
    maxToLoad: int = 0
    loadOptions: AssignedTasksLoadOptions = None


@dataclass
class LoadAssignedTasksResponse(TcBaseObj):
    """
    Response of the loadAssignedTasks operation, containing information about the assigned ScheduleTask objects  to the
    logged in User.
    
    :var assignedTasks: A list of assigned Schedule Task objects to the logged in User.
    :var serviceData: The service data.
    """
    assignedTasks: List[AssignedTasksInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ClaimAssignmentData(TcBaseObj):
    """
    The claimAssignmentData structure holds information needed to claim the assignments.
    
    :var scheduleTask: The ScheduleTask to be assigned to the logged in user.
    :var assignedResourcePool: The ResourcePool assigned to the ScheduleTask. The logged in user must be a member of
    the ResourcePool object.
    """
    scheduleTask: ScheduleTask = None
    assignedResourcePool: ResourcePool = None


"""
Map (string, string) containg a key value pair of string type.
"""
AssignedTasksLoadOptions = Dict[str, str]
