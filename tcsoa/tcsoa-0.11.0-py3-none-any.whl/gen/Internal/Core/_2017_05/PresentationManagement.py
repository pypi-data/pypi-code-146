from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetStylesheetPerPagePref(TcBaseObj):
    """
    A set of preferences related to stylesheet information specified for each input object.
    
    :var returnThumbnailTickets: If true the thumbnail FMS file tickets are returned.
    :var stylesheetFormat: The stylesheet format to be returned. Legal values are "XRTOnly", "HTMLOnly", or
    "HTMLPreferred".
    XRTOnly - Only XRT format is returned, no attempt to return HTML is made.
    HTMLOnly - Only the HTML format is returned, even in error situations.
    HTMLPreferred - HTML format is returned, except in error situations or when unsupported element or rendering hints
    are found in XRT.
    :var processEntireXRT: If true, this operation will process the data for the entire XRT stylesheet.  If false, this
    operation will only process the target page which is defined in the input structure.
    """
    returnThumbnailTickets: bool = False
    stylesheetFormat: str = ''
    processEntireXRT: bool = False


@dataclass
class GetStylesheetPerPageResponse(TcBaseObj):
    """
    Output structure for the getStylesheetPerPage operation.
    
    :var outputs: A list of StylesheetPerPageOutput objects, one for each input object.
    :var serviceData: This service data contains any partial errors which may have been encountered during processing.
    The partial error client Ids match the client Id for the input which failed.
    """
    outputs: List[StylesheetPerPageOutput] = ()
    serviceData: ServiceData = None


@dataclass
class StylesheetPerPageInputData(TcBaseObj):
    """
    A set of input data for which to retrieve stylesheet information. One input object corresponds to one Teamcenter
    object for which to retrieve data.
    
    :var clientId: This is a unique identifier in order to look up Partial Errors and find corresponding output
    structures.
    :var boName: The business object type name. It is used to determine the stylesheet to load. If the boReference
    field is set this field is ignored.
    :var boReference: The workspace object for which to load a stylesheet. If this field is set the boName field is
    ignored.
    :var stylesheetType: The stylesheet type to search for. Supported values are: "Summary", "Form", "Create",
    "SaveAs", or "Properties".
    :var targetPage: The page in the XRT stylesheet to get data for. This field is ignored if the parameter
    processEntireXRT in the preference is set to true.
    Name of the page in the XRT stylesheet to get the data for. The value can either be the page title key value, page
    title or page name, for example "web_xrt_Overview".  If the page refered to is not found or not visible, then first
    visible page in the XRT will be returned.
    If empty string is specified, the first visible page in the XRT
    will be returned.
    """
    clientId: str = ''
    boName: str = ''
    boReference: BusinessObject = None
    stylesheetType: str = ''
    targetPage: str = ''


@dataclass
class StylesheetPerPageOutput(TcBaseObj):
    """
    The StylesheetPerPageOutput structure contains all the data required for a client to present the stylesheet to the
    user for the input object.
    
    :var clientId: This is the client Id which was sent in on input.
    :var xrtStylesheet: The XRT style sheet, if XRT is to be returned.
    :var htmlStylesheet: The HTML stylesheet, if HTML is to be returned.
    :var childrenMap: The map (string, list of business object) where the key is  property name and the value is a list
    of child objects.
    These child objects also needs to be render in the UI along with boReference business object.
    :var thumbnailFileTicketMap: A map (business object, string) of child business objects to its thumbnail file ticket.
    :var processedPage: The name of the page that was processed. If the operation was invoked with processEntireXRT set
    to true, this field is empty.  If the operation was invoked with processEntireXRT set to false, then this field is
    populated with the page that was processed.  Typically the value of the processedPage would be the same as the
    targetPage, except when the targetPage value is empty or not found in the stylesheet.  In that case, then the first
    page in the stylesheet is processed.
    :var visiblePages: A list of visible pages in the XRT. The values can be either the page title key or page title or
    page name. The names from this list can be used in a subsequent call to this operation to query for the data for
    that page.
    """
    clientId: str = ''
    xrtStylesheet: str = ''
    htmlStylesheet: str = ''
    childrenMap: StylesheetPerPageChildrenMap = None
    thumbnailFileTicketMap: FileTicketMap2 = None
    processedPage: str = ''
    visiblePages: List[str] = ()


"""
Map from business object to thumbnail file ticket.
"""
FileTicketMap2 = Dict[BusinessObject, str]


"""
Map of property names to child objects.
"""
StylesheetPerPageChildrenMap = Dict[str, List[BusinessObject]]
