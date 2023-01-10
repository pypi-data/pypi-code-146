from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Folder, Item, Form, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MasterFormPropertiesInfo(TcBaseObj):
    """
    'MasterFormPropertiesInfo' specifies the property values to be set on a form.
    
    :var form: Form object to use as the new master form for the related object and will be populated with the property
    values. Not required. If not specified, a master form will be created and populated with the property values.
    :var propertyValueInfo: The list of 'PropertyNameValueInfo's.
    """
    form: Form = None
    propertyValueInfo: List[PropertyNameValueInfo] = ()


@dataclass
class PropertyNameValueInfo(TcBaseObj):
    """
    This structure specifies a property name and the related value(s) to apply to the property.
    
    :var propertyName: The property name.
    :var propertyValues: The list of values for the property.
    """
    propertyName: str = ''
    propertyValues: List[str] = ()


@dataclass
class RelatedObjectInfo(TcBaseObj):
    """
    Structure for specifying 'RelatedObjectInfo'.
    
    :var relatedObject: A reference representing the other side object used to propagate the relation while applying
    the deep copy rules. This object could be a newly created object or an existing object in the system.
    :var action: An integer representing the action that specifies the how to copy the 'relatedObject' as the other
    side object while applying the deep copy rules.  Valid values are : 
    CopyAsObjectType = 0, (A new copy of the object represented by otherSideObjectTag will be created and while
    propagating the relations) 
    CopyAsRefType = 1, (The same object represented by 'otherSideObject' will be used to propagate the relations)
     DontCopyType =2, (The relation will not be propagated.) 
    RelateToLatest = 3, (If the other side object is an ItemRevision, then the latest version of the revision will be
    used while propagating the relation) 
    ReviseAndRelateToLatest = 4 (If the other side object is an ItemRevision, it will be revised and the newly created
    revision will be used while propagating the relations)
    :var isSecondary: A flag indicating whether the 'relatedObject' is participating as a secondary object in the
    relation.
    :var nRdeepCopyOutput: Related object info for named reference list.
    """
    relatedObject: BusinessObject = None
    action: int = 0
    isSecondary: bool = False
    nRdeepCopyOutput: List[RelatedObjectInfoForNR] = ()


@dataclass
class RelatedObjectInfoForNR(TcBaseObj):
    """
    Structure specifying the results of the deep copy of attached named reference objects.
    
    :var relatedObject: Reference to the related object, can either be a new object or an existing object depending on
    the action performed.
    :var action: An integer representing the action that specifies how to the deep copy rules were applied. Valid
    values are :
    CopyAsObjectType = 0, (A new copy of the object represented by otherSideObjectTag was created and while
    propagatring the relations) 
    CopyAsRefType = 1, (The same object represented by otherSideObjectTag was used to propagate the relations)
    
    :var isSecondary: A flag indicating whether the 'relatedObject' is participating as a secondary object in the
    relation.
    """
    relatedObject: BusinessObject = None
    action: int = 0
    isSecondary: bool = False


@dataclass
class ReviseInfo(TcBaseObj):
    """
    Information to identify the source item revision for the revise and attributes to apply to the new item revision.
    
    :var clientId: Identifier to uniquely identify the input.  Also used in the output to help identify which inputs
    had errors.
    :var baseItemRevision: Original item revision to be used for the 'revise' operation
    :var newRevId: Revision ID string for creating new revision
    :var name: Name to apply to the new revision.
    :var description: Description to apply to the new revision.
    :var deepCopyInfo: List of 'DeepCopyData' which represents rules to be used for propagating the relations of the
    ItemRevision object
    :var newItemRevisionMasterProperties: The properties to be set for the newly created master form of the new
    ItemRevision object.
    """
    clientId: str = ''
    baseItemRevision: ItemRevision = None
    newRevId: str = ''
    name: str = ''
    description: str = ''
    deepCopyInfo: List[DeepCopyData] = ()
    newItemRevisionMasterProperties: MasterFormPropertiesInfo = None


@dataclass
class ReviseOutput(TcBaseObj):
    """
    Output  structure for 'revise' operation.
    
    :var newItemRev: Newly created item revision.
    :var relatedObjects: A list of 'RelatedObjectInfo' which represents the new objects created or the existing objects
    used to propagate the relations during the deep copy.
    """
    newItemRev: ItemRevision = None
    relatedObjects: List[RelatedObjectInfo] = ()


@dataclass
class ReviseResponse(TcBaseObj):
    """
    Results of the service call. The output is a map of the input 'clientId' and the results of the input data
    associated with the 'clientId'.
    
    :var reviseOutputMap: Map whose keys are the input 'clientIds' and values are 'ReviseOutput' structures.
    :var serviceData: Standard ServiceData member that will contain the newly created Iitem Rrevision in the created
    objects list. The deep copy rules used, (either supplied by the client or, if not supplied, then the default deep
    copy rules), will create new objects for any copyAsObject rules and those objects will also be in the created
    objects list. For deep copy rules of copyAsReference, those objects will be in the plain objects list. 
    It will also contain any errors encountered. Any errors will also contain the clientId so the client can cross
    reference the error to the input data. Errors  generated by this service include :
    7007 Invalid Item revision tag
    215269 Failure creating new form.
    """
    reviseOutputMap: ReviseOutputMap = None
    serviceData: ServiceData = None


@dataclass
class SaveAsNewItemInfo(TcBaseObj):
    """
    The 'SaveAsNewItemInfo' structure is the main input to the 'saveAsNewItem' service. This structure refers to the
    item to be saved and information on how the new item is to be stored.
    
    :var clientId: Identifier to uniquely identify the input
    :var baseItemRevision: Original item revision to be used for the operation.
    :var itemPropertyInfo: Attributes to apply to the new item, a list of 'PropertyNameValueInfos'.
    :var newRevId: Revision ID for the new revision
    :var type: Type of the new item.
    :var deepCopyInfo: List of 'DeepCopyData's to be used for propagating the relations of the item revision
    :var newItemMasterProperties: The properties to be set for the newly created master form of the new item.
    :var newItemRevisionMasterProperties: The properties to be set for the newly created master form of the new item
    revision.
    :var containingFolder: The destination folder for the new item. If null, the item will go to the  folder specified
    in 'WsoInsertNoSelectionsPref' preference.
    """
    clientId: str = ''
    baseItemRevision: ItemRevision = None
    itemPropertyInfo: List[PropertyNameValueInfo] = ()
    newRevId: str = ''
    type: str = ''
    deepCopyInfo: List[DeepCopyData] = ()
    newItemMasterProperties: MasterFormPropertiesInfo = None
    newItemRevisionMasterProperties: MasterFormPropertiesInfo = None
    containingFolder: Folder = None


@dataclass
class SaveAsNewItemOutput(TcBaseObj):
    """
    The output structure for the 'SaveAsNewItem' service.
    
    :var newItem: The newly created item.
    :var newItemRev: The newly created item revision.
    :var relatedObjects: The list of Related Objects that were created or referenced when applying the deep copy rules.
    """
    newItem: Item = None
    newItemRev: ItemRevision = None
    relatedObjects: List[RelatedObjectInfo] = ()


@dataclass
class SaveAsNewItemResponse(TcBaseObj):
    """
    Return structure for 'saveAsNewItem' operation
    
    :var saveAsOutputMap: Map whose keys are the input 'clientId's and values are 'SaveAsNewItemOutput' structures
    :var serviceData: Standard 'ServiceData' member that will contain the newly created item revision in the created
    objects list. The deep copy rules used, either supplied by the client or, if not supplied, then the default deep
    copy rules, will create new objects for any copyAsObject rules and those objects will also be in the created
    objects list. For deep copy rules of copyAsReference, those objects will be in the plain objects list
    Will also contain any errors generated by the service of system utilities. Errors will contain the 'clientId' so
    the error can be associated with the input. Errors generated by the service itself include :
        7007 Invalid Item revision
      48043 Duplicate item id ( Item already exists )
    215009 Invalid Item type
    215262 For deep copy with copy other side object, the new name is empty.
    215265 Failure copying dataset.
    215275 Deep copy action not supported.
    215267 Failure copying form.
    215269 Failure creating new form.
    215121 Invalid folder specified.
    """
    saveAsOutputMap: SaveAsNewItemOutputMap = None
    serviceData: ServiceData = None


@dataclass
class DeepCopyData(TcBaseObj):
    """
    The 'DeepCopyData' data structure overrides the deep copy rules defined by the system. Only the data supplied will
    be used. If no data is supplied then all the system data will be used.
    
    :var otherSideObject: This is a reference on which the deep copy action needs to be performed. Must be a Dataset or
    a Form.
    :var nRdeepCopyInfo: Named reference deep copy info structure. Only used if 'otherSideObject' is a Dataset and
    CopyAsObject is specified.    
    :var relationTypeName: This is the relation that needs to be deep copied.
    :var newName: This is the new name for the copied object represented by the 'otherSideObject' member. The value for
    the 'newName' will be ignored if the 'action' is not CopyAsObject or ReviseAndRelateToLatest.
    :var action: This is an integer representing the action to be performed on the object represented by
    'otherSideObject' member. The values for action are: 
    CopyAsObjectType = 0
    CopyAsRefType = 1
    DontCopyType =2
    RelateToLatest = 3
    ReviseAndRelateToLatest = 4
    
    :var isTargetPrimary: Flag representing whether the given item revision is the primary object in the relation. This
    property is passed directly to the deep copy utility for the item revision.
    :var isRequired: Flag representing whether the deep copy information is from a mandatory deep copy rule configured
    by the system. If set then the copy is required to be performed and cannot be overridden. This property is passed
    directly to the deep copy utility for the item revision.
    :var copyRelations: Flag representing whether the relations are to be copied. If true then all relations on the
    current object are copied to the new object. If false then no relations are copied. This property is passed
    directly to the deep copy utility for the Item Revision.
    """
    otherSideObject: BusinessObject = None
    nRdeepCopyInfo: List[DeepCopyDataForNR] = ()
    relationTypeName: str = ''
    newName: str = ''
    action: int = 0
    isTargetPrimary: bool = False
    isRequired: bool = False
    copyRelations: bool = False


@dataclass
class DeepCopyDataForNR(TcBaseObj):
    """
    Deep copy data for named references. Only used if 'otherSideObject' is a dataset and the action is CopyAsObject.
    
    :var otherSideObject: This is a reference on which the deep copy action needs to be performed. Currently only
    Dataset and Form objects are supported.
    :var referenceName: This is the named reference name that needs to be deep copied.
    :var newName: This is the new name for the copied object represented by the 'otherSideObject' member.
    :var action: This is an integer representing the action to be performed on the object represented by the
    'otherSideObject' member. The values for action are: 
    CopyAsObjectType = 0
    CopyAsRefType = 1
    DontCopyType =2
    """
    otherSideObject: BusinessObject = None
    referenceName: str = ''
    newName: str = ''
    action: int = 0


"""
A map of the clientId from the input data to the output from the service.
"""
ReviseOutputMap = Dict[str, ReviseOutput]


"""
A map of the clientId from the input data to the output from the service.
"""
SaveAsNewItemOutputMap = Dict[str, SaveAsNewItemOutput]
