from __future__ import annotations

from tcsoa.gen.BusinessObjects import Vendor, Item, ImanRelation, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ChangeVendorInputInfo(TcBaseObj):
    """
    Input structure containing Vendor to change, VendorPart to change and destination new Vendor.
    
    :var vendorToChange: This is Object pointing to the Vendor to change. If this input is specified, all the related
    VendorPart objects are processed for change Vendor operation. This input takes precedence over VendorPart objects
    input.
    :var vendorParts: VendorPart objects to be processed for change Vendor operation.
    :var newVendor: The new Vendor to be attached to the part.
    """
    vendorToChange: Vendor = None
    vendorParts: List[Item] = ()
    newVendor: Vendor = None


@dataclass
class GetVendorPartsWithSelRuleInputInfo(TcBaseObj):
    """
    A structure of CommercialPartRevision and condition name.
    
    :var comPartRev: Selected CommercialPartRevision object from BOM. This revision is used for searching the related
    VendorPart objects based on selection rule.
    :var conditionName: The name of the condition in Teamcenter which is used as a selection rule while finding the
    VendorPart objects. The service operation will try and search for a valid selection rule based on the condition
    name. If this input is given as an empty string, the default selection rule is used which is governed by the
    preference VMS_vendor_part_selection_rule.
    """
    comPartRev: ItemRevision = None
    conditionName: str = ''


@dataclass
class GetVendorPartsWithSelRuleResponse(TcBaseObj):
    """
    The response structure containing 'VendorPartData' structure which in turn stores information about found
    VendorPart objects.
    
    :var partData: The output structure, which is essentially a list of 'VendorPartData' structures returned. Each of
    them will contain relation and part information for each VendorPart found.
    :var serviceData: Standard Teamcenter service response data.
    """
    partData: List[VendorPartData] = ()
    serviceData: ServiceData = None


@dataclass
class ChangeVendorResponse(TcBaseObj):
    """
    Response structure for the 'changeVendor' operation contains statuses member. It is a list of 'ChangeVendorStatus'
    structures.
    
    :var statuses: List of 'ChangeVendorStatus' structures. There is an entry per entry in input structure.
    :var serviceData: Standard 'ServiceData' structure. It contains partial errors and failures along with the
    clientIds.
    """
    statuses: List[ChangeVendorStatus] = ()
    serviceData: ServiceData = None


@dataclass
class VendorPartAndRel(TcBaseObj):
    """
    Structure containing a VendorPart object and its relation object to a CommercialPart.
    
    :var vendorPart: VendorPart object.
    :var vmRepresentRel: Each of these VendorPart objects are related to the input CommercialPartRevision with a
    relation called VMRepresents. This object represents an instance of that relation.
    """
    vendorPart: Item = None
    vmRepresentRel: ImanRelation = None


@dataclass
class VendorPartData(TcBaseObj):
    """
    Structure containing a filtered list of relation and part information for each VendorPart objects.
    
    :var partAndRel: It is the vector of 'VendorPartAndRel' objects holding the information of individual VendorPart
    objects and relation of input CommercialPartRevision with each of them.
    """
    partAndRel: List[VendorPartAndRel] = ()


@dataclass
class ChangeVendorStatus(TcBaseObj):
    """
    This is the structure containing a list of structures for each VendorPart statuses.
    
    :var changedStatus: This is the structure containing a list of statuses for change Vendor operation.
    """
    changedStatus: List[ChangedPartStatus] = ()


@dataclass
class ChangedPartStatus(TcBaseObj):
    """
    This structure contains the status of VendorPart objects and remarks from the operation.
    
    :var oldPartStr: Id of old VendorPart.
    :var newPartStr: Id of new VendorPart created.
    :var notes: Remarks (notes) corresponding to the each change Vendor operation. e.g. Success, Failure.
    """
    oldPartStr: str = ''
    newPartStr: str = ''
    notes: str = ''
