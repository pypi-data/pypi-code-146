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
    :var lockDate: The freeze date for the license, after which the license cannot be attached to WorkspaceObject
    business objects. A NULL date specifies the license is not locked.
    :var licenseReason: A reason for the license to exist. This parameter can be a maximum of 128 bytes. This is an
    optional parameter and may have value as a blank string
    :var qualifyingCfr: The qualifying Code of Federal Regulations (CFR) for ITAR licenses. This is not applicable for
    IP and Exclude licenses. This parameter can be a maxiumum of 80 bytes. This is an optional parameter and  may have
    value as a blank string.
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
    lockDate: datetime = None
    licenseReason: str = ''
    qualifyingCfr: str = ''
    users: List[str] = ()
    groups: List[str] = ()


@dataclass
class LicenseInput(TcBaseObj):
    """
    'LicenseInput' represents a list of license IDs of ADA licenses, associated WorkspaceObject business objects, and
    applicable authorizing paragraph information (valid for ITAR licenses only).
    
    :var selectedLicenses: List of license IDs of ADA licenses. These are strings with a maximum of 128 bytes size.
    :var objects: List of WorkspaceObject business objects associated with the 'selectedLicenses'.
    :var eadParagraph: List of authorizing paragraphs for the licenses being attached to WorkspaceObject business
    objects. These are strings with a maximum of 80 bytes size. The size of 'eadParagraph' vector should match the size
    of the 'selectedLicenses' (each entry in 'eadParagraph' maps to corresponding entry in 'selectedLicenses'). If a
    paragraph entry is not applicable for a specific license (paragraph entries are applicable only for licenses of
    ITAR type), then that entry can be left blank. System will ignore any paragraph entry if it is not applicable for a
    license to be attached. This is an optional parameter
    """
    selectedLicenses: List[str] = ()
    objects: List[BusinessObject] = ()
    eadParagraph: List[str] = ()
