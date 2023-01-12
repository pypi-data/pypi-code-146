from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetPersonPropertiesResponse(TcBaseObj):
    """
    This structure holds the list of PropertyValuesData for each of the requested person objects.
    
    :var serviceData: The object which holds the partial errors while getting the property values.
    :var personData: The list of PropertyValuesData objects which holds the values of the given properties for all the
    given person business objects.
    """
    serviceData: ServiceData = None
    personData: List[PropertyValuesData] = ()


@dataclass
class PropertyValuesData(TcBaseObj):
    """
    This structure holds the retrieved values of the given properties for a Person object.
    
    :var propValues: The list of property values of a Person object.
    """
    propValues: List[str] = ()


"""
Name and Value pair for properties.
"""
NameValueMap = Dict[str, str]
