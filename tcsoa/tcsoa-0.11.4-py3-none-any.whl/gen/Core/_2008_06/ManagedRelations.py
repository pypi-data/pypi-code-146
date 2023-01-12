from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetManagedRelationInput(TcBaseObj):
    """
    GetManagedRelationInput
    
    :var primaryTags: List of primaryTags
    :var secondaryTags: List of secondaryTags
    :var primaryType: // primaryType of Managed relation
    :var subtype: // subtype of primary type
    """
    primaryTags: List[BusinessObject] = ()
    secondaryTags: List[BusinessObject] = ()
    primaryType: str = ''
    subtype: str = ''


@dataclass
class GetManagedRelationResponse(TcBaseObj):
    """
    GetManagedRelation Response
    
    :var managedRelations: Tracelink relations
    :var serviceData: The successful Object ids, partial errors and failures
    """
    managedRelations: List[WorkspaceObject] = ()
    serviceData: ServiceData = None
