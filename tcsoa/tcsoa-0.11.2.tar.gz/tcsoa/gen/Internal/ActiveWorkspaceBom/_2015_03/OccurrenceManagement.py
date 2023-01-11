from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0Element, ImanRelation, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AttachObjectsRespData(TcBaseObj):
    """
    The relation created between the primary represented by Awb0Element and the secondary object.
    
    :var clientId: The unmodified value from the AttachObjectsInputData.clientId. This is used by the caller to
    identify this data structure with the source input data.
    :var relationObject: The newly created IMANRelation.
    """
    clientId: str = ''
    relationObject: ImanRelation = None


@dataclass
class AttachObjectsInputData(TcBaseObj):
    """
    AttachObjectsInputData Structure represents all required parameters to attach secondary object with primary object
    using given relation.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var relationType: Name of the valid IMANRelation to create between primary and secondary.
    :var primary: The primary object for the relation.
    :var primaryContext: The context in which relation to be created. If NULL then relation is created with underlying
    business object as primary.
    :var secondary: The secondary object for the relation.
    """
    clientId: str = ''
    relationType: str = ''
    primary: Awb0Element = None
    primaryContext: Awb0Element = None
    secondary: WorkspaceObject = None


@dataclass
class AttachObjectsResp(TcBaseObj):
    """
    AttachObjectsResp structure represents the relations created between the primary and secondary object and errors
    occurred.
    
    :var output: A list of created IMANRelation.
    :var serviceData: Standard ServiceData object to hold the partial errors that the operation encounters.
    """
    output: List[AttachObjectsRespData] = ()
    serviceData: ServiceData = None
