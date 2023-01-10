from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from enum import Enum
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ImportExportOptions(TcBaseObj):
    """
    This structure contains additional options required to pass during the Import\ or Export operations. This structure
    is used for providing the import or export options depending on the mode of operation. This is key/value pair.  
    
    The Structure contains following element:
    
    - option         Supported option name is: CheckOutObjects.
    - optionvalue    Supported option value is: CheckOutObjects.
    
    
    
    :var option: option name
    :var optionvalue: value
    """
    option: str = ''
    optionvalue: str = ''


@dataclass
class SetContentInput2(TcBaseObj):
    """
    SetContentInput2 structure represents the input parameter required for SOA operation setRichContent2.
    
    :var objectToProcess: SpecElementRevision or FullText object
    :var bodyText: Value of the new body text on the FullText object.
    :var lastSavedDate: Last saved date of Object.
    :var contentType: The content type on the FullText object.Supported values are: Value can be REQ_HTML,
    REQ_PLAINTEXT and REQ_RICHTEXT.
    :var isPessimisticLock: This parameter is unused currently. The Behavior will be added in future releases. This is
    the placeholder for implementing optimistic/pessimistic locking provided by framework.
    """
    objectToProcess: WorkspaceObject = None
    bodyText: str = ''
    lastSavedDate: datetime = None
    contentType: ContentTypes2 = None
    isPessimisticLock: bool = False


@dataclass
class ExportInputDataAsync(TcBaseObj):
    """
    The ExportInputDataAsync represents the data required to export selected objects to MSExcel.
    
    :var objectsToExport: A list of business objects (WorkspaceObject) to be exported.
    :var targetObjectsToExport: A list of business objects (WorkspaceObject) to be exported which acts as target
    objects used for comparing the contents. This is an optional parameter and can be empty.
    :var recipeSourceObjects: The recipe of selected BOMLine objects which contains information to reconstruct them
    back and export. This is an optional parameter and can be empty.
    :var recipeTargetObjects: The recipe of target BOMLine objects which contains information to reconstruct them back
    and export. This is an optional parameter used for compare scenarios and can be empty.
    :var attributesToExport: A list of attributes to export. This is an optional parameter which can be empty.
    :var applicationFormat: The application formats supported are: 
    "MSExcel", "MExcelLive", "MSExcelReimport".
    :var templateName: The name of the MSWord or MSExcel template.
    :var exportOptions: List of options for export. Supported options are: "CheckOutObjects", "RunInBackground".
    """
    objectsToExport: List[BusinessObject] = ()
    targetObjectsToExport: List[BusinessObject] = ()
    recipeSourceObjects: List[str] = ()
    recipeTargetObjects: List[str] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateName: str = ''
    exportOptions: List[ImportExportOptions] = ()


@dataclass
class ExportToApplicationInputData3(TcBaseObj):
    """
    DEPRECATED: The ExportToApplicationInput represents the data required to export selected objects to MSWord or
    MSExcel.
    
    - objectsToExport          The A list of Teamcenter business objects to be exported.
    - targetObjectsToExport  The list of Teamcenter business objects to be exported which acts as target objects used
    for comparing the contents. This is aAn optional parameter and can be empty.
    - attributesToExport       The A list of attributes to export. This is an optional parameter which can be empty.
    - applicationFormat         The application formats supported are: "MSExcel ", "MSWordXMLLive", "MExcelLive",
    "MSExcelReimport", "MSWordCompare", "HTML".
    - templateIName           The name of the MSWord or MSExcel template.
    - exportOptions             List of options for export. Supported  options are:   such as keywords like 
    "CheckOutObjects".
    
    
    
    :var objectsToExport: The list of Teamcenter business objects to be exported to MSWord or MSExcel.
    :var targetObjectsToExport: The list of Teamcenter business objects to be exported which acts as target objects
    used for comparing the contents. This is an optional parameter and can be empty.
    :var attributesToExport: The list of attributes to export. This is an optional parameter which can be empty.
    :var applicationFormat: The application formats supported are :
    "MSExcel","MSWordXMLLive","MExcelLive","MSExcelReimport","MSWordCompare","HTML"
    :var templateName: The name of the MSWord or MSExcel template.
    :var exportOptions: import export option
    """
    objectsToExport: List[BusinessObject] = ()
    targetObjectsToExport: List[BusinessObject] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateName: str = ''
    exportOptions: List[ImportExportOptions] = ()


class ContentTypes2(Enum):
    """
    ContentTypes2 enumeration represents the valid content types of the FullText object.
    """
    REQ_HTML = 'REQ_HTML'
    REQ_PLAINTEXT = 'REQ_PLAINTEXT'
    REQ_RICHTEXT = 'REQ_RICHTEXT'
