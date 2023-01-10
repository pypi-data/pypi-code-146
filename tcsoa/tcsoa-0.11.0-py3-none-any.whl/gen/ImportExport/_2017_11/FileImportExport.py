from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.ImportExport._2011_06.FileImportExport import ImportExportOptions
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportPackingInfo(TcBaseObj):
    """
    The structure contains a primary business object and a list of secondary business objects.
    
    :var primaryObj: The primary business object. The primary business object can be of any type.
    :var secondaryObjs: A list of secondary business objects. The secondary business objects can be of any type.
    """
    primaryObj: BusinessObject = None
    secondaryObjs: List[BusinessObject] = ()


@dataclass
class ExportToApplicationInputData3(TcBaseObj):
    """
    The ExportToApplicationInputData3 structure represents all of the data necessary to export selected objects to
    specific application like MSExcel.
    
    :var exportPackingInfos: A list of ExportPackingInfo.
    :var columnAttributes: The column attributes to export.
    :var applicationFormat: The application format such as "MSExcel" and "MSExcelLive".
    Supported application formats for this operation:
    - MSExcel    This format is used for exporting Teamcenter objects to static MSExcel application. 
    - MSExcelLive    This format is used for exporting Teamcenter objects to Live MSExcel application.
    
    
    :var exportOptions: List of ImportExportOptions to be used during the export process.
    """
    exportPackingInfos: List[ExportPackingInfo] = ()
    columnAttributes: List[str] = ()
    applicationFormat: str = ''
    exportOptions: List[ImportExportOptions] = ()
