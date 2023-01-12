from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TCCalendar, ScheduleTask, Schedule, ResourceAssignment, TaskDependency, TCCalendarEvent
from tcsoa.gen.Internal.ProjectManagement._2007_06.ScheduleManagement import StringValContainer, KeyValContainer
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GenericAttributesContainer(TcBaseObj):
    """
    A collection of KeyValContainers or StringValContainers reprenting the create or updates for a single object,
    such as Schedule, ScheduleTask, TaskDependency, or ResourceAssignment.
    
    :var object: The tag to the object being updated.
    :var keyValContainer: A collection of updates.
    :var stringValContainer: A collection of updates.
    :var typedAttributesContainer: A collection of updates.
    """
    object: BusinessObject = None
    keyValContainer: List[KeyValContainer] = ()
    stringValContainer: List[StringValContainer] = ()
    typedAttributesContainer: List[TypedAttributesContainer] = ()


@dataclass
class MasterMetaData(TcBaseObj):
    """
    A container for the SubMasterMetaData.
    
    :var uid: The uid of a master schedule.
    :var start: The Start Date of that master schedule.
    :var finish: The Finish Date of that master schedule.
    """
    uid: str = ''
    start: datetime = None
    finish: datetime = None


@dataclass
class MultipleScheduleLoadResponses(TcBaseObj):
    """
    A container for the load schedule response
    
    :var serviceData: The ServiceData.
    :var scheduleData: A collection of the schedule load responses.
    """
    serviceData: ServiceData = None
    scheduleData: List[ScheduleLoadResponse] = ()


@dataclass
class ScheduleLoadResponse(TcBaseObj):
    """
    A container for the load schedule response.
    
    :var schedule: The schedule.
    :var scheduleTask: All the tasks in this schedule.
    :var resourceAssignment: All the resource assignments in this schedule.
    :var taskDependency: All the task dependencies in this schedule.
    :var calendar: All the calendars referenced in this schedule.
    :var calendarEvent: All the calendar events referenced in the calendars.
    :var submasterdata: The meta data regarding master schedules.
    """
    schedule: Schedule = None
    scheduleTask: List[ScheduleTask] = ()
    resourceAssignment: List[ResourceAssignment] = ()
    taskDependency: List[TaskDependency] = ()
    calendar: List[TCCalendar] = ()
    calendarEvent: List[TCCalendarEvent] = ()
    submasterdata: List[SubMasterMetaData] = ()


@dataclass
class ScheduleModifyContainer(TcBaseObj):
    """
    The information necessary to update a schedule.  It contains information about new, updated, and deleted tasks,
    resource assignments, and task dependencies.
    
    :var scheduleUpdates: Updates to the schedule.
    :var deleteAllTasks: Should it delete all the tasks before beginning?  If this is set, it over-rides everything.
    :var deletedAssignments: A list of resource assignments to delete.
    :var newTasks: The information needed to create new tasks.
    :var newDependencies: The information needed to create new dependencies.
    :var newAssignments: The information needed to create new resource assignments.
    :var taskUpdates: The information needed to update existing tasks.
    :var dependencyUpdates: The information needed to update existing dependencies.
    :var assignmentUpdates: The information needed to update existing resource assignments.
    :var deletedTasks: A list of tasks to delete.
    :var deletedDependencies: A list of dependencies to delete.
    """
    scheduleUpdates: GenericAttributesContainer = None
    deleteAllTasks: bool = False
    deletedAssignments: List[ResourceAssignment] = ()
    newTasks: List[GenericAttributesContainer] = ()
    newDependencies: List[GenericAttributesContainer] = ()
    newAssignments: List[GenericAttributesContainer] = ()
    taskUpdates: List[GenericAttributesContainer] = ()
    dependencyUpdates: List[GenericAttributesContainer] = ()
    assignmentUpdates: List[GenericAttributesContainer] = ()
    deletedTasks: List[ScheduleTask] = ()
    deletedDependencies: List[TaskDependency] = ()


@dataclass
class ScheduleModifyResponse(TcBaseObj):
    """
    The response of the schedule modification.
    
    :var newTasks: A list of new tasks.
    :var newDependencies: A list of new dependencies.
    :var newAssignments: A list of new assignments.
    """
    newTasks: List[ScheduleTask] = ()
    newDependencies: List[TaskDependency] = ()
    newAssignments: List[ResourceAssignment] = ()


@dataclass
class ScheduleModifyResponses(TcBaseObj):
    """
    A collection of responses.
    
    :var serviceData: The ServiceData.
    :var responses: A collection of reponses.
    """
    serviceData: ServiceData = None
    responses: List[ScheduleModifyResponse] = ()


@dataclass
class SubMasterMetaData(TcBaseObj):
    """
    A container for the SubMasterMetaData.
    
    :var subschedule: The tag of the sub schedule.
    :var masterdata: A collection of information about all master schedules of the subschedule.
    """
    subschedule: Schedule = None
    masterdata: List[MasterMetaData] = ()


@dataclass
class TypedAttributesContainer(TcBaseObj):
    """
    A container which is used to update custom properties.
    
    :var type: The object type.
    :var attributes: A collection of updates.
    """
    type: str = ''
    attributes: List[StringValContainer] = ()
