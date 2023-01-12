from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awp0XRTObjectSet, POM_object
from tcsoa.gen.Internal.AWS2._2013_12.DataManagement import GetStyleSheetDatasetInfo, GetStyleSheetClassificationData
from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2012_10.DataManagement import ObjectLsdInfo, NameValueStruct
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetInitialTableRowDataResponse(TcBaseObj):
    """
    Structure containing  list of rows on which all proposed property values are populated. This information can be
    used finally to create a row to the table property.
    
    :var tableRows: List of property information which will have property values pre-populated.
    """
    tableRows: List[TableRow] = ()


@dataclass
class GetStyleSheetIn(TcBaseObj):
    """
    Input for the getStyleSheet operation.
    
    :var targetPage: The page in the XRT stylesheet to process. This field is ignored if the parameter processEntireXRT
    is set to true. This value may be an empty string which would cause the server to process the first page in the
    XRT, or it may be a titleKey for a page in the XRT, for example web_xrt_Overview. If the target page is not found,
    then the first page in the XRT is processed.
    :var businessObject: The businessObject for which to retrieve a stylesheet. This field may be NULL. Typically it
    would only be NULL in the case of CREATE.
    :var businessObjectType: The Teamcenter data type for which to retrieve a stylesheet, if the businessObject
    parameter is NULL, then this field must be populated, otherwise it is ignored.
    :var styleSheetType: The type of stylesheet to return. Legal values are: SUMMARY, CREATE, RENDERING, or INFO.
    :var styleSheetLastModDate: The last save date of the stylesheet.
    :var clientContext: The map of client context key value entries, where the key is the client and the location in
    the client, and the value is the unique id for the data being presented in that panel. These values are used to
    process visibleWhen clasuses in the XRT, pages may be enabled or disabled based on where it is being presented in
    the client. If the isRedLineMode key value is true and source object is of type ItemRevision then it is compared
    against configured revision. If configured revision is not found then source object is compared to previous
    revision.
    
    For example valid entries for active workspace may be:
    Key: ActiveWorkspace:Location 
    Value: com.siemens.splm.client.search.SearchLocation
    
    Or
    
    Key: ActiveWorkspace:SubLocation 
    Value: com.siemens.splm.client.search:SavedSearchSubLocation
    
    
    Or
    
    Key: isRedLineMode
    Value: true or false
    """
    targetPage: str = ''
    businessObject: BusinessObject = None
    businessObjectType: str = ''
    styleSheetType: str = ''
    styleSheetLastModDate: datetime = None
    clientContext: StringMap5 = None


@dataclass
class GetStyleSheetOutput(TcBaseObj):
    """
    Output from getStyleSheet operation.
    
    :var processedPage: The name of the page that was processed. If the operation was invoked with processEntireXRT set
    to true, the this field is empty. If the operation was invoked with processEntireXRT set to false, this this field
    is populated with the page that was processed. Typically the value of the processedPage would be the same as the
    targetPage, except when the targetPage value is empty or not found in the stylesheet. In that case, then the first
    page in the stylesheet is processed.
    :var datasetInfo: The information about the stylesheet.
    :var objectSetMap: A Map (string/Teamcenter::Awp0XRTObjectSet) where key is the source field from the stylesheet
    and the value is the data to present inside that objectSet in the application.
    :var tablePropObjectMap: A map(string/vector of POM_object) where key is the name of the table property and the
    value is a vector of Table Row objects which represents the table row data for that property.
    :var localeMap: Map (string/string) where the key is the text, title, or titleKey string from the stylesheet and
    the value is the localized string.
    :var jtFileMap: Map (BusinessObject/string) where the key is the business object to render, and the value is the
    thumbnail ticket for the image to download.
    :var visiblePages: The visible pages in the XRT.  Each index in the array indicates whether that page can be
    displayed.
    :var classificationData: The classification data for the object to be rendered.
    :var objectToRender: The object to render. It could be the input object itself in the case of viewing a stylesheet,
    or the revise descriptor object in the case of the revise operation.
    :var patternMap: Map containing the patterns used for auto-assignable properties. The key is the property name, and
    the value is the patterns to use. Only auto assignable properties exist in the map.
    """
    processedPage: str = ''
    datasetInfo: GetStyleSheetDatasetInfo = None
    objectSetMap: ObjectSetMap4 = None
    tablePropObjectMap: TablePropObjectMap = None
    localeMap: StringMap5 = None
    jtFileMap: ThumbnailMap4 = None
    visiblePages: List[bool] = ()
    classificationData: List[GetStyleSheetClassificationData] = ()
    objectToRender: BusinessObject = None
    patternMap: PatternMap = None


@dataclass
class GetStyleSheetResponse(TcBaseObj):
    """
    Response sent to client from the getStyleSheet operation.
    
    :var output: The vector of output information. One for each input object.
    :var serviceData: The SOA service data.
    """
    output: List[GetStyleSheetOutput] = ()
    serviceData: ServiceData = None


@dataclass
class LoadDataForEditingInfo(TcBaseObj):
    """
    Structure represents the parameters required to save the edits on the input objects and submit them to a workflow
    process.
    
    :var obj: Input object
    :var propertyNames: Property names
    :var isPessimisticLock:  If true, the object needs to be checked out before making any edits (pessimistic locking).
    The locking of object is done during loadDataForEditing() call.If false, the operation takes optimistic lock on the
    object. In optimistic locking the object is locked (based on object last set date "lsd" property) before performing
    the actual save and lock is released after save is complete.
    """
    obj: BusinessObject = None
    propertyNames: List[str] = ()
    isPessimisticLock: bool = False


@dataclass
class LoadDataForEditingOutput(TcBaseObj):
    """
    Output structure of LoadDataForEditing operation
    
    :var obj: Object to start edit or its dependent objects
    :var objLsds: List of last save date of object or dependent objects.
    :var tableProperties: A map(string/list of POM_object) where key is the name of the table property and the value is
    a vector of Table Row objects which represents the table row data for that property.
    """
    obj: BusinessObject = None
    objLsds: List[ObjectLsdInfo] = ()
    tableProperties: TablePropObjectMap = None


@dataclass
class LoadDataForEditingResponse(TcBaseObj):
    """
    Response of LoadDataForEditing SOA
    
    :var outputs: A list of LoadDataForEditingOutput strutures which provide information about the editable status of
    the properties passed in the input. This information can be used by client to show which properties as editable.
    :var serviceData: Partial errors are returned in the Service Data. The following partial errors may be returned:
    
    302021: The input object is not modifiable.
    302022: The property is not modifiable.
    """
    outputs: List[LoadDataForEditingOutput] = ()
    serviceData: ServiceData = None


@dataclass
class PatternInfo(TcBaseObj):
    """
    Structure defining Pattern information.
    
    :var patterns: List of naming rule patterns.
    :var preferredPattern: The preferred pattern to use.
    :var condition: The condition value.
    """
    patterns: List[str] = ()
    preferredPattern: str = ''
    condition: str = ''


@dataclass
class PropertyNameValue(TcBaseObj):
    """
    Input Structure containing information about what properties are to be populated. 
    For normal (non-Table )Properties, user has to populate values. 
    For Table Properties, user has to fill the rowValues structure
    
    :var name: Property name string that needs to be modified.
    :var values: Property values string vector that will be used to update the input object with corresponding values.
    This vector contains string representation of the property value. The calling client is responsible for converting
    the different property types (int, float, date .etc) to a string using the appropriate toXXXString functions in the
    SOA client framework's Property class.
    :var rowValues: A list to hold child object structures. Child structure will be populated in case the property
    contains a collection of sub objects. E.g. table properties. For other properties, the list needs to be empty.
    """
    name: str = ''
    values: List[str] = ()
    rowValues: List[RowDataStruct] = ()


@dataclass
class RowDataStruct(TcBaseObj):
    """
    A structure to hold child information associated with the main object.
    It contains uid of the child, and its name value pairs for different properties.
    
    :var uid: UID for the child object. If the UID is blank  / NULL UID, a new object is created with details as
    populated in nameValues.
    :var nameValues: List of structure containing Information which needs to be saved. If UID is not blank then the
    properties populated in this structure will be updated. If UID is blank, then a new child object is created based
    on the name values input.
    """
    uid: str = ''
    nameValues: List[NameValueStruct] = ()


@dataclass
class SaveEditAndSubmitInfo(TcBaseObj):
    """
    Structure represents the parameters required to save the edits on the input objects and submit them to a workflow
    process.
    
    :var object: Object to save edit and submit to a workflow process.
    :var propertyNameValues: Property name and values structure that will contain all property names and corresponding
    values that needs to be saved.
    :var objLsds: The last set date information for the object.
    :var isPessimisticLock: The flag to control whether this method call performs optimistic locking or not.
    A false value means the operation takes optimistic lock on the object. In optimistic locking the object is locked
    (based on the object last saved date) before performing the actual save and lock is released after save is complete.
    A true value means the object needs to be checked out before making any edits (pessimistic locking). The locking of
    object is done during loadDataForEditing operation.
    :var workflowData: The workflow information that the input object needs to submit to a workflow. Workflow
    information is stored in a name and value string map (string/list of strings).  If workflowData map is empty,
    objects will not be submitted to any workflow.
    Supported keys:
    
    &bull;   submitToWorkflow: Boolean Property to define that input object need to submit to workflow process or not.
    It can contain true or false as value. 
    &bull;   processName: Process name string. 
    &bull;   processDescription: Process description string. 
    &bull;   processTemplate: Name of the process template to be used to create new workflow process. 
    &bull;   processAssignmentList: Name of the process assignment list to use while creating new workflow process. 
    
    If property submitToWorkflow value is true and processTemplate value is empty, then workflow process template to be
    used for workflow creation should be specified in the preference (<TypeName>_default_workflow_template) defined for
    the submitted object type.
    """
    object: BusinessObject = None
    propertyNameValues: List[PropertyNameValue] = ()
    objLsds: List[ObjectLsdInfo] = ()
    isPessimisticLock: bool = False
    workflowData: PropertyValues1 = None


@dataclass
class TableRow(TcBaseObj):
    """
    Structure containing pre-filled values of row information. The values can then be modified, and a subsequent SOA
    call to Save operation (saveEdits() SOA) will persist the row object in database.
    
    :var tableRowTypeName: The business object type name of the table row. This can be Fnd0TableRow or any subtype.
    :var tableRowData: A list of property values, where name is the column name (sub property name) of the table
    property. "dbValues" and "uiValues" are the list of database value and list of display values respectively.
    """
    tableRowTypeName: str = ''
    tableRowData: List[TableRowProperty] = ()


@dataclass
class TableRowProperty(TcBaseObj):
    """
    Structure containing pre-populated property values for columns of the row object.
    
    :var name: The name of the property. Caller can look up the property descriptor to get metadata about the property.
    :var dbValues: Proposed data base value for the property.
    :var uiValues: Proposed display values for the property.
    """
    name: str = ''
    dbValues: List[str] = ()
    uiValues: List[str] = ()


"""
Maps the object set source in the xml rendering style sheet to the business objects.
"""
ObjectSetMap4 = Dict[str, Awp0XRTObjectSet]


"""
Map of string to vector of strings. This map is used to return the auto assignable property name patterns to the client. The key is the property name and the value is the list of patterns.
"""
PatternMap = Dict[str, PatternInfo]


"""
Map (string, vector) that is a generic container that represents property values. The key is the property name and the value is the string representation of the property value.
"""
PropertyValues1 = Dict[str, List[str]]


"""
String map.
"""
StringMap5 = Dict[str, str]


"""
Maps the table property in the xml rendering style sheet to the Table Row objects.
"""
TablePropObjectMap = Dict[str, List[POM_object]]


"""
Maps a business object to a thumbnail file ticket.
"""
ThumbnailMap4 = Dict[BusinessObject, str]
