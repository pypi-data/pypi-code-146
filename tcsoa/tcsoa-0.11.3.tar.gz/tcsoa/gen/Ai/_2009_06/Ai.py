from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateScopedMultipleStructure3Response(TcBaseObj):
    """
    GenerateScopedMultipleStructure3Response struct
    
    :var ticket: The transient file ticket to be used for downloading the generated plmxml
    :var fileTickets: The transient file tickets for any files exported during generation of plmxml
    :var relativeFolderName: Name of the folder where the transient fileTickets have to be downloaded relative to the
    folder where plmxml file is downloaded.
    :var fileNames: filenames as they appear in the transient volume under the plmxml created folder.
    :var data: partial failures are returned - along with object ids for each plmxml data could not be generated.
    """
    ticket: str = ''
    fileTickets: List[str] = ()
    relativeFolderName: str = ''
    fileNames: List[str] = ()
    data: ServiceData = None
