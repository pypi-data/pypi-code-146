from __future__ import annotations

from tcsoa.base import TcService
from tcsoa.gen.Internal.ProjectManagement._2010_04.ScheduleManagement import TranslationDataContainer


class ScheduleManagementService(TcService):

    @classmethod
    def translateFour(cls, scheduleUid: str) -> TranslationDataContainer:
        """
        Translation Data Container
        """
        return cls.execute_soa_method(
            method_name='translateFour',
            library='Internal-ProjectManagement',
            service_date='2010_04',
            service_name='ScheduleManagement',
            params={'scheduleUid': scheduleUid},
            response_cls=TranslationDataContainer,
        )
