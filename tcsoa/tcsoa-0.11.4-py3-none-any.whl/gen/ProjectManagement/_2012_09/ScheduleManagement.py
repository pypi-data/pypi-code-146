from __future__ import annotations

from tcsoa.gen.BusinessObjects import ScheduleTask, Discipline, POM_object
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssignmentCreateContainer(TcBaseObj):
    """
    The information needed to create a new assignment to a task.
    
    :var task: The task to assign the resource.
    :var resource: The resource (User, Group, Role, Resource Pool) being assigned (or null if discipline assignment).
    :var discipline: The discipline of the assignee (if User) or the discipline for the assignment.
    :var assignedPercent: The percentage effort being assigned (I.E. 50.0 == 50%)
    """
    task: ScheduleTask = None
    resource: POM_object = None
    discipline: Discipline = None
    assignedPercent: float = 0.0
