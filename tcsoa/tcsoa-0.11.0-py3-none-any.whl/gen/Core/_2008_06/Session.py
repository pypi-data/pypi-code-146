from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDisplayStringsOutput(TcBaseObj):
    """
    The name/value pair of a Text Server key and its corresponding localized value.
    
    :var key: The textserver key.
    :var value: The localized value for the Text Server key.
    """
    key: str = ''
    value: str = ''


@dataclass
class GetDisplayStringsResponse(TcBaseObj):
    """
    The response for  the 'getDisplayStrings' operation.
    
    :var output: A list Text Server key/localized value pairs.
    :var serviceData: Partial errors with the key name attached to the partial error.
    """
    output: List[GetDisplayStringsOutput] = ()
    serviceData: ServiceData = None
