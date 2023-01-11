from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetLicenseDetailsResponse(TcBaseObj):
    """
    'GetLicenseDetailsResponse' represents the details of ADA_License business objects.
    
    :var licDetails: Structures containing the properties of ADA_License business objects.
    :var serviceData: Contains partial errors encountered while fetching properties for ADA_License business objects.
    The ADA_License business objects for which properties are fetched successfully are added to the Plain list.
    """
    licDetails: List[LicenseDetails] = ()
    serviceData: ServiceData = None


@dataclass
class LicenseDetails(TcBaseObj):
    """
    'LicenseDetails' structure represents all the details of an ADA License object.
    
    :var licenseType: The type of ADA License object. The type can be ITAR_License, Exclude_License, or IP_License.
    :var licenseId: The unique ID of the license. This is string with a maximum of 128 bytes.
    :var expiryDate: The expiry date for the license, after which the license cannot be attached to WorkspaceObject
    business objects and ceases to grant the access to users/groups listed on the license. A NULL date specifies the
    license will never expire.
    :var licenseReason: A reason for the license to exist. This parameter can be a maximum of 128 bytes. This is an
    optional parameter and may have value as a blank string.
    :var users: The list of users associated with a license identified by 'licenseId'. When the license is attached to
    a classified WorkspaceObject, the users listed on the license will get access to the WorkspaceObject, based on the
    access rules.
    :var groups: List of names of groups associated with the license identified by 'licenseId'. For subgroups, the full
    names should be specified. When the license is attached to a classified WorkspaceObject, the users from the
    groups/subgroups listed on the license will get access to the workspace object, based on the access rules. This
    parameter represents an array of group name strings of upto 256 bytes in size.
    """
    licenseType: str = ''
    licenseId: str = ''
    expiryDate: datetime = None
    licenseReason: str = ''
    users: List[str] = ()
    groups: List[str] = ()


@dataclass
class LicenseIdAndType(TcBaseObj):
    """
    'LicenseIdAndType' structure Represents license Type and license ID of an ADA License object.
    
    :var licenseType: The type of a license object.  This is string with a maximum of 32 bytes.
    :var licenseId: The unique ID of the license object. This is string with a maximum of 128 bytes.
    """
    licenseType: str = ''
    licenseId: str = ''


@dataclass
class LicenseIdsAndTypesResponse(TcBaseObj):
    """
    'LicenseIdsAndTypesResponse' Represents the license IDs and types of ADA_License business objects.
    
    :var licIdType: Structures containing the license Type and license ID of fetched ADA_License business objects
    :var serviceData: Contains partial errors encountered while fetching ADA_License business objects.
    """
    licIdType: List[LicenseIdAndType] = ()
    serviceData: ServiceData = None


@dataclass
class LicenseInput(TcBaseObj):
    """
    'LicenseInput' represents a list of license IDs of ADA licenses and the associated WorkspaceObject business objects.
    
    :var selectedLicenses: List of license IDs of ADA licenses. These are strings of each with a maximum of 128 bytes
    size.
    :var objects: List of WorkspaceObject business objects associated with the 'selectedLicenses'.
    """
    selectedLicenses: List[str] = ()
    objects: List[BusinessObject] = ()


@dataclass
class LicenseTypeAndStatusFilter(TcBaseObj):
    """
    'LicenseTypeAndStatusFilter' structure Represents type and status of ADA License objects.
    
    :var licType: The type of ADA License objects. The type can be specified as ITAR_License, ExcludeE_License,
    IP_License, or, ALL. The value of ALL indicates that licenses of all types need to be fetched.
    :var licStatus: The status of ADA License objects. The value should be set to 'ALL' for returning all licenses. Any
    other value for 'licStatus' returns only unlocked and unexpired licenses.
    """
    licType: str = ''
    licStatus: str = ''
