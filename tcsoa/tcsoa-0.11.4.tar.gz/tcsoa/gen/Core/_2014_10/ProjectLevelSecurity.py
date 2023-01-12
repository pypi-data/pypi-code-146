from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0PropagationRule
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PropagateDataElement(TcBaseObj):
    """
    Input structure for propagateData service operation.
    Structure contains operation type, source object and the applicable propagation rules.
    
    :var operationType: The operation type. The following are integers legal values against the name of the operation
    - 1     Check-In 
    - 2     Check-Out
    - 3     Create
    - 4     Delete
    - 5     Export
    - 6     Import
    - 7     Revise
    - 8     Save
    - 9     Save As
    - 10     All
    
    
    :var sourceObject: Source object to propagate data from. It can be any business object.
    :var propagationRulesInfo: A List of rules and source objects.
    """
    operationType: int = 0
    sourceObject: BusinessObject = None
    propagationRulesInfo: List[DataToPropagate] = ()


@dataclass
class DataToPropagate(TcBaseObj):
    """
    Structure contains the applicable propagation rules for propagating data and the associated workspace object.
    This structure is one of the elements of propagateDataElement structure, which is the input structure to
    propagateData service operation.
    
    :var applicablePropagationRules: A list of propagation rules objects. Valid value are Fnd0PropagationRule business
    object types. 
    :var associatedObject: Associated source object. It can be any business object.
    """
    applicablePropagationRules: List[Fnd0PropagationRule] = ()
    associatedObject: BusinessObject = None
