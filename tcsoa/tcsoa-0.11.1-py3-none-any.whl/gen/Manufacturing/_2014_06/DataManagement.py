from __future__ import annotations

from tcsoa.gen.Manufacturing._2012_02.DataManagement import AssociatedContextInfo, GeneralInfo, FileTicket
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProcResourceResponseInfo(TcBaseObj):
    """
    The response contains a structure of the data related to process resource. The following partial errors may be
    returned:
    
    - 253127 - The information for this object cannot be fetched as the object is not in the  context of Plant Bill Of
    Processes (BOP). 
    
    
    :var infoMap: Map of BOMLine objects (business object/list of business objects).
    If the key is process area of type Mfg0BvrProcessArea then value is list of process resources of type
    Mfg0BvrProcessResource that are defined under the process area and process/operation of type
    Mfg0BvrProcess/Mfg0BvrOperation that are unallocated to process resource. The value may also contain children of
    the process area such as process line or station.
    
    If the key is process resource of type Mfg0BvrProcessResource then values are process/operation of type
    Mfg0BvrProcess/Mfg0BvrOperation that are allocated to process resource.
    
    If the key is process of type Mfg0BvrProcess then values are process/operation of type 
    Mfg0BvrProcess/Mfg0BvrOperation that are child of that process. These childs are process/operation that are
    unallocated to any process resource. If the process itself is allocated to process resource then the value is empty
    list.
    
    :var serviceData: The service data containing partial errors.
    """
    infoMap: ProcResourceRelatedInfoMap = None
    serviceData: ServiceData = None


@dataclass
class CloneAssemblyInputData(TcBaseObj):
    """
    Input to the service that is a source object that should be cloned, target parent object for the cloned object and
    additional parameters needed for functionality.
    
    
    :var sourceObject: Business object of the source structure to be cloned. The expected buisness object must be of
    type Item, ItemRevision or BOMLine.
    :var scopeSearchObject: Business object of the scope object to search in for parts to be replaced. The expected
    buisness object must be of type Item, ItemRevision or BOMLine. If not specified, the source object will be used.
    :var parentObject: Business object of the parent object for the new created clone object. The expected buisness
    object must be of BOMLine type. If not specified, the parent of the sourceObject will be used.
    :var sourceOccEff: Occurrence effectivity of the source object.
    :var newCloneOccEff: Occurrence effectivity of the new cloned object.
    :var additionalInfo: Additional information needed to create the new cloned object like name, revision, description
    etc.
    """
    sourceObject: BusinessObject = None
    scopeSearchObject: BusinessObject = None
    parentObject: BusinessObject = None
    sourceOccEff: str = ''
    newCloneOccEff: str = ''
    additionalInfo: GeneralInfo = None


@dataclass
class CloneAssemblyResponse(TcBaseObj):
    """
    output structure of cloneAssemblyAndProcessObjects SOA
    
    :var clonedObject: Business object of new BOMLine object, created as a result of clone operation under the new
    target.
    :var serviceData: Standard Service Data
    """
    clonedObject: BusinessObject = None
    serviceData: ServiceData = None


@dataclass
class AddOrRemoveContextsInfo(TcBaseObj):
    """
    The input parameter to the operation is the target context to associate to, list of source contexts and the
    relation name to associate or disassociate with and the additional action required for association or
    disassociation.
    
    :var context: The target context to associate or disassociate with e.g. Mfg0BvrProductBOP or Mfg0BvrPlantBOP.
    :var addContext: The list of source contexts , e.g  Mfg0BvrGenericBOP or Mfg0BvrProductBOP, that should be
    associated with the target context with the specified relation.
    :var removeContext: The list of source contexts, e.g. Mfg0BvrGenericBOP or Mfg0BvrProductBOP, for which the
    association with the target context should be removed with the specified relation.
    :var actionMap: A map (string, list of string) of context and related actions. The data allows additional action
    required for the add or remove context. e.g. the key of the map will be "RemoveContext" and "AddContext" and the
    values for the key such as for the key "RemoveContext" the action will be "RemoveLink" and "RemoveAllocation".
    "RemoveLink" will remove the link between the allocations.
    "RemoveAllocation" will remove the allocations.
    """
    context: BusinessObject = None
    addContext: List[AssociatedContextInfo] = ()
    removeContext: List[AssociatedContextInfo] = ()
    actionMap: ActionMap = None


@dataclass
class EstablishOriginLinkCandidates(TcBaseObj):
    """
    Source and targets that are candidates to link
    
    :var sourceObject: The source object is either operation of type Mfg0BvrOperation or process of type Mfg0BvrProcess.
    :var targetObjects: The list of target object and its linked state.
    """
    sourceObject: BusinessObject = None
    targetObjects: List[EstablishOriginLinkTargetLinkState] = ()


@dataclass
class EstablishOriginLinkCandidatesInput(TcBaseObj):
    """
    Source and target candidates to establish origin link.
    
    :var sourceObject: Operation of type Mfg0BvrOperation or process of type Mfg0BvrProcess from Generic BOP or Product
    BOP structure. Same object type from target objects are considered to establish the origin link.
    :var targetObjects: Operation of type Mfg0BvrOperation or process of type Mfg0BvrProcess to be linked. The objects
    are in the context of Product BOP or Plant BOP.
    """
    sourceObject: BusinessObject = None
    targetObjects: List[BusinessObject] = ()


@dataclass
class EstablishOriginLinkInfo(TcBaseObj):
    """
    Input to the service is a list of a source and targets to be linked.
    
    :var inputObjects: soure and target candidates to establish origin link.
    :var criteria: The list of criteria based on which the origin link established. Currently, the only criteria
    supported is logical designator property. Possible value of parameter is "LD" signifying that all source and target
    objects with matching logical designator property are considered for the operation.
    :var considerHierarchy: Specifies whether hierarchy of source and target should be considered while establishing
    the origin link. If the value is true then child of source and target are linked based on the criteria. If false
    then child of source and target is not considered.
    :var action: Specifies whether origin link should be established between source and target. Possible values are
    "DryRun" and "Link". If value is "DryRun" then candidates are fetched without establishing the origin link. If
    value is "Link" then the source and target are linked based on criteria specified.
    """
    inputObjects: List[EstablishOriginLinkCandidatesInput] = ()
    criteria: List[str] = ()
    considerHierarchy: bool = False
    action: str = ''


@dataclass
class EstablishOriginLinkResponse(TcBaseObj):
    """
    The response contains service data and list of source and target candidates that are linked.
    
    :var candidates: The source and target objects with their linked state.
    :var serviceData: The ServiceData contains partial errors if any.
    :var logFileTicket: The file ticket containing the UID and file name for the log file generated for this command.
    """
    candidates: List[EstablishOriginLinkCandidates] = ()
    serviceData: ServiceData = None
    logFileTicket: FileTicket = None


@dataclass
class EstablishOriginLinkTargetLinkState(TcBaseObj):
    """
    This structure contains the target object and its linked state with the provided source.
    
    :var targetObject: Target object is either operation of type Mfg0BvrOperation or process of type Mfg0BvrProcess.
    :var linkState:  Flag specifying whether target is linked with the provided source.
    """
    targetObject: BusinessObject = None
    linkState: bool = False


"""
The map (string, list of string) of additional actions required for add or remove contexts operation.
"""
ActionMap = Dict[str, List[str]]


"""
Map of BOMLine objects (business object/list of business objects).
If the key is process area of type Mfg0BvrProcessArea then value is list of process resources of type Mfg0BvrProcessResource that are defined under the process area and process/operation of type Mfg0BvrProcess/Mfg0BvrOperation that are unallocated to process resource. The value may also contain children of the process area such as process line or station.

If the key is process resource of type Mfg0BvrProcessResource then values are process/operation of type Mfg0BvrProcess/Mfg0BvrOperation that are allocated to process resource.

If the key is process of type Mfg0BvrProcess then values are process/operation of type 
Mfg0BvrProcess/Mfg0BvrOperation that are child of that process. These childs are process/operation that are unallocated to any process resource. If the process itself is allocated to process resource then the value is empty list.

"""
ProcResourceRelatedInfoMap = Dict[BusinessObject, List[BusinessObject]]
