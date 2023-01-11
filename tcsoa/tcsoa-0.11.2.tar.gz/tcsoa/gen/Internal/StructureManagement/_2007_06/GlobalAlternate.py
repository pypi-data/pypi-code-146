from __future__ import annotations

from tcsoa.gen.BusinessObjects import Item
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GlobalAlternateList(TcBaseObj):
    """
    Holds a vector of global alternates, to be used by GlobalAlternateResponse Struct
    
    :var globalAlternates: A list of global alternates for the selected item
    """
    globalAlternates: List[Item] = ()


@dataclass
class GlobalAlternateListInput(TcBaseObj):
    """
    The GlobalAlternateListInput struct represents all of the data necessary to
    add and remove a list of global alternates.
    
    :var item: the selected item
    :var gAltItems: a list of global alternates to be added or removed
    """
    item: Item = None
    gAltItems: List[Item] = ()


@dataclass
class GlobalAlternateResponse(TcBaseObj):
    """
    Holds the response for listing, adding and removing global alternates
    
    :var globalAlternateLists: a vector of updated global alternate lists
    :var serviceData: Exceptions from internal processing returned as PartialErrors
    """
    globalAlternateLists: List[GlobalAlternateList] = ()
    serviceData: ServiceData = None


@dataclass
class PreferredGlobalAlternateInput(TcBaseObj):
    """
    The PreferredGlobalAlternateInput struct represents all of the data necessary to
    set the preferred global alternate of the selected item.
    
    :var item: the selected item
    :var gAltItem: the item to be set as preferred global alternate
    """
    item: Item = None
    gAltItem: Item = None
