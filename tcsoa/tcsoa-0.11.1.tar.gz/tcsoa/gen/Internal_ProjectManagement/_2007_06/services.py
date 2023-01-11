from __future__ import annotations

from tcsoa.gen.Internal.ProjectManagement._2007_06.ScheduleManagement import ResourceAssignmentLoadResponse, ScheduleModifyContainer, LoadResourceAssignmentContainer, LoadProgramViewResponse, LoadProgramViewContainer
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def loadProgramView(cls, loadProgramViewContainer: LoadProgramViewContainer) -> LoadProgramViewResponse:
        """
        Load a program view
        Only one program view is accessed at a time. The program view itself consists of multiple schedules
        and is a top-level view of a program consisting of multiple schedules.
        """
        return cls.execute_soa_method(
            method_name='loadProgramView',
            library='Internal-ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'loadProgramViewContainer': loadProgramViewContainer},
            response_cls=LoadProgramViewResponse,
        )

    @classmethod
    def loadResourceAssignments(cls, loadResourceAssignmentContainer: LoadResourceAssignmentContainer) -> ResourceAssignmentLoadResponse:
        """
        Loads all the resource assignments for a given resource(s) in published and non-template schedules only.
        Besides this, if schedulesToAlwaysInclude parameter contains some schedules, they are also taken up.
        """
        return cls.execute_soa_method(
            method_name='loadResourceAssignments',
            library='Internal-ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'loadResourceAssignmentContainer': loadResourceAssignmentContainer},
            response_cls=ResourceAssignmentLoadResponse,
        )

    @classmethod
    def modifySchedule(cls, scheduleModifyContainer: ScheduleModifyContainer) -> ServiceData:
        """
        Updates all the affected scheduling objects based on the initial
        users request to the Application Interface.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='modifySchedule',
            library='Internal-ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'scheduleModifyContainer': scheduleModifyContainer},
            response_cls=ServiceData,
        )
