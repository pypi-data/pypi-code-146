from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetRelatedObjectsResponse(TcBaseObj):
    """
    The GetRelatedObjectsResponse structure contains list of RelatedObjectsInfo and service data of the operation.
    
    :var response: Response structure containing list of objects in the database for a given list of displayed objects.
    :var serviceData: ServiceData for the operation.
    """
    response: List[RelatedObjectsInfo] = ()
    serviceData: ServiceData = None


@dataclass
class RelatedObjectsInfo(TcBaseObj):
    """
    The RelatedObjectsInfo structure contains parent business object, a list of child objects and the relation name by
    which parent and children are related. The RelatedObjectsInfo datastructure is used in both input and output. In
    input RelatedObjectsInfo, childrenObj are displayed objects. In output RelatedObjectsInfo childrenObj are actual
    object in database. The parentObj and propertyName remains same in both input and output.
    
    :var parentObj: A POM_Object  that contains the list of related objects.
    :var childrenObj: A list of POM_Object related to source object.
    :var propertyName: The name of the property that relates the actual child objects to the parent. The property can
    be a relation property or reference property or empty.
    """
    parentObj: BusinessObject = None
    childrenObj: List[BusinessObject] = ()
    propertyName: str = ''
