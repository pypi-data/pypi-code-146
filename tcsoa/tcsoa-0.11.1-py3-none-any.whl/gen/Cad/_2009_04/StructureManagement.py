from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Cad._2008_06.StructureManagement import RelativeStructureChildInfo2
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MappedReturnData(TcBaseObj):
    """
    Map of returned data that is relevant to the created or updated occurrence for the given client ID.
    
    :var occThread: The occurrence thread for tracking the created or updated occurrence.
    :var occurrence: The occurrence object that was created or updated.
    :var bvr: The BOM view revision that was created or updated.
    """
    occThread: BusinessObject = None
    occurrence: BusinessObject = None
    bvr: BusinessObject = None


@dataclass
class AttributesInfoForObject(TcBaseObj):
    """
    Contains classname and vector of AttributesInfos structure
    
    :var topLineAttrThatRefersToObject: Name of the attribute that refers to the object
    :var attrsToSet: List of AttributesInfos
    """
    topLineAttrThatRefersToObject: str = ''
    attrsToSet: List[AttributesInfos] = ()


@dataclass
class AttributesInfos(TcBaseObj):
    """
    Contains name/values pair data to be set as attributes on the related object.
    
    :var name: Attribute name
    :var values: Attribute values
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class RelativeStructureParentInfo(TcBaseObj):
    """
    Contains information about the parent BOM line representation.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var complete: Flag that if true signifies that the structure represented in the input is the full representation
    of the structure under the input parent. Any other structure relations that exist in Teamcenter but are not
    represented in the input will be removed.
    :var bomViewTypeName: The type of the BOM view to create under the parent 'bomViewTypeName' object.  If not
    specified, 'CreateOrUpdateRelativeStructurePref' 'bomViewTypeName' will be used as the default.
    :var parent: Object reference of the Item Revision context assembly object to create or update the child
    occurrence.  This is a required input.  An error will be returned if a valid parent is not specified.
    :var changeContext: Designated for future implementation.
    :var lastModifiedOfBVR: Last modified date of BOM view revision (BVR) under the input 'parent'.  This input is not
    required.  If this input date is different than the current last modified date and the 'overwriteForLastModDate'
    preference is false the input will be ignored and processing will continue with the next input.  In this scenario,
    error 215033 will be returned.  If the dates are different and the 'overwriteForLastModDate' preference is true,
    processing will continue with the current input.  In this scenario, error 215034 will be returned.
    :var precise: Flag for updating the BVR to precise (true) or imprecise (false).  Specifying precise as true means
    the child occurrences reference item revisions, whereas specifying precise as false (imprecise) means the child
    occurrences reference items.
    :var supportingClassAttrs: A list of object property names for the parent BOM line and attributes to set on the
    corresponding objects.  For example, 'supportingClassAttrs' 'topLineAttrThatRefersToObject' could be set to the
    property name bl_bomview_rev and 'attrsToSet' could include the attribute legacy_transform_factor with a value of
    0.5 to set on the BOM view revision object.
    """
    clientId: str = ''
    complete: bool = False
    bomViewTypeName: str = ''
    parent: BusinessObject = None
    changeContext: BusinessObject = None
    lastModifiedOfBVR: datetime = None
    precise: bool = False
    supportingClassAttrs: List[AttributesInfoForObject] = ()


@dataclass
class CreateOrUpdateRelativeStructureInfo(TcBaseObj):
    """
    Input structure for 'createOrUpdateRelativeStructure'.
    
    :var parentInfo: Parent info structure containing information about the parent BOM line representation.
    :var childInfo: Child info structure for creating the occurrence or updating the occurrence attributes.  If no
    child objects are specified and 'RelativeStructureParentInfo' 'complete' is true, all existing child objects will
    be removed.  If no child objects are specified and 'RelativeStructureParentInfo' 'complete' is false, the input is
    ignored.
    """
    parentInfo: RelativeStructureParentInfo = None
    childInfo: List[RelativeStructureChildInfo2] = ()


@dataclass
class CreateOrUpdateRelativeStructurePref(TcBaseObj):
    """
    Preference structure for 'createOrUpdateRelativeStructure'.
    
    :var overwriteForLastModDate: Flag to check whether the structure needs to be updated if the input last modified
    date is different from the current last modified date of the object in Teamcenter.  If false, but the
    'RelativeStructureParentInfo' 'lastModifiedOfBVR' input specified is different than the set modified date, partial
    error 215033 will be returned.
    :var continueOnError: Flag to indicate whether the operation should continue processing to the next input when an
    error is encountered.
    :var bomViewTypeName: The default BOM view type to create or the view type of the child to be added to the parent
    BOMViewRevision This default value can be overridden for individual parent by specifying the 'bomViewTypeName' in 
    'RelativeStructureParentInfo' 'parentInfo' input. The default value can also be overridden for individual children
    by specifying the 'childBomViewType' in the 'RelativeStructureChildInfo' 'childInfo' input.
    :var cadOccIdAttrName: Represents the occurrence note type which holds the value for the CAD occurrence ID or this
    can be the PSOccurrenceThread UID if the integration does not use a note type.
    :var objectTypes: List of object types that the client is interested in.  If 'complete' is true, object types or
    subtypes that exist in the structure in Teamcenter but are not in this list are removed.  If 'complete' is true,
    but no 'objectTypes' are specified, then all objects types or subtypes are removed from the existing structure in
    Teamcenter.  If 'complete' is false, 'objectTypes' is ignored.
    """
    overwriteForLastModDate: bool = False
    continueOnError: bool = False
    bomViewTypeName: str = ''
    cadOccIdAttrName: str = ''
    objectTypes: List[str] = ()


@dataclass
class CreateOrUpdateRelativeStructureResponse(TcBaseObj):
    """
    The response from the 'createOrUpdateRelativeStructure' operation.
    
    :var output: Map of client IDs to 'MappedReturnData'.
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData' with created occurrences, BOM
    views and BOM view revisions, updated occurrences and BOM view revisions, and any implicitly deleted occurrences.
    """
    output: ClientIdToOccurrenceMap = None
    serviceData: ServiceData = None


"""
Map that maps from client Id to MappedReturnData
"""
ClientIdToOccurrenceMap = Dict[str, MappedReturnData]
