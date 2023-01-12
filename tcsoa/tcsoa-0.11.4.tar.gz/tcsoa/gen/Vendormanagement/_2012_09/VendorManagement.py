from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class VendorRoleData(TcBaseObj):
    """
    This is the structure containing VendorRole information.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify the Partial Errors associated
    with this 'VendorRoleData' input.
    :var description: Description of the object to be created.
    :var roleType: VendorRole type, it shall be Manufacturer,Supplier or Distributor
    :var remove: Flag to indicate VendorRole is to be added or removed.
    """
    clientId: str = ''
    description: str = ''
    roleType: str = ''
    remove: bool = False
