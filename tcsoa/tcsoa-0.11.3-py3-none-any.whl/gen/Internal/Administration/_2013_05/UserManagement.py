from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LicenseStatus(TcBaseObj):
    """
    The license status.
    
    :var numPurchasedLicenses: The number of licenses purchased for base license level.
    :var numUsedLicenses: The number of licenses used for base license level.
    :var numPurchasedLicenseBundles: The number of licenses purchased for the license bundle.
    :var numUsedLicenseBundles: The number of licenses used for license bundle.
    """
    numPurchasedLicenses: int = 0
    numUsedLicenses: int = 0
    numPurchasedLicenseBundles: int = 0
    numUsedLicenseBundles: int = 0


@dataclass
class LicenseStatusResponse(TcBaseObj):
    """
    The return data for the activateUsers2 service operation.
    
    :var licStatus: List of LicenseStatus objects, one for each ActivateUserInput object.
    :var serviceData: Object with all activated User objects in updated list and any errors that occurred during
    activating users.
    """
    licStatus: List[LicenseStatus] = ()
    serviceData: ServiceData = None


@dataclass
class ActivateUserInput(TcBaseObj):
    """
    The input arguments for the activateUsers2 service operation.
    
    :var licenseLevel: The license level to be granted to the user.
    :var licenseBundle: The license bundle to be set for the user.
    :var targetUser: The user to be activated and granted the license level.
    """
    licenseLevel: int = 0
    licenseBundle: str = ''
    targetUser: BusinessObject = None
