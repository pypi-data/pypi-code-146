from __future__ import annotations

from tcsoa.gen.ConfigFilterCriteria._2011_06.EffectivityManagement import ConfigExpression
from typing import List
from tcsoa.gen.BusinessObjects import POM_object
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class EffectivityConditionInfo(TcBaseObj):
    """
    This structure provides input data for the operation such as the list of the objects which are affected and the
    effectivity expressions to be processed.
    
    :var targetObjects: A list of all affected business objects on which effectivity is to be set. Any POM_object or
    subtype supporting effectivity behavior is the valid input for this parameter.
    :var expression: The effectivity expression that should be set on the affected objects. Effectivity is set using
    either ConfigFormula, nested ConfigExpressions or EffectivityTableRow in this structure
    """
    targetObjects: List[POM_object] = ()
    expression: ConfigExpression = None


@dataclass
class EffectivityConditionSource(TcBaseObj):
    """
    This structure contains sourceObject and sourceExpression for which the effectivity is to be obtained.
    
    :var sourceObject: The business object which should be used to extract the effectivity expression. Any POM_object
    or  subtype supporting effectivity behavior is the valid input for this parameter.
    :var sourceExpression: This is ConfigExpression contains effectivity expression that should be used as source
    effectivity expression to process. When both fields are populated, sourceObject will be used and sourceExpression
    will be ignored.
    """
    sourceObject: POM_object = None
    sourceExpression: ConfigExpression = None
