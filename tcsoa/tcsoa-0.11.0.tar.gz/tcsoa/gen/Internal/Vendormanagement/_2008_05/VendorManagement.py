from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ItemIDData(TcBaseObj):
    """
    Structure containing an item_id and a reference to an existing object with that ID.
    
    :var clientId: A unique string supplied by the caller which comes through input data.
    :var itemID: Existing Item object with the same item_id. The presence of this object indicates that the item
    already exists in the system, or that the supplied combination of external 'objectID' and 'contextID' is not unique.
    :var existingObject: Object tag of an existing item with the same item_id.
    The presence of this tag indicates that the item
    already exists in the system, or that the supplied
    combination of external object ID and context ID is
    not unique.
    """
    clientId: str = ''
    itemID: str = ''
    existingObject: BusinessObject = None


@dataclass
class ItemIDInput(TcBaseObj):
    """
    A structure of external IDs and context IDs. This data is used to generate the Item IDs with context. It will also
    be used to compare and find out existing Item with such ID.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify returned 'ItemData' elements and
    Partial Errors associated with this 'ItemIDInput'.
    :var externalObjectID: The object ID provided from the external system. The assumption is that this ID is unique
    within the supplied context.
    :var contextID: An ID designating the external system, usually the ID of a vendor or a partner company providing
    the Item information.
    """
    clientId: str = ''
    externalObjectID: str = ''
    contextID: str = ''


@dataclass
class ItemIDResponse(TcBaseObj):
    """
    Response structure for 'getItemIDwithContext'
    
    :var itemData: A list of ItemIDData structures which essentially denote generated IDs with potential existing Item
    with the generated ID. Errors\Partial errors will sit with standard Teamcenter 'ServiceData' structure.
    :var serviceData: Standard 'ServiceData' structure. It contains partial errors and failures along with the
    clientIds.
    """
    itemData: List[ItemIDData] = ()
    serviceData: ServiceData = None


@dataclass
class LineItemPropsWithType(TcBaseObj):
    """
    The information about each BidPackageLineItem type to be processed is provided by way of the
    'LineItemPropsWithType' data structure. This structure accepts the BidPackageLineItem type to be processed.
    
    :var name: Name of the BidPackageLineItem to be created.
    :var description: Description of the BidPackageLineItem Object.
    :var quote: BidPackageQuote object to be added to BidPackageLineItem.
    :var bpliTypeName: BidPackageLineItem Type name to be used.
    :var liccname: Name of the BidPackageLineItemConfigContext to be created.
    :var liccdesc: Description of the BidPackageLineItemConfigContext to be created.
    :var partid: Id of the part to be associated with BidPackageLineItem.
    :var viewtype: PSView Type to be associated with BidPackageLineItemConfigContext.
    :var quantity: Quantity to be created for BidPackageLineItem objects.
    :var revRule: Revision rule to be associated with BidPackageLineItemConfigContext.
    :var varRule: Variant rule to be associated with BidPackageLineItemConfigContext.
    :var closureRule: Closure rule to be associated with BidPackageLineItemConfigContext.
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
