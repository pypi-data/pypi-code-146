from __future__ import annotations

from tcsoa.gen.Internal.Configurator._2014_06.ConfiguratorManagement import ConfigExpression, BusinessObjectConfigExpression, ConfigExpressionTerm, Violation
from tcsoa.gen.BusinessObjects import Cfg0AbsFamily, Cfg0ConfiguratorPerspective
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AvailableProductVariabilityOutput(TcBaseObj):
    """
    The response structure returned by getAvailableProductVariability.
    
    :var availabilityExpressions: A list of AvailableVariability expressions defining available variability. The number
    of elements in this list corresponds to the number of available values in the input families (parameter
    familiesToTest). If an empty familiesToTest list was specified this vector would be empty.
    :var voilations: A list of constraints that were violated for a given user selected values/input expression.
    :var suggestedSatisfyingExpr: A sample expression satisfying the given input expression and existing set of
    constraint in the configurator context. This is an output expression containing system suggested features from the
    available features.
    :var serviceData: The service data for errors and returned objects.
    """
    availabilityExpressions: List[AvailableVariability] = ()
    voilations: List[Violation] = ()
    suggestedSatisfyingExpr: ConfigExpression = None
    serviceData: ServiceData = None


@dataclass
class AvailableVariability(TcBaseObj):
    """
    Defines available features for a given family along with the default value for operation
    getAvailableProductVariability. The AvailableVariability structure is interpreted as "NULL" if it has the following
    values set for its parameters: 
    defaultValue: NULL structure
    availability: empty list
    
    :var defaultValue: Specifies the configuration expression term default value. If no default rules exist, or they
    select a default value such that it is ruled out due to other constraints, this will be an empty
    ConfigExpressionTerm object to indicate a non-existing default value.
    :var availability: The list of configuration expressions referencing values only from the requested families. This
    is a list of discrete values or ranges.
    """
    defaultValue: ConfigExpressionTerm = None
    availability: List[ConfigExpressionTerm] = ()


@dataclass
class AvailableProductVariabilityInput(TcBaseObj):
    """
    It is the object containing input information required to compute the available product variability.
    
    :var criteriaExpression: The input criteria expression for which the available product variability is to be
    calculated.
    :var familiesToTest: The list of configuration families of which available values are requested. 
    :var context: Configurator context details. 
    :var applyConstraints: How to apply the constraints. The action is a bitwise OR the following values: 
    0: disable configurator constraint evaluation 
    1: enable configurator constraint evaluation 
    2: skip constraints if they only reference unset families 
    4: skip constraints that don't reference all configExpression families 
    8: report warnings in addition to errors 
    16: report informational messages 
    32: don't stop if a violation is encountered (use with care) 
    64: treat constraints with warning severity as if they had error severity.
    
    1024: skip criteria update based on validation rules (For example configurator exclusion rule). If this flag is not
    set then the operation will update the variant criteria after applying validation rules.
    
    2048: enable Availability Constraint evaluation. 
    """
    criteriaExpression: BusinessObjectConfigExpression = None
    familiesToTest: List[Cfg0AbsFamily] = ()
    context: Cfg0ConfiguratorPerspective = None
    applyConstraints: int = 0
