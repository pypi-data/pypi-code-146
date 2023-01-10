from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile, Dataset
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DatashareManagerReplaceInfo(TcBaseObj):
    """
    Information about a file to be replaced asynchronously via Datashare Manager.
    
    :var dataset: The Dataset object to which the reference ImanFile object(s) are to be uploaded to the Teamcenter
    volume.
    :var imanFile: The ImanFile currently referenced by the Dataset.  This named reference is intended to be replaced
    by the operation.
    :var namedReferenceName: The named reference relation to the ImanFile object file.
    :var absoluteFilePath: The absolute file path of the file being uploaded on the client host, or an empty string if
    the end user should select the file to be uploaded by using the Data Share Manager user interface.
    """
    dataset: Dataset = None
    imanFile: ImanFile = None
    namedReferenceName: str = ''
    absoluteFilePath: str = ''
