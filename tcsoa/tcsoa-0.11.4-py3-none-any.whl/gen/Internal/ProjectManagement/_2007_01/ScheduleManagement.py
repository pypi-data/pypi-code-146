from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TCCalendar, ScheduleTask, Schedule, ResourceAssignment, TaskDependency, TCCalendarEvent
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class KeyValueContainer(TcBaseObj):
    """
    The key value container.
    
    :var key: An integer key identifying the attribute to be updated or parameterised index
    :var value: A string representation of the new value of the attribute.
    :var type: An integer to help determine the type of object represented by the value.
    """
    key: int = 0
    value: str = ''
    type: int = 0


@dataclass
class MultipleScheduleLoadResponse(TcBaseObj):
    """
    A container for the load schedule response.
    
    :var serviceData: The ServiceData.
    :var scheduleData: A collection of the schedule load responses.
    """
    serviceData: ServiceData = None
    scheduleData: List[ScheduleLoadResponse] = ()


@dataclass
class ScheduleChangeContainer(TcBaseObj):
    """
    A container for updating a schedule.
    
    :var scheduleUpdates: The updates for the schedule.
    :var newTasks: The information needed to create new tasks.
    :var newDependencies: The information needed to create new dependencies.
    :var newAssignments: The information needed to create new resource assignments.
    :var taskUpdates: The information needed to update existing tasks.
    :var dependencyUpdates: The information needed to update existing dependencies.
    :var assignmentUpdates: The information needed to update existing resource assignments.
    :var deletedTasks: The list of tasks to delete.
    :var deletedDependencies: The list of dependencies to delete.
    :var deletedAssignments: The list of resource assignments to delete.
    """
    scheduleUpdates: UpdateContainer = None
    newTasks: List[CreateTaskContainer] = ()
    newDependencies: List[CreateTaskDependencyContainer] = ()
    newAssignments: List[CreateResourceAssignmentContainer] = ()
    taskUpdates: List[UpdateContainer] = ()
    dependencyUpdates: List[UpdateContainer] = ()
    assignmentUpdates: List[UpdateContainer] = ()
    deletedTasks: List[ScheduleTask] = ()
    deletedDependencies: List[TaskDependency] = ()
    deletedAssignments: List[ResourceAssignment] = ()


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
    """
    schedule: Schedule = None
    scheduleTask: List[ScheduleTask] = ()
    resourceAssignment: List[ResourceAssignment] = ()
    taskDependency: List[TaskDependency] = ()
    calendar: List[TCCalendar] = ()
    calendarEvent: List[TCCalendarEvent] = ()


@dataclass
class StringValueContainer(TcBaseObj):
    """
    A container which represents a single attribute's value with a String for a key.
    
    :var key: A string key identifying the attribute.
    :var value: A string representation of the value of the attribute.
    :var type: An integer to help determine the type of object represented by the value.
    """
    key: str = ''
    value: str = ''
    type: int = 0


@dataclass
class UpdateContainer(TcBaseObj):
    """
    A container holder all the updates for a single object.
    
    :var object: The object being updated.
    :var keyValueContainer: The collection of KeyValueContainers.
    :var stringValueContainer: The collection of StringValueContainers.
    """
    object: BusinessObject = None
    keyValueContainer: List[KeyValueContainer] = ()
    stringValueContainer: List[StringValueContainer] = ()


@dataclass
class CreateResourceAssignmentContainer(TcBaseObj):
    """
    A container to create a new ResourceAssignment.
    
    :var taskID: The UID of the task.
    :var resource: The UID of the User or Discipline.
    :var percentage: The percentage assigned.
    :var discipline: Resource's discipline ID (can be blank).
    :var stringValueContainer: A collection of additional attributes.
    """
    taskID: str = ''
    resource: str = ''
    percentage: float = 0.0
    discipline: str = ''
    stringValueContainer: List[StringValueContainer] = ()


@dataclass
class CreateTaskContainer(TcBaseObj):
    """
    A container for the creation of a new task.
    
    :var id: A unique ID for the task.
    :var name: The name.
    :var startDate: The start date.
    :var finishDate: The finsh date.
    :var startDateOffset: NOT USED
    :var finishDateOffset: NOT USED
    :var workEstimate: The number of minutes of estimated work.
    :var workComplete: The number of minutes of completed work.
    :var percentComplete: The % complete of the task.
    :var duration: The minute duration of the task.
    :var stringValueContainer: A collection of additional attributes.
    :var description: The description.
    :var parentTaskID: The UID of the task's parent.
    :var prevSiblingID: The UID of the task directly before this task.
    :var priority: The priority.
    :var fixedType: The fixed type.
    :var autoComplete: Is autocomplete?
    :var taskType: The task type.
    :var constraint: The constraint.
    """
    id: str = ''
    name: str = ''
    startDate: datetime = None
    finishDate: datetime = None
    startDateOffset: int = 0
    finishDateOffset: int = 0
    workEstimate: int = 0
    workComplete: int = 0
    percentComplete: float = 0.0
    duration: int = 0
    stringValueContainer: List[StringValueContainer] = ()
    description: str = ''
    parentTaskID: str = ''
    prevSiblingID: str = ''
    priority: int = 0
    fixedType: int = 0
    autoComplete: bool = False
    taskType: int = 0
    constraint: int = 0


@dataclass
class CreateTaskDependencyContainer(TcBaseObj):
    """
    A container for the creation of a new task dependency.
    
    :var predecessorTaskID: The UID of the predecessor Task.
    :var successorTaskID: The UID of the sucessor Task.
    :var type: The type of dependency.
    :var lag: The number of minutes lag time.
    :var stringValueContainer: A collection of additional attributes.
    """
    predecessorTaskID: str = ''
    successorTaskID: str = ''
    type: int = 0
    lag: int = 0
    stringValueContainer: List[StringValueContainer] = ()
