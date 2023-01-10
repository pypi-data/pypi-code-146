from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ListOfValues, WorkspaceObject, Folder, Dataset, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FormAttributesInfo(TcBaseObj):
    """
    This structure contains the Form Attributes Information.
    
    :var formType: Form Type
    :var formPDs: A list of property descriptors
    """
    formType: str = ''
    formPDs: List[FormPropDescriptor] = ()


@dataclass
class FormInfo(TcBaseObj):
    """
    Holds the Information of Form to be created or updated
    
    :var clientId: Identifier that helps the client to track the object(s) created, required; should be unique for the
    input set
    :var formObject: The Form object, if null then create; otherwise, update.
    :var parentObject: Parent object of the Form to be created
    :var relationName: Relation name between Parent and Form to be created
    :var saveDB: If true, save the Form to database
    :var name: Name of the Form to be created
    :var description: Description of the Form to be created, can be an empty string.
    :var formType: Form Type of the Form to be created
    :var attributesMap: Form property map for the Form to be updated
    """
    clientId: str = ''
    formObject: BusinessObject = None
    parentObject: BusinessObject = None
    relationName: str = ''
    saveDB: bool = False
    name: str = ''
    description: str = ''
    formType: str = ''
    attributesMap: StringArrayMap = None


@dataclass
class FormPropDescriptor(TcBaseObj):
    """
    This structure contains information for Form Properties Descriptor.
    
    :var propName: Propety name
    :var displayName: Property display name
    :var attachedSpecifier: Attached specifier
    :var maxLength: Property maximumlLength
    :var interdependentProps: A list of interdependent properties
    :var propValueType: Property value type
    :var propType: Property type
    :var isDisplayable: true if property is displayable, otherwise false
    :var isArray: true if property is an array, otherwise false
    :var lov: List of values
    :var isRequired: true if propety is required, otherwise false
    :var isEnabled: true if property is enabled, otherwise false
    :var isModifiable: true if Property is Modifiable
    """
    propName: str = ''
    displayName: str = ''
    attachedSpecifier: int = 0
    maxLength: int = 0
    interdependentProps: List[str] = ()
    propValueType: int = 0
    propType: int = 0
    isDisplayable: bool = False
    isArray: bool = False
    lov: ListOfValues = None
    isRequired: bool = False
    isEnabled: bool = False
    isModifiable: bool = False


@dataclass
class GenerateUIDResponse(TcBaseObj):
    """
    Return structure for 'generateUID' operation
    
    :var uids: List of the UIDs that were generated
    :var serviceData: Contains any errors encountered during processing in the partial errors list.
    """
    uids: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class GetDatasetCreationRelatedInfoResponse(TcBaseObj):
    """
    Holds the Response data from getDatasetCreationRelatedInfo
    
    :var toolNames: List of Tool names
    :var newDatasetName: The name of the new Dataset, can be an empty string
    :var nameCanBeModified: If true, the name of the Dataset can be modified
    :var initValuePropertyRules: List of properties have the initialized values from property constant attachments
    :var serviceData: Standard 'ServiceData' member
    """
    toolNames: List[str] = ()
    newDatasetName: str = ''
    nameCanBeModified: bool = False
    initValuePropertyRules: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class GetItemCreationRelatedInfoResponse(TcBaseObj):
    """
    This data structure contains a naming rules, property rules, form property descriptor, unit of measure, and
    ItemRevision type. Partial failure message will be returned in 'ServiceData'.
    
    :var complexValuePropertyRules: List of complex value property rules
    :var initValuePropertyRules: List of initial values
    :var patternMap: Pattern map (string/string)
    :var uoms: List of unit of measures
    :var formAttrs: List of Form attributes
    :var revTypeName: ItemRevision type name
    :var serviceData: The successful object ids, partial errors and failures
    """
    complexValuePropertyRules: List[str] = ()
    initValuePropertyRules: List[str] = ()
    patternMap: StringArrayMap = None
    uoms: List[str] = ()
    formAttrs: List[FormAttributesInfo] = ()
    revTypeName: str = ''
    serviceData: ServiceData = None


@dataclass
class GetItemFromIdInfo(TcBaseObj):
    """
    Input structure for getItemFromIdInfo, each of which contain an item id and optionally a list of revision ids which
    specify which Item Revisions to retrieve.
    
    :var itemId: Item id string for Item to retrieve, required
    :var revIds: Revision ids which specify which Item Revisions to retrieve, optional
    """
    itemId: str = ''
    revIds: List[str] = ()


@dataclass
class GetItemFromIdItemOutput(TcBaseObj):
    """
    This structure contains information for 'getItemFromId' operation.
    
    :var item: Item object reference of the item found
    :var itemRevOutput: List of 'GetItemFromIdItemRevOutput'
    """
    item: Item = None
    itemRevOutput: List[GetItemFromIdItemRevOutput] = ()


@dataclass
class GetItemFromIdItemRevOutput(TcBaseObj):
    """
    This structure contains an ItemRevision object and a list of found Dataset objects.
    
    :var itemRevision: ItemRevision object reference of the item revision found
    :var datasets: List of Dataset object references found
    """
    itemRevision: ItemRevision = None
    datasets: List[Dataset] = ()


@dataclass
class GetItemFromIdPref(TcBaseObj):
    """
    Input structure for 'getItemFromAttribute' used to filter the returned ItemRevision objects.
    
    :var prefs: A list of 'RelationFilter' structures for determining which ItemRevision objects to return
    """
    prefs: List[RelationFilter] = ()


@dataclass
class GetItemFromIdResponse(TcBaseObj):
    """
    Return structure for getItemFromId operation
    
    :var output: List of GetItemFromIdItemOutput
    :var serviceData: Standard ServiceData member
    """
    output: List[GetItemFromIdItemOutput] = ()
    serviceData: ServiceData = None


@dataclass
class MoveToNewFolderInfo(TcBaseObj):
    """
    Input structure for the 'moveToNewFolder' operation.
    
    
    :var oldFolder: Folder object reference of the old folder, whose content is going to move to new folder.
    :var newFolder: Folder object reference of the new folder, where object content is going to move, required. If not
    specified, processing will continue to the new input.
    :var objectsToMove: List of object references to be moved from the old folder to the new folder or copied to the
    new folder, required. If not specified, processing will continue to the next input.
    """
    oldFolder: Folder = None
    newFolder: Folder = None
    objectsToMove: List[BusinessObject] = ()


@dataclass
class MoveToNewFolderResponse(TcBaseObj):
    """
    Return structure for the 'moveToNewFolder' operation.
    
    
    :var serviceData: Contains the updated old folder, the new folder, and partial errors from this operation.
    """
    serviceData: ServiceData = None


@dataclass
class RelationFilter(TcBaseObj):
    """
    A filter for determining which ItemRevision objects to return.
    
    :var relationTypeName: The  relation type name that specifies the relation that relates the ItemRevision to the
    Dataset.
    :var objectTypeNames: A list of  Dataset object type names to return
    """
    relationTypeName: str = ''
    objectTypeNames: List[str] = ()


@dataclass
class SaveAsNewItemInfo(TcBaseObj):
    """
    Input structure for saveAsNewItem operation
    
    :var clientId: Used to uniquely identify the input (Required)
    :var itemRevision: Original Item Revision to be used for the SaveAsNewItem operation (Required)
    :var itemId: Item id string for creating new item, optional
    :var revId: Revision id string for creating new revision, optional
    :var name: Name string for creating new item/revision, optional
    :var description: Description string for creating new item/revision, optional
    :var folder: Folder object reference to attach Item to, if null, the Item will go to the default preference
    location for created objects.
    """
    clientId: str = ''
    itemRevision: ItemRevision = None
    itemId: str = ''
    revId: str = ''
    name: str = ''
    description: str = ''
    folder: Folder = None


@dataclass
class SaveAsNewItemOutput(TcBaseObj):
    """
    The data strucutre contains newly created object inforamtiobn.
    
    :var item: New Item object
    :var itemRev: New ItemRevision object
    """
    item: Item = None
    itemRev: ItemRevision = None


@dataclass
class SaveAsNewItemResponse(TcBaseObj):
    """
    The data structure contains return information for the operation.
    
    :var inputToNewItem: Map whose keys are the input clientIds and output values (newly created Item and ItemRevision
    objects) pairs ('string', 'SaveAsNewItemOutput')
    :var serviceData: Service data
    """
    inputToNewItem: InputToNewItemMap = None
    serviceData: ServiceData = None


@dataclass
class VecStruct(TcBaseObj):
    """
    This structure contains string list.
    
    :var stringVec: A list of strings
    """
    stringVec: List[str] = ()


@dataclass
class WhereReferencedInfo(TcBaseObj):
    """
    This data structure contains output information of referencer, relation and level.
    
    :var referencer: WorkspaceObject that references the input object
    :var relation: String name of the relation between the reference and the input object
    :var level: Level at which referencer was found.
    """
    referencer: WorkspaceObject = None
    relation: str = ''
    level: int = 0


@dataclass
class WhereReferencedOutput(TcBaseObj):
    """
    This data structure contains output information of reference, relation name and level for given input objects.
    
    :var inputObject: WorkspaceObject that is referenced by info
    :var info: Output information containing reference, relation name and level for 'inputObject'
    """
    inputObject: WorkspaceObject = None
    info: List[WhereReferencedInfo] = ()


@dataclass
class WhereReferencedResponse(TcBaseObj):
    """
    This data structure contains output information for a list of where referenced objects.
    
    :var output: List of information containing reference, relation name and level for input object
    :var serviceData: Service data
    """
    output: List[WhereReferencedOutput] = ()
    serviceData: ServiceData = None


@dataclass
class WhereUsedOutput(TcBaseObj):
    """
    This structure contains information for 'WhereUsedOutput'.
    
    :var inputObject: Input WorkspaceObject object reference for mapping to the output
    :var info: List of 'WhereUsedParentInfo' structures
    """
    inputObject: WorkspaceObject = None
    info: List[WhereUsedParentInfo] = ()


@dataclass
class WhereUsedParentInfo(TcBaseObj):
    """
    This structure contains Generic Parent Info.
    
    :var parentItemRev: Parent ItemRevision object reference which uses the given object
    :var level: The level at which the parent ItemRevision was found
    """
    parentItemRev: ItemRevision = None
    level: int = 0


@dataclass
class WhereUsedResponse(TcBaseObj):
    """
    'WhereUsedResponse' contains list of 'WhereUsedOutput'  structure. This structure contains list of Item and
    ItemRevision objects which are results of 'whereUsed' search.
    
    :var output: List of WhereUsedOutput structures
    :var serviceData: Standard 'ServiceData' member
    """
    output: List[WhereUsedOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateFormsOutput(TcBaseObj):
    """
    This structure contains newly created form or updated form information.
    
    :var clientId: Identifier that helps the client to track the object(s) created or updated.
    :var form: The Form object created or updated
    """
    clientId: str = ''
    form: BusinessObject = None


@dataclass
class CreateOrUpdateFormsResponse(TcBaseObj):
    """
    Holds the Response of created or updated Forms
    
    :var outputs: List of created or updated Form objects
    :var serviceData: Standard 'ServiceData' member
    """
    outputs: List[CreateFormsOutput] = ()
    serviceData: ServiceData = None


"""
A map of 'InputToNewItem' '(string, SaveAsNewItemOutput').
"""
InputToNewItemMap = Dict[str, SaveAsNewItemOutput]


"""
A map of attribute names and desired value pairs (string/VecStruct).
"""
NameValueMap = Dict[str, VecStruct]


"""
Map of string array property names to values ('string, vector<string>').
"""
StringArrayMap = Dict[str, List[str]]
