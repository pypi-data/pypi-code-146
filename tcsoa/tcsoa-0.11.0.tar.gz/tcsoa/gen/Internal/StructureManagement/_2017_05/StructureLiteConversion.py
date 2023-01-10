from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import RuntimeBusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ClassicBOMLineInfo(TcBaseObj):
    """
    This has the index of input Fnd0BOMLineLite object for which conversion is to be done along with the new BOMLine
    object created by the operation.
    
    :var inputLWBIndex: The index of input Fnd0BOMLineLite object for which conversion was done.
    :var convertedBOMLine: A corresponding BOMLine object that is created from the input Fnd0BOMLineLite object.
    :var lwbChildren: A list of existing Fnd0BOMLineLite child objects of 'convertedBOMLine'.
    """
    inputLWBIndex: int = 0
    convertedBOMLine: RuntimeBusinessObject = None
    lwbChildren: List[RuntimeBusinessObject] = ()


@dataclass
class ConversionResponse(TcBaseObj):
    """
    'ConversionResponse' contains list of 'ClassicBOMLineInfo'.
    
    :var convertedBOMLines: A list of 'ClassicBOMLineInfo'. This has the index of input Fnd0BOMLineLite object for
    which conversion is to be done along with the new BOMLine object created by the operation.
    :var serviceData: All BOMLine parent objects created during the conversion process are added to serviceData.
    All UIDs of deleted Fnd0BOMLineLite objects are added to serviceData.
    """
    convertedBOMLines: List[ClassicBOMLineInfo] = ()
    serviceData: ServiceData = None
