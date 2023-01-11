from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProcessTextDatasetResponse(TcBaseObj):
    """
    This ProcessTextDatasetResponse structure is for the response of all processTextDataset operations.
    
    :var content: For the "load" action, this string contains the contents of the text file that is a named reference
    in the Dataset. If there is more than one named reference, only the first one is returned.  For "save" action, this
    string is empty.
    :var serviceData: The Service Data that may contain partial errors.
    """
    content: str = ''
    serviceData: ServiceData = None
