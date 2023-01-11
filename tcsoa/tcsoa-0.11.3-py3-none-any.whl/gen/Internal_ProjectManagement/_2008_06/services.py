from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.ProjectManagement._2008_06.ScheduleManagement import ScheduleModifyContainer, ScheduleModifyResponses, MultipleScheduleLoadResponses
from tcsoa.gen.BusinessObjects import Schedule
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def getSchedulesToinsert(cls, masterSchedule: Schedule) -> ServiceData:
        """
        The operation is used to query for all schedules where the user is a ScheduleMember  object with schedule
        manager coordinator privilege. After querying for the schedules, the business logic filters the list to ensure
        that schedules in the list that is returned do not cause circular dependencies when used in a master schedule.
        The operation returns the list of schedules in the 'ServiceData'  as 'm_plainObjs'. By design the list is meant
        to be inserted into a designated master schedule. 
        """
        return cls.execute_soa_method(
            method_name='getSchedulesToinsert',
            library='Internal-ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'masterSchedule': masterSchedule},
            response_cls=ServiceData,
        )

    @classmethod
    def loadSchedules(cls, schedule: List[str]) -> MultipleScheduleLoadResponses:
        """
        Loads all the objects in a schedule needed for the scheduling logic.
        """
        return cls.execute_soa_method(
            method_name='loadSchedules',
            library='Internal-ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'schedule': schedule},
            response_cls=MultipleScheduleLoadResponses,
        )

    @classmethod
    def modifySchedule(cls, scheduleModifyContainers: List[ScheduleModifyContainer]) -> ScheduleModifyResponses:
        """
        Updates all the affected scheduling objects based on the initial users request to the application interface. 
        Schedule properties can be updated. New schedule tasks, dependencies and resource assignments can be created
        through this operation. Existing schedule tasks, dependencies and resource assignments can be updated. Existing
        schedule tasks, dependencies and resource assignments can be deleted.
        
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='modifySchedule',
            library='Internal-ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'scheduleModifyContainers': scheduleModifyContainers},
            response_cls=ScheduleModifyResponses,
        )
