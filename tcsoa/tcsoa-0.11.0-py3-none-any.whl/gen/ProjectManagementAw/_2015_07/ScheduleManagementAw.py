from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import SchTaskDeliverable, ScheduleTask, SchDeliverable, WorkspaceObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class TaskDeliverableContainer(TcBaseObj):
    """
    The input information for a single task deliverable.
    
    :var scheduleTask: The task which to which the new delievable will be associated to.
    :var submitType: Specifies the type of the workflow submittal to which the deliverable is routed. Valid values are
    3=Don't submit, 0=submit as target, 1=submit as reference.
    :var deliverableReference: The instance of the Item, Form, Folder Dataset and Document using which the
    SchDeliverable and SchTaskDeliverable are createad.
    :var deliverableName: The name of the deliverable.
    :var deliverableType: The type of the instance associated with the deliverable (Item, Form, Folder Dataset and
    Document).
    """
    scheduleTask: ScheduleTask = None
    submitType: int = 0
    deliverableReference: WorkspaceObject = None
    deliverableName: str = ''
    deliverableType: str = ''


@dataclass
class TaskDeliverablesResponse(TcBaseObj):
    """
    The response container for CreatedTaskDeliverable. CreatedScheduleDeliverable, ScheduleTask that contains
    Delieverable.
    
    :var scheduleTask: The ScheduleTask that is associated with the deliverable.
    :var scheduleDeliverable: The created ScheduleDeliverable to reference. Tag of ScheduleDeliverable.
    :var scheduleTaskDeliverable: The ScheduleTaskDeliverable to reference. Tag of scheduleTask deliverable.
    """
    scheduleTask: ScheduleTask = None
    scheduleDeliverable: SchDeliverable = None
    scheduleTaskDeliverable: SchTaskDeliverable = None


@dataclass
class CreateTaskDeliverablesResponse(TcBaseObj):
    """
    The collection of individual TaskDeilverableResponse.
    
    :var responses: The list of individual Created ScheduleTaskDeliverable,Created Scheduledeliverable and Schedule
    task to which the ScheduleDeliverable and ScheduleTaskDeliverable are associated.
    :var serviceData: The service data.
    """
    responses: List[TaskDeliverablesResponse] = ()
    serviceData: ServiceData = None
