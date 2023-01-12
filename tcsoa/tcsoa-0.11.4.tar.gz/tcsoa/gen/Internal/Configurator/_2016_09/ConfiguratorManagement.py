from __future__ import annotations

from tcsoa.gen.Internal.Configurator._2015_10.ConfiguratorManagement import BusinessObjectConfigExpression, ConfigExpressionTerm
from tcsoa.gen.BusinessObjects import Cfg0AbsFamily, Cfg0ConfiguratorPerspective
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AvailabilityInput(TcBaseObj):
    """
    It is the object containing input information required to compute the availability.
    
    :var criteriaExpression: A list of structures each relating a business object to a set of configuration expressions.
    For the details of the structure BusinessObjectConfigExpression please refer to
    Cfg0::Soa::Internal::Configurator::_2015_10::ConfiguratorManagement:: BusinessObjectConfigExpression
    :var familiesToTest: The list of configuration families (Cfg0AbsFamily) for which available features are requested.
    :var valuesToTest: The list of Configuration Expression Terms (ConfigExpressionTerm) whose availability is to be
    calculated.
    :var perspective: Configurator perspective details.
    Property cfg0ProductItems of perspective must contain reference to a single Configurator context item and property
    cfg0RevisonRule must be set to a RevisionRule
    :var applyConstraints: Defines the mode to apply the constraints. The value is a bitwise OR the following values: 
    0: disable configurator constraint evaluation 
    1: enable configurator constraint evaluation 
    512:  get available features for each family individually after resetting the config expression for the inquired
    family
    2048: enable Availability Constraint evaluation.
    """
    criteriaExpression: List[BusinessObjectConfigExpression] = ()
    familiesToTest: List[Cfg0AbsFamily] = ()
    valuesToTest: List[ConfigExpressionTerm] = ()
    perspective: Cfg0ConfiguratorPerspective = None
    applyConstraints: int = 0


@dataclass
class AvailabilityOutput(TcBaseObj):
    """
    An object containing input information required to represent avialability of features for models.
    
    :var availabilityStruct: A list of list containing AvailableFamilyVariabilityStruct. This represents availability
    records for all the models in the input. The entry corresponds to the input by index.
    :var serviceData: The service data for errors and returned objects.
    """
    availabilityStruct: List[AvailableFamilyVariabilityStruct] = ()
    serviceData: ServiceData = None


@dataclass
class AvailableFamilyVariability(TcBaseObj):
    """
    Defines the availability status of option values from the given family input for the operation
    getOptionValueAvailability.
    
    :var availability: Specifies the list of configuration expression terms referencing available features from the
    requested family.
    :var availibilityStatus: A string representing the availability status of the feature. Presently three values are
    supported
    - Available
    - Not Available
    - Not Editable
    
    """
    availability: List[ConfigExpressionTerm] = ()
    availibilityStatus: List[str] = ()


@dataclass
class AvailableFamilyVariabilityStruct(TcBaseObj):
    """
    Represents availability for features for a single model.
    
    :var availabilityExpressions: List of family variability, each element represents variability of features form a
    single family
    """
    availabilityExpressions: List[AvailableFamilyVariability] = ()
