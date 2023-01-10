from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, PSBOMView, Item, WorkspaceObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ObjectInfo(TcBaseObj):
    """
    This structure holds object information of parent object of trace link in Report structure.
    
    :var contextName: This parameter will hold the name of context for source or target object of Trace Link.
    :var displayObj: If the Trace Link is created on the occurrence then this variable will represent the object to
    show in the Trace Report.
    :var object: This object represent any Business Object in Teamcenter on which Trace Link is created
    :var bomView: This field represents the BOM View of context line for the Trace Link.
    """
    contextName: str = ''
    displayObj: WorkspaceObject = None
    object: BusinessObject = None
    bomView: PSBOMView = None


@dataclass
class Report(TcBaseObj):
    """
    This structure holds information each trace link report with information of parent object, and its children
    associated with trace link relation.
    
    :var parent: Parent object of trace link.
    :var children: list of all child objects for the parent with trace link relation
    """
    parent: ObjectInfo = None
    children: List[ObjectInfo] = ()


@dataclass
class SaveAsIn(TcBaseObj):
    """
    'SaveAsI'n structure contains the object to be saved and the corresponding 'DeepCopyData' of the attached objects
    of the object to be saved.
    
    :var targetObject: Target object being saved as
    :var saveAsInput: SaveAsInput (user input from SaveAs dialog) for the targetobject being saved as
    :var deepCopyDatas: DeepCopyData of the objects attached to the targetobject
    """
    targetObject: BusinessObject = None
    saveAsInput: SaveAsInput = None
    deepCopyDatas: List[DeepCopyData] = ()


@dataclass
class SaveAsInput(TcBaseObj):
    """
    This structure is used to capture the inputs required for savingof a business object.
    
    :var boName: Business object type name
    :var stringProps: Map of string property names to values ('string, string')
    :var boolArrayProps: Map of boolean array property names to values ('string, vector<bool>')
    :var dateProps: Map of DateTime property names to values ('string, DateTime')
    :var dateArrayProps: Map of DateTime array property names to values ('string, vector<DateTime>')
    :var tagProps: Map of BusinessObject property names to values ('string, BusinessObject')
    :var tagArrayProps: Map of BusinessObject array property names to values ('string, vector<BusinessObject>')
    :var stringArrayProps: Map of string array property names to values ('string, vector<string>')
    :var doubleProps: Map of double property names to values ('string, double')
    :var doubleArrayProps: Map of double array property names to values ('string, vector<double>')
    :var floatProps: Map of float property names to values '(string, float')
    :var floatArrayProps: Map of float array property names to values ('string, vector<float>')
    :var intProps: Map of int property names to values ('string, int')
    :var intArrayProps: Map of int array property names to values ('string, vector<int>')
    :var boolProps: Map of boolean property names to values ('string, bool')
    """
    boName: str = ''
    stringProps: StringMap1 = None
    boolArrayProps: BoolVectorMap1 = None
    dateProps: DateMap1 = None
    dateArrayProps: DateVectorMap1 = None
    tagProps: TagMap1 = None
    tagArrayProps: TagVectorMap1 = None
    stringArrayProps: StringVectorMap1 = None
    doubleProps: DoubleMap1 = None
    doubleArrayProps: DoubleVectorMap1 = None
    floatProps: FloatMap1 = None
    floatArrayProps: FloatVectorMap1 = None
    intProps: IntMap1 = None
    intArrayProps: IntVectorMap1 = None
    boolProps: BoolMap1 = None


@dataclass
class SaveAsObjectsResponse(TcBaseObj):
    """
    This structure contains a vector corresponding to the input target objects that holds mapping between the original
    objects and the saved objects.
    
    :var output: SaveAsout vector
    :var saveAsTrees: List of the input target objects that holds mapping between the original objects and the copied 
    objects.
    :var serviceData: Service data containing created objects, errors, etc
    """
    output: List[SaveAsOut] = ()
    saveAsTrees: List[SaveAsTree] = ()
    serviceData: ServiceData = None


@dataclass
class SaveAsOut(TcBaseObj):
    """
    This structure contains information for 'SaveAs' operation including unique target object.
    
    :var targetObject: BusinessObject name
    :var objects: Input data for 'SaveAs' Operation
    """
    targetObject: BusinessObject = None
    objects: List[BusinessObject] = ()


@dataclass
class SaveAsTree(TcBaseObj):
    """
    This structure contains tree structure for 'SaveAs'.
    
    :var originalObject: Original object being saved as
    :var objectCopy: Object copy after 'SaveAs'. This could be NULL if no copy was made or same as original object if
    the copy is a reference to the original
    :var childSaveAsNodes: Nested information for next level of the tree
    """
    originalObject: BusinessObject = None
    objectCopy: BusinessObject = None
    childSaveAsNodes: List[SaveAsTree] = ()


@dataclass
class TraceReport(TcBaseObj):
    """
    This structure holds information about generated trace reports with defining and complying trace trees with
    selected objects, and its persistent objects.
    
    :var definingTree: Represents the Defining Tree in the Trace Report giving all defining trace link details.
    :var indirectDefiningTree: Represents an Indirect Defining Tree in the Trace  Report.
    :var complyingTree: Represents the Complying Tree in the Trace Report giving all complying trace link details.
    :var indirectComplyingTree: Represents an Indirect Complying Tree in the Trace Report
    :var selectedObject: Represents selected object for which Trace Report generated.
    :var persistentObjects: Represents persistent object for the selected object for which Trace Report generated.
    """
    definingTree: List[Report] = ()
    indirectDefiningTree: List[Report] = ()
    complyingTree: List[Report] = ()
    indirectComplyingTree: List[Report] = ()
    selectedObject: BusinessObject = None
    persistentObjects: List[BusinessObject] = ()


@dataclass
class TraceabilityInfoInput(TcBaseObj):
    """
    Information required to generate a trace report, it includes objects for which this trace report should be
    generated, type of trace report, if indirect trace link included, and type of base relation of trace link.
    
    :var selectedObjs: List of objects on which to generate the Trace Report.
    :var reportType: Type of Report that is defining, complying, or both. Below are 
                    allowed values
                    1 for Complying Report  
                    2 for Defining Report
                    3 for Complete Report
    :var reportDepth: Level to which Trace Report should be generated. The allowed value is any number greater than
    zero.
    :var isIndirectTraceReportNeeded: If this variable is true then only Indirect Trace Report will be 
    included in the final Trace Report.
    :var relationTypeName: The Trace Report will be generated for this type of relations, the type should be
    FND_TraceLink or its subtype.
    """
    selectedObjs: List[BusinessObject] = ()
    reportType: int = 0
    reportDepth: int = 0
    isIndirectTraceReportNeeded: bool = False
    relationTypeName: str = ''


@dataclass
class TraceabilityReportOutput(TcBaseObj):
    """
    TraceabilityReportOutput structure holds information about generated trace reports with defining and complying
    trace trees with selected objects and its persistent objects, including service data.
    
    :var traceReports: This member holds all the Trace Reports user has asked for. This is vector of 
    TraceReport type of structures.
    :var serviceData: Service Data.
    """
    traceReports: List[TraceReport] = ()
    serviceData: ServiceData = None


@dataclass
class ValidateRevIdsInfo(TcBaseObj):
    """
    Input structure for 'validateRevIds' operation. It contains the revision id to be validated along with information
    about the object and object type.
    
    :var revId: Input Revision id to be validated.
    :var itemObject: Item object for which revision id needs to be validated. For new a Item to be created this
    property must be set to null.
    :var itemType: String describing the type of the Item for which the identifier is being validated.
    """
    revId: str = ''
    itemObject: Item = None
    itemType: str = ''


@dataclass
class ValidateRevIdsOutput(TcBaseObj):
    """
    This structure contains the modified revision id and enum status of the id.  Valid values for the enums are Valid
    (ids are valid), Invalid (ids are not valid), Modified (ids are not ideal but can be used if the user really wants
    them), Override (ids are not valid, silently replace with modified ones), and Duplicate (ids are already allocated
    in the system).
    
    :var modRevId: Modified rev id if specified by Naming Rules/Revision Naming Rules.
    :var revIdStatus: Status of the revision id represented as a 'ValidateRevIdsStatus' enum.
    """
    modRevId: str = ''
    revIdStatus: ValidateRevIdsStatus = None


@dataclass
class ValidateRevIdsResponse(TcBaseObj):
    """
    Response structure for 'validateRevIds' service operation.
    
    :var output: List of 'ValidateRevIdsOutput' structures, which contain the modified revision id and the validation
    status of the input revision id.
    :var serviceData: Standard 'ServiceData' structure. It contains partial errors and failures along with the
    clientIds.
    """
    output: List[ValidateRevIdsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DeepCopyData(TcBaseObj):
    """
    DeepCopyData definition
    
    :var attachedObject: Other side object
    :var propertyName: Name of relation type or reference property for which DeepCopy rule is configured
    :var propertyType: enumeration value indicating if DeepCopyRule is configured for Relation or Reference property
    :var copyAction: DeepCopy action [NoCopy, CopyAsReference, CopyAsObject or Select]
    :var isTargetPrimary: Flag indicating if target object is primary or secondary
    :var isRequired: If this flag is false, the copy action can be dynamicaly changed by user
    :var copyRelations: This is a Boolean representing whether the Properties on the Relation if any in the Relation
    that exists between
    :var saveAsInputTypeName: SaveAsInput type name
    :var childDeepCopyData: Vector of DeepCopy data for the secondary objects on the other side
    :var saveAsInput: SaveAsInput field to capture user inputs on the SaveAs dialog. NOTE: This field is unused in the
    getSaveAsDesc operation. It is used in the saveAsObjects operation
    """
    attachedObject: BusinessObject = None
    propertyName: str = ''
    propertyType: PropertyType = None
    copyAction: str = ''
    isTargetPrimary: bool = False
    isRequired: bool = False
    copyRelations: bool = False
    saveAsInputTypeName: str = ''
    childDeepCopyData: List[DeepCopyData] = ()
    saveAsInput: SaveAsInput = None


class PropertyType(Enum):
    """
    Map of the enumeration of the different property types for which DeepCopy Rule configuration is enabled.
    """
    Relation = 'Relation'
    Reference = 'Reference'


class ValidateRevIdsStatus(Enum):
    """
    Revision Id status enum after validation against Naming Rules/Revision Naming Rules.
    Meanings of the enum values are as follows:
    - ValidRevID            Revision Id is valid.
    - InvalidRevID            Revision Id is not valid. Do not allow the user to create a revision with this revision
    id.
    - ModifiedRevID        Revision Id is not valid. However, allow user to create revision with this id if they really
    want to.
    - OverrideRevID        Revision Id was not valid. Use the modified versions without telling the user. (Useful for
    case conversions)
    - DuplicateRevID        Revision Id is not valid, because it is already in use.
    
    """
    ValidRevID = 'ValidRevID'
    InvalidRevID = 'InvalidRevID'
    ModifiedRevID = 'ModifiedRevID'
    OverrideRevID = 'OverrideRevID'
    DuplicateRevID = 'DuplicateRevID'


"""
DateMap1
"""
DateMap1 = Dict[str, datetime]


"""
Map of DateTime array property names to values ('string, vector< DateTime>').
"""
DateVectorMap1 = Dict[str, List[datetime]]


"""
DoubleMap1
"""
DoubleMap1 = Dict[str, float]


"""
Map of double array property names to values ('string, vector< double>').
"""
DoubleVectorMap1 = Dict[str, List[float]]


"""
Map of float property names to values ('string, float').
"""
FloatMap1 = Dict[str, float]


"""
Map of float array property names to values ('string, vector<float>').
"""
FloatVectorMap1 = Dict[str, List[float]]


"""
Map of int property names to values ('string, int').
"""
IntMap1 = Dict[str, int]


"""
Map of int array property names to values ('string, vector< int>').
"""
IntVectorMap1 = Dict[str, List[int]]


"""
Map of BusinessObject property names to values ('string, BusinessObject').
"""
StringMap1 = Dict[str, str]


"""
Map of bool property names to values '(string, bool').
"""
BoolMap1 = Dict[str, bool]


"""
StringVectorMap1
"""
StringVectorMap1 = Dict[str, List[str]]


"""
TagMap1
"""
TagMap1 = Dict[str, BusinessObject]


"""
Map of BusinessObject array property names to values '(string, vector< BusinessObject >').
"""
TagVectorMap1 = Dict[str, List[BusinessObject]]


"""
Map of bool array property names to values ('string, vector< bool >').
"""
BoolVectorMap1 = Dict[str, List[bool]]
