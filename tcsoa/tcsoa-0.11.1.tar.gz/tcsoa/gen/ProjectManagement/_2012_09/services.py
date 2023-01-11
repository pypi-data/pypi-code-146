from __future__ import annotations

from tcsoa.gen.ProjectManagement._2012_09.ScheduleManagement import AssignmentCreateContainer
from tcsoa.gen.ProjectManagement._2012_02.ScheduleManagement import CreatedObjectsContainer
from typing import List
from tcsoa.gen.BusinessObjects import ScheduleTask, Schedule, ResourceAssignment
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def claimAssignment(cls, task: ScheduleTask, assignment: ResourceAssignment) -> CreatedObjectsContainer:
        """
        Claims an assignment
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='claimAssignment',
            library='ProjectManagement',
            service_date='2012_09',
            service_name='ScheduleManagement',
            params={'task': task, 'assignment': assignment},
            response_cls=CreatedObjectsContainer,
        )

    @classmethod
    def assignResources(cls, schedule: Schedule, createAssignments: List[AssignmentCreateContainer]) -> CreatedObjectsContainer:
        """
        Assigns resources to tasks.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='assignResources',
            library='ProjectManagement',
            service_date='2012_09',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'createAssignments': createAssignments},
            response_cls=CreatedObjectsContainer,
        )
