from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import VerificationRule
from dataclasses import dataclass


@dataclass
class GetVerificationRulesResponse(TcBaseObj):
    """
    The response information returned by getVerificationRules.
    
    :var serviceData: The ServiceData object  which contains generic information like error number and error
    information.
    :var outputs: The list of VerificationRule objects information.
    """
    serviceData: ServiceData = None
    outputs: List[VerificationRulesInfo] = ()


@dataclass
class VerificationRuleInput(TcBaseObj):
    """
    The criteria to get VerificationRule objects.
    
    :var functionality: The desired value of the functionality property of the VerificationRule objects.
    :var conditionName: The desired value of the condition_reference property of the VerificationRule objects.
    :var typeName: The desired value (business object type name) of the type property of the VerificationRule objects.
    :var subGroup: The desired value of the subGroup property of the VerificationRule objects. It should be the value
    of LOV in subGroupLOV  property of FunctionalityRule object associated with the VerificationRule object.
    """
    functionality: str = ''
    conditionName: str = ''
    typeName: str = ''
    subGroup: str = ''


@dataclass
class VerificationRulesInfo(TcBaseObj):
    """
    The returned VerificationRule objects and it associated VerificationRuleInput index.
    
    :var index: The index of VerificationRuleInput in parameter vector that this list of rules is associated with.
    :var verificationRules: The list of VerificationRule objects which match the desired criteria.
    """
    index: int = 0
    verificationRules: List[VerificationRule] = ()
