from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.ProjectManagement._2011_06.ScheduleManagement import ScheduleModifyContainer, ScheduleModifyResponses, LoadProgramViewContainer
from tcsoa.gen.Internal.ProjectManagement._2007_06.ScheduleManagement import LoadProgramViewResponse
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def loadProgramView(cls, loadProgramViewContainer: LoadProgramViewContainer) -> LoadProgramViewResponse:
        """
        Load a specified program view. Only one program view is accessed at a time. A program view provides a read-only
        view of tasks across multiple schedules. The program view itself consists of multiple schedules and is a
        top-level view of a program consisting of multiple schedules.
        """
        return cls.execute_soa_method(
            method_name='loadProgramView',
            library='Internal-ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'loadProgramViewContainer': loadProgramViewContainer},
            response_cls=LoadProgramViewResponse,
        )

    @classmethod
    def modifySchedules(cls, scheduleModifyContainers: List[ScheduleModifyContainer]) -> ScheduleModifyResponses:
        """
        This operation updates all the affected scheduling objects based on the users request to the Application
        Interface. Schedule properties can be updated. New schedule tasks, dependencies and resource assignments can be
        created through this operation. Existing schedule tasks, dependencies and resource assignments can be updated.
        Existing schedule tasks, dependencies and resource assignments can be deleted.
         The information needed to modify schedule is specified in the 'ScheduleModifyContainer' structure. It returns
        'ScheduleModifyResponses' which contains the response data from the modify request . Errors will be returned in
        the list of partial errors in the 'ServiceData'.
        
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='modifySchedules',
            library='Internal-ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'scheduleModifyContainers': scheduleModifyContainers},
            response_cls=ScheduleModifyResponses,
        )
