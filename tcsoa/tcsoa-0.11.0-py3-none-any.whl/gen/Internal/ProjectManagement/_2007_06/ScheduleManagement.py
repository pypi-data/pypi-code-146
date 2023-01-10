from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TCCalendar, ScheduleTask, Schedule, ResourceAssignment, TaskDependency, TCCalendarEvent
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
    
    :var object: A tag to the object being updated.
    :var keyValueContainer: A collection of updates.
    :var stringValueContainer: A collection of updates.
    """
    object: BusinessObject = None
    keyValueContainer: List[KeyValContainer] = ()
    stringValueContainer: List[StringValContainer] = ()


@dataclass
class KeyValContainer(TcBaseObj):
    """
    The key value container.
    
    :var key: An integer key identifying the attribute  or parameterised index
    :var value: A string representation of the value of the attribute.
    :var type: An integer to help determine the type of object represented by the value.
    """
    key: int = 0
    value: str = ''
    type: int = 0


@dataclass
class LoadProgramViewContainer(TcBaseObj):
    """
    An input container containing the list of schedules and filter conditions.
    
    :var schedules: The UIDs of the Schedules which are included in this program view.
    :var loadProgramViewSets: The collection of filters to be applied.
    """
    schedules: List[str] = ()
    loadProgramViewSets: List[LoadProgramViewSet] = ()


@dataclass
class LoadProgramViewFilter(TcBaseObj):
    """
    The represents the a single input filter in the query for loading the program view.
    
    :var field: The integer value of property to filter out tasks or schedules.
    :var value: The value of the property to filter out schedules or tasks.
    :var condition: The condition: greater-than, less-than etc.
    """
    field: int = 0
    value: str = ''
    condition: int = 0


@dataclass
class LoadProgramViewResponse(TcBaseObj):
    """
    Contains all the necessary response for the program view.  The Schedules, ScheduleTasks, ResourceAssignments, and
    TaskDependencies.
    
    :var schedules: The Schedules.
    :var scheduleTask: The ScheduleTasks.
    :var resourceAssignment: The ResourceAssignments of the scheduleTasks.
    :var taskDependency: The TaskDependecies of the scheduleTasks.
    :var calendar: The Calenders of the schedules.
    :var calendarEvent: The calendar events for the calendars.
    :var serviceData: The ServiceData.
    """
    schedules: List[Schedule] = ()
    scheduleTask: List[ScheduleTask] = ()
    resourceAssignment: List[ResourceAssignment] = ()
    taskDependency: List[TaskDependency] = ()
    calendar: List[TCCalendar] = ()
    calendarEvent: List[TCCalendarEvent] = ()
    serviceData: ServiceData = None


@dataclass
class LoadProgramViewSet(TcBaseObj):
    """
    The collection of input filters
    
    :var loadProgramViewFilters: The filters.
    """
    loadProgramViewFilters: List[LoadProgramViewFilter] = ()


@dataclass
class LoadResourceAssignmentContainer(TcBaseObj):
    """
    A container representing the Query input for the resource load.
    
    :var resource: The resource Tag(s). could be a user or discipline or group. (Currently only user is supported)
    :var schedulesToAlwaysInclude: An optional list of Schedules to always include to search criteria.
    :var startDate: An optional Start Date to filter with (requires endDate).
    :var endDate: An optional Finish Date to filter with (requires startDate).
    """
    resource: List[BusinessObject] = ()
    schedulesToAlwaysInclude: List[Schedule] = ()
    startDate: datetime = None
    endDate: datetime = None


@dataclass
class ResourceAssignmentLoadResponse(TcBaseObj):
    """
    The response container with several SingleAssignmentLoadRespones.
    
    :var serviceData: The ServiceData.
    :var resourceData: The collection of SingleAssignmentLoadResponses.
    """
    serviceData: ServiceData = None
    resourceData: List[SingleAssignmentLoadResponse] = ()


@dataclass
class ScheduleModifyContainer(TcBaseObj):
    """
    The information necessary to update a schedule.  It contains information about new, updated, and deleted tasks,
    resource assignments, and task dependcies
    
    :var scheduleUpdates: The updates to this schedule.
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
class SingleAssignmentLoadResponse(TcBaseObj):
    """
    The container representing a single resources's assignment output data which matched the query.
    
    :var resource: The resource (could be a user or discipline or group).
    :var resourceAssignment: The resource assignments referencing the resource.
    :var schedules: The schedules which contain the resourceAssignments and tasks.
    :var tasks: The assigned tasks.
    :var calendars: The calendars referenced in the assignment (can be base, resource, schedule and schedule member
    calendars).
    :var calendarEvents: The events referenced in the calendars.
    """
    resource: BusinessObject = None
    resourceAssignment: List[ResourceAssignment] = ()
    schedules: List[Schedule] = ()
    tasks: List[ScheduleTask] = ()
    calendars: List[TCCalendar] = ()
    calendarEvents: List[TCCalendarEvent] = ()


@dataclass
class StringValContainer(TcBaseObj):
    """
    The container represents a single attribute's value. 
    The name of the attribute is represented by the key field. 
    The data type of the attribute is represented by the type field. The type field can be one of the following;
    char = 0;
    date = 1;
    double = 2;
    float = 3;
    int = 4;
    bool = 5;
    short = 6;
    string = 7;
    ModelObject = 8;
    
    :var key: A string key identifying the attribute.
    :var value: A string representation of the value of the attribute.
    :var type: An integer to help determine the type of object represented by the value.
    """
    key: str = ''
    value: str = ''
    type: int = 0
