from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, Folder, Dataset, Item, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportToApplicationInputData(TcBaseObj):
    """
    The ExportToApplicationInputData structure represents all of the data necessary to export selected objects to
    Word/Excel.
    
    :var objectsToExport: The list of Teamcenter business objects to export.
    :var attributesToExport: The list of attributes to export.
    :var applicationFormat: The application format such as MSWordXML, MSExcel and MSExcelLive.
    Supported application formats for this operation
    - MSWordXML    This format is used for exporting Workspace objects to static MSWord application.
    - MSExcel    This format is used for exporting Teamcenter objects to static MSExcel  application.    
    - MSExcelLive    This format is used for exporting Teamcenter objects to Live MSExcel  application.
    
    
    :var templateId: The name of the MSWord/MSExcel template
    """
    objectsToExport: List[BusinessObject] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateId: str = ''


@dataclass
class ExportToApplicationResponse(TcBaseObj):
    """
    ExportToApplicationResponse structure represents the output of export to application operation. It contains the
    read ticket to the exported MSWord/MSExcel file.
    
    :var transientFileReadTickets: The transient file read tickets for the exported file.
    :var serviceData: The serviceData.
    """
    transientFileReadTickets: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class ExtraObjectInfo(TcBaseObj):
    """
    The 'ExtraObjectInfo' structure represents additional object information that may be required to complete an
    operation. Example - It may be required by the client application to pass additional information about the relation
    (GRM) and properties on the relation to the server. This structure can be used to store the information about any
    relation objects.
    
    :var object: The tag of the Teamcenter Business object.
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var relationTypeName: The real type name of the relation.
    :var typeName: The real type name of the object.
    :var attrNameValuePairs: The vector of attributes names and its values to be set on the object.
    """
    object: BusinessObject = None
    clientId: str = ''
    relationTypeName: str = ''
    typeName: str = ''
    attrNameValuePairs: List[AttributeInfo] = ()


@dataclass
class ExtraObjectOutput(TcBaseObj):
    """
    This structure is defined to store information about the additional objects that are updated during the
    createOrUpdate operation.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var object: The tag of the Business object.
    """
    clientId: str = ''
    object: BusinessObject = None


@dataclass
class ExtraObjectOutputCAD(TcBaseObj):
    """
    This structure is defined to add additional objects as part of the response structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var object: The tag of the Business object.
    """
    clientId: str = ''
    object: BusinessObject = None


@dataclass
class GetContentInput(TcBaseObj):
    """
    The parameters required to open requirement in word.
    
    :var objectToProcess: Fulltext object, whose content to be  viewed.
    :var applicationFormat: The viewing application format. Only MSWordXML is supported.
    :var templateId: This parameter is not used currently.
    """
    objectToProcess: WorkspaceObject = None
    applicationFormat: str = ''
    templateId: str = ''


@dataclass
class GetRichContentResponse(TcBaseObj):
    """
    This structure holds FMS ticket of MSWord file generated as part of getRichContent operation.
    
    :var transientFileReadTickets: FMS ticket of word file that is generated as part of getRichContent operation.
    :var serviceData: The 'ServiceData'.
    """
    transientFileReadTickets: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class ImportFromApplicationInputData(TcBaseObj):
    """
    The ImportFromApplicationInputData structure represents all of the data necessary to import an MSWord document into
    Teamcenter.
    
    :var transientFileWriteTicket: The file ticket of the. docx file to be imported into Teamcenter.
    :var applicationFormat: The supported application format is "MSWordXML"
    :var createSpecElementType: The subtype of SpecElement to be created.
    """
    transientFileWriteTicket: str = ''
    applicationFormat: str = ''
    createSpecElementType: str = ''


@dataclass
class ImportFromApplicationResponse(TcBaseObj):
    """
    ImportFromApplicationResponse structure represents the output of import from application operation. It contains the
    UID of the BOMWindow after the document is imported to Teamcenter.
    
    :var resultObjects: The resultant objects which contains the UID of the BOMWindow created after the document is
    imported.
    :var serviceData: The Service Data
    """
    resultObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class ItemInfo(TcBaseObj):
    """
    The 'ItemInfo' structure represents all of the data necessary to construct the Item object. It contains the
    information about the attributes that are set on the Item object. All attributes are passed as name/value pairs in
    the 'AttributeInfo' structure. The extraObject field contains information about the objects that are related to the
    newly created Item.
    
    :var item: The object tag of the object to be updated. If it is NULL then a new object will be created.
    :var itemId: The object Id (item_id) of the object to be updated. If it is NULL then a new ID is created.
    :var itemType: The object Type (object_type) of the object to be created or updated.
    :var name: The Name (object_name) of the object.
    :var description: The Description (object_desc) of the object.
    :var attrList: The attributes to be set on the object. This is in the form of map that stores attribute name and
    attribute value.
    :var extraObject: The structure containing information about the objects that are related to the Item.
    :var folder: The tag of the Folder under which newly created Item is to be pasted.
    """
    item: Item = None
    itemId: str = ''
    itemType: str = ''
    name: str = ''
    description: str = ''
    attrList: List[AttributeInfo] = ()
    extraObject: List[ExtraObjectInfo] = ()
    folder: Folder = None


@dataclass
class ItemRevInfo(TcBaseObj):
    """
    The 'ItemRevInfo' structure represents all of the data necessary to construct the ItemRevision object. It contains
    information about the attributes to be set on the revision object. All attributes are passed as name/value pairs in
    the 'AttributeInfo' structure. The extraObject field allows for the creation of an objects that will be related to
    this newly created ItemRevision.
    
    :var itemRevision: A tag of the ItemRevision to be created or updated. It is NULL for newly created Item.
    :var revId: The Id of the ItemRevision. It is NULL for new ItemRevision object.
    :var attrList: The attribute name and attribute value to be set on the ItemRevision.
    :var extraObject: The information about the objects that are related to the ItemRevision.
    """
    itemRevision: ItemRevision = None
    revId: str = ''
    attrList: List[AttributeInfo] = ()
    extraObject: List[ExtraObjectInfo] = ()


@dataclass
class NamedReferenceObjectInfo(TcBaseObj):
    """
    The 'NamedReferenceObjectInfo' structure represents all of the data necessary to construct the named reference file
    attached to a Dataset.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify 
    return data element and partial errors associated with this input structure.
    
    :var object: The reference to the named reference file for Dataset.
    :var relationTypeName: The real type name of the relation between the revision and the Dataset.
    
    :var typeName: The real type name of the Dataset.
    :var attrNameValuePairs: The attribute name-value pair to set on the Dataset.
    :var namedReferenceName: The real Dataset type.
    """
    clientId: str = ''
    object: BusinessObject = None
    relationTypeName: str = ''
    typeName: str = ''
    attrNameValuePairs: List[AttributeInfo] = ()
    namedReferenceName: str = ''


@dataclass
class AttributeInfo(TcBaseObj):
    """
    This structure allows the caller to create or update named attributes. This structure must contain the name of the
    attribute and the value of the attribute to set.
    
    :var name: The name of the attribute to set.
    :var value: The value of the attribute to set.
    """
    name: str = ''
    value: str = ''


@dataclass
class AttributeInfoCAD(TcBaseObj):
    """
    This structure allows the caller to create or update named attributes. This structure must contain the name of the
    attribute and the value of the attribute to set.
    
    :var name: The name of the attribute to set.
    :var value: The value of the attribute to set.
    """
    name: str = ''
    value: str = ''


@dataclass
class PartInfo(TcBaseObj):
    """
    The data required to create an Item, ItemRevision and one or more Dataset.  If the Item already exists then it also
    has the information required to be updated for that Item.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return 
    data elements and partial errors associated with this input structure.
    :var itemInput: The information required to create or update an Item.
    :var itemRevInput: The information required to create or update an ItemRevision.
    :var datasetInput: The information required to create or update one or more Dataset objects.
    """
    clientId: str = ''
    itemInput: ItemInfo = None
    itemRevInput: ItemRevInfo = None
    datasetInput: List[DatasetInfo] = ()


@dataclass
class SetContentInput(TcBaseObj):
    """
    'SetContentInput' structure represents the parameters required to set the contents to Fulltext object.
    
    :var objectToProcess: Fulltext object.
    :var transientFileWriteTicket: FMS ticket of Word file.
    """
    objectToProcess: WorkspaceObject = None
    transientFileWriteTicket: str = ''


@dataclass
class SetRichContentResponse(TcBaseObj):
    """
    'SetRichContentResponse' - structure represents response parameters of setRichContent SOA.
    
    :var resultObjects: This parameter is not used.
    :var serviceData: The Service Data.
    """
    resultObjects: List[WorkspaceObject] = ()
    serviceData: ServiceData = None


@dataclass
class CommitDatasetFileInfoCAD(TcBaseObj):
    """
    This structure has information to commit named reference files to input Dataset. This structure contains the
    necessary  information like the file ticket and if a new version of Dataset is to be created.
    
    :var dataset: A tag of the Dataset to be updated with the named reference file.
    :var createNewVersion: The value of true means that a new Dataset to be created, value of false means that the
    existing Dataset to be updated with the named reference file.
    :var datasetFileTicketInfos: The information about the Dataset file tickets.
    """
    dataset: Dataset = None
    createNewVersion: bool = False
    datasetFileTicketInfos: List[DatasetFileTicketInfoCAD] = ()


@dataclass
class CreateOrUpdateOutput(TcBaseObj):
    """
    This structure is defined to store information about the newly created Dataset or updates to the existing Dataset.
    It contains all the information about the related objects that user needs to pass during the creation or update of
    Dataset.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var item: The tag of the Item that is created or updated.
    :var itemRev: The tag of the ItemRevision that is created or updated.
    :var datasetOutput: The tag of the Dataset that is created or updated.
    :var extraItemObjs: The structure containing information about the additional Item objects created.
    :var extraItemRevObjs: The structure containing information about the additional ItemRevision objects created.
    """
    clientId: str = ''
    item: Item = None
    itemRev: ItemRevision = None
    datasetOutput: List[DatasetOutput] = ()
    extraItemObjs: List[ExtraObjectOutput] = ()
    extraItemRevObjs: List[ExtraObjectOutputCAD] = ()


@dataclass
class CreateOrUpdateResponse(TcBaseObj):
    """
    This structure represents the output of createOrUpdate operation.  It has the information about the newly created
    Dataset or update to existing Dataset.
    
    :var output: The list of structures containing information about the Item,
    ItemRevision or the Dataset to be created or updated.
    :var serviceData: The serviceData.
    """
    output: List[CreateOrUpdateOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DatasetFileInfoCAD(TcBaseObj):
    """
    This structure allows the user to create or update the dataset with the named attributes information. This
    structure must contain either an "AttributesToSet" element or an "AttributesToUnset" element, but not both.
    
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var fileName: The name of the named reference file to be updated.
    :var namedReferencedName: The named references string for that object.
    :var isText: Flag to indicate if it is text data. Value of true indicates it is text data. Value of false indicates
    binary data.
    :var allowReplace: Flag to indicate whether to replace the data. Value of true indicates data to be overwritten.
    Value of false indicates data will not be overwritten.
    """
    clientId: str = ''
    fileName: str = ''
    namedReferencedName: str = ''
    isText: bool = False
    allowReplace: bool = False


@dataclass
class DatasetFileTicketInfoCAD(TcBaseObj):
    """
    This structure has Dataset FMS file ticket information.
    
    :var datasetFileInfo: The Dataset file ticket information.
    :var ticket: The name of the ticket.
    """
    datasetFileInfo: DatasetFileInfoCAD = None
    ticket: str = ''


@dataclass
class DatasetInfo(TcBaseObj):
    """
    The DatasetInfo structure represents all of the data necessary to construct the Dataset object. All the attributes
    required to be set on the Dataset are passed as name/value pairs in the 'AttributeInfo' structure. The extraObject
    field allows for the creation of an object(s) that will be related to this newly created Dataset.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var dataset: The tag of Dataset.
    :var mappingAttributes: The mapping attributes to be set on the Dataset.
    :var extraObject: Additional objects to be created and related to the Dataset.
    :var datasetFileInfos: The information about files attached to the Dataset.
    :var namedReferenceObjectInfos: The information about objects attached to the Dataset.
    :var name: The name of Dataset.
    :var description: The description for Dataset.
    :var type: The real type name of Dataset.
    :var id: The id of Dataset.
    :var datasetRev: The name of Dataset revision.
    :var itemRevRelationName: The relation name of the revision to Dataset.
    :var createNewVersion: The flag to create new version. Value of true indicates new revision to be created, value of
    false indicates no new revision to be created.
    :var attrList: The attributes to be set on the Dataset.
    """
    clientId: str = ''
    dataset: Dataset = None
    mappingAttributes: List[AttributeInfoCAD] = ()
    extraObject: List[ExtraObjectInfo] = ()
    datasetFileInfos: List[DatasetFileInfoCAD] = ()
    namedReferenceObjectInfos: List[NamedReferenceObjectInfo] = ()
    name: str = ''
    description: str = ''
    type: str = ''
    id: str = ''
    datasetRev: str = ''
    itemRevRelationName: str = ''
    createNewVersion: bool = False
    attrList: List[AttributeInfo] = ()


@dataclass
class DatasetOutput(TcBaseObj):
    """
    This structure is defined to store information about the output Dataset objects. It also contains information about
    the additional objects that are related to the Dataset.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var dataset: The tag of the Dataset.
    :var commitInfo: The structure containing information to commit named reference files.
    :var extraObjs: The structure containing information about the objects that are related to the Dataset.
    :var namedRefObjs: The structure containing information about the additional named reference objects
    """
    clientId: str = ''
    dataset: Dataset = None
    commitInfo: List[CommitDatasetFileInfoCAD] = ()
    extraObjs: List[ExtraObjectOutput] = ()
    namedRefObjs: List[ExtraObjectOutputCAD] = ()
