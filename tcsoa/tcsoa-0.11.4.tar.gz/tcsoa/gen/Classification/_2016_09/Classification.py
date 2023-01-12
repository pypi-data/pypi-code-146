from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindValueInput(TcBaseObj):
    """
    Structure containing the additional criteria value(s) and unit systems which should be used to find the values for
    a certain attribute.
    
    :var attributeID: The attribute ID to find the values for.
    :var classID: The unique ID of the classification class in which to search (can be empty to find all values in all
    classes).
    :var searchInBothUnitSystems: Indicates to search for values stored in both unit systems. True to find the values
    stored in both the unit system, false otherwise.
    :var activeUnitsystem: The current unit system, 0 for metric, 1 for non-metric.
    :var attributeValues: A vector of AttributeValue structures containing attribute Ids and their corresponding UI
    values to use additionally to find the values for 'attributeID'.
    """
    attributeID: int = 0
    classID: str = ''
    searchInBothUnitSystems: bool = False
    activeUnitsystem: int = 0
    attributeValues: List[AttributeValue] = ()


@dataclass
class FindValuesOutput(TcBaseObj):
    """
    Structure containing the value(s) which have been found for the attribute.
    
    :var foundValues: The found values.
    """
    foundValues: List[FoundValue] = ()


@dataclass
class FindValuesResponse(TcBaseObj):
    """
    Structure containing the vector of found values. Any failures with the conversion will be mapped to the error
    message in the ServiceData list of partial errors.
    
    :var findValuesOutputs: The found values.
    :var svcData: Any failures with the operation will be mapped to the error message in the ServiceData list of
    partial errors.
    """
    findValuesOutputs: List[FindValuesOutput] = ()
    svcData: ServiceData = None


@dataclass
class FoundValue(TcBaseObj):
    """
    Structure containing the existing values, the count how many times the value is used and in which unit system.
    
    :var unitSystem: The unit system in which the value was found. 0 for metric, 1 for non-metric.
    :var value: The found value.
    :var count: The count how many times the value was found.
    """
    unitSystem: int = 0
    value: str = ''
    count: int = 0


@dataclass
class AttributeValue(TcBaseObj):
    """
    This structure contains the attribute ID and the corresponding value.
    
    :var id: The ID of the attribute.
    :var value: The value of the attribute.
    The calling client is responsible for converting the different property types (int, float, date etc) to a string
    using the appropriate functions in the SOA client framework's Property class.
    """
    id: int = 0
    value: str = ''
