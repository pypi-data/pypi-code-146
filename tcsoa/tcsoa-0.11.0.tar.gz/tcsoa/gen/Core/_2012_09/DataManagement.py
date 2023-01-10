from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RelateInfoIn(TcBaseObj):
    """
    Information to perform relate operation
    
    :var target: parent object to which the created object will be related. This value will be ignored if relate is
    false. If value is null and relate is true, then a default target will be used based on WsoInsertNoSelectionsPref.
    :var propertyName: Name of the property with which the created object will be related to the input target object if
    defined or the default one.This value will be ignored if relate is false. If value is empty and relate is true,
    then default relation will be used.
    :var relate: A relation is created only if this value is true.
    """
    target: BusinessObject = None
    propertyName: str = ''
    relate: bool = False
