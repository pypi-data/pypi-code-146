from __future__ import annotations

from typing import List
from tcsoa.gen.ProjectManagement._2011_06.ScheduleManagement import ScheduleCopyOptionsContainer, LockRequest, ProxyTaskContainer, LoadScheduleContainer, ScheduleCopyOptionsContainerAsync, RefreshScheduleContainer, ProxyTaskResponses, TaskExecUpdate, LockResponses, MultipleScheduleLoadResponses
from tcsoa.gen.BusinessObjects import Schedule
from tcsoa.gen.ProjectManagement._2008_06.ScheduleManagement import ScheduleCopyResponses
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def loadSchedules(cls, loadScheduleContainers: List[LoadScheduleContainer]) -> MultipleScheduleLoadResponses:
        """
        The operation loads into memory all the objects belonging to a schedule. The objects are those needed to manage
        and validate the schedule. The objects are can be  instances of Schedule, ScheduleTask, ResourceAssignment,
        TaskDependency, TCCalendar TCCalendarEvents and 'SubMasterMetaData' .
        This operation requires a load option which defines how it behaves, such as loading sections of a structured
        schedule on demand or loading the full schedule if system resources are available to accomplish request. The
        load option is defined by the preference "SM_Structure_Partial_Context" which can be set to one of the
        following values: 
        1)    0 -> load all the schedule objects
        2)    1 -> load the schedule objects on demand.
        The default load option is 0 (load all objects).
        """
        return cls.execute_soa_method(
            method_name='loadSchedules',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'loadScheduleContainers': loadScheduleContainers},
            response_cls=MultipleScheduleLoadResponses,
        )

    @classmethod
    def manageScheduleLocks(cls, requests: List[LockRequest]) -> LockResponses:
        """
        This is an operation that is used to manage concurrent access to schedule data. The server concurrent access
        capability allows schedule data to be accessed simultaneously from different sessions. To ensure data
        integrity, the server enforces a first-in-first-out execution logic by locking out access to the same data from
        other sessions until the lock is removed. During the lock period the session that owns the lock is allowed to
        add and update the schedule data. For deferred save or bulk update, the operation is used to purposely lock the
        schedule data until an unlock request is received.
        """
        return cls.execute_soa_method(
            method_name='manageScheduleLocks',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'requests': requests},
            response_cls=LockResponses,
        )

    @classmethod
    def refreshScheduleObject(cls, refreshScheduleContainer: RefreshScheduleContainer) -> MultipleScheduleLoadResponses:
        """
        The server allows concurrent access to a schedule data and because of this capability updates and additions can
        be added to the schedule data from other sessions apart from a client session. This operation loads all the
        objects in a schedule since the last modified date in the client session. The client can also specify the date
        from which to begin the load. The operation would then return all schedule objects that were modified from the
        specified date. It may also include objects modified in the client's session. The objects are Schedule,
        ScheduleTask, ResourceAssignment, TaskDependency, TCCalendar TCCalendarEvents and SubMasterMetaData.
        """
        return cls.execute_soa_method(
            method_name='refreshScheduleObject',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'refreshScheduleContainer': refreshScheduleContainer},
            response_cls=MultipleScheduleLoadResponses,
        )

    @classmethod
    def copySchedules(cls, containers: List[ScheduleCopyOptionsContainer]) -> ScheduleCopyResponses:
        """
        This operation makes a deep copy of the schedule with options to reset work and copy existing baselines. 
        The following  are the options:  'resetWork' (false if not provided), 
        'copyBaselines' (false if not provided), 
        'copyProxyTasks' (false if not provided), 
        'copyCrossScheduleDependencies' (false if not provided ) 
        
        The information needed to copy the schedule is specified in the 'ScheduleCopyOptionsContainer' structure. It
        returns 'ScheduleCopyResponses' which will have information of copied  schedules and 'ServiceData'. Errors will
        be returned in the list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='copySchedules',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'containers': containers},
            response_cls=ScheduleCopyResponses,
        )

    @classmethod
    def copySchedulesAsync(cls, schToCopy: List[ScheduleCopyOptionsContainerAsync]) -> None:
        """
        This operation copies schedule asynchronously. This is a server function for copySchedule asynchronous
        operation. When this operation is called it files asynchronous request to copy schedule and hence it will not
        block the client for whole copy schedule operation. It will release the client after filing asynchronous
        request immediately so user can perform other operation. The information required to copy the schedule
        asynchronously is passed as parameter to the operation as ScheduleCopyOptionsContainerAsync data structure
        """
        return cls.execute_soa_method(
            method_name='copySchedulesAsync',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'schToCopy': schToCopy},
            response_cls=None,
        )

    @classmethod
    def copySchedulesAsyncClient(cls, schToCopy: List[ScheduleCopyOptionsContainerAsync]) -> bool:
        """
        This operation copies schedule asynchronously. The information required to copy the schedule asynchronously is
        passed as parameter to the operation as 'ScheduleCopyOptionsContainerAsync' data structure.
        """
        return cls.execute_soa_method(
            method_name='copySchedulesAsyncClient',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'schToCopy': schToCopy},
            response_cls=bool,
        )

    @classmethod
    def updateTaskExecution(cls, taskUpdateExec: List[TaskExecUpdate]) -> ServiceData:
        """
        Updates the execution data attributes of Schedule Tasks. The updates are specified through 'TaskExecUpdate' 
        structures. actual start date, actual finish date, percent complete, status, work complete and work remaining
        attributes on schedule task can be updated through this operation.
        """
        return cls.execute_soa_method(
            method_name='updateTaskExecution',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'taskUpdateExec': taskUpdateExec},
            response_cls=ServiceData,
        )

    @classmethod
    def createProxyTasks(cls, newProxyTasks: List[ProxyTaskContainer]) -> ProxyTaskResponses:
        """
        This operation creates proxy tasks. The information needed to create proxy tasks are specified in the
        'ProxyTaskContainer' structure. It returns 'ProxyTaskResponses' which will have information of created proxy
        tasks and 'ServiceData'. Errors will be returned in the list of partial errors in the 'ServiceData' if
        operation fails to create proxy task.
        """
        return cls.execute_soa_method(
            method_name='createProxyTasks',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'newProxyTasks': newProxyTasks},
            response_cls=ProxyTaskResponses,
        )

    @classmethod
    def deleteScheduleAsync(cls, schToDelete: Schedule) -> None:
        """
        Deletes a specified schedule asynchronously. The operation returns after triggering the asynchronous delete on
        the schedule.
        """
        return cls.execute_soa_method(
            method_name='deleteScheduleAsync',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'schToDelete': schToDelete},
            response_cls=None,
        )

    @classmethod
    def deleteScheduleAsyncClient(cls, schToDelete: Schedule) -> bool:
        """
        Deletes the specified schedule asynchronously but will check that there is a connection between client and
        server before performing the delete action. After the check is performed successfully a call to
        'deleteScheduleAsync' operation is made to finalize the deletion of the schedule. See operation
        'deleteScheduleAsync' for more details. 
        """
        return cls.execute_soa_method(
            method_name='deleteScheduleAsyncClient',
            library='ProjectManagement',
            service_date='2011_06',
            service_name='ScheduleManagement',
            params={'schToDelete': schToDelete},
            response_cls=bool,
        )
