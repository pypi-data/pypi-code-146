from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import BusinessObject


@dataclass
class GetProductScopeForProcessResponse(TcBaseObj):
    """
    Response of getProductScopeForProcess operation.
    Returns a list of product line from BOM structure which are connected to the given process line with relation
    "Fnd0ProcessToScopeRel".
    
    The following partial errors may be returned as part of service data
    &bull;    200603     Invalid object type for process line.
    
    :var scopedProductBOMLine: list of map < Teamcenter::BusinessObject, std::vector<Teamcenter:: BusinessObject> >
    containing the input process line as key and a list of product line as value.
    :var serviceData: service data containing partial errors.
    """
    scopedProductBOMLine: List[InputProcLineToProductLinesMap] = ()
    serviceData: ServiceData = None


"""
A Map <BusinessObject, std::vector<BusinessObject> > contains the input process line as key and a list of related product lines from BOM structure as value.
"""
InputProcLineToProductLinesMap = Dict[BusinessObject, List[BusinessObject]]
