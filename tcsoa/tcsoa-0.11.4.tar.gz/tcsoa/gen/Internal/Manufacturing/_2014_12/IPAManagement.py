from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SearchDynamicIPAsOutput(TcBaseObj):
    """
    Object containing parent process or study and its dynamic in-process assembly objects.
    
    :var bopLine: Parent process Mfg0BvrProcess or study Mfg0BvrShdStudy object.
    :var dipaLines: A list of dynamic in-process assembly Mfg0BvrDynamicIPA objects.
    """
    bopLine: BusinessObject = None
    dipaLines: List[BusinessObject] = ()


@dataclass
class SearchDynamicIPAsResponse(TcBaseObj):
    """
    Response object for searchDynamicIPAs operation.
    
    :var output: List of objects containing parent process or study and its dynamic in-process assembly objects.
    :var serviceData: Standard service data.
    """
    output: List[SearchDynamicIPAsOutput] = ()
    serviceData: ServiceData = None
