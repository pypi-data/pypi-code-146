from __future__ import annotations

from tcsoa.gen.ProjectManagement._2009_10.ScheduleManagement import ScheduleModifyContainer, GenericResponseContainer, GenericAttributesContainer
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def modifySchedules(cls, scheduleModifyContainers: List[ScheduleModifyContainer]) -> ServiceData:
        """
        Not Implemented
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='modifySchedules',
            library='ProjectManagement',
            service_date='2009_10',
            service_name='ScheduleManagement',
            params={'scheduleModifyContainers': scheduleModifyContainers},
            response_cls=ServiceData,
        )

    @classmethod
    def updateTasks(cls, updates: List[GenericAttributesContainer], scheduleUid: List[str]) -> GenericResponseContainer:
        """
        Updates Schedule Tasks. Note: You must use PERSIST for the ServiceType and ScheduleTaskUpdate for the
        operationType inside the GenericAttributesContainers which are passed.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='updateTasks',
            library='ProjectManagement',
            service_date='2009_10',
            service_name='ScheduleManagement',
            params={'updates': updates, 'scheduleUid': scheduleUid},
            response_cls=GenericResponseContainer,
        )
