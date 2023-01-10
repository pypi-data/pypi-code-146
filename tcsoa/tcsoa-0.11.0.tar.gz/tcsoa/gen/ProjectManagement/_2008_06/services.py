from __future__ import annotations

from tcsoa.gen.ProjectManagement._2008_06.ScheduleManagement import ScheduleCopyOptionsContainer, CreateBillRateResponse, NewScheduleContainer, ScheduleDeliverableData, AddMembershipResponse, TaskCostUpdate, BillRateContainer, UpdateTaskCostDataResponse, MembershipData, ScheduleCopyResponses, CreateScheduleResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def copySchedules(cls, scheduleCopyContainer: List[ScheduleCopyOptionsContainer]) -> ScheduleCopyResponses:
        """
        This operation makes a deep copy of the schedule with options to reset work and copy existing baselines. The
        information needed to copy schedule is specified in the 'ScheduleCopyOptionsContainer' structure. It returns
        'ScheduleCopyResponses' which will have information of copied  schedules and 'ServiceData'. Errors will be
        returned in the list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='copySchedules',
            library='ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'scheduleCopyContainer': scheduleCopyContainer},
            response_cls=ScheduleCopyResponses,
        )

    @classmethod
    def updateTaskCostData(cls, updates: List[TaskCostUpdate]) -> UpdateTaskCostDataResponse:
        """
        This operation creates, updates and deletes fixed cost entries and task costing metadata such as bill code, sub
        code etc. This operation throws exceptions that are system and database exceptions. There are no specific
        business logic errors. The created objects are returned back in the service data of the response.
        
        """
        return cls.execute_soa_method(
            method_name='updateTaskCostData',
            library='ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'updates': updates},
            response_cls=UpdateTaskCostDataResponse,
        )

    @classmethod
    def createBillRates(cls, rates: List[BillRateContainer]) -> CreateBillRateResponse:
        """
        This operation creates a new BillRates. BillRate is a business object  that is used to represent Rate
        Modifiers,which are used  with resource costing information to calculate schedule and task costs and are
        defined by billing types, rates and currency. This operation throws exceptions that are system and database
        exceptions . There are no specific business logic errors. The created objects are returned back in the service
        data of the response.
        """
        return cls.execute_soa_method(
            method_name='createBillRates',
            library='ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'rates': rates},
            response_cls=CreateBillRateResponse,
        )

    @classmethod
    def addMemberships(cls, membershipData: List[MembershipData]) -> AddMembershipResponse:
        """
        This operation adds resources to the schedule with given membership levels. 
        
        The information required to add  new resource  to the schedule is passed to the function through
        'MembershipData' structure.
        
        The operation saves the references to the newly created membership objects and errors if any in the
        'ServiceData' of the 'MembershipDataResponse' data structure.
         
        When a resource that needs to be added doesnot exist,the operation returns and  the error is saved in the
        'ServiceData' of the response.
        """
        return cls.execute_soa_method(
            method_name='addMemberships',
            library='ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'membershipData': membershipData},
            response_cls=AddMembershipResponse,
        )

    @classmethod
    def createSchedule(cls, newSchedules: List[NewScheduleContainer]) -> CreateScheduleResponse:
        """
        This operation creates new schedule based on the initial user's request to the application interface. The
        information needed to create Schedule is specified in the 'NewScheduleContainer' structure. It returns
        'CreateScheduleResponse' which will have information of created schedules and 'ServiceData'. Errors will be
        returned in the list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='createSchedule',
            library='ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'newSchedules': newSchedules},
            response_cls=CreateScheduleResponse,
        )

    @classmethod
    def createScheduleDeliverableTemplates(cls, scheduleDeliverableData: List[ScheduleDeliverableData]) -> ServiceData:
        """
        This operation creates new schedule deliverable. The created objects are returned back in the 'ServiceData' of
        the response. 'ServiceData' will contain partial errors in case of operation failure.
        """
        return cls.execute_soa_method(
            method_name='createScheduleDeliverableTemplates',
            library='ProjectManagement',
            service_date='2008_06',
            service_name='ScheduleManagement',
            params={'scheduleDeliverableData': scheduleDeliverableData},
            response_cls=ServiceData,
        )
