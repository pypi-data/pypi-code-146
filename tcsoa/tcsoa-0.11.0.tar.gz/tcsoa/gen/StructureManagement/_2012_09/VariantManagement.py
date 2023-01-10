from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, ItemRevision
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExtendedAttributes(TcBaseObj):
    """
    Structure to collect additional attributes to be assigned apart from default 'Save As' or 'Cretae New' Item
    operation.
    
    :var objectType: Type of Business Object.
    :var attributes: Map of attribute name and its value. pairs( String, String )
    """
    objectType: str = ''
    attributes: AttributeNameValueMap = None


@dataclass
class ItemProperties(TcBaseObj):
    """
    Specifies attributes for the new Item or ItemRevision. Mainly used in 'Create new Item' scenario, describes
    specific attributes to be assigned.
    
    :var clientId: Identifier that helps the client to track the object(s) created
    :var itemId: Id of the Item to be created
    :var name: Name of the Item to be created
    :var type: Business Object type of the Item to be created
    :var revId: Id of the initial revision of the Item to be created
    :var uom: UOM of the Item to be created
    :var description: Description of the Item to be created
    :var extendedAttributes: List of ''extendedAttributes'' structures having Name/value pairs for additional
    attributes to set.
    """
    clientId: str = ''
    itemId: str = ''
    name: str = ''
    type: str = ''
    revId: str = ''
    uom: str = ''
    description: str = ''
    extendedAttributes: List[ExtendedAttributes] = ()


@dataclass
class SaveAsIn(TcBaseObj):
    """
    Input for save as operation
    
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
    Structure encapsulating all information related to a Workspace Object which may be required for "Save As" operation
    during operations ''createVariantItem'' or ''createAndSubstituteVariantItem''.
    
    :var boName: Type Name Of Business Object
    :var stringProps: Map containing string property values . Pairs (string, string)
    :var boolArrayProps: Map containing boolean array property values. Pairs (string, boolean[])
    :var dateProps: Map containing date property values. Pairs (string, Date)
    :var dateArrayProps: Map containing date array property values . Pairs (string, Date[])
    :var tagProps: Map containing tag property values. Pairs (string, Tag)
    :var tagArrayProps: Map containing tag array property values. Pairs (string, Tag[])
    :var stringArrayProps: Map containing string array property values. Pairs (string, string[])
    :var doubleProps: Map containing double property values. Pairs (string, double)
    :var doubleArrayProps: Map containing double array property values. Pairs (string,  double[])
    :var floatProps: Map containing float property values. Pairs (string, float)
    :var floatArrayProps: Map containing float array property values. Pairs (string, float[])
    :var intProps: Map containing integer property values. Pairs (string, integer)
    :var intArrayProps: Map containing integer array property values. Pairs (string, integer[])
    :var boolProps: Map containing boolean property values. Pairs (string, boolean)
    """
    boName: str = ''
    stringProps: StringMap = None
    boolArrayProps: BoolVectorMap = None
    dateProps: DateMap = None
    dateArrayProps: DateVectorMap = None
    tagProps: TagMap = None
    tagArrayProps: TagVectorMap = None
    stringArrayProps: StringVectorMap = None
    doubleProps: DoubleMap = None
    doubleArrayProps: DoubleVectorMap = None
    floatProps: FloatMap = None
    floatArrayProps: FloatVectorMap = None
    intProps: IntMap = None
    intArrayProps: IntVectorMap = None
    boolProps: BoolMap = None


@dataclass
class CreateAndSubsVIInput(TcBaseObj):
    """
    Input structure for operation ''createAndSubstituteVariantItem''. One structure represents One new variant Item to
    be created.
    
    :var genericBOMLine: BOMLine of configured structure from which new variant Item Structure should be created. This
    structure has Variants defined and can be configured for some given variant Configuration. For more details please
    refer section 'Creating and updating variant Items' from Teamcenter Documentation.
    :var createOrSaveAsDescriptor: Create or SaveAs description required for Item Creation. This will include
    information about new variant Item creation such as Item Id, name, description, objects that need to be copied or
    done 'Save As' along with new Item.
    :var viBOMLine: BOMLine of variant Item structure. After creating new variant Item from genericBOMLine, the newly
    created variant ItemRevision will be substituted on this viBOMLine.
    :var linkVIToGenericItem: Flag to decide Variant Item should be linked to its generic structure or not. Value of
    this parameter will be overriden by preference ''PSEIsNewVILinkedToModule'', if exists on SITE level.
    :var findVIBeforeCreate: Find existing Variant Item before creating new Variant Item. If existing Variant Item is
    found, then new Variant Item is not created. This existing Variant Item will be replaced on viBOMLine.
    """
    genericBOMLine: BOMLine = None
    createOrSaveAsDescriptor: CreateOrSaveAsDescriptor = None
    viBOMLine: BOMLine = None
    linkVIToGenericItem: bool = False
    findVIBeforeCreate: bool = False


@dataclass
class CreateAndSubsVIOutput(TcBaseObj):
    """
    Output structure for 'CreateAndSubstituteVI' SOA
    
    :var genericBOMLine: Generic BOMLine from which variant Item is created.
    :var viBOMLine: BOMLine of variant Item structure. After creating new variant Item from 'genericBOMLine', the newly
    created variant ItemRevision will be substituted on this 'viBOMLine'.
    :var newVariantItemRevision: ItemRevision of newly created Variant Item.
    :var isExistingVIFound: This flag will be returned populated only when flag ''findVIBeforeCreate'' in server input
    ''CreateAndSubsVIInput'' is passed as 'True'. Flag to indicate that if existing Variant Item was not found and new
    Variant Item is created. If value is true, this means existing Variant Item was found, and was used for substitute
    operation.
    """
    genericBOMLine: BOMLine = None
    viBOMLine: BOMLine = None
    newVariantItemRevision: ItemRevision = None
    isExistingVIFound: bool = False


@dataclass
class CreateAndSubsVIResponse(TcBaseObj):
    """
    Response structure to operation ''createAndSubstituteVariantItem''.
    
    :var createAndSubsOutputs: List of 'CreateAndSubsVIOutput' s for each 'CreateAndSubsVIInput'.
    :var serviceData: Service Data to return error back to caller.
    """
    createAndSubsOutputs: List[CreateAndSubsVIOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrSaveAsDescriptor(TcBaseObj):
    """
    This is helper structure to collect all information of new variant Item required for either creating New Item or
    saving existing Item as variant Item.
    
    :var properties: Input properties for new variant Item.
    :var saveAsIn: Input for save as operation
    :var bCreateOrSaveAsFlag: bool flag to indicate Create new Item as true and "Save as" operation as false value.
    """
    properties: List[ItemProperties] = ()
    saveAsIn: SaveAsIn = None
    bCreateOrSaveAsFlag: bool = False


@dataclass
class CreateVIInput(TcBaseObj):
    """
    Input Structure for operation ''createVariantItem''.
    
    :var genericBOMLine: BOMLine of configured structure from which new variant Item Structure should be created. This
    structure has Variants defined and can be configured for some given variant Configuration. For more details please
    refer section 'Creating and updating variant Items' from Teamcenter Documentation.
    :var createOrSaveAsDescriptor: Create or SaveAs description required for Item Creation. This will include
    information about new variant Item creation such as Item Id, name, description, objects that need to be copied or
    done 'Save As' along with new Item.
    :var linkVIToGenericItem: Flag to decide variant Item should be linked to its generic structure or not. Value of
    this parameter will be overridden by preference 'PSEIsNewVILinkedToModule', if exists on SITE location.
    """
    genericBOMLine: BOMLine = None
    createOrSaveAsDescriptor: CreateOrSaveAsDescriptor = None
    linkVIToGenericItem: bool = False


@dataclass
class CreateVIOutput(TcBaseObj):
    """
    Output structure for operation ''createVariantItem''. There will be one 'CreateVIOutput' for each 'CreateVIInput'.
    
    :var genericBOMLine: BOM Line of configured structure from which new Variant Item Structure should be created. This
    structure has Variants defined and can be configured for some given Variant Configuration. For more details please
    refer section 'Creating and updating variant items' from Teamcenter Documentation.
    :var newVariantItemRevision: Item Revision of newly created Variant Item.
    """
    genericBOMLine: BOMLine = None
    newVariantItemRevision: ItemRevision = None


@dataclass
class CreateVIResponse(TcBaseObj):
    """
    Response structure for operation ''createVariantItem''
    
    :var createVariantItemOutput: List of outputs one each for ''CreateVIInput''
    :var serviceData: Service Data to return error back to caller.
    """
    createVariantItemOutput: List[CreateVIOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DeepCopyData(TcBaseObj):
    """
    Structure to collect information about objects which should be copied or referenced in new variant Item.
    
    :var attachedObject: Other side object
    :var propertyName: Name of relation type or reference property for which DeepCopy rule is configured
    :var propertyType: Name of relation type or reference property for which DeepCopy rule is configured
    :var copyAction: DeepCopy action [NoCopy, CopyAsReference, CopyAsObject or Select]
    :var isTargetPrimary: Flag indicating if target object is primary or secondary
    :var isRequired: If this flag is false, the copy action can be dynamically changed by user
    :var copyRelations: This is a Boolean representing whether the Properties on the Relation if any in the Relation
    that exists between
    :var saveAsInputTypeName: SaveAsInput type name
    :var saveAsInput: SaveAsInput field to capture user inputs on the SaveAs dialog. NOTE: This field is unused in the
    getSaveAsDesc operation. It is used in the saveAsObjects operation
    :var childDeepCopyData: Vector of DeepCopy data for the secondary objects on the other side
    """
    attachedObject: BusinessObject = None
    propertyName: str = ''
    propertyType: PropertyType = None
    copyAction: str = ''
    isTargetPrimary: bool = False
    isRequired: bool = False
    copyRelations: bool = False
    saveAsInputTypeName: str = ''
    saveAsInput: SaveAsInput = None
    childDeepCopyData: List[DeepCopyData] = ()


class PropertyType(Enum):
    """
    Enumeration of the different property types for which DeepCopy Rule  configuration is enabled
    """
    Relation = 'Relation'
    Reference = 'Reference'


"""
DateMap
"""
DateMap = Dict[str, datetime]


"""
DateVectorMap
"""
DateVectorMap = Dict[str, List[datetime]]


"""
DoubleMap
"""
DoubleMap = Dict[str, float]


"""
DoubleVectorMap
"""
DoubleVectorMap = Dict[str, List[float]]


"""
FloatMap
"""
FloatMap = Dict[str, float]


"""
FloatVectorMap
"""
FloatVectorMap = Dict[str, List[float]]


"""
IntMap
"""
IntMap = Dict[str, int]


"""
IntVectorMap
"""
IntVectorMap = Dict[str, List[int]]


"""
AttributeNameValueMap
"""
AttributeNameValueMap = Dict[str, str]


"""
Map containing string property values
"""
StringMap = Dict[str, str]


"""
BoolMap
"""
BoolMap = Dict[str, bool]


"""
StringVectorMap
"""
StringVectorMap = Dict[str, List[str]]


"""
TagMap
"""
TagMap = Dict[str, BusinessObject]


"""
BoolVectorMap
"""
BoolVectorMap = Dict[str, List[bool]]


"""
TagVectorMap
"""
TagVectorMap = Dict[str, List[BusinessObject]]
