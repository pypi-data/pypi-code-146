from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import TimeSheetEntry


class ScheduleManagementService(TcService):

    @classmethod
    def submitTimesheetEntries(cls, timesheetEntries: List[TimeSheetEntry], runInBackground: bool) -> ServiceData:
        """
        This operation submits the list of TimeSheetEntry to workflow. The preference SM_TIMESHEET_APPROVE_WORKFLOW
        will be used to determine the workflow template. If not specified, TimeSheetApproval template will be used.
        """
        return cls.execute_soa_method(
            method_name='submitTimesheetEntries',
            library='ProjectManagement',
            service_date='2018_11',
            service_name='ScheduleManagement',
            params={'timesheetEntries': timesheetEntries, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def submitTimesheetEntriesAsync(cls, timesheetEntries: List[TimeSheetEntry]) -> None:
        """
        This operation submits the list of TimeSheetEntry to workflow. The preference SM_TIMESHEET_APPROVE_WORKFLOW
        will be used to determine the workflow template. If not specified, TimeSheetApproval template will be used.
        This operation runs asynchronously in its own server in the background.
        """
        return cls.execute_soa_method(
            method_name='submitTimesheetEntriesAsync',
            library='ProjectManagement',
            service_date='2018_11',
            service_name='ScheduleManagement',
            params={'timesheetEntries': timesheetEntries},
            response_cls=None,
        )
