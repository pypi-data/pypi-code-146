from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, Item, NamedVariantExpression, MEAppearancePathNode
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetProductItemResponse(TcBaseObj):
    """
    The 'GetProductItemResponse' structure contains a list of all Product Items found in the database and a
    'ServiceData' object.
    
    :var output: A list of  all Product Items found in the database.
    :var serviceData: The 'ServiceData' object containing error codes and error messages in case of failure.
    """
    output: List[Item] = ()
    serviceData: ServiceData = None


@dataclass
class GetRemoveABEPartsResponse(TcBaseObj):
    """
    The 'GetRemoveABEPartsResponse' structure contains the 'ServiceData' object.
    
    :var serviceData: The 'ServiceData' containing error codes and error messages along with the indices for which the
    'removePartsRelatedToABE' operation fails.
    """
    serviceData: ServiceData = None


@dataclass
class OccNotesAttributes(TcBaseObj):
    """
    The part data information about each component is provided
    by way of the OccNotesAttributes data structure.
    
    :var noteType: Note type for selected component
    :var noteText: Note text for selected component
    """
    noteType: str = ''
    noteText: str = ''


@dataclass
class RemoveABEPartsInputInfo(TcBaseObj):
    """
    The information to remove parts related to ABE is provided by way of the 'RemoveABEPartsInputInfo' data structure.
    
    :var abeAPN: The reference to the Appearance Path Node of the Architecture Breakdown Element of which Part
    Solutions are to be removed. This is a mandatory attribute for the operation to succeed and cannot be null.
    :var topline: The reference to the topline to which Architecture Breakdown Element is linked. This is a mandatory
    attribute for the operation to succeed and cannot be null.
    """
    abeAPN: MEAppearancePathNode = None
    topline: BOMLine = None


@dataclass
class ReplacePartSolutionInputInfo(TcBaseObj):
    """
    The information to replace part is provided by way of the
    ReplacePartSolutionInputInfo data structure.
    
    :var values: Vector of OccNotesAttributes for each added component
    :var component: Component by which the replacement has been doing
    :var bomLine: Bomline to which the part is to be replaced
    :var abeAPN: APN of the associated ABE
    :var aNves: Vector of authorized NVEs present on ABE
    :var splitAndClone: splitAndClone
    :var carrySubstitutes: carrySubstitutes
    """
    values: List[OccNotesAttributes] = ()
    component: Item = None
    bomLine: BOMLine = None
    abeAPN: MEAppearancePathNode = None
    aNves: List[NamedVariantExpression] = ()
    splitAndClone: bool = False
    carrySubstitutes: bool = False


@dataclass
class ReplacePartSolutionResponse(TcBaseObj):
    """
    The ReplacePartSolutionResponse structure represents one output
    vector ReplacePartSolutionOutputInfo and the service data.
    
    :var component: component
    :var serviceData: serviceData returned as response for retrieving
    replace part in product information
    """
    component: List[Item] = ()
    serviceData: ServiceData = None


@dataclass
class AddPartSolutionInputInfo(TcBaseObj):
    """
    The information of added part is provided by way of the
    AddPartSolutionInputInfo data structure.
    
    :var values: Vector of OccNotesAttributes for each added component
    :var component: Component to be added
    :var abe: BomLine to which the component is to be added
    :var prodRevTags: Vector of product revisions for each selected component
    :var abeApnTag: Appearance Path Node for each added component
    :var aNves: Vector of authorized NVEs present on ABE
    :var quantity: Quantity of part to be added
    """
    values: List[OccNotesAttributes] = ()
    component: Item = None
    abe: BOMLine = None
    prodRevTags: List[Item] = ()
    abeApnTag: MEAppearancePathNode = None
    aNves: List[NamedVariantExpression] = ()
    quantity: int = 0


@dataclass
class AddPartSolutionResponse(TcBaseObj):
    """
    The AddPartSolutionResponse structure represents one output
    vector AddPartSolutionOutputInfo and the service data.
    
    :var partSolutionAPNs: partSolutionAPNs
    :var serviceData: serviceData returned as response
    for retrieving add part to product information
    """
    partSolutionAPNs: List[MEAppearancePathNode] = ()
    serviceData: ServiceData = None
