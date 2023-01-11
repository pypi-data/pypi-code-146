from __future__ import annotations

from tcsoa.gen.BusinessObjects import Schedule
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.ProjectManagement._2017_11.ScheduleManagement import WhatIfAnalysisOption


class ScheduleManagementService(TcService):

    @classmethod
    def whatIfAnalysis(cls, schedule: Schedule, whatIfOption: WhatIfAnalysisOption) -> ServiceData:
        """
        This operation allows the user to perform What-If analysis on a Schedule by making scheduling changes locally
        without affecting other users and save or cancel the changes made during the What-If analysis.
        
        Only the following operations can be performed by the user who has started the What-If analysis:
        1. Modify all properties of the Schedule. 
        2. Modify all properties of the ScheduleTask other than the following execution proeprties : status, work
        complete, complete percent, actual start date, actual finish date, work remaining.
        3. Create, delete and update ScheduleTask, ResourceAssignment, TaskDependency, and Fnd0ProxyTask objects.
        
        The following operations cannot be performed by the user who has started the What-If analysis:
        1. Modify the following execution properties of the ScheduleTask : status, work complete, complete percent,
        actual start date, actual finish date, work remaining.
        2. Insert Schedule and detach Schedule operations.
        
        Only the following operations can be performed by other users when a Schedule is in What-If analysis mode:
        1. Modify the following execution properties of the ScheduleTask : status, work complete, complete percent,
        actual start date, actual finish date, work remaining.
        """
        return cls.execute_soa_method(
            method_name='whatIfAnalysis',
            library='ProjectManagement',
            service_date='2017_11',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'whatIfOption': whatIfOption},
            response_cls=ServiceData,
        )
