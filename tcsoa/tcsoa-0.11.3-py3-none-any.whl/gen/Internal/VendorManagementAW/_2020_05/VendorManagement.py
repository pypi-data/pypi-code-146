from __future__ import annotations

from tcsoa.gen.BusinessObjects import WorkspaceObject, ItemRevision
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssignPartnerContractInput2(TcBaseObj):
    """
    The structure holds information of the partner contract to assign, selected object, preferred status and
    configuration context.
    
    :var selectedObject: Selected ManufacturerPart or ItemRevision to assign partner contract.
    :var configurationContext: Awb0SavedBookmark or Fnd0AppSession object of selectedObject.
    :var partnerContract: Vm0PrtnrContractRevision object to assign.
    :var preferredStatus: Preferred status for partner contract in the context of an object. Valid values are given in
    LOV preference: "Vm0PrtnrContractAssignmentStatus".
    """
    selectedObject: WorkspaceObject = None
    configurationContext: WorkspaceObject = None
    partnerContract: ItemRevision = None
    preferredStatus: str = ''


@dataclass
class RemovePartnerContractInput2(TcBaseObj):
    """
    The structure holds information of the partner contract to remove and selected object.
    
    :var selectedObject: ManufacturerPart or ItemRevision and its subtypes.
    :var partnerContract: Vm0PrtnrContractRevision object to remove.
    :var configurationContext: Awb0SavedBookmark or Fnd0AppSession object of selectedObject.
    """
    selectedObject: WorkspaceObject = None
    partnerContract: ItemRevision = None
    configurationContext: WorkspaceObject = None
