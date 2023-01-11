from __future__ import annotations

from typing import List
from tcsoa.gen.ProjectManagementAw._2020_05.ScheduleManagementAw import ResourceChartResponse, NameValueStringPair
from tcsoa.gen.BusinessObjects import Schedule, WorkspaceObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from datetime import datetime


class ScheduleManagementAwService(TcService):

    @classmethod
    def shiftSchedules(cls, scheduleUIDs: List[str], shiftByDays: int, shiftByDate: datetime, runInBackground: bool) -> ServiceData:
        """
        Shifts the given list of Schedule objects to a new date based on the given number of days or date. In case of
        background mode, this operation files an asynchronous request to shift the Schedule and releases the client
        immediately so that the user can perform other operation.
        """
        return cls.execute_soa_method(
            method_name='shiftSchedules',
            library='ProjectManagementAw',
            service_date='2020_05',
            service_name='ScheduleManagementAw',
            params={'scheduleUIDs': scheduleUIDs, 'shiftByDays': shiftByDays, 'shiftByDate': shiftByDate, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def shiftSchedulesAsync(cls, scheduleUIDs: List[str], shiftByDays: int, shiftByDate: datetime) -> None:
        """
        Shifts the given list of Schedule objects to a new date based on the given number of days or date. This
        operation runs asynchronously in its own server in the background.
        """
        return cls.execute_soa_method(
            method_name='shiftSchedulesAsync',
            library='ProjectManagementAw',
            service_date='2020_05',
            service_name='ScheduleManagementAw',
            params={'scheduleUIDs': scheduleUIDs, 'shiftByDays': shiftByDays, 'shiftByDate': shiftByDate},
            response_cls=None,
        )

    @classmethod
    def getResourceChartInfo(cls, resources: List[str], assignedObjects: List[WorkspaceObject], startDate: datetime, endDate: datetime, schedulesToInclude: List[Schedule], loadOptions: List[NameValueStringPair]) -> ResourceChartResponse:
        """
        The operation returns the resource chart information for the given resources assigned to the context objects.
        The resource load will be calculated for the date range between the given start and finish dates. The
        schedulesToInclude specifies the list of Schedule objects to be considered for calculating the resource chart
        information.
        """
        return cls.execute_soa_method(
            method_name='getResourceChartInfo',
            library='ProjectManagementAw',
            service_date='2020_05',
            service_name='ScheduleManagementAw',
            params={'resources': resources, 'assignedObjects': assignedObjects, 'startDate': startDate, 'endDate': endDate, 'schedulesToInclude': schedulesToInclude, 'loadOptions': loadOptions},
            response_cls=ResourceChartResponse,
        )
