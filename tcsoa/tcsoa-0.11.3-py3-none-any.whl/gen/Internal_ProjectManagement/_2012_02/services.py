from __future__ import annotations

from tcsoa.base import TcService
from tcsoa.gen.Internal.ProjectManagement._2012_02.ScheduleManagement import TranslatorResponseScheduleModifyContainer


class ScheduleManagementService(TcService):

    @classmethod
    def translateFive(cls, scheduleUid: str) -> TranslatorResponseScheduleModifyContainer:
        """
        this is a non functional internal soa that would never be called. It is a tagging
        method for  translatorResponseScheduleModifyContainer structure which is used internally
        to transfer objects between C++ and Java codes. Without the tagging the soa generate
         command would fail.
        """
        return cls.execute_soa_method(
            method_name='translateFive',
            library='Internal-ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'scheduleUid': scheduleUid},
            response_cls=TranslatorResponseScheduleModifyContainer,
        )
