from __future__ import annotations

from typing import List
from tcsoa.gen.ProjectManagementAw._2016_12.ScheduleManagementAw import LoadScheduleInfo, LoadScheduleResponse, ReplaceMemberAssignmentData
from tcsoa.gen.BusinessObjects import ScheduleMember
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementAwService(TcService):

    @classmethod
    def loadSchedule(cls, loadScheduleInfo: LoadScheduleInfo) -> LoadScheduleResponse:
        """
        Loads the ScheduleTask objects of a given Schedule based on the reference ScheduleTask. The number of
        ScheduleTask objects to be loaded will be determined by AWC_DefaultPageSize preference or &lsquo;50&rsquo;, if
        the preference is not found. This operation also loads all the Fnd0ProxyTask objects and TaskDependency
        relations which are referencing the loaded ScheduleTask objects.
        """
        return cls.execute_soa_method(
            method_name='loadSchedule',
            library='ProjectManagementAw',
            service_date='2016_12',
            service_name='ScheduleManagementAw',
            params={'loadScheduleInfo': loadScheduleInfo},
            response_cls=LoadScheduleResponse,
        )

    @classmethod
    def removeAssignments(cls, membersToRemoveAssignments: List[ScheduleMember], runInBackground: bool) -> ServiceData:
        """
        This operation removes all assignments of a ScheduleMember. The system will not delete the ScheduleMember
        object.
        """
        return cls.execute_soa_method(
            method_name='removeAssignments',
            library='ProjectManagementAw',
            service_date='2016_12',
            service_name='ScheduleManagementAw',
            params={'membersToRemoveAssignments': membersToRemoveAssignments, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def removeAssignmentsAsync(cls, membersToRemoveAssignments: List[ScheduleMember]) -> None:
        """
        This operation removes all assignments of a ScheduleMember specified in the input. This operation runs
        asynchronously in its own server in the background.
        """
        return cls.execute_soa_method(
            method_name='removeAssignmentsAsync',
            library='ProjectManagementAw',
            service_date='2016_12',
            service_name='ScheduleManagementAw',
            params={'membersToRemoveAssignments': membersToRemoveAssignments},
            response_cls=None,
        )

    @classmethod
    def replaceMemberAssignments(cls, replaceMemberAssignmentData: List[ReplaceMemberAssignmentData], runInBackground: bool) -> ServiceData:
        """
        This operation removes all assignments of a ScheduleMember and assigns them to a new ScheduleMember. While
        replacing the assignments, the system will check if the new resource is a ScheduleMember. If not, the system
        will create a ScheduleMember for the resource and replace the assignments.
        """
        return cls.execute_soa_method(
            method_name='replaceMemberAssignments',
            library='ProjectManagementAw',
            service_date='2016_12',
            service_name='ScheduleManagementAw',
            params={'replaceMemberAssignmentData': replaceMemberAssignmentData, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def replaceMemberAssignmentsAsync(cls, replaceMemberAssignmentData: List[ReplaceMemberAssignmentData]) -> None:
        """
        This operation removes all assignments of a ScheduleMember and assigns them to a new ScheduleMember. While
        replacing the assignments, the system will check if the new resource is a ScheduleMember. If not, the system
        will create a ScheduleMember for the resource and replace the assignments. This operation runs asynchronously
        in its own server in the background.
        """
        return cls.execute_soa_method(
            method_name='replaceMemberAssignmentsAsync',
            library='ProjectManagementAw',
            service_date='2016_12',
            service_name='ScheduleManagementAw',
            params={'replaceMemberAssignmentData': replaceMemberAssignmentData},
            response_cls=None,
        )
