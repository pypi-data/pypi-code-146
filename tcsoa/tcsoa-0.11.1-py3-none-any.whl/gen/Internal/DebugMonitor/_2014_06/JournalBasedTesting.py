from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class InitializeJBTResponse(TcBaseObj):
    """
    This structure contains the information of the site database that the client is connecting to.
    
    :var siteDBInfo: The last six characters of an UID which uniquely identifies a site database.
    :var serviceData: Partial errors and client id.
    :var additionalInfo: The additional information about the Journal Based Testing environment, such as the template
    names installed in the database.
    """
    siteDBInfo: str = ''
    serviceData: ServiceData = None
    additionalInfo: AuxiliaryInfo = None


@dataclass
class AuxiliaryInfo(TcBaseObj):
    """
    Auxiliary information about the Journal Based Testing environment, such as the template names installed in the
    database.
    
    :var strToStrVectorMap: A map of string to list of strings.
    :var strToDblVectorMap: A map of string to list of doubles.
    :var strToIntVectorMap: A map of string to list of integers.
    :var strToDateVectorMap: A map of string to list of dates.
    :var strToObjVectorMap: A map of string to list of Business Objects.
    """
    strToStrVectorMap: StringToStringVectorMap = None
    strToDblVectorMap: StringToDoubleVectorMap = None
    strToIntVectorMap: StringToIntegerVectorMap = None
    strToDateVectorMap: StringToDateMap = None
    strToObjVectorMap: StringToObjectVectorMap = None


@dataclass
class PropertyData(TcBaseObj):
    """
    The PropertyData structure contains the property data of a single object.
    
    :var object: The object whose property values will be validated.
    :var properties: The list of expected property values.
    """
    object: BusinessObject = None
    properties: List[SinglePropertyData] = ()


@dataclass
class SinglePropertyData(TcBaseObj):
    """
    The SinglePropertyData data structure contains the array value of a single property.
    
    :var propertyName: The name of the property.
    :var value: The array value of a property. For example, if the property is bl_child_lines, its value will be stored
    in a SinglePropertyData object. Because the value of this property represents multiple child BOMLine objects, the
    vector in SinglePropertyData is used to store all the child BOMLine objects. For all non-string values (e.g., float
    value), the value field stores their string representations.
    """
    propertyName: str = ''
    value: List[str] = ()


"""
A map of string to list of dates.
"""
StringToDateMap = Dict[str, List[datetime]]


"""
A map of string to list of doubles.
"""
StringToDoubleVectorMap = Dict[str, List[float]]


"""
A map of string to list of integers.
"""
StringToIntegerVectorMap = Dict[str, List[int]]


"""
A map of string to list of Business Objects.
"""
StringToObjectVectorMap = Dict[str, List[BusinessObject]]


"""
A map of string to list of strings.
"""
StringToStringVectorMap = Dict[str, List[str]]
