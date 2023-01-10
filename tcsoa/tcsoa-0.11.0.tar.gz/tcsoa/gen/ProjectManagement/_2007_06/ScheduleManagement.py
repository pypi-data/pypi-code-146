from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TCCalendar, ScheduleTask, Schedule, ResourceAssignment, TaskDependency, TCCalendarEvent
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetNotificationRuleContainer(TcBaseObj):
    """
    The input information needed to find all notifications for a particular task or schedule.
    
    :var target: The tag of a Schedule or ScheduleTask.
    :var subscriber: The tag of the subscriber.
    """
    target: BusinessObject = None
    subscriber: BusinessObject = None


@dataclass
class MultiScheduleCopyResponse(TcBaseObj):
    """
    Container to hold multiple ScheduleCopyResponse objects.
    
    :var scheduleResponse: A collection of the schedule responses.
    :var serviceData: The ServiceData.
    """
    scheduleResponse: List[ScheduleCopyResponse] = ()
    serviceData: ServiceData = None


@dataclass
class NotificationRuleContainer(TcBaseObj):
    """
    The information needed for the creation of a single Notification rule.
    
    :var target: The tag of a schedule or task
    :var subscriber: The subscriber for this notification.  It is the Target object in the case of a notification or a
    User object in the case of a subscription.
    :var notificationSubject: Subject of the email. Valid value- can be empty string
    :var notificationMessage: Message of the e-mail. Valid value- can be empty string
    :var recipient: The Users, groups, disciplines, or schedule members to be notified.
    :var additionalEmails: A semi-colon separated list of e-mail addresses. Valid value - can be empty string
    :var notificationCondition: The condition data for notifications that are triggered conditionally.  E.g.  Schedule
    Task near due. Valid value - can be empty string
    :var ruleType: The type of rule to create. Valid values are
    {__Add_Task,__Delete_Task,__Near_Due,__Overdue,__Start_Date_Change,__Finish_Date_Change,__Status_Change,__Status_ChangeTo,__Priority_Change,__Priority_ChangeTo,__Work_Estimate_Change,__Work_Complete_Change,__Work_Ready,__User_Assigned
    }
    :var status: Active or inactive status of the notification.
    :var update: Attempting to update an existing rule.
    """
    target: BusinessObject = None
    subscriber: BusinessObject = None
    notificationSubject: str = ''
    notificationMessage: str = ''
    recipient: List[BusinessObject] = ()
    additionalEmails: str = ''
    notificationCondition: str = ''
    ruleType: str = ''
    status: bool = False
    update: bool = False


@dataclass
class NotificationRulesList(TcBaseObj):
    """
    A collection of the single NotificationRuleContainer objects.
    
    :var notificationRules: The collection of Notification Rules.
    :var serviceData: The ServiceData.
    """
    notificationRules: List[NotificationRuleContainer] = ()
    serviceData: ServiceData = None


@dataclass
class ScheduleCopyOptionsContainer(TcBaseObj):
    """
    The input information necessary to copy a schedule.
    
    :var name: The name of the new schedule.
    :var description: The description of the new schedule.
    :var scheduleToCopy: The tag to the schedule to copy.
    :var resetWork: Flag to indicate whether or not to reset the tasks' execution data (%, status, work complete, etc).
    :var copyBaselines: Flag to indicate whether or not to copy baselines.
    :var loadOnResponse: Flag to indicate whether or not to load the schedule in the response.
    """
    name: str = ''
    description: str = ''
    scheduleToCopy: Schedule = None
    resetWork: bool = False
    copyBaselines: bool = False
    loadOnResponse: bool = False


@dataclass
class ScheduleCopyResponse(TcBaseObj):
    """
    The response from a schedule copy call.  It includes all the data necessary to load that schedule.
    
    :var schedule: The schedule.
    :var scheduleTask: The schedule tasks.
    :var resourceAssignment: The task assignments.
    :var taskDependency: The task dependencies.
    :var calendar: The calendars asssociated with the schedule and its members.
    :var calendarEvent: The calendar events associated with the calendars.
    """
    schedule: Schedule = None
    scheduleTask: List[ScheduleTask] = ()
    resourceAssignment: List[ResourceAssignment] = ()
    taskDependency: List[TaskDependency] = ()
    calendar: List[TCCalendar] = ()
    calendarEvent: List[TCCalendarEvent] = ()


@dataclass
class TaskDeliverableContainer(TcBaseObj):
    """
    The input information for a single task deliverable.
    
    :var scheduleTask: The task which will contain this delievable. Tag of the task
    :var scheduleDeliverable: The ScheduleDeliverable to reference. Tag of schedule deliverable.
    :var submitType: The submit type  (3=Don't submit, 0=submit as target, 1=submit as reference).
    """
    scheduleTask: ScheduleTask = None
    scheduleDeliverable: BusinessObject = None
    submitType: int = 0


@dataclass
class DeleteNotificationRuleContainer(TcBaseObj):
    """
    The input information needed to delete an existing notification rule.
    
    :var target: The tag  of  the Schedule  or ScheduleTask.
    :var subscriber: The tag of the subscriber.
    :var ruleType: The type of rule to delete. Valid values-{
    __Add_Task,__Delete_Task,__Near_Due,__Overdue,__Start_Date_Change,__Finish_Date_Change,__Status_Change,__Status_ChangeTo,__Priority_Change,__Priority_ChangeTo,__Work_Estimate_Change,__Work_Complete_Change,__Work_Ready,__User_Assigned}
    """
    target: BusinessObject = None
    subscriber: BusinessObject = None
    ruleType: str = ''
