from __future__ import annotations

from tcsoa.gen.Internal.ProjectManagement._2014_10.ScheduleManagement import PasteTaskContainer, DeferredSaveOption, DeferredSaveResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def pasteTasks(cls, inputs: List[PasteTaskContainer]) -> ServiceData:
        """
        The pasteTasks operation pastes the input ScheduleTask to the specified position in the Schedule. The operation
        takes as input the task being pasted, the new parent task under which the task has to be pasted and the
        position in the new parent task after which the task needs to be pasted. The operation performs the cut
        functionality is the input specifies that it's a cut operation. The task is removed from its orginal position
        in the Schedule if the input specifies so.
        """
        return cls.execute_soa_method(
            method_name='pasteTasks',
            library='Internal-ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def deferredSave(cls, deferredOption: DeferredSaveOption) -> DeferredSaveResponse:
        """
        This operation performs the following actions depending on the input specified 
        1.Start a deferred session on a Schedule. Starting a deferred session locks the Schedule so that the other
        users are not be able to update the Schedule in different sessions.
        2.Save the edits made on the Schedule in the deferred session to the database. 
        3.Exit the deferred session after saving the edits made on the Schedule in the deferred session to the
        database. On exit, the lock on the Schedule is released which enables the Schedule for editing by other users.
        4.Discards the contents of the deferred session.
        
        The following data is editable by the user who has started the deferred session on the Schedule when the
        Schedule is in deferred session
        1.Only scheduling attributes of the Schedule such as (planned start date, planned end date, work estimate,
        duration, constraint).
        2.Only scheduling attributes of the ScheduleTask such as (planned start date, planned end date, work estimate,
        duration, constraint).
        3.Create, delete and update of ScheduleTask, ResourceAssignment, TaskDependency and ScheduleMember.
        
        The following data cannot be edited by the user who has started the deferred session on the Schedule
        1.Execution data of ScheduleTask
        2.Insert Schedule, detatch Schedule actions.
        
        The following data can be edited on the Schedule by other users when the Schedule is in deferred session
        1.Only execution data of the Schedule and ScheduleTask. No other update is allowed on the Schedule and
        ScheduleTask.
        
        
        
        Exceptions:
        >ServiceException
        """
        return cls.execute_soa_method(
            method_name='deferredSave',
            library='Internal-ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'deferredOption': deferredOption},
            response_cls=DeferredSaveResponse,
        )
