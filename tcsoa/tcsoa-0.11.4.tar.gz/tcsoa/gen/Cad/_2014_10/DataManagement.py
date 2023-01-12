from __future__ import annotations

from tcsoa.gen.BusinessObjects import CadAttrMappingDefinition
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAttrMappingsFilter(TcBaseObj):
    """
    Input filter for the data returned from the 'getAttrMappings' operation.
    
    :var itemTypeName: The item type name used to find an attribute mapping.
    :var datasetTypeName: The dataset type name used to find an attribute mapping.
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure. If 'clientId' is not provided then it can be difficult to align the
    input with any returned errors.
    """
    itemTypeName: str = ''
    datasetTypeName: str = ''
    clientId: str = ''


@dataclass
class GetAttrMappingsResponse(TcBaseObj):
    """
    The response returned from the 'getAttrMappings' operation.
    
    :var attrMappingInfos: A list of attribute mapping information.
    :var serviceData: The 'ServiceData'. This operation will populate the ServiceData plain objects with
    CadAttrMappingDefinition objects and property descriptor LOV objects.
    """
    attrMappingInfos: List[AttrMappingInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AttrMappingInfo(TcBaseObj):
    """
    Attribute mapping information.
    
    :var cadAttrMappingDefinition: The CadAttrMappingDefinition object reference representing the mapping definition.
    :var propDescInfo: The property descriptor information for the attribute mapping.  This information can be used to
    look up the client-side business object 'Type' and 'PropertyDescription' object in the 'ClientMetaModel' data.
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure. If 'clientId' is not provided then it can be difficult to align the
    input with any returned errors.
    """
    cadAttrMappingDefinition: CadAttrMappingDefinition = None
    propDescInfo: PropDescInfo = None
    clientId: str = ''


@dataclass
class PropDescInfo(TcBaseObj):
    """
    The 'PropDescInfo' struct contains information about the Teamcenter property descriptor associated with the
    attribute mapping definition.
    
    :var boTypeName: The business object type name with which the property descriptor is associated.  This can be used
    to look up the client-side 'PropertyDescription' object in the SOA 'ClientMetaModel' data.
    :var propDescName: The name of the property descriptor.  This can be used to look up the client-side
    'PropertyDescription' object in the 'ClientMetaModel' data.
    """
    boTypeName: str = ''
    propDescName: str = ''
