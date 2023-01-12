from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.ProjectManagement._2008_06.ScheduleManagement import StringValContainer, TypedAttributeContainer
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenericAttributesContainer(TcBaseObj):
    """
    A collection of KeyValContainers or StringValContainers reprenting the create or updates for a single object, such
    as Schedule, ScheduleTask, TaskDependency, or ResourceAssignment
    
    :var serviceType: The service type. Valid values are "GET" or "POST","VALIDATE" or "PERSIST"
    :var operationType: The operation type (may be set by the system if the API does not have multiple contracts)
    :var scheduleUid: the schedule uid. This is required for batch updates in multiple schedules.
    :var object: The tag to the object being updated
    :var stringValContainer: A collection of updates. Valid values are  key = property name which is to be updated eg
    "priority"
     value = value of the property eg. "2"
    :var typedAttributesContainer: A collection of updates for extended properties if there are any (optional)
    """
    serviceType: ServiceAction = None
    operationType: TranslatorOperation = None
    scheduleUid: str = ''
    object: BusinessObject = None
    stringValContainer: List[StringValContainer] = ()
    typedAttributesContainer: List[TypedAttributeContainer] = ()


@dataclass
class GenericResponseContainer(TcBaseObj):
    """
    This is the generic response container
    
    :var serviceData: The ServiceData
    :var objectUids: The list of objects uid
    :var objects: The list of objects
    """
    serviceData: ServiceData = None
    objectUids: List[str] = ()
    objects: List[BusinessObject] = ()


@dataclass
class ScheduleModifyContainer(TcBaseObj):
    """
    The information necessary to update a schedule.  It contains information about new, updated, and deleted tasks,
    resource assignments, and task dependencies.
    
    :var scheduleUid: the schedule uid
    :var serviceType: The service action
    :var deletedTasks: The deleted tasks
    :var deletedDependencies: The deleted dependencies
    :var deletedAssignments: The deleted assignments
    :var scheduleUpdates: the schedule updates
    :var deleteAllTasks: Delete all tasks flag
    :var newTasks: The new tasks to add
    :var newDependencies: The new dependencies
    :var newAssignments: The new assignments
    :var taskUpdates: The existing task updates
    :var dependenciesUpdate: The existing dependencies updates
    :var assignmentUpdates: The existing assignment updates
    """
    scheduleUid: str = ''
    serviceType: ServiceAction = None
    deletedTasks: List[BusinessObject] = ()
    deletedDependencies: List[BusinessObject] = ()
    deletedAssignments: List[BusinessObject] = ()
    scheduleUpdates: GenericAttributesContainer = None
    deleteAllTasks: bool = False
    newTasks: List[GenericAttributesContainer] = ()
    newDependencies: List[GenericAttributesContainer] = ()
    newAssignments: List[GenericAttributesContainer] = ()
    taskUpdates: List[GenericAttributesContainer] = ()
    dependenciesUpdate: List[GenericAttributesContainer] = ()
    assignmentUpdates: List[GenericAttributesContainer] = ()


class ServiceAction(Enum):
    """
    Enumerator for service actions
    """
    GET = 'GET'
    POST = 'POST'
    VALIDATE = 'VALIDATE'
    PERSIST = 'PERSIST'
    ANALYSE = 'ANALYSE'


class TranslatorOperation(Enum):
    """
    Enumerator for translator operations
    """
    AssignmentAssign = 'AssignmentAssign'
    AssignmentUnassign = 'AssignmentUnassign'
    ScheduleCreate = 'ScheduleCreate'
    ScheduleDelete = 'ScheduleDelete'
    ScheduleRecalculate = 'ScheduleRecalculate'
    ScheduleModify = 'ScheduleModify'
    ScheduleTaskCreate = 'ScheduleTaskCreate'
    ScheduleTaskDelete = 'ScheduleTaskDelete'
    ScheduleTaskUpdate = 'ScheduleTaskUpdate'
    ScheduleGetCriticalPath = 'ScheduleGetCriticalPath'
    ScheduleShift = 'ScheduleShift'
    ScheduleScale = 'ScheduleScale'
    AssignmentUpdate = 'AssignmentUpdate'
    ScheduleTaskMove = 'ScheduleTaskMove'
    Undefined = 'Undefined'
    AssignmentDelegate = 'AssignmentDelegate'
    AssignmentReplace = 'AssignmentReplace'
    AssignmentRevert = 'AssignmentRevert'
    ResourceGetAssignments = 'ResourceGetAssignments'
    DependencyCreate = 'DependencyCreate'
    DependencyUpdate = 'DependencyUpdate'
    DependencyDelete = 'DependencyDelete'
