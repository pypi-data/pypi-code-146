from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import ScheduleTask, TaskDependency
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreatedDependenciesContainer(TcBaseObj):
    """
    The created dependencies
    
    :var createdDependencies: The new dependencies
    :var updatedTasks: The updated tasks
    :var serviceData: The service data
    """
    createdDependencies: List[TaskDependency] = ()
    updatedTasks: List[ScheduleTask] = ()
    serviceData: ServiceData = None


@dataclass
class DependencyCreateContainer(TcBaseObj):
    """
    Creates Dependencies between tasks in the same schedule.
    
    :var predTask: The predecessor task for the dependency
    :var succTask: The successor task for the dependency
    :var depType: The type of dependency: 0-FS, 1-FF, 2-SS, 3-SF
    :var lagTime: The lag time in minutes (480 ~ 1 day)
    """
    predTask: ScheduleTask = None
    succTask: ScheduleTask = None
    depType: int = 0
    lagTime: int = 0
