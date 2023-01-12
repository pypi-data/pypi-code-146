from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awb0Element, Awb0ProductContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceBom._2012_10.OccurrenceManagement import InfoForElementCreation
from typing import Dict, List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2019_06.OccurrenceManagement import NewElementInfo3
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_05.OccurrenceManagement import OccurrenceSortInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_12.OccurrenceManagement import OccurrenceInfo6


@dataclass
class OccTypeInfo(TcBaseObj):
    """
    Contains  parent, map/list of OccTypeName objects retrieved based on parent, source and request preference.
    
    :var parentObject: The parent of selected object. Valid types are Item, ItemRevision, BOMLine or Awb0Element.
    :var srcObjectOccTypesMap: A map (BusinessObject, list of OccTypeName) of source BusinessObject to list of
    OccTypeName. When preference "useMEDisplayOccurrenceTypePref" with value true is specified the operation shall
    return a map containing entries. An empty map is returned otherwise.
    :var srcObjectDefaultOccTypeMap: A map (BusinessObject, OccTypeName) of source BusinessObject to default
    OccTypeName. The default occurrence type is decided based on Teamcenter preference
    MEAssignCustomizedOccurrenceType. When preference "useMEDisplayOccurrenceTypePref" with value true is specified the
    operation shall return a map containing entries. An empty map is returned otherwise.
    :var occTypeNames: A list of OccTypeName objects when value of preference "useMEDisplayOccurrenceTypePref" is not
    set or is false.
    """
    parentObject: BusinessObject = None
    srcObjectOccTypesMap: SourceObjectOccTypesMap = None
    srcObjectDefaultOccTypeMap: SourceObjectDefaultOccTypeMap = None
    occTypeNames: List[OccTypeName] = ()


@dataclass
class OccTypeName(TcBaseObj):
    """
    Contains internal and display name of the allowed PSOccurrenceType.
    
    :var internalName: Internal name of the PSOccurrenceType
    :var displayName: Display name of the PSOccurrenceType
    """
    internalName: str = ''
    displayName: str = ''


@dataclass
class OccTypesInputData(TcBaseObj):
    """
    Contains parent and list of source objects. Optionally request contains criteria to filter occurrence types based
    on Teamcenter preference MEDisplayOccurrenceType.
    
    :var parentObject: The parent of selected object.Valid types are Item, ItemRevision, BOMLine or Awb0Element. This
    field is ignored if request preference useMEDisplayOccurrenceTypePref is false.
    :var sourceObjects: A list of BusinessObject for which allowed occurrence type information is retrieved.Valid types
    are Item, ItemRevision, BOMLine or Awb0Element. This field is ignored if request preference
    useMEDisplayOccurrenceTypePref is false.
    :var requestPref: A map (string, string) of preference names and value pairs. Allowed preference name is 
    useMEDisplayOccurrenceTypePref. Allowed values are true/false. Keys and values are case sensitive.
    """
    parentObject: BusinessObject = None
    sourceObjects: List[BusinessObject] = ()
    requestPref: RequestPreference12 = None


@dataclass
class OccTypesResp(TcBaseObj):
    """
    The PSOccurrenceType internal and display names.
    
    :var occTypeInfo: Contains  parent and list/map of OccTypeName objects.
    :var serviceData: The Service Data with partial errors for getAllowedOccurrenceTypes operation.
    """
    occTypeInfo: OccTypeInfo = None
    serviceData: ServiceData = None


@dataclass
class RemoveLevelInputData(TcBaseObj):
    """
    A list of selected Awb0Element objects which are to be removed.
    
    :var elementsToRemoveLevel: A list of Awb0Element objects to be removed from content and their children to be added
    as children of parent of these objects.
    :var productContext: Awb0ProductContextInfo contains the product as well as all the configuration information.
    :var sortCriteria: Criteria to sort the occurrences based on internal property name and sorting order e.g. "ASC"
    and "DESC".
    """
    elementsToRemoveLevel: List[Awb0Element] = ()
    productContext: Awb0ProductContextInfo = None
    sortCriteria: OccurrenceSortInput = None


@dataclass
class ResetWorkingContextInputData(TcBaseObj):
    """
    Contains the Awb0ProductContextInfo for the opened object and a map of preference names and value pairs.
    
    :var productContext: Awb0ProductContextInfo containing configuration information.
    :var requestPref: A map (string, string) of preference names and value pairs. Allowed preference names are:
    "deleteCloneData". Allowed values are: True/False.  Keys and values are case sensitive. When preference
    "deleteCloneData" with value true is specified the operation shall delete clone data associated with
    Awb0Autobookmark. If map is empty then special processing like &lsquo;deleteCloneData&rsquo; is not be performed.
    """
    productContext: Awb0ProductContextInfo = None
    requestPref: RequestPreference12 = None


@dataclass
class ResetWorkingContextResp(TcBaseObj):
    """
    Contains ServiceData and map of preference names and value pairs.
    
    :var serviceData: The Service Data.
    :var responsePref: A map (string, string) of preference names and value pairs. Allowed preference names are:
    "recipeReset". Allowed values are: True/False. Keys and values are case sensitive. If filterRecipeList assoicated
    with Awb0Autobookmark has been cleared then preference "recipeReset" is set to true.
    """
    serviceData: ServiceData = None
    responsePref: RequestPreference12 = None


@dataclass
class InfoForInsertLevelData(TcBaseObj):
    """
    A list of selected Awb0Element objects for which new element would be added as a parent.
    
    :var elementsToBeReparented: A list of Awb0Element objects to be reparented.
    :var fetchAllowedOccRevTypes: If true, operation returns allowed occurrence revision (Fnd0AbstractOccRevision)
    types.The allowed occurrence revision types can be specified using preference TcAllowedOccRevTypes_<ParentItemType>.
    """
    elementsToBeReparented: List[Awb0Element] = ()
    fetchAllowedOccRevTypes: bool = False


@dataclass
class InfoForInsertLevelResp(TcBaseObj):
    """
    The allowable parent type name and information for Full Text Search along with preferred object type information.
    
    :var preferredTypeInfo: Preferred type information to create new parent Awb0Element.
    :var allowedTypeInfos: A list of all allowed types to create Awb0Element as parent of the selected Awb0Element
    objects.
    :var serviceData: The ServiceData containing partial error if any.
    """
    preferredTypeInfo: InfoForElementCreation = None
    allowedTypeInfos: List[InfoForElementCreation] = ()
    serviceData: ServiceData = None


@dataclass
class InsertLevelInputData2(TcBaseObj):
    """
    The information to insert a BusinessObject as parent of the given Awb0Element objects.
    
    :var elements: A list of Awb0Element objects which the user intends to group and create a new parent for.
    :var objectToBeInserted: Business object for which a Awb0Element is to be created and inserted as parent of the
    given Awb0Element objects. The supported types are Item, ItemRevision, and Awb0Element.
    :var productContext: Awb0ProductContextInfo contains the product as well as all the configuration information.
    :var sortCriteria: Criteria to sort the occurrences based on internal property name and sorting order e.g. "ASC"
    and "DESC".
    """
    elements: List[Awb0Element] = ()
    objectToBeInserted: BusinessObject = None
    productContext: Awb0ProductContextInfo = None
    sortCriteria: OccurrenceSortInput = None


@dataclass
class InsertLevelResponse2(TcBaseObj):
    """
    InsertLevelResponse2 structure contains successfully inserted Awb0Element object corresponding to the input and the
    ServiceData
    
    :var newParent: The Awb0Element object which is the new inserted parent object of the given set of objects.
    :var childOccurrencesInfo: The map(Awb0Element, std::vector<OccurrenceInfo6>) of parent Awb0Element object
    (inserted and old parent) to the list of OccurrenceInfo6 corresponds to the child occurrrences.
    :var newElementInfos: A list of NewElementInfo3 populated when the parent is instantiated more than once.
    :var serviceData: The service data containing partial error if any.
    """
    newParent: Awb0Element = None
    childOccurrencesInfo: ParentToChildOccurrencesMap = None
    newElementInfos: List[NewElementInfo3] = ()
    serviceData: ServiceData = None


@dataclass
class RemoveLevelResponse(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    pass


"""
The map which can have a key and value pair. The key and value are case sensitive.
"""
RequestPreference12 = Dict[str, List[str]]


"""
A map (BusinessObject/OccTypeName) of source BusinessObject and default OccTypeName object.
"""
SourceObjectDefaultOccTypeMap = Dict[BusinessObject, OccTypeName]


"""
A map (BusinessObject/list of OccTypeName) of source BusinessObject and  list of OccTypeName objects.
"""
SourceObjectOccTypesMap = Dict[BusinessObject, List[OccTypeName]]


"""
The map(Awb0Element, std::vector<OccurrenceInfo6>) of parent Awb0Element object to the list of OccurrenceInfo6 corresponds to the child occurrrences.
"""
ParentToChildOccurrencesMap = Dict[Awb0Element, List[OccurrenceInfo6]]
