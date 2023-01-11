from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetSharedCommonClientFilesResponse(TcBaseObj):
    """
    The response structure for the getSharedCommonClientFiles operation.  This response contains a map of dataset name
    to DatasetInfo structures.  It also contains the serviceData.
    
    :var datasetInfoMap: This field contains the map of dataset names to thier DatasetInfo objects.
    :var serviceData: The SOA service data, this structure contains any partial errors encountered during processing.
    """
    datasetInfoMap: DatasetInfoMap = None
    serviceData: ServiceData = None


@dataclass
class GetStylesheetPref(TcBaseObj):
    """
    This structure defines the set of preferences that the client maybe defined for the operation.
    
    :var returnThumbnailTickets: If true the thumbnail FMS file tickets are returned.
    :var stylesheetFormat: The stylesheet format to be returned. Legal values are "XRTOnly", "HTMLOnly", or
    "HTMLPreferred".
    
    XRTOnly - Only XRT format is returned, no attempt to return HTML is made.
    
    HTMLOnly - Only the HTML format is returned, even in error situations.
    
    HTMLPreferred - HTML format is returned, except in error situations or when unsupported element or rendering hints
    are found in XRT.
    """
    returnThumbnailTickets: bool = False
    stylesheetFormat: str = ''


@dataclass
class GetStylesheetResponse(TcBaseObj):
    """
    Output structure for the getStylesheet operation.
    
    :var outputs: List of StylesheetOutput objects, one for each input object.
    :var serviceData: This service data contains any partial errors which may have been encountered during processing. 
    The partial error client Ids match the client Id for the input which failed.
    """
    outputs: List[StylesheetOutput] = ()
    serviceData: ServiceData = None


@dataclass
class StylesheetInputData(TcBaseObj):
    """
    The StylesheetInputData structure contains all the data required in order to a server to process the input object
    and return the result to the client.
    
    :var clientId: This is a unique identifier in order to look up Partial Errors and find corresponding output
    structures.
    :var boName: The business object type name.  It is used to determine the stylesheet to load.  If the boReference
    field is input, then this field is ignored.
    :var boReference: The object for which to load a stylesheet.  If this field is input then the boName field is
    ignored.
    :var stylesheetType: The stylesheet type to search for. The value may be "Summary", "Form", "Create", "SaveAs", or
    "Properties".
    """
    clientId: str = ''
    boName: str = ''
    boReference: BusinessObject = None
    stylesheetType: str = ''


@dataclass
class StylesheetOutput(TcBaseObj):
    """
    The StylesheetOutput structure contains all the data required for a client to present the stylesheet to the user
    for the input object.
    
    :var clientId: This is the client Id which was sent in on input.
    :var xrtStylesheet: The XRT style sheet, if XRT is to be returned.
    :var htmlStylesheet: The HTML stylesheet, if HTML is to be returned.
    :var childrenMap: The map of property names on the input type to children(string/vector<BusinessObject>) which are
    to be displayed in UI.
    :var thumbnailFileTicketMap: A map of child BusinessObject to its thumbnail file ticket (business object/string).
    """
    clientId: str = ''
    xrtStylesheet: str = ''
    htmlStylesheet: str = ''
    childrenMap: StylesheetChildrenMap = None
    thumbnailFileTicketMap: FileTicketMap = None


@dataclass
class DatasetInfo(TcBaseObj):
    """
    This structure contains the ZIPFILE file tickets and last mod date for the dataset.
    
    :var lastModDate: This field contains the dataset's last modified date.
    :var fileTickets: This is the vector of ZIPFILE file tickets for the dataset.
    """
    lastModDate: datetime = None
    fileTickets: List[str] = ()


"""
This is a map of dataset name to DatasetInfo object.
"""
DatasetInfoMap = Dict[str, DatasetInfo]


"""
Map from business object to thumbnail file ticket.
"""
FileTicketMap = Dict[BusinessObject, str]


"""
Map of property names to child objects.
"""
StylesheetChildrenMap = Dict[str, List[BusinessObject]]
