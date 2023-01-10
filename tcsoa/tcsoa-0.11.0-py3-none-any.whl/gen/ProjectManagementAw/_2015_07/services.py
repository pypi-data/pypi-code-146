from __future__ import annotations

from tcsoa.gen.ProjectManagementAw._2015_07.ScheduleManagementAw import TaskDeliverableContainer, CreateTaskDeliverablesResponse
from typing import List
from tcsoa.base import TcService


class ScheduleManagementAwService(TcService):

    @classmethod
    def createTaskDeliverables(cls, taskDeliverableData: List[TaskDeliverableContainer]) -> CreateTaskDeliverablesResponse:
        """
        This operation takes in an instance of Item, Form, Folder, Dataset and Document and creates a new
        ScheduleTaskDeliverable and ScheduleDeliverable and relates them to the ScheduleTask and Schedule.
        """
        return cls.execute_soa_method(
            method_name='createTaskDeliverables',
            library='ProjectManagementAw',
            service_date='2015_07',
            service_name='ScheduleManagementAw',
            params={'taskDeliverableData': taskDeliverableData},
            response_cls=CreateTaskDeliverablesResponse,
        )
