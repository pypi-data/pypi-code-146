from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RIAttributeInfo(TcBaseObj):
    """
    The 'RIAttributeInfo' structures holds the name/value pairs of import option. Value can be single or multiple
    valued. The import options influences the business object export and has default value.
    
    :var name: Import option name for remote import.
    
    :var value: Values for remote import option (can be multi-valued strings).
    """
    name: str = ''
    value: List[str] = ()


@dataclass
class RemoteImportInfo(TcBaseObj):
    """
    The 'RemoteImportInfo' holds the business object and related information meant for remote import.
    
    
    :var object: Object for the remote import service
    :var reason: User input to explain, why the remote import of business object required. Its not a mandatory input
    and user can pass empty string.
    :var importOptions: Import options that influence, how the Business Objects are imported to target site.
    """
    object: BusinessObject = None
    reason: str = ''
    importOptions: List[RIAttributeInfo] = ()
