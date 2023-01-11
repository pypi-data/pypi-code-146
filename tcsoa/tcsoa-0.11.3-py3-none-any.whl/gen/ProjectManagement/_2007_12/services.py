from __future__ import annotations

from tcsoa.gen.ProjectManagement._2007_12.ScheduleManagement import DemandProfileRequest, DemandProfileResponses
from typing import List
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def getDemandProfile(cls, requests: List[DemandProfileRequest]) -> DemandProfileResponses:
        """
        Calculates the demand profile data for a schedule based on the initial
        input request to the Application Interface..
        """
        return cls.execute_soa_method(
            method_name='getDemandProfile',
            library='ProjectManagement',
            service_date='2007_12',
            service_name='ScheduleManagement',
            params={'requests': requests},
            response_cls=DemandProfileResponses,
        )
