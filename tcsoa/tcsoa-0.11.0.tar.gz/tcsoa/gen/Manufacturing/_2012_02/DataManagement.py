from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileTicket(TcBaseObj):
    """
    To represent a file ticket and its original file name.
    
    :var ticket: The FMS file Ticket.
    :var fileName: The original file name.
    """
    ticket: str = ''
    fileName: str = ''


@dataclass
class GeneralInfo(TcBaseObj):
    """
    Holds all additional flags that are needed for the connect like quantity (number of occurrences),  copy predecessor
    flag, copy occurrence type from the source flag, propagate XForm flag.
    
    :var stringProps: Map containing string property values
    :var stringArrayProps: Map containing string array property values
    :var dateProps: Map containing DateTime property values
    :var dateArrayProps: Map containing DateTime array property values
    :var tagProps: Map containing string property values
    :var tagArrayProps: Map containing string array property values
    :var doubleProps: Map containing string property values
    :var doubleArrayProps: Map containing string array property values
    :var floatProps: Map containing string property values
    :var floatArrayProps: Map containing string array property values
    :var intProps: Map containing string property values
    :var intArrayProps: Map containing string array property values
    :var boolProps: Map containing string property values
    :var boolArrayProps: Map containing string array property values
    """
    stringProps: StringMap1 = None
    stringArrayProps: StringVectorMap1 = None
    dateProps: DateMap1 = None
    dateArrayProps: DateVectorMap1 = None
    tagProps: TagMap1 = None
    tagArrayProps: TagVectorMap1 = None
    doubleProps: DoubleMap1 = None
    doubleArrayProps: DoubleVectorMap1 = None
    floatProps: FloatMap1 = None
    floatArrayProps: FloatVectorMap1 = None
    intProps: IntMap1 = None
    intArrayProps: IntVectorMap1 = None
    boolProps: BoolMap1 = None
    boolArrayProps: BoolVectorMap1 = None


@dataclass
class GetAssociatedContextsInputData(TcBaseObj):
    """
    GetAssociatedContextsInputData
    
    :var associateToContext: associateToContext
    :var relationName: relationName
    """
    associateToContext: BusinessObject = None
    relationName: List[str] = ()


@dataclass
class AssociateAndAllocateInput(TcBaseObj):
    """
    Input for the automatic allocation commands such as automaticAssociateAndAllocate, associateAndAllocatePreview and
    associateAndAllocateByPreview command.
    
    :var sourceProductBOP: Source Product BOP for which allocate command was called
    :var targetPlantBOPLines: Target Plant BOP's lines to which the allocation is to be done.
    :var referenceProductBOP: Reference Product BOP according to which allocation is to be done.
    """
    sourceProductBOP: BusinessObject = None
    targetPlantBOPLines: List[BusinessObject] = ()
    referenceProductBOP: BusinessObject = None


@dataclass
class AssociateAndAllocateResponse(TcBaseObj):
    """
    Response for the automatic allocation commands such as automaticAssociateAndAllocate, and
    associateAndAllocateByPreview.
    
    :var serviceData: Service data will hold partial errors, warnings  and errors, if any.
    :var logFileTicket: File Ticket Containing the UID and file name for the Log File generated for this command.
    """
    serviceData: ServiceData = None
    logFileTicket: FileTicket = None


@dataclass
class AssociateOutput(TcBaseObj):
    """
    Associated BOMLines to the input context
    
    :var context: Input context
    :var associatedContextsInfo: vector of pairs of contexts and relation name that are associated with the input
    context
    """
    context: BusinessObject = None
    associatedContextsInfo: List[AssociatedContextInfo] = ()


@dataclass
class AssociatedContextInfo(TcBaseObj):
    """
    AssociatedContextInfo
    
    :var context: context  The added (source) context that should be associated (linked) associate to target context
    (associateToContext parameter).
    :var relationName: relationName  The relation to use to connect. If the string is empty then the relation defined
    as default will be used. It should be possible to define the default association relation for each pair of types.
    """
    context: BusinessObject = None
    relationName: str = ''


@dataclass
class AssociationResponse(TcBaseObj):
    """
    Contains a list of items tags representing the associated BOMLines with the given context.
    
    :var output: A vector of BOMLines associated to the input context
    :var serviceData: Partial errors mapped to the client id
    """
    output: List[AssociateOutput] = ()
    serviceData: ServiceData = None


@dataclass
class AutomaticAllocatePreviewResponse(TcBaseObj):
    """
    Response for the automatic allocation commands automaticAllocatePreview.
    
    :var serviceData: Service data will hold partial errors, warnings  and errors, if any.
    :var previewFileTicket: File Ticket Containing the UID and file name for the CSV File generated for preview during
    this command.
    :var allocationMap: Map of allocations from the source structure to the target structure.
    """
    serviceData: ServiceData = None
    previewFileTicket: FileTicket = None
    allocationMap: AllocationMap = None


@dataclass
class SourceInfo(TcBaseObj):
    """
    contains all needed information in order to connect source BOMLines to the target
    
    :var sourceObjects: BOMLines to connect the target
    :var relationType: occurrence type for new assigned line. If its empty  server will use the default occurrence type
    :var relationName: The relation for the connect. If the string is empty then the default relation will be defined
    and used by the server
    :var additionalInfo: Holds all additional flags that are needed for connect like quantity (number of occurrences), 
    copy predecessor flag, copy occurrence type from the source flag, propagate XForm flag. Can be easily extended
    without changing the signature of the SOA
    """
    sourceObjects: List[BusinessObject] = ()
    relationType: str = ''
    relationName: str = ''
    additionalInfo: GeneralInfo = None


@dataclass
class ConnectObjectResponse(TcBaseObj):
    """
    ConnectObjectResponse
    
    :var newObjects: new BOMLines, created as a result of connection operation under the new target BOMLines
    :var serviceData: serviceData
    """
    newObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class ConnectObjectsInputData(TcBaseObj):
    """
    A list of ConnectInput BOMLines for the nodes to be connect
    
    :var targetObjects: BOMLines to connect with. Can be a vector as a result of the multiple selection of the targets
    :var sourceInfo: all needed information in order to connect source BOMLines to the target
    """
    targetObjects: List[BusinessObject] = ()
    sourceInfo: SourceInfo = None


@dataclass
class AddAssociationInput(TcBaseObj):
    """
    BOMLines for the contexts to be associated
    
    :var associateToContext: target (primary) context to associate (link) to.
    :var addedContexts: vector of contexts info that are going to be associated(added) to the target.
    """
    associateToContext: BusinessObject = None
    addedContexts: List[AssociatedContextInfo] = ()


@dataclass
class DisconnectFromOriginInputData(TcBaseObj):
    """
    Input structure for DisconnectFromOrigin Command
    
    :var lineToDisconnect: Plant BOP or Product BOP line that needs to be disconnected from their origin.
    :var isRecursive: Flag specifying whether the sub-processes and sub-operations are to be disconnected recursively.
    """
    lineToDisconnect: BusinessObject = None
    isRecursive: bool = False


"""
DateMap
"""
DateMap1 = Dict[str, datetime]


"""
DateVectorMap
"""
DateVectorMap1 = Dict[str, List[datetime]]


"""
DoubleMap
"""
DoubleMap1 = Dict[str, float]


"""
DoubleVectorMap
"""
DoubleVectorMap1 = Dict[str, List[float]]


"""
FloatMap
"""
FloatMap1 = Dict[str, float]


"""
FloatVectorMap
"""
FloatVectorMap1 = Dict[str, List[float]]


"""
IntMap
"""
IntMap1 = Dict[str, int]


"""
IntVectorMap
"""
IntVectorMap1 = Dict[str, List[int]]


"""
StringMap
"""
StringMap1 = Dict[str, str]


"""
BoolMap
"""
BoolMap1 = Dict[str, bool]


"""
StringVectorMap
"""
StringVectorMap1 = Dict[str, List[str]]


"""
TagMap
"""
TagMap1 = Dict[str, BusinessObject]


"""
TagVectorMap
"""
TagVectorMap1 = Dict[str, List[BusinessObject]]


"""
BoolVectorMap
"""
BoolVectorMap1 = Dict[str, List[bool]]


"""
Map of allocations from the source structure to the target structure. Relevant to the commands such as associateAndAllocateByPreview
"""
AllocationMap = Dict[BusinessObject, List[BusinessObject]]
