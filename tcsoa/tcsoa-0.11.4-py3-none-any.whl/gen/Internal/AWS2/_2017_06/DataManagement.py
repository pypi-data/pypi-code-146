from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2013_12.DataManagement import GetStyleSheetDatasetInfo, GetStyleSheetClassificationData
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Internal.AWS2._2016_03.DataManagement import StylesheetContext
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetStyleSheetOutput(TcBaseObj):
    """
    Output from getStyleSheet operation.
    
    :var processedPage: The name of the page that was processed. If the operation was invoked with processEntireXRT set
    to true, the this field is empty.  If the operation was invoked with processEntireXRT set to false, this this field
    is populated with the page that was processed.  Typically the value of the processedPage would be the same as the
    targetPage, except when the targetPage value is empty or not found in the stylesheet.  In that case, then the first
    page in the stylesheet is processed.
    :var datasetInfo: The information about the stylesheet.
    :var context: The context to which this stylesheet was registered
    :var imageTypeTicketMap: Map (string/string) where the key is the image resolution type from the stylesheet and
    value is the FMS ticket of the image for that resolution type.When resolution is not specified in the stylesheet or
    is invalid, FMS ticket mentioned in the default key will be populated.If the styesheet being rendered is SUMMARY,
    default value will be FMS ticket of the High resolution derived Dataset else default value would be FMS ticket of
    the Medium resolution derived Dataset.If derived Dataset does not exist,default value will be FMS ticket of the
    original Dataset.
    :var propDescriptors: List of LogicalPropertyDescriptors required to render the object properties in stylesheet.
    :var additionalObjects: List of additional objects to support Descriptor use cases in stylesheeet
    :var objectSetInfo: Structure containing the source field from the stylesheet, vector of LogicalObjects and list of
    LogicalPropertyDescriptors required to present inside that objectSet in the application.
    :var tablePropObjectMap: A map(string, list of POM_object) where key is the name of the table property and the
    value is a list of Table Row objects which represents the table row data for that property. 
    Note: This output data structure is not available for consumption in Teamcenter 10.1.x Release stream.
    :var localeMap: Map (string, string) where the key is the text, title, or titleKey string from the stylesheet and
    the value is the localized string.
    :var jtFileMap: Map (business object, string) where the key is the business object to render, and the value is the
    thumbnail ticket for the image to download.
    :var visiblePages: The visible pages in the XRT.  Each index in the array indicates whether that page can be
    displayed.
    :var classificationData: The classification data for the object to be rendered.
    :var objectToRender: The object to render in the UI.  For revise, this is the revise descriptor.  For all other
    operations it is the input businessObject.
    :var patternMap: Key is the property name, and value is the Pattern Information which are valid for that property
    """
    processedPage: str = ''
    datasetInfo: GetStyleSheetDatasetInfo = None
    context: StylesheetContext = None
    imageTypeTicketMap: StringMap7 = None
    propDescriptors: List[ViewModelPropertyDescriptor] = ()
    additionalObjects: AdditionalObjectsStruct = None
    objectSetInfo: List[ObjectSetInfo] = ()
    tablePropObjectMap: TablePropObjectMap3 = None
    localeMap: StringMap7 = None
    jtFileMap: ThumbnailMap6 = None
    visiblePages: List[bool] = ()
    classificationData: List[GetStyleSheetClassificationData] = ()
    objectToRender: ViewModelObject = None
    patternMap: PatternMap3 = None


@dataclass
class GetStyleSheetResponse(TcBaseObj):
    """
    Response sent to client from the getStyleSheet operation.
    
    :var output: The list of output information.  One for each input object
    :var serviceData: The SOA service data.
    """
    output: List[GetStyleSheetOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetViewModelPropertiesOutput(TcBaseObj):
    """
    Output structure containing ViewModelObject structures and corresponding ViewModelPropertyDescriptor structures.
    
    :var objects: A list of ViewModelObject structures.
    :var propDescriptors: A list of ViewModelPropertyDescriptors.
    """
    objects: List[ViewModelObject] = ()
    propDescriptors: List[ViewModelPropertyDescriptor] = ()


@dataclass
class GetViewModelPropsResponse(TcBaseObj):
    """
    Response for getViewModelProperties service operation
    
    :var output: Single GetViewModelPropertiesOutput structure.
    :var serviceData: Service Data.
    """
    output: GetViewModelPropertiesOutput = None
    serviceData: ServiceData = None


@dataclass
class GetViewerDataIn(TcBaseObj):
    """
    The input structure for GetViewerData.
    
    :var obj: The input object for which associated dataset and relevant viewer
    needs to be fetched.
    :var dataset: The dataset object which is currently displayed in the viewer. Sending dataset object as empty
    results in fetching the default viewer associated with the input object.
    :var direction: Indicates the direction for dataset retrieval from input object based on dataset currently
    displayed in the viewer. If direction is null or empty, then the dataset input argument is ignored and input object
    is processed to get the associated dataset and relevant viewer. If direction is 'next', then the input object is
    processed to find the dataset and relevant viewer that is next in line to the received dataset argument. If
    direction is 'previous', then the input object is processed to find the dataset and relevant viewer that is
    previous to the received dataset argument. Valid values for direction are "", next, previous.
    """
    obj: BusinessObject = None
    dataset: BusinessObject = None
    direction: str = ''


@dataclass
class GetViewerDataOutput(TcBaseObj):
    """
    Output structure for viewer data.
    
    :var dataset: The dataset whose associated file needs to be displayed in the viewer.
    :var views: The list of ViewData objects.
    :var hasMoreDatasets: Flag to indicate if more than one datasets are related to input object.
    """
    dataset: BusinessObject = None
    views: List[ViewData] = ()
    hasMoreDatasets: bool = False


@dataclass
class GetViewerDataResponse(TcBaseObj):
    """
    Response structure for getViewerData SOA operation.
    
    :var output: The list of GetViewerDataOutput objects.
    :var serviceData: The SOA service data.
    """
    output: GetViewerDataOutput = None
    serviceData: ServiceData = None


@dataclass
class AdditionalObjectsStruct(TcBaseObj):
    """
    Structure to store additional ViewModelObjects for descriptors in stylesheet
    
    :var additionalObjects: List of additional objects
    :var propDescriptors: ViewModelPropertyDescriptors for additional Objects
    """
    additionalObjects: List[ViewModelObject] = ()
    propDescriptors: List[ViewModelPropertyDescriptor] = ()


@dataclass
class LoadViewModelForEditingInfo(TcBaseObj):
    """
    Structure represents the parameters required to load the view model objects for editing.
    
    :var objs: Input objects
    :var propertyNames: Property names to edit
    :var isPessimisticLock: If true, the object needs to be checked out before making any edits (pessimistic locking).
    The locking of object is done during loadViewModelForEditing() call. Otherwise, the operation takes optimistic lock
    on the object. In optimistic locking the object is locked (based on object last set date "lsd" property) before
    performing the actual save and lock is released after save is complete.
    """
    objs: List[BusinessObject] = ()
    propertyNames: List[str] = ()
    isPessimisticLock: bool = False


@dataclass
class LoadViewModelForEditingOutput(TcBaseObj):
    """
    Output structure of loadViewModelForEditing operation
    
    :var viewModelObjects: View model objects corresponding to the input model object
    """
    viewModelObjects: List[ViewModelObject] = ()


@dataclass
class LoadViewModelForEditingResponse(TcBaseObj):
    """
    Response of LoadViewModelForEditing service operation
    
    :var outputs: outputs of loadViewModelForEditing operation
    :var serviceData: Partial errors are returned in the Service Data.
    """
    outputs: List[LoadViewModelForEditingOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ObjectSetColumnInfo(TcBaseObj):
    """
    Structure representing a sigle column in the object set table
    
    :var propDescriptor: Property Descriptor for the properties required for ViewModelObjects.
    :var userSortable: If true, the column is to be used for sorting.
    :var isRelationProperty: If true, the column represents a relation property; otherwise, other property types like
    attribute, reference, compound or runtime are used.
    """
    propDescriptor: ViewModelPropertyDescriptor = None
    userSortable: bool = False
    isRelationProperty: bool = False


@dataclass
class ObjectSetInfo(TcBaseObj):
    """
    Contains information about the object set source in the xml rendering stylesheet that is to be mapped to the
    Logical business objects
    
    :var xmlSource: Object Source in the xml
    :var rows: A list of ObjectSetRowInfo objects representing the rows in Objectset.
    :var columns: A list of ObjectSetColumnInfo objects representing the columns in Objectset.
    """
    xmlSource: str = ''
    rows: List[ObjectSetRowInfo] = ()
    columns: List[ObjectSetColumnInfo] = ()


@dataclass
class ObjectSetRowInfo(TcBaseObj):
    """
    Structure representing a single row in the objectset table.
    
    :var viewModelObject: ModelObject to be displayed in the row of the ObjectSet.
    :var relationTypeName: Relation Type Name
    :var relationTypeDisplayName: Relation Type display name
    :var relationObject: ImaRelation object
    :var relTypeObject: Model Object for ImanRelationType
    :var refPropertyName: Reference Property Name
    """
    viewModelObject: ViewModelObject = None
    relationTypeName: str = ''
    relationTypeDisplayName: str = ''
    relationObject: ViewModelObject = None
    relTypeObject: BusinessObject = None
    refPropertyName: str = ''


@dataclass
class PatternInfo3(TcBaseObj):
    """
    Structure defining pattern information
    
    :var patterns: The naming rule patterns
    :var preferredPattern: The preferred pattern to use. Typically would be the last used pattern.
    :var condition: The condition
    """
    patterns: List[str] = ()
    preferredPattern: str = ''
    condition: str = ''


@dataclass
class SaveViewModelEditAndSubmitInfo(TcBaseObj):
    """
    Structure represents the parameters required to save the edits on the input objects and submit them to a workflow
    process.
    
    :var obj: Object to save edit and submit to a workflow process.
    :var viewModelProperties: Information of view model properties to be saved.
    :var isPessimisticLock: If false, the operation takes optimistic lock on the object. In optimistic locking the
    object is locked (based on the object last saved date) before performing the actual save and lock is released after
    save is complete. If true, the object needs to be checked out before making any edits (pessimistic locking). The
    locking of object is done during loadViewModelForEditing operation.
    :var workflowData: The workflow information that the input object needs to submit to a workflow. Workflow
    information is stored in a name and value string map (string, list of strings).  If workflowData map is empty,
    objects will not be submitted to any workflow. Supported keys are:
    submitToWorkflow: Boolean Property to define that input object need to submit to workflow process or not. The
    values for the key are: "true" and "false". 
    processName: Process name string. 
    processDescription: Process description string. 
    processTemplate: Name of the process template to be used to create new workflow process. 
    processAssignmentList: Name of the process assignment list to use while creating new workflow process. 
    If property submitToWorkflow value is true and processTemplate value is empty, then workflow
    """
    obj: BusinessObject = None
    viewModelProperties: List[ViewModelProperty] = ()
    isPessimisticLock: bool = False
    workflowData: PropertyValues3 = None


@dataclass
class SaveViewModelEditAndSubmitOutput(TcBaseObj):
    """
    Structure containing information about each input object and whether it was saved and submitted to workflow
    successfully or not.
    
    :var clientId: Input string to uniquely identify the input, used primarily for error handling and output mapping.
    :var workflowProcess: Workflow template object for each input object that will be created after it is submitted to
    workflow successfully.
    """
    clientId: str = ''
    workflowProcess: BusinessObject = None


@dataclass
class SaveViewModelEditAndSubmitResponse(TcBaseObj):
    """
    Structure containing saveViewModelEditAndSubmit() operation response.
    
    :var output: A list of SaveEditAndSubmitOutput structures that will contain information about that object such as
    whether it is submitted to workflow or not. It will contain the workflow template for each input object.
    :var serviceData: Partial errors are returned in the Service Data.
    """
    output: List[SaveViewModelEditAndSubmitOutput] = ()
    serviceData: ServiceData = None


@dataclass
class TablePropStruct(TcBaseObj):
    """
    Structure containing ViewModel Objects and ViewModelPropertyDescriptors for table row objects
    
    :var tableRows: ViewModel objects list representing table rows
    :var propDescriptors: A list of ViewModelPropertyDescriptors for the table row ViewModel Objects.
    """
    tableRows: List[ViewModelObject] = ()
    propDescriptors: List[ViewModelPropertyDescriptor] = ()


@dataclass
class ViewData(TcBaseObj):
    """
    View data for GetViewerDataOutput.
    
    :var file: The ImanFile associated as a named reference to the dataset.
    :var fmsTicket: The read FMS ticket of ImanFile.
    :var viewer: Name of the viewer to render the file.
    """
    file: BusinessObject = None
    fmsTicket: str = ''
    viewer: str = ''


@dataclass
class ViewModelObject(TcBaseObj):
    """
    Object to store the Teamcenter BusinessObject and its associated ViewModel properties to be displayed in the view.
    
    :var modelObject: Represents the Model object.
    :var viewModelProperties: A list of ViewModelProperty structures.
    """
    modelObject: BusinessObject = None
    viewModelProperties: List[ViewModelProperty] = ()


@dataclass
class ViewModelProperty(TcBaseObj):
    """
    ViewModel property represents a property that is displayed in the view, it can be simple property, runtime
    property, compound property or dynamic compound property.
    
    :var propertyName: Property name.
    :var dbValues: Real value for the property.
    :var uiValues: Display values for the property.
    :var intermediateObjectUids: A list of UIDs of intermediate objects across the property traversal path.
    :var srcObjLsd: Last saved date of source object.
    :var isModifiable: The flag that indicates if the property is modifiable
    """
    propertyName: str = ''
    dbValues: List[str] = ()
    uiValues: List[str] = ()
    intermediateObjectUids: List[str] = ()
    srcObjLsd: datetime = None
    isModifiable: bool = False


@dataclass
class ViewModelPropertyDescriptor(TcBaseObj):
    """
    Represents the property descriptor details for a ViewModelProperty.
    
    :var srcObjectTypeName: Type name of the source object on which the property is defined.
    :var propertyName: Name of the property.
    :var valueType: Indicates the value type for the property. Valid value types are: 
    1 - Char
    2 - Date
    3 - Double
    4 - Float
    5 - Integer
    6 - Boolean
    7 - Short Integer
    8 - String
    9 - Type Reference
    10 - UnTyped Reference
    11 - External Reference
    12 - Note
    13 - Typed Relation
    14 - UnTyped Relation
    :var isArray: Has value as true in case of array properties and value as false for single valued properties.
    :var propConstants: A map(string,string) consisting of propertyConstant name as key and  and value being the
    property constant value.
    :var displayName: Display name of the property.
    :var lovCategory: Indicates the LOV category, if the property is attached to LOV.
    :var lov: LOV object reference associated with the property.
    :var maxArraySize: Maximimum number of elements allowed in case of VLA properties.
    :var maxLength: Max allowed length for the property
    :var propertyType: Indicates the property type. Valid property types are: 
    1 - attribute. 
    2 - Reference Property. 
    3 - Relation Property. 
    4 - Compound Property. 
    5 - Runtime Property.
    6 - Operation input.
    """
    srcObjectTypeName: str = ''
    propertyName: str = ''
    valueType: int = 0
    isArray: bool = False
    propConstants: PropertyConstantsMap = None
    displayName: str = ''
    lovCategory: int = 0
    lov: BusinessObject = None
    maxArraySize: int = 0
    maxLength: int = 0
    propertyType: int = 0


"""
Map of string to vector of strings. This map is used to return the auto assignable property name patterns to the client. The key is the property name and the value is the list of patterns.
"""
PatternMap3 = Dict[str, PatternInfo3]


"""
Map to store the property constant name and value pair.
"""
PropertyConstantsMap = Dict[str, str]


"""
Map (string, list of strings) that is a generic container that represents property values. The key is the property name and the value is the string representation of the property value.
"""
PropertyValues3 = Dict[str, List[str]]


"""
String map.
"""
StringMap7 = Dict[str, str]


"""
Map containing table property as key and corresponding table row information as value.
"""
TablePropObjectMap3 = Dict[str, TablePropStruct]


"""
Maps a business object to a thumbnail file ticket.
"""
ThumbnailMap6 = Dict[BusinessObject, str]
