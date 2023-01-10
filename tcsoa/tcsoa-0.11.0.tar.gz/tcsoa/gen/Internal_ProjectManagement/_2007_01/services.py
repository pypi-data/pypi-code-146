from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.ProjectManagement._2007_01.ScheduleManagement import MultipleScheduleLoadResponse, ScheduleChangeContainer
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def loadSchedule(cls, schedule: List[str]) -> MultipleScheduleLoadResponse:
        """
        Loads all the objects in a schedule needed for the scheduling logic.
        """
        return cls.execute_soa_method(
            method_name='loadSchedule',
            library='Internal-ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'schedule': schedule},
            response_cls=MultipleScheduleLoadResponse,
        )

    @classmethod
    def modifySchedule(cls, scheduleChangeContainer: ScheduleChangeContainer) -> ServiceData:
        """
        Updates all the affected scheduling objects based on the initial
        users request to the Application Interface.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='modifySchedule',
            library='Internal-ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'scheduleChangeContainer': scheduleChangeContainer},
            response_cls=ServiceData,
        )
