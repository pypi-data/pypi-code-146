from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetLicenseBundlesResponse(TcBaseObj):
    """
    List of license bundle information, one for each unique license server. It represents the response data structure
    for the getLicenseBundles operation.
    
    :var licServerInfo: List of license server information.
    :var serviceData: Contains any partial errors.
    """
    licServerInfo: List[LicenseServerInfo] = ()
    serviceData: ServiceData = None


@dataclass
class LicenseBundleInfo(TcBaseObj):
    """
    This structure represents the details of a license bundle.
    
    :var licenseBundleName: The name of a license bundle. It is a string of upto 9 bytes in size.
    :var baseFeatureKey: The base license level feature key included in the license bundle. An empty string for this
    element indicates that there is no base license feature key in the license bundle.
    :var numberPurchased: The number of licenses purchased for the license bundle.
    :var expirationDate: The date after which the license bundle is not available for use.
    """
    licenseBundleName: str = ''
    baseFeatureKey: str = ''
    numberPurchased: int = 0
    expirationDate: datetime = None


@dataclass
class LicenseServerInfo(TcBaseObj):
    """
    This structure holds the name of the license server and a list of all license bundles associated with the license
    server. If there are no license bundles in a license server, then an empty list is returned.
    
    :var licenseServerName: The name of the license server for which bundles are fetched.
    :var licenseBundles: List of license bundles associated with this license server.
    """
    licenseServerName: str = ''
    licenseBundles: List[LicenseBundleInfo] = ()
