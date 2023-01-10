from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ScheduleTask, SchDeliverable, Schedule
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MembershipData(TcBaseObj):
    """
    The information needed to create a new member in a schedule.
    
    :var schedule: The schedule for the new membership.
    :var resource: The resource to add.  (This can be a UserLogin, Group, or Discipline).
    :var membershipLevel: The membership level in that schedule.
    """
    schedule: Schedule = None
    resource: BusinessObject = None
    membershipLevel: int = 0


@dataclass
class ScheduleCopyContainer(TcBaseObj):
    """
    The information need to copy a schedule.
    
    :var name: The name of the new schedule.
    :var scheduleToCopy: The tag of the schedule to copy.
    :var resetWork: Flag to indicate whether or not to reset the tasks' execution data (%, status, work complete, etc).
    :var copyBaselines: Flag to indicate whether or not to copy baselines.
    """
    name: str = ''
    scheduleToCopy: Schedule = None
    resetWork: bool = False
    copyBaselines: bool = False


@dataclass
class ScheduleDeliverableData(TcBaseObj):
    """
    A container for a new Schedule Deliverable.
    
    :var schedule: The schedule to contain this deliverable.
    :var deliverableType: The type of the deliverable.
    :var deliverableName: The name of the deliverable.
    """
    schedule: Schedule = None
    deliverableType: str = ''
    deliverableName: str = ''


@dataclass
class ScheduleObjDeleteContainer(TcBaseObj):
    """
    An object to delete.
    
    :var object: A tag to the object to be deleted.
    """
    object: BusinessObject = None


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


@dataclass
class TaskDeliverableData(TcBaseObj):
    """
    The input information for a single task deliverable.
    
    :var scheduleTask: The task which will contain this delievable.
    :var scheduleDeliverable: The ScheduleDeliverable to reference.
    :var submitType: The submit type  (3=Don't submit, 0=submit as target, 1=submit as reference).
    """
    scheduleTask: ScheduleTask = None
    scheduleDeliverable: SchDeliverable = None
    submitType: int = 0


@dataclass
class CreateBaselineContainer(TcBaseObj):
    """
    The information to create a baseline.
    
    :var name: The name of the baseline. If empty, uses the schedule ID of the baseline.
    :var schedule: The 'Schedule' to baseline.
    :var parentBaseline: The 'Schedule' baseline to copy from.
    :var isActive: If true, then set the newly created 'baseline' as the active 'baseline'.
    :var includeNewTasks: If true, then baseline the newly created tasks.
    :var updateScheduleBaselineCost: If true, update the baselined 'Schedule' cost. (Not currently used)
    :var taskRebaseOption: A bitmask of types of task to rebaseline (0=none, 1=non-started, 2=non-complete).
    """
    name: str = ''
    schedule: Schedule = None
    parentBaseline: Schedule = None
    isActive: bool = False
    includeNewTasks: bool = False
    updateScheduleBaselineCost: bool = False
    taskRebaseOption: int = 0


@dataclass
class CreateScheduleContainer(TcBaseObj):
    """
    The container for a new schedule.
    
    :var name: The name. Valid value- can not be null.
    :var description: The description. Valid value- can be empty string.
    :var datesLinked: areDatesLinked?
    :var percentLinked: isPercentLinked?
    :var isTemplate: isTemplate?
    :var scheduleType: The schedule type. Valid value (0-Standard)
    :var isPublic: isPublic?
    :var stringValueContainer: A collection of additional attributes.(optional)
    :var customerName: The customer's name. Valid value- can be empty string.
    :var customerNumber: The customer's ID. Valid value- can be empty string.
    :var startDate: The start date.
    :var finishDate: The finish date.
    :var priority: The priority. Valid values are {0-lowest,1-low,2-MediumLow,3-Medium,4-High,5-VeryHigh,6-Highest}
    :var status: The status. Valid values are { 0-Not
    started,1-InProgress,2-NeedsAttention,3-Complete,4-Abandoned,5-Late}
    :var published: isPubished?
    :var linksAllowed: areLinksAllowed?
    """
    name: str = ''
    description: str = ''
    datesLinked: bool = False
    percentLinked: bool = False
    isTemplate: bool = False
    scheduleType: int = 0
    isPublic: bool = False
    stringValueContainer: List[StringValContainer] = ()
    customerName: str = ''
    customerNumber: str = ''
    startDate: datetime = None
    finishDate: datetime = None
    priority: int = 0
    status: str = ''
    published: bool = False
    linksAllowed: bool = False
