from __future__ import annotations

from tcsoa.gen.Ai._2009_10.Ai import GetPropertyValuesData, GetPropertyValuesResponse
from typing import List
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def getPropertyValues(cls, input: List[GetPropertyValuesData]) -> GetPropertyValuesResponse:
        """
        get the property values for the object supplied as ApplicationReferences and configuration.
        """
        return cls.execute_soa_method(
            method_name='getPropertyValues',
            library='Ai',
            service_date='2009_10',
            service_name='Ai',
            params={'input': input},
            response_cls=GetPropertyValuesResponse,
        )
