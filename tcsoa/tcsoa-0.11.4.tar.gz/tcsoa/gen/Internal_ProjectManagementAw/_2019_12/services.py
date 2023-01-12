from __future__ import annotations

from tcsoa.gen.Internal.ProjectManagementAw._2019_12.ScheduleManagementAw import ProgramViewInfo, ManageProgramViewResponse
from tcsoa.base import TcService


class ScheduleManagementAwService(TcService):

    @classmethod
    def manageProgramView(cls, programViewInfo: ProgramViewInfo) -> ManageProgramViewResponse:
        """
        Manages a ProgramView object based on the information provided in the ProgramViewInfo. This operation can
        create, configure and save a ProgramView object. You can also load the ProgramView by filtering and grouping
        ScheduleTask objects based on the ProgramView configuration. The ProgramView configuration contains the list of
        Schedule UIDs, filters and groups.
        """
        return cls.execute_soa_method(
            method_name='manageProgramView',
            library='Internal-ProjectManagementAw',
            service_date='2019_12',
            service_name='ScheduleManagementAw',
            params={'programViewInfo': programViewInfo},
            response_cls=ManageProgramViewResponse,
        )
