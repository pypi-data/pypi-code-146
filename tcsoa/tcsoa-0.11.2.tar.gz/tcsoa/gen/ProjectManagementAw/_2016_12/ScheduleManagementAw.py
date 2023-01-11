from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0ProxyTask, ScheduleMember, POM_object, ScheduleTask, Schedule, TaskDependency
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LoadScheduleInfo(TcBaseObj):
    """
    Information required to load a Schedule based on a reference ScheduleTask and its parents.
    
    :var schedule: The Schedule to load.
    :var referenceTask: The reference ScheduleTask from where to start loading the subsequent ScheduleTask objects,
    which could be either siblings of reference ScheduleTask or siblings of one of the parents of reference
    ScheduleTask. If the reference ScheduleTask is null, the children of the parentTasks specified in the input will be
    loaded.
    :var parentTasks: List of all top level parents of the referenceTask, with immediate parent at the start of the
    list. If not specified, no ScheduleTask objects will be loaded.
    """
    schedule: Schedule = None
    referenceTask: ScheduleTask = None
    parentTasks: List[ScheduleTask] = ()


@dataclass
class LoadScheduleResponse(TcBaseObj):
    """
    Response of the load schedule operation, containing the list of loaded ScheduleTask, parent ScheduleTask,
    Fnd0ProxyTask and TaskDependency objects.
    
    :var scheduleTasks: List of ScheduleTask objects loaded.
    :var parentTasks: List of parents of ScheduleTask objects loaded. The order of parents will be same as that of the
    order of ScheduleTask objects loaded.
    :var proxyTasks: List of Fnd0ProxyTask objects referencing the loaded ScheduleTask objects.
    :var taskDependencies: List of TaskDependency objects relating the loaded ScheduleTask objects.
    :var hasMoreTasks: If true, there are more ScheduleTask objects in the Schedule, which are not loaded by this
    operation.
    :var dayRanges: Map (int, list of string) containing the ranges for each day in a week. Maps the days of the week
    to their ranges. The valid values for days are 0 to 6 which represents Sunday through Saturday in the respective
    order. A range is a pair of start and end time of working hours. A day can have multiple ranges with breaks
    in-between in a working day.
    :var eventRanges: The event dates and their respective ranges. The events are exceptions where the working hours
    are different from the default working hours.
    :var serviceData: The ServiceData.
    """
    scheduleTasks: List[ScheduleTask] = ()
    parentTasks: List[ScheduleTask] = ()
    proxyTasks: List[Fnd0ProxyTask] = ()
    taskDependencies: List[TaskDependency] = ()
    hasMoreTasks: bool = False
    dayRanges: DayRanges = None
    eventRanges: List[EventDateRanges] = ()
    serviceData: ServiceData = None


@dataclass
class ReplaceMemberAssignmentData(TcBaseObj):
    """
    The replaceMemberAssignmentData structure holds information needed to replace member assignments in the Schedule.
    
    :var oldResource: The ScheduleMember assignments to be replaced.
    :var newResource: The resource (User, Group, or Discipline) to be assigned replacing the oldResource.
    """
    oldResource: ScheduleMember = None
    newResource: POM_object = None


@dataclass
class EventDateRanges(TcBaseObj):
    """
    Maps an event date with its ranges. The number of ranges must be an even number as a range is represented as a pair
    of start and end time of working hours. The ranges will be empty if the event date is a non-working day.
    
    :var eventDate: The event date.
    :var ranges: An array of ranges for the event date. The number of ranges must be an even number as a range is
    represented as a pair of start and end time of working hours. A range must be represented in &lsquo;hh:mm&rsquo;
    format, where &lsquo;hh&rsquo; represents hours and &lsquo;mm&rsquo; represents minutes. For example, the array
    [08:30, 12:30, 13:45, 16:45] represents two ranges. The first range has start time of 08:30 hours and end time of
    12:30 hours. The second range has start time of 13:45 hours and end time of 16:45 hours.
    """
    eventDate: datetime = None
    ranges: List[str] = ()


"""
Maps the weekdays to their ranges. The valid values for the days are 0 to 6 which represents Sunday through Saturday in the respective order. A range is a pair of start and end time of working hours. A day can have multiple ranges with breaks in-between in a working day.
"""
DayRanges = Dict[int, List[str]]
