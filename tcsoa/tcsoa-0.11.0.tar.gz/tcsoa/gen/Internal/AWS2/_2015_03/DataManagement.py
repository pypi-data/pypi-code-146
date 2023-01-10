from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awp0XRTObjectSet
from tcsoa.gen.Internal.AWS2._2013_12.DataManagement import GetStyleSheetDatasetInfo, GetStyleSheetClassificationData
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetStyleSheetIn(TcBaseObj):
    """
    Input for the getStyleSheet operation.
    
    :var targetPage: The page in the XRT stylesheet to process.  This field is ignored if the parameter
    processEntireXRT is set to true. This value may be an empty string which would cause the server to process the
    first page in the XRT, or it may be a titleKey for a page in the XRT, for example web_xrt_Overview.  If the target
    page is not found, then the first page in the XRT is processed.
    :var businessObject: The businessObject for which to retrieve a stylesheet.  This field may be NULL.  Typically it
    would only be NULL in the case of CREATE.
    :var businessObjectType: The Teamcenter data type for which to retrieve a stylesheet, if the businessObject
    parameter is NULL, then this field must be populated, otherwise it is ignored.
    :var styleSheetType: The type of stylesheet to return.  Legal values are: SUMMARY, CREATE, RENDERING, or INFO.
    :var styleSheetLastModDate: The last save date of the stylesheet.
    :var clientContext: The map of client context key value entries, where the key is the client and the location in
    the client, and the value is the unique id for the data being presented in that panel.  These values are used to
    process visibleWhen clasuses in the XRT, pages may be enabled or disabled based on where it is being presented in
    the client.
    
    For example valid entries for active workspace may be:
    Key: ActiveWorkspace:Location  
    Value: com.siemens.splm.client.search.SearchLocation
    
    Or
    
    Key: ActiveWorkspace:SubLocation  
    Value: com.siemens.splm.client.search:SavedSearchSubLocation
    """
    targetPage: str = ''
    businessObject: BusinessObject = None
    businessObjectType: str = ''
    styleSheetType: str = ''
    styleSheetLastModDate: datetime = None
    clientContext: StringMap4 = None


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
    :var objectSetMap: A Map (string/Teamcenter::Awp0XRTObjectSet) where key is the source field from the stylesheet
    and the value is the data to present inside that objectSet in the application.
    :var localeMap: Map (string/string) where the key is the text, title, or titleKey string from the stylesheet and
    the value is the localized string.
    :var jtFileMap: Map (BusinessObject/string) where the key is the business object to render, and the value is the
    thumbnail ticket for the image to download.
    :var visiblePages: The visible pages in the XRT.  Each bit indicates whether that page can be displayed. Currently
    the maximum number of pages allowed in an XRT is 32.
    :var classificationData: The classification data for the object to be rendered.
    """
    processedPage: str = ''
    datasetInfo: GetStyleSheetDatasetInfo = None
    objectSetMap: ObjectSetMap3 = None
    localeMap: StringMap4 = None
    jtFileMap: ThumbnailMap3 = None
    visiblePages: int = 0
    classificationData: List[GetStyleSheetClassificationData] = ()


@dataclass
class GetStyleSheetResponse(TcBaseObj):
    """
    Response sent to client from the getStyleSheet operation.
    
    :var output: The vector of output information.  One for each input object.
    :var serviceData: The SOA service data.
    """
    output: List[GetStyleSheetOutput] = ()
    serviceData: ServiceData = None


"""
Maps the object set source in the xml rendering style sheet to the business objects.
"""
ObjectSetMap3 = Dict[str, Awp0XRTObjectSet]


"""
String map.
"""
StringMap4 = Dict[str, str]


"""
Maps a business object to a thumbnail file ticket.
"""
ThumbnailMap3 = Dict[BusinessObject, str]
