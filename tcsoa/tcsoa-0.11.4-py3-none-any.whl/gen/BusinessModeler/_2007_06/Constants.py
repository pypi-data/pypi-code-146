from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GlobalConstantValue(TcBaseObj):
    """
    The 'GlobalConstantValue' data structure holds a the name of the global constant corresponding global constant value
    
    :var key: Name of the global constant.
    :var value: The global constant value corresponding to the specified constant.
    """
    key: str = ''
    value: str = ''


@dataclass
class GlobalConstantValueResponse(TcBaseObj):
    """
    Holds the response for the getGlobalConstantValues operation.
    
    :var constantValues: The requested global constants.
    :var serviceData: This contains the status of the operation. A partial error is returned if the name global
    constant cannot be added to the global default cache (74502), or if the named constant is multivalued(74528) .
    """
    constantValues: List[GlobalConstantValue] = ()
    serviceData: ServiceData = None


@dataclass
class PropertyConstantKey(TcBaseObj):
    """
    Holds the name of the constant, name of the type and name of the property which are required to get the value of a
    property constant.
    
    :var constantName: Name of the constant.
    :var typeName: Name of the type.
    :var propertyName: Name of the property.
    """
    constantName: str = ''
    typeName: str = ''
    propertyName: str = ''


@dataclass
class PropertyConstantValue(TcBaseObj):
    """
    Holds a the name of the property constant and corresponding property constant value
    
    :var key: The requested property constant.
    :var value: The property constant value corresponding to the specified constant
    """
    key: PropertyConstantKey = None
    value: str = ''


@dataclass
class PropertyConstantValueResponse(TcBaseObj):
    """
    The 'PropertyConstantValueResponse' data structure holds the response for the 'getPropertyConstantValues' method.
    
    :var constantValues: The resultant property constant values are returned as keyvalue pairs using
    'PropertyConstantValue' structure.
    :var serviceData: This contains the status of the operation.
    """
    constantValues: List[PropertyConstantValue] = ()
    serviceData: ServiceData = None


@dataclass
class TypeConstantKey(TcBaseObj):
    """
    Holds the name of the constant, name of the type which are required to get the value of a type constant.
    
    :var constantName: Name of the constant.
    :var typeName: Name of the type.
    """
    constantName: str = ''
    typeName: str = ''


@dataclass
class TypeConstantValue(TcBaseObj):
    """
    Holds a the name of the type constant and corresponding type constant value.
    
    :var key: The requested type constant.
    :var value: The type constant value corresponding to the specified constant.
    """
    key: TypeConstantKey = None
    value: str = ''


@dataclass
class TypeConstantValueResponse(TcBaseObj):
    """
    Holds the response for the 'getTypeConstantValues' operation.
    
    :var constantValues: The resultant type constant values are returned as key/value pairs using 'TypeConstantValue'
    structure.
    :var serviceData: This contains the status of the operation.
    """
    constantValues: List[TypeConstantValue] = ()
    serviceData: ServiceData = None
