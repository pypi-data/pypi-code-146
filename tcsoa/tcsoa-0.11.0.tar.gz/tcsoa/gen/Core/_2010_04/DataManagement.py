from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Dataset
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAvailableBusinessObjectTypesResponse(TcBaseObj):
    """
    Returned service response structure to represents the displayable Business Objects information.
    
    :var inputClassToTypes: A map of Business Object names and associated descendant Business Objects (string,
    vector<AvailableBusinessObjectTypeInfo>>)
    :var serviceData: The ServiceData.
    """
    inputClassToTypes: BusinessObjectClassToTypesMap = None
    serviceData: ServiceData = None


@dataclass
class GetDatasetCreationRelatedInfoResponse2(TcBaseObj):
    """
    Holds the Response data from getDatasetCreationRelatedInfo2
    
    :var toolNames: List of Tool names
    :var toolDisplayNames: List of Tool display names.
    :var newDatasetName: The name of the new Dataset, can be an empty string
    :var nameCanBeModified: If true, the name of the Dataset can be modified
    :var initValuePropertyRules: List of properties have the initialized values from property constant attachments
    :var serviceData: Standard 'ServiceData' member
    """
    toolNames: List[str] = ()
    toolDisplayNames: List[str] = ()
    newDatasetName: str = ''
    nameCanBeModified: bool = False
    initValuePropertyRules: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class LocalizableResults(TcBaseObj):
    """
    This data structure contains property names and boolean value to indicate whether this property is localizable.
    
    :var propName: Internal property name.
    :var islocalizable: boolean value to indicate localizability of this property.
    """
    propName: str = ''
    islocalizable: bool = False


@dataclass
class LocalizableStatusInput(TcBaseObj):
    """
    This data structure contains the type of the business object and its internal property names.
    
    :var objTypeName: String Object Type Name
    :var propNames: A list of the internal property names of the object.
    """
    objTypeName: str = ''
    propNames: List[str] = ()


@dataclass
class LocalizableStatusOutput(TcBaseObj):
    """
    This structure contains object type name and localizable information.
    
    :var objTypeName: Object Type Name
    :var results: Result containing localizable information.
    """
    objTypeName: str = ''
    results: List[LocalizableResults] = ()


@dataclass
class LocalizableStatusResponse(TcBaseObj):
    """
    This data structure contains a list of localized results and 'ServiceData'.
    
    :var results: A list of 'LocalizableResults' structure to hold the localizable information for all properties.
    :var serviceData: 'serviceData'
    """
    results: List[LocalizableStatusOutput] = ()
    serviceData: ServiceData = None


@dataclass
class LocalizedPropertyValuesInfo(TcBaseObj):
    """
    This data structure contains business object tag and a list of of 'NameValueLocaleStruct'
    
    :var object: The business object.
    :var propertyValues:  A list of 'NameValueLocaleStruct' that holds property name, value and locale information.
    """
    object: BusinessObject = None
    propertyValues: List[NameValueLocaleStruct] = ()


@dataclass
class LocalizedPropertyValuesList(TcBaseObj):
    """
    This structure contains  a list of output localized property value info and  partial error.
    
    :var output: A list of structure LocalizedPropertyValuesInfo to keep the localized property values info.
    :var partialErrors: Used for storing partial error and standard service data.
    """
    output: List[LocalizedPropertyValuesInfo] = ()
    partialErrors: ServiceData = None


@dataclass
class NameLocaleStruct(TcBaseObj):
    """
    This structure contains a property name and list of possible locales.
    
    :var name: A property name string
    :var locales:  A list of language locales.
    """
    name: str = ''
    locales: List[str] = ()


@dataclass
class NameValueLocaleStruct(TcBaseObj):
    """
    This structure contains localization related information for property values.
    
    :var name: Property name (internal)
    :var values: A list of property values
    :var locale: The name of the locale
    :var seqNum: Sequence number
    :var status: The name of the localization status.
    The status must be one of the following values:
    - for the approved status: "A", "Approved" or the version of the "Approved" string for the client/server log-in
    locale.
    - for the in-review status: "R", "In Review", "In-Review", "InReview" or the version of the "In Review" string for
    the client/server log-in locale.
    - for the pending status: "P", "Pending" or the version of the "Pending" string for the client/server log-in locale.
    - for the invalid status: "I", "Invalid" or the version of the "Invalid" string for the client/server log-in locale.
    - for the master status: "M", "Master" or the version of the "Master" string for the client/server log-in locale.
    
    
    :var statusDesc: Description of statuses used for tooltip on the user interface
    :var master: Master value indication
    """
    name: str = ''
    values: List[str] = ()
    locale: str = ''
    seqNum: int = 0
    status: List[str] = ()
    statusDesc: List[str] = ()
    master: bool = False


@dataclass
class NamedReferenceObjectInfo(TcBaseObj):
    """
    This structure contains information regarding named reference type value, object reference, object type name and
    list of attribute information to set on the object.
    
    :var clientId: Identifier defined by user to track the related object.
    :var object: Object reference of the object to attach to dataset as named reference.
    :var namedReferenceName: The Named Reference from the dataset to this object, required
    :var referenceType: Reference Type. It is either AE_PART_OF or AE_ASSOCIATION
    """
    clientId: str = ''
    object: BusinessObject = None
    namedReferenceName: str = ''
    referenceType: str = ''


@dataclass
class AttributeInfo(TcBaseObj):
    """
    This structure contains the name value pairs.
    
    :var name: Name of the attribute that needs to be set.
    :var values: Values to be set
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class AvailableBusinessObjectTypeInfo(TcBaseObj):
    """
    This structure represents Business Object name, display name, and its hierarchy.
    
    :var type: Name of the Business Object
    :var displayType: Display name of the Business Object
    :var hierarchies: Bottom up hierarchy of the Business Object going up to the input Business Object
    """
    type: str = ''
    displayType: str = ''
    hierarchies: List[str] = ()


@dataclass
class PropertyInfo(TcBaseObj):
    """
    This data structure contains business object and a list of properties and locales.
    
    :var object: The desired business object to retrieved localized property values
    :var propsToget:  A list of NameLocaleStruct to hold the desired properties and locales.
    """
    object: BusinessObject = None
    propsToget: List[NameLocaleStruct] = ()


@dataclass
class BusinessObjectHierarchy(TcBaseObj):
    """
    This structure contains information about a bottom up hierarchy starting with a Business Object name and going up
    the hierarchy of parents up to the primary Business Object.
    
    :var boName: Name of the Business Object
    :var boDisplayName: Display Name of the Business Object
    :var boParents: Names of Business Objects going up the hierarchy of parents up to the primary Business Object
    """
    boName: str = ''
    boDisplayName: str = ''
    boParents: List[str] = ()


@dataclass
class CommitDatasetFileInfo(TcBaseObj):
    """
    This structure contains the basic info for a file to be uploaded to a dataset.
    
    :var dataset: Dataset object reference.
    :var createNewVersion: Flag to create new version ( TRUE ) or not ( FALSE ).
    :var datasetFileTicketInfos: A list of 'DatasetFileTicketInfos'.
    """
    dataset: Dataset = None
    createNewVersion: bool = False
    datasetFileTicketInfos: List[DatasetFileTicketInfo] = ()


@dataclass
class CreateDatasetsResponse(TcBaseObj):
    """
    Return structure for createDatasets operation
    
    :var datasetOutput: List of output structure for creatDatasets operation. Each element in the list contains a
    client Id and the related Dataset object created.
    :var servData: Standard 'ServiceData' member
    """
    datasetOutput: List[DatasetOutput] = ()
    servData: ServiceData = None


@dataclass
class DatasetFileInfo(TcBaseObj):
    """
    Holds the basic info for a file to be uploaded to a Dataset.
    
    :var clientId: A unique string used to identify return data elements and partial errors associated with this input
    structure.
    :var fileName: Name of file to be uploaded.  Filename only, should not contain path to filename.
    :var namedReferenceName: Named Reference relation to file.
    :var isText: Flag to indicate if file is text ( TRUE ) or binary (FALSE ).
    :var allowReplace: Flag to indicate if file can be overwritten ( TRUE ) or not ( FALSE ).
    """
    clientId: str = ''
    fileName: str = ''
    namedReferenceName: str = ''
    isText: bool = False
    allowReplace: bool = False


@dataclass
class DatasetFileTicketInfo(TcBaseObj):
    """
    This structure contains the basic info for a file to be uploaded to a dataset.
    
    :var datasetFileInfo: Member of type DatasetFileInfo.
    :var ticket: ID of ticket.
    """
    datasetFileInfo: DatasetFileInfo = None
    ticket: str = ''


@dataclass
class DatasetInfo(TcBaseObj):
    """
    The DatasetInfo struct represents all of the data necessary to construct the Dataset object.  The basic attributes
    that required are passed as named elements in the struct.  All other attributes are passed as name/value pairs in
    the AttributeInfo struct.  The nrObjectInfos field allows for the attachment of an object that will be related to
    this newly created Dataset.
    
    :var clientId: A unique string used to identify return data elements and partial errors associated with this input
    structure.
    :var name: Name attribute value
    :var container: Object reference of the container used to hold the created Dataset
    :var relationType: Name of the relation type for the Dataset to be created
    :var description: Description attribute value
    :var type: Type attribute value
    :var datasetId: ID attribute value
    :var datasetRev: Revision attribute value
    :var toolUsed: Name of the Tool used to open the created Dataset, may be an empty string.
    :var attrs: List of attribute name values pairs to be set
    :var datasetFileInfos: List of  info of the files to be uploaded
    :var nrObjectInfos: list of info of named references of the Dataset
    """
    clientId: str = ''
    name: str = ''
    container: BusinessObject = None
    relationType: str = ''
    description: str = ''
    type: str = ''
    datasetId: str = ''
    datasetRev: str = ''
    toolUsed: str = ''
    attrs: List[AttributeInfo] = ()
    datasetFileInfos: List[DatasetFileInfo] = ()
    nrObjectInfos: List[NamedReferenceObjectInfo] = ()


@dataclass
class DatasetOutput(TcBaseObj):
    """
    This structure contains return data from 'createDatasets' operation.
    
    :var clientId: Identifier defined by user to track the input criteria.
    :var dataset: Dataset object reference of the created dataset
    :var commitInfo: List of 'CommitDatasetFileInfos'
    """
    clientId: str = ''
    dataset: Dataset = None
    commitInfo: List[CommitDatasetFileInfo] = ()


@dataclass
class DisplayableBusinessObjectsOut(TcBaseObj):
    """
    This structure contains a list of displayable business objects (BO) under a given BO(displayable sub-BO hierarchy).
    
    :var boTypeName: The Business Object name for which displayable Hierarchy is returned.
    :var displayableBOTypeNames: Displayable BO hierarchy
    """
    boTypeName: str = ''
    displayableBOTypeNames: List[BusinessObjectHierarchy] = ()


@dataclass
class DisplayableSubBusinessObjectsResponse(TcBaseObj):
    """
    Structure to hold list of Business Objects and its displayable names.
    
    :var output: List of displayable Business Objects.
    :var serviceData: The Service data.
    """
    output: List[DisplayableBusinessObjectsOut] = ()
    serviceData: ServiceData = None


"""
A map of classes and their types
"""
BusinessObjectClassToTypesMap = Dict[str, List[AvailableBusinessObjectTypeInfo]]
