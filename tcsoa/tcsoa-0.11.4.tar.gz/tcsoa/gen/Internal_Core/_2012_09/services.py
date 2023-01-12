from __future__ import annotations

from tcsoa.gen.Internal.Core._2012_09.Envelope import EmailInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class EnvelopeService(TcService):

    @classmethod
    def sendEmail(cls, emailinfos: List[EmailInfo]) -> ServiceData:
        """
        This operation sends email for each EmailInfo supplied. EmailInfo structure contains the email information such
        as the subject, message body, list of external and internal Teamcenter recipients, and FMS read tickets for the
        file attachments. File attachments are retrieved from FMS using the given FMS read tickets.
        """
        return cls.execute_soa_method(
            method_name='sendEmail',
            library='Internal-Core',
            service_date='2012_09',
            service_name='Envelope',
            params={'emailinfos': emailinfos},
            response_cls=ServiceData,
        )
