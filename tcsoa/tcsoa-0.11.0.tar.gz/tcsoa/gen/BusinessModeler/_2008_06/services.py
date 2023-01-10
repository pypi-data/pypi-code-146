from __future__ import annotations

from tcsoa.gen.BusinessModeler._2008_06.ConditionEngine import EvaluateConditionsResponse, ConditionInput
from tcsoa.gen.BusinessModeler._2008_06.DeepCopyRules import DeepCopyInfoResponse, DeepCopyInfoKey
from typing import List
from tcsoa.base import TcService


class ConditionEngineService(TcService):

    @classmethod
    def evaluateConditions(cls, inputs: List[ConditionInput]) -> EvaluateConditionsResponse:
        """
        This operation tells the CLIPS rules engine to evaluate the expression defined on the specified Condition using
        the specified input parameter(s) defined on the ConditionParameter.  This operation takes as input a set of
        conditions along with parameters for each condition and returns a set of outputs containing the result
        (true/false) and exit code of each condition evaluation. There is a one to one correspondence between the
        elements in the input set and the elements in the output set.  This allows for evaluation of multiple
        conditions in one operation call.
        """
        return cls.execute_soa_method(
            method_name='evaluateConditions',
            library='BusinessModeler',
            service_date='2008_06',
            service_name='ConditionEngine',
            params={'inputs': inputs},
            response_cls=EvaluateConditionsResponse,
        )


class DeepCopyRulesService(TcService):

    @classmethod
    def getDeepCopyInfo(cls, keys: List[DeepCopyInfoKey]) -> DeepCopyInfoResponse:
        """
        Deep copy rules define whether objects belonging to a business object instance can be copied when a user
        performs a save as or revise operation on that instance. Deep copy rules can be applied to any business object
        type, and are inherited by children business object types. This operation gets the applicable deep copy rules
        for the given list of objects and the operation specified for each object.
        """
        return cls.execute_soa_method(
            method_name='getDeepCopyInfo',
            library='BusinessModeler',
            service_date='2008_06',
            service_name='DeepCopyRules',
            params={'keys': keys},
            response_cls=DeepCopyInfoResponse,
        )
