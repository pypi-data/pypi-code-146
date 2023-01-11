from __future__ import annotations

from tcsoa.base import TcService
from tcsoa.gen.Internal.ProjectManagement._2009_10.ScheduleManagement import TranslatorResponseScheduleModifyContainer, TranslatorResponseContainer, TranslationDataContainer


class ScheduleManagementService(TcService):

    @classmethod
    def translateOne(cls, scheduleUid: str) -> TranslatorResponseContainer:
        """
        this is a non functional internal soa that would never be called. It is a tagging method for
        TranslatorResponseContainer structure which is used internally to transfer objects between C++ and Java codes.
        """
        return cls.execute_soa_method(
            method_name='translateOne',
            library='Internal-ProjectManagement',
            service_date='2009_10',
            service_name='ScheduleManagement',
            params={'scheduleUid': scheduleUid},
            response_cls=TranslatorResponseContainer,
        )

    @classmethod
    def translateThree(cls, scheduleUid: str) -> TranslationDataContainer:
        """
        Dummy  internal operation
        """
        return cls.execute_soa_method(
            method_name='translateThree',
            library='Internal-ProjectManagement',
            service_date='2009_10',
            service_name='ScheduleManagement',
            params={'scheduleUid': scheduleUid},
            response_cls=TranslationDataContainer,
        )

    @classmethod
    def translateTwo(cls, scheduleUid: str) -> TranslatorResponseScheduleModifyContainer:
        """
        this is a non functional internal soa that would never be called. It is a tagging method for 
        TranslatorResponseScheduleModifyContainer structure which is used internally to transfer objects between C++
        and Java codes.
        Without the tagging the soa generate command would fail.
        """
        return cls.execute_soa_method(
            method_name='translateTwo',
            library='Internal-ProjectManagement',
            service_date='2009_10',
            service_name='ScheduleManagement',
            params={'scheduleUid': scheduleUid},
            response_cls=TranslatorResponseScheduleModifyContainer,
        )
