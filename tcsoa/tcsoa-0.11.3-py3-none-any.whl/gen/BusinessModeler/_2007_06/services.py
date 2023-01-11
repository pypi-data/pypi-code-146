from __future__ import annotations

from tcsoa.gen.BusinessModeler._2007_06.RulesBasedFramework import RbfNameValue, ExecuteRbfRulesResponse
from tcsoa.gen.BusinessModeler._2007_06.Constants import TypeConstantKey, TypeConstantValueResponse, PropertyConstantValueResponse, GlobalConstantValueResponse, PropertyConstantKey
from typing import List
from tcsoa.base import TcService


class ConstantsService(TcService):

    @classmethod
    def getPropertyConstantValues(cls, keys: List[PropertyConstantKey]) -> PropertyConstantValueResponse:
        """
        This operation gets the values of the named property constants ('keys').
        """
        return cls.execute_soa_method(
            method_name='getPropertyConstantValues',
            library='BusinessModeler',
            service_date='2007_06',
            service_name='Constants',
            params={'keys': keys},
            response_cls=PropertyConstantValueResponse,
        )

    @classmethod
    def getTypeConstantValues(cls, keys: List[TypeConstantKey]) -> TypeConstantValueResponse:
        """
        This operation gets the values of the named type constants ('keys').
        """
        return cls.execute_soa_method(
            method_name='getTypeConstantValues',
            library='BusinessModeler',
            service_date='2007_06',
            service_name='Constants',
            params={'keys': keys},
            response_cls=TypeConstantValueResponse,
        )

    @classmethod
    def getGlobalConstantValues(cls, keys: List[str]) -> GlobalConstantValueResponse:
        """
        Global constants provide consistent definitions that can be used throughout the system. These constants have
        one or multiple values.  User can retrieve the values of global constants to determine the system behavior
        based on values. This operation gets the values of the named global constants ('keys'). This operation only
        supports single valued global constants, for multivalued constants use the 'getGlobalConstantValues2' operation.
        """
        return cls.execute_soa_method(
            method_name='getGlobalConstantValues',
            library='BusinessModeler',
            service_date='2007_06',
            service_name='Constants',
            params={'keys': keys},
            response_cls=GlobalConstantValueResponse,
        )


class RulesBasedFrameworkService(TcService):

    @classmethod
    def executeRbfRules(cls, id: str, inputs: List[RbfNameValue]) -> ExecuteRbfRulesResponse:
        """
        This operation invokes the CLIPS rules engine to apply the set of application extension rules that belong to
        the specified application extension point for the specified input name/value pairs.  The result of the
        execution is returned in the output name/value pairs.
        """
        return cls.execute_soa_method(
            method_name='executeRbfRules',
            library='BusinessModeler',
            service_date='2007_06',
            service_name='RulesBasedFramework',
            params={'id': id, 'inputs': inputs},
            response_cls=ExecuteRbfRulesResponse,
        )
