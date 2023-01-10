from __future__ import annotations

from tcsoa.gen.Internal.Ai._2016_03.Ai import GetAITypesResponse
from typing import List
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def getApplicationInterfaceTypes(cls, specificTypeNames: List[str]) -> GetAITypesResponse:
        """
        This operation returns all  the AppInterfaceType objects in the system. If specific names are provided in the
        input, then only the matching AppInterfaceType objects are returned.
        """
        return cls.execute_soa_method(
            method_name='getApplicationInterfaceTypes',
            library='Internal-Ai',
            service_date='2016_03',
            service_name='Ai',
            params={'specificTypeNames': specificTypeNames},
            response_cls=GetAITypesResponse,
        )
