from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetLicenseDetailsResponse(TcBaseObj):
    """
    LicenseDetailsResponse structure represents all the details of an ADA ADA_License business objects in  licDetails
    and operation status in serviceData.
    
    :var licDetails: Structures containing the properties of the given licenseADA_License business objects.
    :var serviceData: ServiceDataContains partial errors encountered while fetching properties for ADA_License business
    objects. The ADA_License business objects for which properties are fetched successfully are added to the Plan list.
    """
    licDetails: List[LicenseDetails] = ()
    serviceData: ServiceData = None


@dataclass
class LicenseDetails(TcBaseObj):
    """
    LicenseDetails structure represents all the details of an ADA License object.
    
    :var licenseType: The type of ADA License object. The type can be "ITAR_License", "Exclude_License", or
    "IP_License". The license type of existing licenses cannot be modified. An error will be thrown if the value of
    licenseType does not match the type of the license being modified.
    :var licenseId: The unique ID of the license. This is string with a maximum of 128 bytes.
    :var licenseCategory: The category property of an ADA license. This is an optional parameter of string type 128
    bytes in size. The value specified for licenseCategory parameter must match one of the values in the LOV associated
    with Category property on the specifc ADA license type.This is an optional parameter and may be left as a blank
    string ("").
    :var expiryDate: The expiry date for the license, after which the license cannot be attached to WorkspaceObjects
    and ceases to grant the access to users/groups listed on the license. The value specified for expiryDate should be
    greater than or equal to current date, unless the value is same as current value on an existing license. A NULL
    date specifies the lincense will never expire.
    :var lockDate: The freeze date for the license, after which the license cannot be attached to WorkspaceObjects. The
    value specified for this parameter should be greater than the current date and should be less than the value
    specified for expiryDate parameter, unless the value is same as current value on an existing license. A NULL date
    specifies the license is not locked.
    :var licenseReason: A reason for the license to exist. This parameter can be a maxiumum of 128 bytes. This is an
    optional parameter and may be left as a blank string ("").
    :var qualifyingCfr: The qualifying Code of Federal Regulations (CFR) for ITAR licenses. This is not applicable for
    IP and Exclude licenses. This parameter can be a maxiumum of 80 bytes. This is an optional parameter and  may be
    left as a blank string ("").
    :var users: The list of users associated with a license identified by licenseId. When the license is attached to a
    classified WorkspaceObject, the users listed on the license will get access to the WorkspaceObject, based on the
    access rules.
    :var groups: List of names of groups associated with the license identified by licenseId. For sub-groups, the full
    names should be specified. When the license is attached to a classified WorkspaceObject, the users from the
    groups/sub-groups listed on the license will get access to the workspace object, based on the access rules. This
    parameter takes an array of group name strings of upto 256 bytes in size.
    """
    licenseType: str = ''
    licenseId: str = ''
    licenseCategory: str = ''
    expiryDate: datetime = None
    lockDate: datetime = None
    licenseReason: str = ''
    qualifyingCfr: str = ''
    users: List[str] = ()
    groups: List[str] = ()
