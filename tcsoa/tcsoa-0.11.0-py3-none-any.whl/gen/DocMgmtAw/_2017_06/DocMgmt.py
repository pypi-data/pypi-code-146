from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dma1PrintConfigRuntime
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PrinterDefinitionResponse(TcBaseObj):
    """
    Printer Definition Response structure.
    
    :var printConfigurations: A list of Print Configuration Runtime business objects.  This business object contains
    all print configuration information properties such as Print Configuration Name, Printer Name, Paper Sizes, etc.
    :var serviceData: Standard return; includes any error information.
    """
    printConfigurations: List[Dma1PrintConfigRuntime] = ()
    serviceData: ServiceData = None
