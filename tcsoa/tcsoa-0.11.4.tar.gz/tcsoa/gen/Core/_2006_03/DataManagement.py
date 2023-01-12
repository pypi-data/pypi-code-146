from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Group, ImanRelation, Folder, Dataset, User, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtendedAttributes(TcBaseObj):
    """
    This structure contains information for 'createItems' operation to support setting attribute values on the created
    Item, ItemRevision, or corresponding master forms that may be created with the objects.
    
    :var objectType: The type of object to set these properties on i.e. Connection, ConnectionRevision
    :var attributes: A map of  attributes names and initial values pairs ('string/string'). Multi-valued properties are
    represented with a comma separated string
    """
    objectType: str = ''
    attributes: AttributeNameValueMap = None


@dataclass
class GenerateItemIdsAndInitialRevisionIdsProperties(TcBaseObj):
    """
    The input information for 'generateItemIdsAndInitialRevisionIds' operation.
    
    :var item: Item object reference to use as a basis for the next Item ID. This value is optional.
    :var itemType: Type of the Item for which the IDs will be generated.  This value is optional.  The default is Item.
    :var count: Total number of IDs to be generated
    """
    item: BusinessObject = None
    itemType: str = ''
    count: int = 0


@dataclass
class GenerateItemIdsAndInitialRevisionIdsResponse(TcBaseObj):
    """
    Return structure for 'generateItemIdsAndInitialRevisionIds' operation
    
    :var outputItemIdsAndInitialRevisionIds: A list of the new Item and ItemRevision IDs and flags indicating if the
    system is configured to allow modification of the id values after they have been generated.
    :var serviceData: Service data
    """
    outputItemIdsAndInitialRevisionIds: IndexToIdMap = None
    serviceData: ServiceData = None


@dataclass
class GenerateRevisionIdsProperties(TcBaseObj):
    """
    The data structure contains information for 'generateRevisionIds' operation
    
    :var item: Item object reference to get the next revision id, optional
    :var itemType: Type of the ids to generate, optional
    """
    item: BusinessObject = None
    itemType: str = ''


@dataclass
class GenerateRevisionIdsResponse(TcBaseObj):
    """
    The data structure contains returned information for 'generateRevisionIds' operation
    
    :var outputRevisionIds: A list of the new generated id values
    :var serviceData: Service data
    """
    outputRevisionIds: IndexToRevIdMap = None
    serviceData: ServiceData = None


@dataclass
class ItemIdsAndInitialRevisionIds(TcBaseObj):
    """
    This structure contain output information for 'generateItemIdsAndInitialRevisionIds' operation indicating the new
    item id, new revision id, and a flag for each that indicates if the caller should be able to override the generated
    values.
    
    :var newItemId: Newly generated Item Id
    :var newRevId: Newly generated ItemRevision Id
    :var isItemModify: Flag to specify whether Item id is modifiable
    :var isRevModify: Flag to specify whether ItemRevision id is modifiable
    """
    newItemId: str = ''
    newRevId: str = ''
    isItemModify: bool = False
    isRevModify: bool = False


@dataclass
class ItemProperties(TcBaseObj):
    """
    Input structure for createItems operation.  Specifies attributes for the new Item or ItemRevision.
    
    :var clientId: Identifier that helps the client to track the object(s) created, optional.
    :var itemId: Id of the Item to be created, optional
    :var name: Name of the Item to be created, optional
    :var type: Type of the Item to be created, optional, default is Item
    :var revId: Id of the initail revision of the Item to be created, optional
    :var uom: Unit of measure(UOM) of the Item to be created, optional
    :var description: Description of the Item to be created, optional
    :var extendedAttributes: Name/value pairs for additional attributes to set, optional
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
class ObjectOwner(TcBaseObj):
    """
    This structure contains the business object whose owner needs to be changed, new owning user of the object and new
    owning group of the object.
    
    :var object: Teamcenter Business object.
    :var owner: New owning user of the business object.
    :var group: New owning group of the business object.
    """
    object: BusinessObject = None
    owner: User = None
    group: Group = None


@dataclass
class Relationship(TcBaseObj):
    """
    'Relationship' structure represents all required parameters to create the relation between the primary and
    secondary object.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this 'Relationship' structure.
    :var relationType: Name of the relation type to create, required. This could be an empty string, in which case the
    relation name will be searched in the preference, ParentTypeName_ChildTypeName_default_relation or
    ParentTypeName_default_relation.
    :var primaryObject: The primary object to create the relation from
    :var secondaryObject: The secondary object to create the relation to.
    :var userData: The user data object used to create the relation. This parameter is optional.
    """
    clientId: str = ''
    relationType: str = ''
    primaryObject: BusinessObject = None
    secondaryObject: BusinessObject = None
    userData: BusinessObject = None


@dataclass
class ReviseProperties(TcBaseObj):
    """
    This structure contains information about new revision id, name, description and extended attributes.
    
    :var revId: New revision id of the Item to be revised, optional
    :var name: Name of the new ItemRevision, optional
    :var description: Description of the new ItemRevision, optional
    :var extendedAttributes: Name/value pairs for additional attributes to set, optional
    """
    revId: str = ''
    name: str = ''
    description: str = ''
    extendedAttributes: AttributeNameValueMap = None


@dataclass
class ReviseResponse(TcBaseObj):
    """
    Return structure for revise operation
    
    :var oldItemRevToNewItemRev: A Map whose keys are the input old item revisions and values are the newly created
    revisions
    :var serviceData: Standard ServiceData member
    """
    oldItemRevToNewItemRev: ItemRevMap = None
    serviceData: ServiceData = None


@dataclass
class RevisionIds(TcBaseObj):
    """
    This structure contains information for 'generateRevisionIds' operation
    
    :var newRevId: Revision id that was generated
    :var isModify: Flag to specify whether revision id is modifiable
    """
    newRevId: str = ''
    isModify: bool = False


@dataclass
class CreateDatasetsOutput(TcBaseObj):
    """
    This structure contains information for createDatasets operation.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var dataset: Dataset object reference that was created
    """
    clientId: str = ''
    dataset: Dataset = None


@dataclass
class CreateDatasetsResponse(TcBaseObj):
    """
    Return structure for createDatasets operation
    
    :var output: A list of created Dataset output
    :var serviceData: Standard 'ServiceData' member
    """
    output: List[CreateDatasetsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateFolderInput(TcBaseObj):
    """
    Input structure for createFolders operation
    
    :var clientId: Identifier that helps the client to track the object created, optional.
    :var name: Name of the folder to be created, optional, if null, uses value from USER_new_folder_name user exit
    :var desc: Description of the folder to be created, optional
    """
    clientId: str = ''
    name: str = ''
    desc: str = ''


@dataclass
class CreateFoldersOutput(TcBaseObj):
    """
    This structure contains information for 'createFolders' operation.
    
    :var clientId: Identifier that helps the client to track the object created.
    :var folder: Folder object reference that was created
    """
    clientId: str = ''
    folder: Folder = None


@dataclass
class CreateFoldersResponse(TcBaseObj):
    """
    Return structure for createFolders operation
    
    :var output: Each element in the list contains a client Id and the related Folder object created.
    :var serviceData: Standard 'ServiceData' member
    """
    output: List[CreateFoldersOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateItemsOutput(TcBaseObj):
    """
    The data structure contains a list of created items and item revisions.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var item: The created Item object
    :var itemRev: The created ItemRevision object
    """
    clientId: str = ''
    item: Item = None
    itemRev: ItemRevision = None


@dataclass
class CreateItemsResponse(TcBaseObj):
    """
    Return structure for 'createItems' operation.
    
    :var output: A list of the created Item and ItemRevision
    :var serviceData: Service data
    """
    output: List[CreateItemsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateRelationsOutput(TcBaseObj):
    """
    The relations created between the primary and secondary object.
    
    :var clientId: The unmodified value from the 'Relationship.clientId'. This can be used by the caller to indentify
    this data structure with the source input data.
    :var relation: The newly created relation.
    """
    clientId: str = ''
    relation: ImanRelation = None


@dataclass
class CreateRelationsResponse(TcBaseObj):
    """
    'CreateRelationsResponse' structure represents the relations created between the primary and secondary object and
    errors occurred.
    
    :var output: A list of created relations.
    :var serviceData: Standard 'ServiceData' object to hold the partial errors that the operation encounters.
    """
    output: List[CreateRelationsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DatasetProperties(TcBaseObj):
    """
    Input structure for createDatasets operation
    
    :var clientId: Identifier that helps the client to track the object(s) created, required, should be unique for the
    input set
    :var type: Type of the Dataset to be created
    :var name: Name of the Dataset to be created
    :var description: Description of the Dataset to be created, may be an empty string
    :var toolUsed: Name of the Tool used to open the created Dataset, may be an empty string.
    :var container: Object reference of the container used to hold the created Dataset, may be an empty string
    :var relationType: Name of the relation type for the Dataset to be created, may be an empty string.
    """
    clientId: str = ''
    type: str = ''
    name: str = ''
    description: str = ''
    toolUsed: str = ''
    container: BusinessObject = None
    relationType: str = ''


"""
A map of index to 'ItemIdsAndInitialRevisionIds'.
"""
IndexToIdMap = Dict[int, List[ItemIdsAndInitialRevisionIds]]


"""
IndexToRevIdMap
"""
IndexToRevIdMap = Dict[int, RevisionIds]


"""
ItemRevMap
"""
ItemRevMap = Dict[ItemRevision, ItemRevision]


"""
Map of ItemRevision to 'ReviseProperties' ('ItemRevision', 'ReviseProperties').
"""
ItemRevPropertyMap = Dict[ItemRevision, ReviseProperties]


"""
A map represents the property name and display value pair.
"""
AttributeNameValueMap = Dict[str, str]
