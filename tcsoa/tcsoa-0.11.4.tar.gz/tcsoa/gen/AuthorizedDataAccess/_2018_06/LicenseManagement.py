from __future__ import annotations

from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LicenseDetails(TcBaseObj):
    """
    LicenseDetails structure represents all the details of an ADA License object.
    
    :var licenseType: The type of ADA License object. Supported types are 
    &amp;lt;i&amp;gt;ITAR_License&amp;lt;/i&amp;gt;, &amp;lt;i&amp;gt;Exclude_License&amp;lt;/i&amp;gt;, or
    &amp;lt;i&amp;gt;IP_License&amp;lt;/i&amp;gt;.
    :var licenseId: The unique ID of the license. This is string with a maximum of 128 characters.
    :var groups: A list of names of groups associated with the license identified by &amp;lt;font
    face=&amp;amp;quot;courier&amp;amp;quot;
    height=&amp;amp;quot;10&amp;amp;quot;&amp;gt;licenseId&amp;lt;/font&amp;gt;. For subgroups, the full names should
    be specified. When the license is attached to a classified WorkspaceObject;, the users from the groups or subgroups
    listed on the license will get access to the workspace objects, based on the access rules. This parameter
    represents an array of group name strings of upto 256 characters in size.
    :var newLicenseId: The unique ID of the license. This is string with a maximum of 128 characters. A non-empty value
    indicates the licenseId will be replaced by newLicenseId.
    :var licenseCategory: The category property of an ADA license. This is an optional parameter of string type 128
    characters in size. The value specified for licenseCategory parameter must match one of the values in the LOV
    associated with Category property on the specifc ADA license type.This is an optional parameter and may be left as
    a blank string (&amp;quot;&amp;quot;).
    :var userCitizenships: A list of user citizenships property values of an ADA license. This is an optional
    parameter. The value specified for userCitizenships parameter is an ISO-3166 two-letter country code. If a valid
    country code is not specified, partial error code 10219 will be returned.
    :var expiryDate: The expiry date for the license, after which the license cannot be attached to a WorkspaceObject
    and ceases to grant the access to users or groups listed on the license. The value specified for expiryDate should
    be greater than or equal to current date, unless the value is same as current value on an existing license. A NULL
    date specifies the license will never expire.
    :var lockDate: The freeze date for the license, after which the license cannot be attached to a WorkspaceObject.
    The value specified for this parameter should be greater than the current date and should be less than the value
    specified for expiryDate parameter, unless the value is same as current value on an existing license. A NULL date
    specifies the license is not locked.
    :var licenseReason: A reason for the license to exist. This parameter can be a maximum of 128 characters. This is
    an optional parameter and and  may be left as a blank string (&amp;quot;&amp;quot;).
    :var qualifyingCfr: The qualifying Code of Federal Regulations (CFR) for ITAR licenses. This is not applicable for
    IP and Exclude licenses. This parameter can be a maxiumum of 80 characters. This is an optional parameter and  may
    have value as a blank string (&amp;quot;&amp;quot;).
    :var users: A list of users associated with a license identified by &amp;lt;font
    face=&amp;amp;quot;courier&amp;amp;quot;
    height=&amp;amp;quot;10&amp;amp;quot;&amp;gt;licenseId&amp;lt;/font&amp;gt;. When the license is attached to a
    classified WorkspaceObject, the users listed on the license will get access to the WorkspaceObject, based on the
    access rules.
    """
    licenseType: str = ''
    licenseId: str = ''
    groups: List[str] = ()
    newLicenseId: str = ''
    licenseCategory: str = ''
    userCitizenships: List[str] = ()
    expiryDate: datetime = None
    lockDate: datetime = None
    licenseReason: str = ''
    qualifyingCfr: str = ''
    users: List[str] = ()
