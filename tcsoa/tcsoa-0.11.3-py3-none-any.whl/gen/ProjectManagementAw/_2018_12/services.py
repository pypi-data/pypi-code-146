from __future__ import annotations

from tcsoa.gen.ProjectManagementAw._2015_07.ScheduleManagementAw import CreateTaskDeliverablesResponse
from tcsoa.gen.BusinessObjects import User, Discipline, Schedule
from typing import List
from tcsoa.gen.ProjectManagementAw._2018_12.ScheduleManagementAw import LoadScheduleInfo2, TaskDeliverableInput, LoadBaselineResponse, LoadBaselineInfo, LoadScheduleResponse2, RecalculateInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementAwService(TcService):

    @classmethod
    def loadSchedule2(cls, loadScheduleInfo: LoadScheduleInfo2) -> LoadScheduleResponse2:
        """
        Loads the ScheduleTask objects of a given Schedule based on the reference ScheduleTask. The number of
        ScheduleTask objects to be loaded will be determined by AWC_DefaultPageSize preference or &lsquo;50&rsquo;, if
        the preference is not found. This operation also loads the baseline tasks, Fnd0ProxyTask objects and
        TaskDependency relations which are referencing the loaded ScheduleTask objects.
        """
        return cls.execute_soa_method(
            method_name='loadSchedule2',
            library='ProjectManagementAw',
            service_date='2018_12',
            service_name='ScheduleManagementAw',
            params={'loadScheduleInfo': loadScheduleInfo},
            response_cls=LoadScheduleResponse2,
        )

    @classmethod
    def recalculateSchedules(cls, recalculateInputs: List[RecalculateInput], runInBackground: bool) -> ServiceData:
        """
        This operation performs the revalidation and rerunning of the business logic on the properties of the schedule
        and its child objects based on the requested properties flag or ALL.
        """
        return cls.execute_soa_method(
            method_name='recalculateSchedules',
            library='ProjectManagementAw',
            service_date='2018_12',
            service_name='ScheduleManagementAw',
            params={'recalculateInputs': recalculateInputs, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def recalculateSchedulesAsync(cls, recalculateInputs: List[RecalculateInput]) -> None:
        """
        This operation performs the revalidation and rerunning of the business logic on the properties of the schedule
        and its child objects based on the requested properties flag or ALL. This operation runs asynchronously in its
        own server in the background.
        """
        return cls.execute_soa_method(
            method_name='recalculateSchedulesAsync',
            library='ProjectManagementAw',
            service_date='2018_12',
            service_name='ScheduleManagementAw',
            params={'recalculateInputs': recalculateInputs},
            response_cls=None,
        )

    @classmethod
    def createMultipleTaskDeliverables(cls, taskDeliverableInputs: List[TaskDeliverableInput]) -> CreateTaskDeliverablesResponse:
        """
        This operation takes in an instance of Item, Form, Folder, Dataset and Document and creates one or more
        ScheduleTaskDeliverables and ScheduleDeliverable and relates them to one or more ScheduleTask and its
        associated Schedule.
        """
        return cls.execute_soa_method(
            method_name='createMultipleTaskDeliverables',
            library='ProjectManagementAw',
            service_date='2018_12',
            service_name='ScheduleManagementAw',
            params={'taskDeliverableInputs': taskDeliverableInputs},
            response_cls=CreateTaskDeliverablesResponse,
        )

    @classmethod
    def designateDiscipline(cls, schedule: Schedule, discipline: Discipline, user: User, revert: bool, runInBackground: bool) -> ServiceData:
        """
        This operation removes all assignments in a schedule of a Discipline and assigns them to the specified User.
        While designating the discipline, the system will check if the user is a ScheduleMember. If not, the system
        will create a ScheduleMember for the user. 
        The system will get and delete all resources assignments for the discipline in the schedule and create new
        resource assignments for the user.
        The revert option is to revert the ResourceAssignment objects from the User to Discipline object for all
        schedule tasks in the schedule.
        """
        return cls.execute_soa_method(
            method_name='designateDiscipline',
            library='ProjectManagementAw',
            service_date='2018_12',
            service_name='ScheduleManagementAw',
            params={'schedule': schedule, 'discipline': discipline, 'user': user, 'revert': revert, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def designateDisciplineAsync(cls, schedule: Schedule, discipline: Discipline, user: User, revert: bool) -> None:
        """
        This operation removes all assignments in a schedule of a Discipline and assigns them to the specified User.
        While designating the discipline, the system will check if the user is a ScheduleMember. If not, the system
        will create a ScheduleMember for the user. 
        The system will get and delete all resources assignments for the discipline in the Schedule and create new
        resource assignments for the user.
        The revert option is to revert the ResourceAssignment objects from the User to Discipline object for all
        schedule tasks in the Schedule.
        """
        return cls.execute_soa_method(
            method_name='designateDisciplineAsync',
            library='ProjectManagementAw',
            service_date='2018_12',
            service_name='ScheduleManagementAw',
            params={'schedule': schedule, 'discipline': discipline, 'user': user, 'revert': revert},
            response_cls=None,
        )

    @classmethod
    def loadBaseline(cls, loadBaselineInfo: LoadBaselineInfo) -> LoadBaselineResponse:
        """
        Loads the information about the baseline tasks of the given ScheduleTask objects based on the source Schedule
        and the baseline Schedule.
        """
        return cls.execute_soa_method(
            method_name='loadBaseline',
            library='ProjectManagementAw',
            service_date='2018_12',
            service_name='ScheduleManagementAw',
            params={'loadBaselineInfo': loadBaselineInfo},
            response_cls=LoadBaselineResponse,
        )
