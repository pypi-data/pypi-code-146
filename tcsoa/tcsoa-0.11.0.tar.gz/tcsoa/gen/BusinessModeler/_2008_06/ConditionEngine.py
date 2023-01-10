from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ConditionInput(TcBaseObj):
    """
    Holds the name of the condition to be evaluated along with the set of input parameter business object values.
    
    :var conditionName: This is the name of the condition to be evaluated.
    :var conditionSignature: This is set of condition parameters (tag_t) required by the specified condition name.
    """
    conditionName: str = ''
    conditionSignature: List[BusinessObject] = ()


@dataclass
class ConditionOutput(TcBaseObj):
    """
    Holds the results of a condition evaluation along with any exit code that was captured during the condition
    evaluation.
    
    :var result: This is the result of the rules engine evaluation (True or False).
    :var exitCode: This is the exit code (zero for success or non zero indicating an error) captured during the
    condition evaluation.
    """
    result: bool = False
    exitCode: int = 0


@dataclass
class EvaluateConditionsResponse(TcBaseObj):
    """
    Holds the response for the 'evaluateConditions' operation.
    
    :var outputs: This is a set of condition evaluation results from the rules engine execution.
    :var serviceData: This contains the status of the operation.
    """
    outputs: List[ConditionOutput] = ()
    serviceData: ServiceData = None
