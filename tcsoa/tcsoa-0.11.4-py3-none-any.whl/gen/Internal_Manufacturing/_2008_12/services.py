from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Manufacturing._2008_12.Core import CheckoutInput, CheckinInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class CoreService(TcService):

    @classmethod
    def checkinForProcessSimulate(cls, rootLines: List[BusinessObject], params: CheckinInput) -> ServiceData:
        """
        The service checkins entire structures under the roots and the parameters given.
        """
        return cls.execute_soa_method(
            method_name='checkinForProcessSimulate',
            library='Internal-Manufacturing',
            service_date='2008_12',
            service_name='Core',
            params={'rootLines': rootLines, 'params': params},
            response_cls=ServiceData,
        )

    @classmethod
    def checkoutForProcessSimulate(cls, rootLines: List[BusinessObject], params: CheckoutInput) -> ServiceData:
        """
        The service checkouts entire structures under the roots and the parameters given.
        """
        return cls.execute_soa_method(
            method_name='checkoutForProcessSimulate',
            library='Internal-Manufacturing',
            service_date='2008_12',
            service_name='Core',
            params={'rootLines': rootLines, 'params': params},
            response_cls=ServiceData,
        )
