from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NameValueStringPair(TcBaseObj):
    """
    Structure containing a pair (string, string) of name and value respectively.
    
    :var name: The name of key in Pair.
    :var keyValue: The value of key in Pair.
    """
    name: str = ''
    keyValue: str = ''


@dataclass
class ResourceChartInfo(TcBaseObj):
    """
    This represents the UID of the resource which can be of type User, Group, ResourcePool or Discipline and the
    resource information for the given resource on a specific date.
    
    :var resource: The UID of User, Group, ResourcePool or Discipline to load resource information.
    :var resourceInfoPerDay: The list of resource information for each day in the start and end date range.
    """
    resource: str = ''
    resourceInfoPerDay: List[ResourceInfoPerDay] = ()


@dataclass
class ResourceChartResponse(TcBaseObj):
    """
    This contains the list of resource chart information per resource and ServiceData. The plain objects list of the
    ServiceData containing the list of assigned ScheduleTask objects and the resources.
    
    :var resourceChartInfoList: A list of Resource chart information per resource.
    :var serviceData: If the loadOptions contains &lsquo;loadAssignedTasks:true&rsquo;, then the assigned ScheduleTask
    objects will be added to the plain objects list of the ServiceData
    """
    resourceChartInfoList: List[ResourceChartInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ResourceInfoPerDay(TcBaseObj):
    """
    The structure containing a date, resource information on the date and the list of ScheduleTask objects to the
    assigned to a resource.
    
    :var date: The date for which the resource information will be loaded.
    :var resourceInfo: The list of the resource information on the given date.  Examples of valid values are:
    availability :  120 (value is represented only in minutes)
    capacity :  480  (value is represented only in minutes)
    percentLoad : 75%
    :var assignedTasksInfo: A list of UIDs of assigned ScheduleTask objects on the given date and its associated
    information like resource load on the ScheduleTask.
    """
    date: datetime = None
    resourceInfo: List[NameValueStringPair] = ()
    assignedTasksInfo: List[TaskInfo] = ()


@dataclass
class TaskInfo(TcBaseObj):
    """
    This contains the information of a given ScheduleTask object.
    
    :var taskUid: The UID of the ScheduleTask object.
    :var info: The information for the assigned ScheduleTask object in key value pair  . Valid values are:
    percentLoad : 70%   (Valid values are represented as number greater than 0 which can include decimals. e.g. 5%,
    7.5%, 150%, etc.)
    """
    taskUid: str = ''
    info: List[NameValueStringPair] = ()
