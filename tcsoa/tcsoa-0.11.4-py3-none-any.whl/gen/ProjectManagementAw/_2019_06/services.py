from __future__ import annotations

from tcsoa.gen.ProjectManagementAw._2019_06.ScheduleManagementAw import ClaimAssignmentData, LoadAssignedTasksResponse, LoadAssignedTasksInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementAwService(TcService):

    @classmethod
    def claimAssignments(cls, claimAssignmentsData: List[ClaimAssignmentData]) -> ServiceData:
        """
        This operation claims assignments by deleting the resource pool assignments and assinging them to the logged in
        user. An assignment can be claimed only if the ScheduleTask object is assigned to any member in the
        ResourcePool object and the logged in user is a member of the ResourcePool object.
        """
        return cls.execute_soa_method(
            method_name='claimAssignments',
            library='ProjectManagementAw',
            service_date='2019_06',
            service_name='ScheduleManagementAw',
            params={'claimAssignmentsData': claimAssignmentsData},
            response_cls=ServiceData,
        )

    @classmethod
    def loadAssignedTasks(cls, loadTasksInfo: List[LoadAssignedTasksInfo]) -> LoadAssignedTasksResponse:
        """
        Loads the ScheduleTask objects assigned to the logged in user based on the information provided in the    
        &lsquo;LoadAssignedTasksInfo&rsquo; inputs. The assigned tasks are determined by the ResourceAssigment relation
        where the  primary object is ScheduleTask and the secondary is the current logged in User.
        """
        return cls.execute_soa_method(
            method_name='loadAssignedTasks',
            library='ProjectManagementAw',
            service_date='2019_06',
            service_name='ScheduleManagementAw',
            params={'loadTasksInfo': loadTasksInfo},
            response_cls=LoadAssignedTasksResponse,
        )
