from __future__ import annotations

from tcsoa.gen.BusinessObjects import IDCWindow
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateIDCWindowOutput(TcBaseObj):
    """
    Contains IDCWindow created and index to map IDCWindow to source BOMLine OR ItemRevision.
    
    :var inputIndex: Integer pointing to input BOMLine or ItemRevision.
    :var idcWindow: The IDCWindow created for input BOMLine or ItemRevision.
    """
    inputIndex: int = 0
    idcWindow: IDCWindow = None


@dataclass
class CreateIDCWindowResponse(TcBaseObj):
    """
    Contains 'CreateIDCWindowOutput' containing created IDCWindow and index to map with source BOMLine OR ItemRevision.
    Response also contains 'ServiceData'.
    
    :var output: 'FindTargetsOutput' containing created IDCWindow for input BOMLine or ItemRevision and integer index
    to map IDCWindow to input source.
    :var serviceData: 'ServiceData' with created objects containing IDCWindow in created list and partial errors.
    """
    output: List[CreateIDCWindowOutput] = ()
    serviceData: ServiceData = None
