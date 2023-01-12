from __future__ import annotations

from tcsoa.gen.ProjectManagement._2015_07.ScheduleManagement import AssignmentCreateContainer
from tcsoa.gen.ProjectManagement._2012_02.ScheduleManagement import CreatedObjectsContainer
from typing import List
from tcsoa.gen.BusinessObjects import Schedule
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from datetime import datetime


class ScheduleManagementService(TcService):

    @classmethod
    def shiftSchedule(cls, schedule: Schedule, newDate: datetime, isNewFinishDate: bool, runInBackground: bool) -> ServiceData:
        """
        Shifts the specified Schedule to the new start or finish date. In case of background mode, this operation files
        an asynchronous request to shift the Schedule and releases the client immediately so that the user can perform
        other operation.
        
        Exceptions:
        >If an unhandled error is encountered during the shift schedule operation.
        """
        return cls.execute_soa_method(
            method_name='shiftSchedule',
            library='ProjectManagement',
            service_date='2015_07',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'newDate': newDate, 'isNewFinishDate': isNewFinishDate, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def shiftScheduleAsync(cls, schedule: Schedule, newDate: datetime, isNewFinishDate: bool) -> None:
        """
        Shifts the specified Schedule to the new start or finish date. This operation runs asynchronously in its own
        server in the background.
        """
        return cls.execute_soa_method(
            method_name='shiftScheduleAsync',
            library='ProjectManagement',
            service_date='2015_07',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'newDate': newDate, 'isNewFinishDate': isNewFinishDate},
            response_cls=None,
        )

    @classmethod
    def assignResources(cls, schedule: Schedule, createAssignments: List[AssignmentCreateContainer]) -> CreatedObjectsContainer:
        """
        Assign Resource
        """
        return cls.execute_soa_method(
            method_name='assignResources',
            library='ProjectManagement',
            service_date='2015_07',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'createAssignments': createAssignments},
            response_cls=CreatedObjectsContainer,
        )
