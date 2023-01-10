from __future__ import annotations

from typing import List
from tcsoa.gen.ProjectManagementAw._2017_06.ScheduleManagementAw import MasterScheduleCreateInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementAwService(TcService):

    @classmethod
    def createMasterSchedule(cls, createMasterInputs: List[MasterScheduleCreateInput], runInBackground: bool) -> ServiceData:
        """
        This operation creates new master Schedule and inserts one or more Schedule objects specified in the input,into
        a master Schedule. The information needed to create the master Schedule is specified in the
        MasterScheduleCreateInput structure. In case of background mode,this operation files an asynchronous request to
        create master Schedule and releases the client immediately so that the user can perform other operation.
        """
        return cls.execute_soa_method(
            method_name='createMasterSchedule',
            library='ProjectManagementAw',
            service_date='2017_06',
            service_name='ScheduleManagementAw',
            params={'createMasterInputs': createMasterInputs, 'runInBackground': runInBackground},
            response_cls=ServiceData,
        )

    @classmethod
    def createMasterScheduleAsync(cls, createMasterInputs: List[MasterScheduleCreateInput]) -> None:
        """
        This operation creates new master Schedule and inserts one or more Schedule objects specified in the input,
        into a master Schedule. The information needed to create the master Schedule is specified in the
        MasterScheduleCreateInput structure. This operation runs asynchronously in its own server in the background.
        """
        return cls.execute_soa_method(
            method_name='createMasterScheduleAsync',
            library='ProjectManagementAw',
            service_date='2017_06',
            service_name='ScheduleManagementAw',
            params={'createMasterInputs': createMasterInputs},
            response_cls=None,
        )
