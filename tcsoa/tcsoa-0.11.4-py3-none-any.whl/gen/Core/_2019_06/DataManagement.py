from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import POM_object
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DeleteIn(TcBaseObj):
    """
    The DeleteIn structure is used to hold the input container, objects to be deleted associated as the property of the
    container. This structure also holds a flag to unlink the objects from the input container in case deletion fails.
    
    :var container: A  POM_object that is related to the objects to be deleted.
    :var objectsToDelete: A list POM_object objects be unrelated from the container object and  then deleted.
    :var property: The  name of the TypedRef or relation property with which the objects to be deleted are related to
    the input container
    :var unlinkAlways: If true the operation will unlink the objects from the input container in case of delete
    operation otherwise they remained linked.
    """
    container: POM_object = None
    objectsToDelete: List[POM_object] = ()
    property: str = ''
    unlinkAlways: bool = False
