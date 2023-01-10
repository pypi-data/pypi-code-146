from __future__ import annotations

from tcsoa.gen.ProjectManagement._2011_02.ScheduleManagement import MultiSchSpecialCopyResponse, SpecialCopyContainer
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def specialPasteScheduleTasks(cls, copyContainer: SpecialCopyContainer) -> MultiSchSpecialCopyResponse:
        """
        Gets the selected Schedule and their tasks and paste it to target task as specified by the options
        """
        return cls.execute_soa_method(
            method_name='specialPasteScheduleTasks',
            library='ProjectManagement',
            service_date='2011_02',
            service_name='ScheduleManagement',
            params={'copyContainer': copyContainer},
            response_cls=MultiSchSpecialCopyResponse,
        )
