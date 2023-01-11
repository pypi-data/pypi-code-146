from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetSubscribableTypesAndSubtypesResponse(TcBaseObj):
    """
    It returns  'TypesAndSubtypesData'  containing type name and associated display names. If there are any unexpected
    errors while getting the licenses, the errors are returned in 'serviceData' of 
    'GetSubscribableTypesAndSubtypesResponse'. Partial errors are returned via sericeData if there are any.
    
    :var serviceData: Teamcenter service response data
    :var typesNames: structure containing typeNames and associated Display names.
    """
    serviceData: ServiceData = None
    typesNames: List[TypesAndSubtypesData] = ()


@dataclass
class TypesAndSubtypesData(TcBaseObj):
    """
    'TypesAndSubtypesData' structure represents 'typeName' and associated 'displayName' for a subscribable types and
    subtypes.
    
    :var displayName: Contains display name associated with the typename.
    :var typeName: Contains type name for a type and subtype that is subscribable.
    """
    displayName: str = ''
    typeName: str = ''
