from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class StateNameValue(TcBaseObj):
    """
    This structure is used to hold a single name/value pair.
    
    :var name: The name of the UserSession state property.
    :var value: The value of the state property.
    """
    name: str = ''
    value: str = ''
