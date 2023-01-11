from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awp0XRTObjectSet, POM_object, Dataset
from tcsoa.gen.Internal.AWS2._2013_12.DataManagement import GetStyleSheetDatasetInfo, GetStyleSheetClassificationData
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


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
    :var context: Contains the information about what this stylesheet was registered to.
    :var imageTypeTicketMap: Map (string/string) where the key is the image resolution type from the stylesheet and
    value is the FMS ticket of the image for that resolution type.When resolution is not specified in the stylesheet or
    is invalid, FMS ticket mentioned in the default key will be populated.If the styesheet being rendered is SUMMARY,
    default value will be FMS ticket of the High resolution derived Dataset else default value would be FMS ticket of
    the Medium resolution derived Dataset.If derived Dataset does not exist,default value will be FMS ticket of the
    original Dataset.
    :var objectSetMap: A Map (string/Teamcenter::Awp0XRTObjectSet) where key is the source field from the stylesheet
    and the value is the data to present inside that objectSet in the application.
    :var tablePropObjectMap: A map(string/vector of POM_object) where key is the name of the table property and the
    value is a vector of Table Row objects which represents the table row data for that property.
    :var localeMap: Map (string/string) where the key is the text, title, or titleKey string from the stylesheet and
    the value is the localized string.
    :var jtFileMap: Map (BusinessObject/string) where the key is the business object to render, and the value is the
    thumbnail ticket for the image to download.
    :var visiblePages: The visible pages in the XRT. Each index in the array indicates whether that page can be
    displayed.
    :var classificationData: The classification data for the object to be rendered.
    :var objectToRender: The object to render.  It could be the input object itself in the case of viewing a
    stylesheet, or the revise descriptor object in the case of the revise operation.
    :var patternMap: Map containing the patterns used for auto-assignable properties. The key is the property name, and
    the value is the patterns to use. Only auto assignable properties exist in the map.
    """
    processedPage: str = ''
    datasetInfo: GetStyleSheetDatasetInfo = None
    context: StylesheetContext = None
    imageTypeTicketMap: StringMap6 = None
    objectSetMap: ObjectSetMap5 = None
    tablePropObjectMap: TablePropObjectMap2 = None
    localeMap: StringMap6 = None
    jtFileMap: ThumbnailMap5 = None
    visiblePages: List[bool] = ()
    classificationData: List[GetStyleSheetClassificationData] = ()
    objectToRender: BusinessObject = None
    patternMap: PatternMap2 = None


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
class GetUnprocessedXRTResponse(TcBaseObj):
    """
    Returns unprocessed XRT information.
    
    :var serviceData: The SOA service data.
    :var dsInfo: The stylesheet dataset information.
    """
    serviceData: ServiceData = None
    dsInfo: DSInfo = None


@dataclass
class InjectDSInfo(TcBaseObj):
    """
    Represents injected dataset (snippet) information.
    
    :var dataset: The dataset object.
    :var datasetName: The dataset name.
    :var xml: The contents of the XRT file.
    """
    dataset: Dataset = None
    datasetName: str = ''
    xml: str = ''


@dataclass
class PatternInfo2(TcBaseObj):
    """
    Structure defining pattern information.
    
    :var patterns: The naming rule patterns.
    :var preferredPattern: The preferred pattern to use. Typically would be the last used pattern.
    :var condition: The condition.
    """
    patterns: List[str] = ()
    preferredPattern: str = ''
    condition: str = ''


@dataclass
class StylesheetContext(TcBaseObj):
    """
    Defines what context the stylesheet was registered to.
    
    :var client: The client for which this is applicable. Ex: "AWC".
    :var type: The Teamcenter data type.
    :var location: The location in the client, if applicable. Example: showObjectLocation
    :var sublocation: The sublocation in the client, if applicable. Example: objectNavigationSubLocation
    :var stylesheetType: The stylesheet type.  Valid values are CREATE, SAVEAS, REVISE, SUMMARY and INFO.
    :var preferenceLocation: The preference location. Valid values are USER, ROLE, GROUP, SITE and ALL.
    :var datasetName: The dataset name to which this Dataset was registered.
    """
    client: str = ''
    type: str = ''
    location: str = ''
    sublocation: str = ''
    stylesheetType: str = ''
    preferenceLocation: str = ''
    datasetName: str = ''


@dataclass
class DSInfo(TcBaseObj):
    """
    The stylesheet information.
    
    :var datasetObject: The dataset object.
    :var stylesheetContext: The context to which this stylesheet was registered.
    :var xrt: The content of the XRT.
    :var injectedByPreference: Map(string, list of InjectDSInfo) where the key is a preference name and the value is  a
    list of InjectDSInfo objects which contain the Dataset object, name and contents of the XRT.
    :var injectedByDatasetName: Map(string, InjectDSInfo) where the key is a Dataset name and the value is an
    InjectDSInfo object which contains the Dataset object, name, and contents of the XRT.
    """
    datasetObject: Dataset = None
    stylesheetContext: StylesheetContext = None
    xrt: str = ''
    injectedByPreference: InjectedByPreferenceMap = None
    injectedByDatasetName: InjectedByNameMap = None


"""
Map of dataset name to its DSInfo object.
"""
InjectedByNameMap = Dict[str, InjectDSInfo]


"""
Map of preferenceName to vector of InjectDSInfo.
"""
InjectedByPreferenceMap = Dict[str, List[InjectDSInfo]]


"""
Maps the object set source in the xml rendering style sheet to the business objects.
"""
ObjectSetMap5 = Dict[str, Awp0XRTObjectSet]


"""
Map of string to vector of strings. This map is used to return the auto assignable property name patterns to the client. The key is the property name and the value is the list of patterns.
"""
PatternMap2 = Dict[str, PatternInfo2]


"""
String map.
"""
StringMap6 = Dict[str, str]


"""
Maps the table property in the xml rendering style sheet to the Table Row objects.
Note: This output data structure is not available for consumption in Teamcenter 10.1.x Release stream.
"""
TablePropObjectMap2 = Dict[str, List[POM_object]]


"""
Maps a business object to a thumbnail file ticket.
"""
ThumbnailMap5 = Dict[BusinessObject, str]
