from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindSourcesOutput(TcBaseObj):
    """
    Contains multiple source BOMLine and integer based index to point output to corresponding input.
    
    :var inputIndex: Index to input list. Useful to map output list to input list.
    :var sourceLines: The source BOMLines objects for input target BOMLine and source BOMWindow. Source BOMLine and
    Target BOMLine are associated via PublishLink.
    """
    inputIndex: int = 0
    sourceLines: List[BOMLine] = ()


@dataclass
class FindSourcesResponse(TcBaseObj):
    """
    Contains 'FindSourcesOutput' containing multiple source BOMLine and index to map to source BOMLine to corresponding
    input target BOMLine.
    
    :var output: 'FindSourcesOutput' containing multiple source BOMLine and integer index to map source BOMLine to
    input target BOMLine.
    :var serviceData: 'ServiceData' with plain objects containing multiple source BOMLine and partial errors.
    """
    output: List[FindSourcesOutput] = ()
    serviceData: ServiceData = None
