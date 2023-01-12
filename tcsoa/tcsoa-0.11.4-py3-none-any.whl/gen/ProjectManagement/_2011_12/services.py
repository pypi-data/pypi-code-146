from __future__ import annotations

from tcsoa.gen.ProjectManagement._2011_12.ScheduleManagement import DependencyCreateContainer, CreatedDependenciesContainer
from typing import List
from tcsoa.gen.BusinessObjects import Schedule
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def createDependencies(cls, schedule: Schedule, newDependencies: List[DependencyCreateContainer]) -> CreatedDependenciesContainer:
        """
        Creates Dependencies between tasks in the same schedule, between a task and a proxy task in the same schedule,
        or between a tasks in different schedules (but in the same master schedule).  It returns the created
        dependencies, created proxy tasks (if any), and the ob
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='createDependencies',
            library='ProjectManagement',
            service_date='2011_12',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'newDependencies': newDependencies},
            response_cls=CreatedDependenciesContainer,
        )
