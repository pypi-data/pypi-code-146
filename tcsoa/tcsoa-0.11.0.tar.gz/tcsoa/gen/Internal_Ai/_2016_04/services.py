from __future__ import annotations

from tcsoa.gen.Internal.Ai._2016_04.Ai import InvokeResponse
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def invoke2(cls, methodName: str, xmlIn: str) -> InvokeResponse:
        """
        This operation is for backward compatibility with existing NX clients that use this method to call custom PDI
        functions. This method will return InvokeResponse structure containing plain objects that are also returned as
        part of formatted XML. These plain objects can be used by test framework for tracking purposes.
        
        Exceptions:
        >Thrown on service failure. The exception can result from calls to more than 400 PDI APIs and depends on case
        to case basis.
        """
        return cls.execute_soa_method(
            method_name='invoke2',
            library='Internal-Ai',
            service_date='2016_04',
            service_name='Ai',
            params={'methodName': methodName, 'xmlIn': xmlIn},
            response_cls=InvokeResponse,
        )
