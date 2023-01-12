from __future__ import annotations

from tcsoa.gen.ProjectManagement._2007_01.ScheduleManagement import CreateBaselineContainer
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def createNewBaselines(cls, createBaselineContainer: List[CreateBaselineContainer], runInBackground: bool) -> ServiceData:
        """
        This operation creates new schedule baselines. In case of background mode, this operation files an asynchronous
        request to create the baselines and releases the client immediately so that the user can perform other
        operation.
        """
        return cls.execute_soa_method(
            method_name='createNewBaselines',
            library='ProjectManagement',
            service_date='2016_04',
            service_name='ScheduleManagement',
            params={'createBaselineContainer': createBaselineContainer, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def createNewBaselinesAsync(cls, createBaselineContainer: List[CreateBaselineContainer]) -> None:
        """
        This operation creates new 'schedule' baselines. This operation runs asynchronously in its own server in the
        background.
        """
        return cls.execute_soa_method(
            method_name='createNewBaselinesAsync',
            library='ProjectManagement',
            service_date='2016_04',
            service_name='ScheduleManagement',
            params={'createBaselineContainer': createBaselineContainer},
            response_cls=None,
        )
