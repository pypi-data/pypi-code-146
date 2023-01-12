from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Cfg0ConfiguratorPerspective
from tcsoa.gen.Internal.Configurator._2015_10.ConfiguratorManagement import BusinessObjectConfigExpression
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConfigurationProfile(TcBaseObj):
    """
    Structure consisting maps of different primitive types.
    Following are the Configuration Profile keys that can be passed:
    - applyConfigConstraints  - Boolean - Enables configurator constraint evaluation in the solve operation.
    - applyDefaults - Boolean - Enables configurator default rules evaluation in the solve operation.
    - intentFilterInclude - List of Strings - The list of configurator Intents which should participate in the solve
    operation.
    - intentFilterExclude - List of Strings - The list of configurator Intents which should be ignored in the solve
    operation.
    - violationComputationTimeout - Integer - Indicates the max time in seconds that should be spent in violations
    computation.
    - minReportSeverity - Integer - Indicates the minimum report severity to be evaluated for validation failures.
    - minErrorSeverity - Integer - Indicates the minimum error severity to be evaluated for validation failures.
    - computeAllProblems - Boolean - Enables computation of all the problems of the unsat core while reporting
    violations.
    - minimizeProblem - Boolean - Decides if minimization of computed essential violation is required.
    
    
    
    :var intMap: Map (string/list of ints) of configuration Profile preferences of Integer type.
    :var boolMap: Map (string/list of booleans) of configuration Profile preferences of Boolean type.
    :var stringMap: Map (string/list of strings) of configuration Profile preferences of String type.
    :var doubleMap: Map (string/list of doubles) of configuration Profile preferences of Double type.
    :var objectMap: Map (string/list of business objects) of configuration Profile preferences of Business Object type.
    :var dateMap: Map (string/list of dates) of configuration Profile preferences of Date type.
    """
    intMap: IntVectorMap2 = None
    boolMap: BoolVectorMap2 = None
    stringMap: StringVectorMap2 = None
    doubleMap: DoubleVectorMap2 = None
    objectMap: ObjectVectorMap2 = None
    dateMap: DateVectorMap2 = None


@dataclass
class ConfigurationSessionInfoInput(TcBaseObj):
    """
    An input structure containing list of configurator perspective object, configuration profile map and a vector of
    variant rule objects.
    
    :var perspective: The Cfg0ConfiguratorPerspective instance which provides the RevisionRule and the Configurator
    Context.
    :var configProfile: The Configuration Profile information required for Configurator Solver.
    :var targetObjects: A list of target objects on which the Configuration Profile information needs to be set.
    """
    perspective: Cfg0ConfiguratorPerspective = None
    configProfile: ConfigurationProfile = None
    targetObjects: List[BusinessObject] = ()


@dataclass
class GetContextBasedVariantExprsResponse(TcBaseObj):
    """
    The response structure for operation getContextBasedVariantExpressions.
    
    :var configObjectExpressions: A list of structures each relating a business object to a set of configuration
    expressions.
    :var serviceData: Teamcenter service data.
    """
    configObjectExpressions: List[BusinessObjectConfigExpression] = ()
    serviceData: ServiceData = None


"""
Map of String to List of Integer values.
"""
IntVectorMap2 = Dict[str, List[int]]


"""
Map of String to List of BO values.
"""
ObjectVectorMap2 = Dict[str, List[BusinessObject]]


"""
Map of String to List of Boolean values.
"""
BoolVectorMap2 = Dict[str, List[bool]]


"""
Map of String to List of String values.
"""
StringVectorMap2 = Dict[str, List[str]]


"""
Map of String to List of DateTime values.
"""
DateVectorMap2 = Dict[str, List[datetime]]


"""
Map of String to List of Double values.
"""
DoubleVectorMap2 = Dict[str, List[float]]
