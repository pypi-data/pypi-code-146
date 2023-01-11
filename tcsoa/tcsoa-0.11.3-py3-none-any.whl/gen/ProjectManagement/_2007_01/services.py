from __future__ import annotations

from tcsoa.gen.ProjectManagement._2007_01.ScheduleManagement import CreateBaselineContainer, TaskDeliverableData, CreateScheduleContainer, ScheduleObjDeleteContainer, ScheduleDeliverableData, MembershipData, ScheduleCopyContainer
from typing import List
from tcsoa.gen.BusinessObjects import ScheduleTask, Schedule
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def copySchedules(cls, scheduleCopyContainer: List[ScheduleCopyContainer]) -> ServiceData:
        """
        Makes a deep copy of the schedule with options to reset work and copy existing baselines.
        """
        return cls.execute_soa_method(
            method_name='copySchedules',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'scheduleCopyContainer': scheduleCopyContainer},
            response_cls=ServiceData,
        )

    @classmethod
    def addMemberships(cls, membershipData: List[MembershipData]) -> ServiceData:
        """
        Add resources to the schedule with given membership levels.
        """
        return cls.execute_soa_method(
            method_name='addMemberships',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'membershipData': membershipData},
            response_cls=ServiceData,
        )

    @classmethod
    def createNewBaselines(cls, createBaselineContainer: List[CreateBaselineContainer]) -> ServiceData:
        """
        This operation creates a new schedule baselines possibly based on a previous baseline.
        The created objects are returned back in the 'ServiceData' of the response.The information required to create
        new baseline is passed as input parameter to the operation through 'CreateBaselineContainer' data structure.
        """
        return cls.execute_soa_method(
            method_name='createNewBaselines',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'createBaselineContainer': createBaselineContainer},
            response_cls=ServiceData,
        )

    @classmethod
    def createSchedule(cls, newSchedules: List[CreateScheduleContainer]) -> ServiceData:
        """
        Create new scheduling object based on the initial
        user's request to the Application Interface.
        """
        return cls.execute_soa_method(
            method_name='createSchedule',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'newSchedules': newSchedules},
            response_cls=ServiceData,
        )

    @classmethod
    def createScheduleDeliverableTemplates(cls, scheduleDeliverableData: List[ScheduleDeliverableData]) -> ServiceData:
        """
        Creates new schedule deliverable templates and relates them to the schedule.
        """
        return cls.execute_soa_method(
            method_name='createScheduleDeliverableTemplates',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'scheduleDeliverableData': scheduleDeliverableData},
            response_cls=ServiceData,
        )

    @classmethod
    def createTaskDeliverableTemplates(cls, taskDeliverableData: List[TaskDeliverableData]) -> ServiceData:
        """
        Creates new task deliverable templates and relates them to the task.
        """
        return cls.execute_soa_method(
            method_name='createTaskDeliverableTemplates',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'taskDeliverableData': taskDeliverableData},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteSchedulingObjects(cls, scheduleObjDeleteContainer: List[ScheduleObjDeleteContainer]) -> ServiceData:
        """
        The operation is used to delete a scheduling object which cannot be deleted by 'deleteObjects' operation. After
        the operation is called, the business logic determines whether to delete the scheduling objects by examining
        the schedule preservation rule, SM_PREVENT_DELETE_STATE. The SM_PREVENT_DELETE_STATE rule is optional and the
        system admin can remove the rule from the system or set its value to an empty list. But if the rule is in the
        system and set to any status or statuses then the value of the rule would be applied.
        The scheduling objects are Schedule, ScheduleTask, TaskDependency and ResourceAssignment.
        """
        return cls.execute_soa_method(
            method_name='deleteSchedulingObjects',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'scheduleObjDeleteContainer': scheduleObjDeleteContainer},
            response_cls=ServiceData,
        )

    @classmethod
    def baselineTasks(cls, scheduleTasks: List[ScheduleTask], scheduleBaseline: Schedule) -> ServiceData:
        """
        This operation baselines or re-baselines a task's data in the context of an existing schedule baseline. The
        updated objects or added task baselines are returned back in the service data of the response. This operation
        throws a 'ServiceException' in case of failure. The service exception will contain the error message of the
        failure. Additional errors will be returned in the list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='baselineTasks',
            library='ProjectManagement',
            service_date='2007_01',
            service_name='ScheduleManagement',
            params={'scheduleTasks': scheduleTasks, 'scheduleBaseline': scheduleBaseline},
            response_cls=ServiceData,
        )
