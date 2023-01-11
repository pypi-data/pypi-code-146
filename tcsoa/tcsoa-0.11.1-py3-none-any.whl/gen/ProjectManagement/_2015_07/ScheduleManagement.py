from __future__ import annotations

from tcsoa.gen.BusinessObjects import ScheduleTask, Discipline, ResourcePool, POM_object
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssignmentCreateContainer(TcBaseObj):
    """
    AssignResource SOA
    
    :var task: ScheduleTask.
    :var resource: Resource.
    :var discipline: Discipline.
    :var assignedPercent: Percent
    :var placeholderAssignment: PlaceHolder assignment.
    :var isPlaceHolder: isPlaceHolder
    """
    task: ScheduleTask = None
    resource: POM_object = None
    discipline: Discipline = None
    assignedPercent: float = 0.0
    placeholderAssignment: ResourcePool = None
    isPlaceHolder: bool = False
