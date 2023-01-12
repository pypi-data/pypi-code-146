from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LineItemPropertiesWithType(TcBaseObj):
    """
    The information about each BidPackageLineItem to be processed is provided by way of the
    'LineItemPropertiesWithType' data structure.
    
    :var name: Name of the BidPackageLineItem to be created.
    :var description: Description of the BidPackageLineItem Object.
    :var quote: Quote form to be added to BidPackageLineItem.
    :var bpliTypeName: Name of the type of the BidPackageLineItem to be used.
    :var liccname: Name of the LineItemConfigContext to be created.
    :var liccdesc: Description of the LineItemConfigContext to be created.
    :var partid: Id of the part to be associated with BidPackageLineItem.
    :var viewtype: PSView Type to be associated with LineItemConfigContext.
    :var quantity: Quantity to be created for BidPackageLineItem.
    :var revRule: Revision rule to be associated with LineItemConfigContext.
    :var varRule: Variant rule to be associated with LineItemConfigContext.
    :var closureRule: Closure rule to be associated with LineItemConfigContext.
    """
    name: str = ''
    description: str = ''
    quote: BusinessObject = None
    bpliTypeName: str = ''
    liccname: str = ''
    liccdesc: str = ''
    partid: str = ''
    viewtype: str = ''
    quantity: int = 0
    revRule: str = ''
    varRule: str = ''
    closureRule: str = ''
