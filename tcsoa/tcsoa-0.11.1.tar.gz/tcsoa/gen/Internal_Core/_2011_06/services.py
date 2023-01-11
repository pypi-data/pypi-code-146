from __future__ import annotations

from tcsoa.gen.Internal.Core._2011_06.ICT import InvokeICTMethodResponse, Arg
from typing import List
from tcsoa.base import TcService


class ICTService(TcService):

    @classmethod
    def invokeICTMethod(cls, className: str, methodName: str, args: List[Arg]) -> InvokeICTMethodResponse:
        """
        Invoke ICT method.
        """
        return cls.execute_soa_method(
            method_name='invokeICTMethod',
            library='Internal-Core',
            service_date='2011_06',
            service_name='ICT',
            params={'className': className, 'methodName': methodName, 'args': args},
            response_cls=InvokeICTMethodResponse,
        )
