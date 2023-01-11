from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportUnmanagedDataResponse(TcBaseObj):
    """
    ImportUnmanagedDataResponse type of structure is return as response from this SOA operation.
    
    :var transientFileReadTickets: FMS Ticket of log files.
    :var modifiedObjectList: List of modified objects.
    :var serviceData: The Service Data.
    """
    transientFileReadTickets: List[str] = ()
    modifiedObjectList: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class RelativeStructureChildInfo(TcBaseObj):
    """
    'RelativeStructureChildInfo' structure holds information about child objects in a structure.
    RelativeStructureParentInfo holds list of structures of type RelativeStructureChildInfo.
    
    :var childID: Item Id for child object
    :var objectType: Type of the object e.g. Item, Part, Vendor, Part etc
    :var refDesignator: The reference designator value.
    :var childAttrList: List of attribute on child object
    :var attrListRel: The list of attributes on the relationship between parent and child.
    :var relationType: Type of relation PSOccurrence or GRM
    :var actionRequired: If the object is modified, New or Deleted from Teamcenter. If user passed as empty string then
    server will figure out the action to be trigger.
    :var structModification: The map to store id of the child element if it is added, replaced  or deleted.
    :var childChangeType: Possible value for this parameter are  "BVR","GRM","FORM","FOLDERS"  and "NO_CHANGE". If user
    passed as empty string then server will figure out the change type.
    """
    childID: str = ''
    objectType: str = ''
    refDesignator: str = ''
    childAttrList: AttrMap = None
    attrListRel: AttrMap = None
    relationType: str = ''
    actionRequired: str = ''
    structModification: AttrMap = None
    childChangeType: AttrMap = None


@dataclass
class RelativeStructureParentInfo(TcBaseObj):
    """
    'RelativeStructureParentInfo' structure holds information about parent object.
    
    :var parentID: ID of Parent.
    :var objectType: Business object type of parent.
    :var parentAttrList: Attribute map of parent object.
    :var childInfo: Vector that holds structure of type  RelativeStructureChildInfo.
    :var actionRequired: Possible value for this parameter are "New" or "Modify". If user passed as empty string then
    server will figure out the action to be trigger.
    :var parentChangeType: Possible value for this parameter are "BVR","GRM","FORM","FOLDERS" and "NO_CHANGE". If user
    passed as empty string then server will figure out the change type.
    """
    parentID: str = ''
    objectType: str = ''
    parentAttrList: AttrMap = None
    childInfo: List[RelativeStructureChildInfo] = ()
    actionRequired: str = ''
    parentChangeType: AttrMap = None


"""
This map will hold the name value pair being passed to SOA
"""
AttrMap = Dict[str, List[str]]
