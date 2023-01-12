from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List
from tcsoa.gen.BusinessObjects import Item, ItemRevision


@dataclass
class ParentsWhereUsedResponse(TcBaseObj):
    """
    Used to return the response for ParentsWhereUsed operation
    
    :var itemRevisionToParentItemRevisions: Contains the Map of input Item Revisions with the Parent Item Revisions
    where they are used.
    :var totalPageCount: Return the total number of pages created while processing the input Item Revisions.
    :var serviceData: An object of the ServiceData that contains list of added, updated, or deleted objects.  Also
    contains list of any errors which occurred within the call.
    """
    itemRevisionToParentItemRevisions: ItemRevisionToItemRevisionsMap = None
    totalPageCount: int = 0
    serviceData: ServiceData = None


@dataclass
class ProductsWhereUsedRespone(TcBaseObj):
    """
    Used to return the response for ProductsWhereUsed operation.
    
    :var itemRevToProductItems: Contains the Map of input item revisions with the product items they are used in.
    :var totalPageCount: Return the total number of pages created while processing the request. The end user can use
    this count to ask for any page they want back from the operation.
    :var serviceData: An object of the ServiceData that contains list of added, updated, or deleted objects.  Also
    contains list of any errors which occurred within the call.
    """
    itemRevToProductItems: ItemRevToProductItemsMap = None
    totalPageCount: int = 0
    serviceData: ServiceData = None


"""
Defines a map that will be used to return Product Items where the Item Revision are used.
"""
ItemRevToProductItemsMap = Dict[ItemRevision, List[Item]]


"""
Defines a map that will be used to return Parent Item Revisions where the given Item Revisions are used as children.
"""
ItemRevisionToItemRevisionsMap = Dict[ItemRevision, List[ItemRevision]]
