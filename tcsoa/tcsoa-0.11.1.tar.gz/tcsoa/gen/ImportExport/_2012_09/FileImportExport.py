from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.ImportExport._2011_06.FileImportExport import FileMetaData, ImportExportOptions
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportFromApplicationInputData3(TcBaseObj):
    """
    Structure represents the parameters required to import a requirement specification.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var transientFileWriteTicket: Transient File write ticket for the file to be imported.
    :var applicationFormat: Application format associated with the file to be imported into system.
    :var createSpecElementType: Subtype of specification element to be imported.
    :var specificationType: Type of the specification to be imported. RequirementSpec is default.
    :var isLive: Flag to determine live or non live import.
    :var selectedBomLine: BOMLine under which new structure will get imported.
    :var fileMetaDatalist: List of FileMetaData that has the imported file information. One for each imported
    specification.
    :var importOptions: List of options for import such as keywords. One for each imported specification.
    :var specDesc: Description to be set for an Item.
    """
    clientId: str = ''
    transientFileWriteTicket: str = ''
    applicationFormat: str = ''
    createSpecElementType: str = ''
    specificationType: str = ''
    isLive: bool = False
    selectedBomLine: BusinessObject = None
    fileMetaDatalist: List[FileMetaData] = ()
    importOptions: List[ImportExportOptions] = ()
    specDesc: str = ''
