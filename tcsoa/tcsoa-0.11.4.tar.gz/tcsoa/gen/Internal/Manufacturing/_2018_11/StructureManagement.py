from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2015_10.StructureManagement import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindBrokenPartsDetails(TcBaseObj):
    """
    FindBrokenPartsDetails represents a list of first level children Clone Stable ID (CSID), CSID to property map, CSID
    children map for broken parts for each product view Dataset.
    
    :var targetPV: Target Dataset for finding broken parts.
    :var firstLevelChildrenCSID: A list of clone stable ID (CSID) for the first level children.
    :var propertyInfo: Properties for a CSID.
    :var childrenMap: A map (string, list of strings) representing parent and children&rsquo;s CSID, where key
    represents CSID of parent and value represents the list of CSID values of the children.
    :var additonalInfo: Currently unused, Possible future example usage:
    additionalInfo.strToIntVectorMap["hasIPANodes"] = (1);
    """
    targetPV: BusinessObject = None
    firstLevelChildrenCSID: List[str] = ()
    propertyInfo: BrokenPartsCSIDToPropsInfo = None
    childrenMap: BrokenPartsParentToChildrenMap = None
    additonalInfo: AdditionalInfo = None


@dataclass
class FindBrokenPartsInPVInputInfo(TcBaseObj):
    """
    This input structure contains target product view Dataset objects and target scope (BOMLine) for identifying the
    broken parts and any optional key/value pairs of information.
    
    :var targetDatasets: A list of Product View Dataset objects.
    :var targetScope: Scope BOMLine for resolving the Product View.
    :var additionalInfo: Currently unused. Possible future example usage:
    additionalInfo.strToIntVectorMap["ignoreIPA"] = (1);
    """
    targetDatasets: List[BusinessObject] = ()
    targetScope: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class FindBrokenPartsInPVResponse(TcBaseObj):
    """
    FindBrokenPartsInPVResponse represents list of FindBrokenPartsDetails and any partial errors captured during the
    service call.
    
    :var serviceData: Object that captures any partial errors.
    :var brokenPartsDetail: A list of broken parts details for input Dataset objects.
    """
    serviceData: ServiceData = None
    brokenPartsDetail: List[FindBrokenPartsDetails] = ()


@dataclass
class FindBrokenProductViewsDetails(TcBaseObj):
    """
    FindBrokenProductViewsDetails represents a list of BrokenProductViewsData for each scope.
    
    :var scope: Input BOMLine object.
    :var brokenProductViews: A list of broken product views details for current scope.
    """
    scope: BusinessObject = None
    brokenProductViews: List[BrokenProductViewsData] = ()


@dataclass
class FindBrokenProductViewsInputInfo(TcBaseObj):
    """
    A structure containing list of non-nested scopes for finding broken PVs in their hierarchy and any optional
    key/value pairs of information.
    
    :var unnestedScopes: A list of non-nested BOMLine objects as scope.
    :var additionalInfo: Currently unused. Future example usage: 
    additionalInfo.strToIntVectorMap["getRelatedStructures"] = (1);
    """
    unnestedScopes: List[BusinessObject] = ()
    additionalInfo: AdditionalInfo = None


@dataclass
class FindBrokenProductViewsResponse(TcBaseObj):
    """
    Response for findBrokenProductViews operation. Containing list of FindBrokenProductViewsDetails and any partial
    errors captured during the service call.
    
    :var serviceData: Object that captures any partial errors.
    :var brokenProductViewsDetails: A list of BrokenProductViews for each non-nested scope.
    """
    serviceData: ServiceData = None
    brokenProductViewsDetails: List[FindBrokenProductViewsDetails] = ()


@dataclass
class OpenContextInfo(TcBaseObj):
    """
    The structure containing the BOMWindow information for BOMLine represented by the link. If the CCObject contains
    more than one window, the object member will only be present in the window which actually contains the BOMLine
    represented by the link.
    Elements:
    - context     The root BOMLine of the window.
    - object     BOMLine represented by the link.
    - views     Any AppearanceGroup objects that are opened as part of the link.
    - structureContext     The StructureContext representing this context or window.
    
    
    
    :var context: The root BOMLine of the window.
    :var object: BOMLine represented by the link.
    :var views: Any AppearanceGroup objects that are opened as part of the link.
    :var structureContext: The StructureContext representing this context or window.
    """
    context: BusinessObject = None
    object: BusinessObject = None
    views: List[BusinessObject] = ()
    structureContext: BusinessObject = None


@dataclass
class BrokenPartsCSIDToPropsInfo(TcBaseObj):
    """
    BrokenPartsCSIDToPropsInfo represents the property for rendering clone stable ID (CSID) on the view. It contains a
    list of property types and their corresponding property values in another list. If a value is null or empty for a
    given property then the entry in the propValues for that property would be null.
    
    :var csidValue: Clone stable ID for broken part.
    :var propTypes: A list of property types.
    :var propValues: A list of property values mapping to the property types.
    """
    csidValue: str = ''
    propTypes: List[str] = ()
    propValues: List[str] = ()


@dataclass
class BrokenProductViewsData(TcBaseObj):
    """
    BrokenProductViewsData represents the product view and the attached line for each product view along with any
    additional information in key/value format.
    
    :var productView: Dataset object for the product view.
    :var attachedToLine: Business object for the BOMLine to which the PV is attached.
    :var additionalInfo: Currently unused. Future example usage: additionalInfo.strToIntVectorMap
    ["containsInProcessAssembly"] = (1);
    """
    productView: BusinessObject = None
    attachedToLine: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class ContextGroup(TcBaseObj):
    """
    The structure containing the contextual BOMLine or persistent BusinessObject represented by the link.
    Elements:
    - context     A list of OpenContextInfo objects representing the structures providing the context for the BOMLine
    represented by the link.
    - persistentObject     Persistent BusinessObject represented by the link. Will not be set, if the link represents a
    BOMLine. 
    - applicationId     Currently unused. Probable example usage: applicationId="aws"
    - collaborationContext     If the BOMLine represented by the link is part of structure contained by the CCObject,
    will be set to that object.
    
    
    
    :var contexts: A list of OpenContextInfo objects representing the structures providing the context for the BOMLine
    represented by the link.
    :var persistentObject: Persistent BusinessObject represented by the link. Will not be set, if the link represents a
    BOMLine.
    :var applicationId: Currently unused. Probable example usage: applicationId="aws".
    :var collaborationContext: If the BOMLine represented by the link is part of structure contained by the CCObject,
    will be set to that object.
    """
    contexts: List[OpenContextInfo] = ()
    persistentObject: BusinessObject = None
    applicationId: str = ''
    collaborationContext: BusinessObject = None


@dataclass
class EvaluateLinksData(TcBaseObj):
    """
    A structure containing the link to be evaluated and any optional key/value pairs of information.
    - link     Link to be evaluated.
    - additionalInfo     Currently unused. Probable example usage:  additionalInfo.strToIntVectorMap["GetComponent"]
    =(1)
    
    
    
    :var link: Link to be evaluated.
    :var additionalInfo: additional information to be passed to the client. Currently, one probable value
    strToIntVectorMap["GetComponent"]=(1) is supported. If the first element of the value vector is not 0, the
    operation will return either the CCObject or StructureContext. The objects will be returned in the
    EvaluateLinksResponse additionalInfo.StringToObjectVectorMap member.
    """
    link: str = ''
    additionalInfo: AdditionalInfo = None


@dataclass
class EvaluateLinksResponse(TcBaseObj):
    """
    Response for evaluateLinks operation.
    - group    A list of ContextGroup elements, each representing the BOMLine and it&rsquo;s contextual information
    (CCObject or StructureContext as OpenContextInfo), or persistent BusinessObject.
    - serviceData
    - additionalInfo    Partial errors as part of the serviceData.
    - Currently unused. Probable example usage: additionalInfo.strToObjVectorMap["Component"]=(BOM::12345)
    
    
    
    :var output: A list of ContextGroup elements, each representing the BOMLine and it&rsquo;s contextual information
    (CCObject or StructureContext as OpenContextInfo), or persistent BusinessObject.
    :var serviceData: Partial errors as part of the serviceData.
    :var additionaInfo: If the input has additionalInfo value of "GetComponents" and the link contains a CCObject, then
    additionalInfo will be populated as, additionalInfo.strToObjVectorMap["CC"]=(CCObject), 
    additionalInfo.strToObjVectorMap["CCSC"]=(StructureContext). If the link contains a StructureContext object, the
    data will be returned as additionalInfo.strToObjVectorMap["SC"]=(StructureContext). If the link contains a
    StructureContext representing a Manufacturing Study that is linked to the CCObject, the data will be returned as,
    additionalInfo.strToObjVectorMap["StudySC"]=(StructureContext) in addition to the CCObject.
    """
    output: List[ContextGroup] = ()
    serviceData: ServiceData = None
    additionaInfo: AdditionalInfo = None


"""
BrokenPartsParentToChildrenMap represents the parent to children clone stable ID (CSID) map, where key represents CSID of parent and value represents the list of children&rsquo;s.
"""
BrokenPartsParentToChildrenMap = Dict[str, List[str]]
