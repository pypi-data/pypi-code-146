from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LicenseStatus(TcBaseObj):
    """
    This structure  holds the number of licenses purchased and the number of licenses used.
    
    :var numPurchasedLicenses: The number of licenses purchased.
    :var numUsedLicenses: The number of licenses used.
    """
    numPurchasedLicenses: int = 0
    numUsedLicenses: int = 0


@dataclass
class LicenseStatusResponse(TcBaseObj):
    """
    This structure  holds a list of license statuses for the each given user license type.
    
    :var licStatus: List of LicenseStatus objects, one for each ActivateUserInput object.
    :var serviceData: Object with all activated User objects in updated list and any errors that occurred during
    activating users.
    """
    licStatus: List[LicenseStatus] = ()
    serviceData: ServiceData = None


@dataclass
class ActivateUserInput(TcBaseObj):
    """
    This structure holds the User object to be activated and the license level to be granted for the user.
    
    :var licenseLevel: The license level to be granted to the user.
    :var targetUser: The user to be activated and granted the licnese level.
    """
    licenseLevel: int = 0
    targetUser: BusinessObject = None


@dataclass
class DeactivateUserInput(TcBaseObj):
    """
    This structure holds the target user to be deactivated and new user and group to take the ownership of objects
    owned by the target user.
    
    :var targetUser: The user to be deactivated.
    :var newUser: The new user to take ownership transferred from the deactivated user.
    :var newGroup: The new group to take ownership transferred from the deactivated user.
    """
    targetUser: BusinessObject = None
    newUser: BusinessObject = None
    newGroup: BusinessObject = None
