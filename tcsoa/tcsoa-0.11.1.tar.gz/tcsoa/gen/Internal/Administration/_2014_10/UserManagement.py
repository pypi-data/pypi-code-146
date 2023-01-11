from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ActivateUserInput(TcBaseObj):
    """
    The input arguments for the activateUsers2 service operation.
    
    :var licenseLevel: The license level to be granted to the user. Valid values are:  
    - 0: author
    - 1: consumer
    - 2: occasional user
    - 3: viewer
    
    
    :var licenseBundle: The license bundle to be set for the user.  Bundle names are found in the license server or
    enter null for no bundle.  
    :var targetUser: The user to be activated and granted the license level, license bundle, and/or license server.
    :var licenseServer: The license server for the user.  This is a valid license server name configured by the
    administrator or null when using the site default license server.
    """
    licenseLevel: int = 0
    licenseBundle: str = ''
    targetUser: BusinessObject = None
    licenseServer: str = ''
