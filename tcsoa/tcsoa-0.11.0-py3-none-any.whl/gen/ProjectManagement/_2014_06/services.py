from __future__ import annotations

from tcsoa.gen.ProjectManagement._2014_06.ScheduleManagement import FilterCriteria, FilteredUsersInfo
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def filterUsers(cls, filteringcriteria: FilterCriteria) -> FilteredUsersInfo:
        """
        In Schedule Manager, Discipline, Group, Role and Fnd0Qualification can be assigned to the ScheduleTask as
        placeholder assignments. These placeholder assignments can then be assigned to specific users who are a part of
        the placeholder assignment. 
        
        The operation returns a list of Users which match the input filter criteria of Discipline, Group, Role and
        Fnd0Qualification. 
        """
        return cls.execute_soa_method(
            method_name='filterUsers',
            library='ProjectManagement',
            service_date='2014_06',
            service_name='ScheduleManagement',
            params={'filteringcriteria': filteringcriteria},
            response_cls=FilteredUsersInfo,
        )
