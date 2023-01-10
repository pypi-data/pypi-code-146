from __future__ import annotations

from enum import Enum
from typing import List
from tcsoa.gen.BusinessObjects import ScheduleMember, ScheduleTask, SchDeliverable, ResourceAssignment, Schedule, TaskDependency
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FromSchedule(TcBaseObj):
    """
    The information regarding a schedule to copy from.
    
    :var schedule: The schedule to copy from.
    :var tasks: The list of tasks in that schedule to copy.
    :var schmgtOptions: Option structure for list of logical, integer and string options IntegerOptions {
    numberOfCopies - the number of copies } LogicalOptions { includeAssignments - copy assignments,includeDependencies
    - copy dependencies,includeDeliverables - copy deliverables,useExistingDeliverables - link copied to existing (by
    name), createMembership - copy missing members, resetDeliverableInstances - reset the instance of Schedule
    Deliverables, copyWorkflowTemplate - copy workflow template information, copyCostOfTask - copy costs,
    offsetBasedOnPositionInTemplate - shift tasks relative of original offset, recalcAsyncDispatcher - recalculate in
    asynchronously }
    """
    schedule: Schedule = None
    tasks: List[ScheduleTask] = ()
    schmgtOptions: SchMgtOptions = None


@dataclass
class MultiSchSpecialCopyResponse(TcBaseObj):
    """
    Return type of SOA for special paste
    
    :var createdTasks: Created Tasks
    :var modifiedTasks: Modified Tasks
    :var createdMembers: Created Members
    :var createdDeliverables: Created Schedule Deliverables
    :var createdDependencies: Created Dependencies
    :var createdAssignments: Created Assignments
    :var serviceData: Service Data
    """
    createdTasks: List[ScheduleTask] = ()
    modifiedTasks: List[ScheduleTask] = ()
    createdMembers: List[ScheduleMember] = ()
    createdDeliverables: List[SchDeliverable] = ()
    createdDependencies: List[TaskDependency] = ()
    createdAssignments: List[ResourceAssignment] = ()
    serviceData: ServiceData = None


@dataclass
class SchMgtIntegerOption(TcBaseObj):
    """
    Integer Options for special copy-paste
    
    :var name: The name of the option.
    :var value: The integer value of the option.
    """
    name: str = ''
    value: int = 0


@dataclass
class SchMgtLogicalOption(TcBaseObj):
    """
    Logical options for special copy-paste
    
    :var name: The name of the option.
    :var value: The value of logical option (True or False).
    """
    name: str = ''
    value: bool = False


@dataclass
class SchMgtOptions(TcBaseObj):
    """
    Special copy-paste options
    
    :var logicalOptions: List of logical options
    :var integerOptions: List of integer options
    :var stringOptions: List of string options
    """
    logicalOptions: List[SchMgtLogicalOption] = ()
    integerOptions: List[SchMgtIntegerOption] = ()
    stringOptions: List[SchMgtStringOption] = ()


@dataclass
class SchMgtStringOption(TcBaseObj):
    """
    String Options for special copy-paste
    
    :var name: The name of the option.
    :var value: The string value of the option
    """
    name: str = ''
    value: str = ''


@dataclass
class SpecialCopyContainer(TcBaseObj):
    """
    Input container
    
    :var fromSchedule: List of FromSchedules
    :var toSchedule: Target Schedule
    """
    fromSchedule: List[FromSchedule] = ()
    toSchedule: ToSchedule = None


@dataclass
class ToSchedule(TcBaseObj):
    """
    Target Schedule under which tasks will be pasted.
    
    :var targetSchedule: The target Schedule
    :var task: The target Task
    :var pasteType: Paste Type - PasteBeforeTask/PasteUnderTask/PasteAfterTask
    """
    targetSchedule: Schedule = None
    task: ScheduleTask = None
    pasteType: PasteType = None


class PasteType(Enum):
    """
    Enums which describes where to paste the copied tasks.
    """
    PasteBeforeTask = 'PasteBeforeTask'
    PasteUnderTask = 'PasteUnderTask'
    PasteAfterTask = 'PasteAfterTask'
