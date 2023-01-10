from __future__ import annotations

from tcsoa.gen.BusinessModeler._2011_06.Constants import GlobalConstantValueResponse2
from typing import List
from tcsoa.base import TcService


class ConstantsService(TcService):

    @classmethod
    def getGlobalConstantValues2(cls, keys: List[str]) -> GlobalConstantValueResponse2:
        """
        Global constants provide consistent definitions that can be used throughout the system. These constants have
        one or multiple values.  User can retrieve the values of global constants to determine the system behavior
        based on values. This operation gets the values of the named global constants ('keys'). This operation supports
        single value and multi valued global constants. This operation replaces deprecated operation
        'getGlobalConstantValues'.
        """
        return cls.execute_soa_method(
            method_name='getGlobalConstantValues2',
            library='BusinessModeler',
            service_date='2011_06',
            service_name='Constants',
            params={'keys': keys},
            response_cls=GlobalConstantValueResponse2,
        )
