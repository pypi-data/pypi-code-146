from __future__ import annotations

from tcsoa.gen.ProjectManagementAw._2016_12.ScheduleManagementAw import EventDateRanges
from tcsoa.gen.BusinessObjects import Fnd0ProxyTask, WorkspaceObject, ScheduleTask, Schedule, TaskDependency
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BaselineTaskInfo(TcBaseObj):
    """
    Contains information about the baselineTask.
    
    :var baselineTask: The baseline ScheduleTask object.
    :var properties: Map (string, string) of baseline task property names and their values.
    """
    baselineTask: ScheduleTask = None
    properties: StringToStringMap = None


@dataclass
class LoadBaselineInfo(TcBaseObj):
    """
    Information required to load the baseline tasks of a Schedule baseline based on a source Schedule and load options.
    
    :var sourceSchedule: The Schedule for which the baseline needs to be loaded.
    :var baselineSchedule: The baseline Schedule to load.
    :var scheduleTasks: The list of ScheduleTask objects, in the source Schedule, for which the respective baseline
    tasks are to be returned.
    :var loadOptions: Specifies the options for loading Schedule Baseline. Valid options (key : value) are:
    loadBaselineTasks : true/false (Set true to return the baseline tasks; false otherwise)
    loadCompleteBaseline : true/false (Set true to return information of all the baseline tasks in the schedule
    baseline; Set false or do not specify this option to return the baseline task information of only the input
    ScheduleTask objects.)
    """
    sourceSchedule: Schedule = None
    baselineSchedule: Schedule = None
    scheduleTasks: List[ScheduleTask] = ()
    loadOptions: StringToStringMap = None


@dataclass
class LoadBaselineResponse(TcBaseObj):
    """
    Response of the load baseline operation, containing information about the loaded baseline tasks.
    
    :var baselineTasksInfo: Map (string, BaselineTaskInfo) of original ScheduleTask UID and its baseline task
    information.
    :var serviceData: The ServiceData.
    """
    baselineTasksInfo: TaskUidToBaselineTaskInfoMap = None
    serviceData: ServiceData = None


@dataclass
class LoadScheduleInfo2(TcBaseObj):
    """
    Information required to load a Schedule based on a reference ScheduleTask, parents of the reference task and
    schedule load options.
    
    :var schedule: The Schedule to load.
    :var referenceTask: The reference ScheduleTask from where to start loading the subsequent ScheduleTask objects,
    which could be either siblings of reference ScheduleTask or siblings of one of the parents of reference
    ScheduleTask. If the reference ScheduleTask is null, the children of the parentTasks specified in the input will be
    loaded.
    :var parentTasks: List of all top level parents of the referenceTask, with immediate parent at the start of the
    list. If not specified, no ScheduleTask objects will be loaded.
    :var loadOptions: Specifies the options for loading a Schedule. Valid options (key : value) are:
    baselineUid : UID of the schedule baseline
    loadBaselineTasks : true/false (Set true to return the baseline tasks; false otherwise)
    loadCalendarInfo : true/false (Set true to return the calendar information; false otherwise)
    """
    schedule: Schedule = None
    referenceTask: ScheduleTask = None
    parentTasks: List[ScheduleTask] = ()
    loadOptions: StringToStringMap = None


@dataclass
class LoadScheduleResponse2(TcBaseObj):
    """
    Response of the load schedule operation, containing the list of loaded ScheduleTask, parent ScheduleTask, baseline
    ScheduleTask, Fnd0ProxyTask and TaskDependency objects. Also, contains the calendar information of the loaded
    Schedule.
    
    :var scheduleTasksInfo: Information about the ScheduleTask objects loaded.
    :var proxyTasks: List of Fnd0ProxyTask objects referencing the loaded ScheduleTask objects.
    :var taskDependenciesInfo: Information about the Task Dependency objects loaded.
    :var hasMoreTasks: If true, there are more ScheduleTask objects in the Schedule, which are not loaded by this
    operation.
    :var taskBaselineMap: Map (ScheduleTask, BaselineTaskInfo) containing the loaded ScheduleTask objects and their
    respective baseline tasks information. If a loaded ScheduleTask object does not have a baseline task, it will not
    be added to the map.
    :var calendarInfo: Calendar information of the loaded Schedule. It contains details about the standard working
    hours and holidays within the Schedule boundaries.
    :var serviceData: The ServiceData.
    """
    scheduleTasksInfo: List[ScheduleTaskInfo] = ()
    proxyTasks: List[Fnd0ProxyTask] = ()
    taskDependenciesInfo: List[TaskDependencyInfo] = ()
    hasMoreTasks: bool = False
    taskBaselineMap: BaselineTasks = None
    calendarInfo: CalendarInfo = None
    serviceData: ServiceData = None


@dataclass
class CalendarInfo(TcBaseObj):
    """
    Contains calendar information of a Schedule object.
    
    :var dayRanges: Map (int, list of string) containing the ranges for each day in a week. Maps the days of the week
    to their ranges. The valid values for days are 0 to 6 which represents Sunday through Saturday in the respective
    order. A range is a pair of start and end time of working hours. A day can have multiple ranges with breaks
    in-between in a working day.
    :var eventRanges: The event dates and their respective ranges. The events are exceptions where the working hours
    are different from the default working hours.
    """
    dayRanges: DayRanges2 = None
    eventRanges: List[EventDateRanges] = ()


@dataclass
class RecalculateInput(TcBaseObj):
    """
    A list of structures containing information to recalculate schedule.
    
    :var schedule: The Schedule to be recalculated.
    :var recalcType: The recalculation type: -1-All, 1-Execution Data, 2-Scheduling Data.
    """
    schedule: Schedule = None
    recalcType: int = 0


@dataclass
class ScheduleTaskInfo(TcBaseObj):
    """
    Contains a ScheduleTask object and its parent ScheduleTask object.
    
    :var scheduleTask: The ScheduleTask object in context.
    :var parentTask: The parent of the scheduleTask. It will be null if the scheduleTask is of Schedule Summary Task
    type.
    """
    scheduleTask: ScheduleTask = None
    parentTask: ScheduleTask = None


@dataclass
class TaskDeliverableInput(TcBaseObj):
    """
    The input information required for creating task deliverables.
    
    :var schedule: The owning Schedule of the Schedule Task objects.
    :var scheduleTasks: The list of Schedule Task objects in the schedule for which the deliverables are to be created.
    :var submitType: The type of submission of workflow to which the deliverable is routed. Valid values are 3=Don't
    submit, 0=submit as target, 1=submit as reference.
    :var deliverableReference: The deliverable instance to be referenced by the Schedule deliverable.
    :var deliverableName: The name of the deliverable.
    :var deliverableType: The type of the instance associated with the deliverable (Item, Form, Folder, Dataset, and
    Document)
    """
    schedule: Schedule = None
    scheduleTasks: List[ScheduleTask] = ()
    submitType: int = 0
    deliverableReference: WorkspaceObject = None
    deliverableName: str = ''
    deliverableType: str = ''


@dataclass
class TaskDependencyInfo(TcBaseObj):
    """
    Contains information about the TaskDependency object.
    
    :var taskDependency: The Task Dependency object.
    :var properties: Map (string, string) of task dependency property names and their values
    """
    taskDependency: TaskDependency = None
    properties: StringToStringMap = None


"""
Map of ScheduleTask object and its baseline task information.
"""
BaselineTasks = Dict[ScheduleTask, BaselineTaskInfo]


"""
Maps the weekdays to their ranges. The valid values for the days are 0 to 6 which represents Sunday through Saturday in the respective order. A range is a pair of start and end time of working hours. A day can have multiple ranges with breaks in-between in a working day.
"""
DayRanges2 = Dict[int, List[str]]


"""
Map (string, string) containg a key value pair of string type.
"""
StringToStringMap = Dict[str, str]


"""
Map (string, BaselineTaskInfo) of original ScheduleTask UID and its baseline task information.
"""
TaskUidToBaselineTaskInfoMap = Dict[str, BaselineTaskInfo]
