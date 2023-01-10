from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ACLInfos(TcBaseObj):
    """
    This structure holds the business object and corresponding effective ACL information derived through access rule
    evaluation.  Each effective ACL contains a list of ACE objects. Each ACE object is a single row in the effective
    ACL table that contains information like granted privileges, revoked privileges, Accessor Type name, Accessor Id
    and the ACL name.
    
    :var workSpaceObject: The business object for which effective ACL was derived.
    :var aclInfos: List of ACE objects returned from the server that make up the effective ACL for the business object.
    """
    workSpaceObject: BusinessObject = None
    aclInfos: List[ACLInfo] = ()


@dataclass
class ExtraProtectionInfo(TcBaseObj):
    """
    This structure contains the derived extra protection information corresponding to a single access privilege on a
    given business object for the given user.
    
    :var privilegeNameInfo: Object that holds the internal name and display name of the access privilege.
    :var verdict: The verdict for the privilege for the user on the object.
    :var rules: A list of access rules evaluated to arrive at the verdict for the privilege.
    :var ruleEvaluation: A list of access rule arrangements involved in arriving at the verdict. Arrangements means the
    order in which the rules are evaluated.
    :var aclNameInfo: Object that holds the internal and display names of the named ACL. For object ACLs the internal
    name is "OBJECT".
    :var accessorTypeNameInfo: Object that holds the internal and display names of the accessor type name corresponding
    to the ACE that involved in arriving at the privilege verdict.
    :var accessorIdInfo: Object that holds the internal and display names of the accessor Id  corresponding to the ACE
    that involved in arriving at the privilege verdict.
    """
    privilegeNameInfo: DisplayNameInfo = None
    verdict: bool = False
    rules: List[str] = ()
    ruleEvaluation: List[str] = ()
    aclNameInfo: DisplayNameInfo = None
    accessorTypeNameInfo: DisplayNameInfo = None
    accessorIdInfo: DisplayNameInfo = None


@dataclass
class ExtraProtectionInfoReport(TcBaseObj):
    """
    This structure holds the business object and corresponding derived extra protection information for all the access
    privileges for the given user.
    
    :var workSpaceObject: POM_object on which extra protection information is derived for the given user.
    :var extraProtectionInfos: The derived extra protection information corresponding to the single business object.
    """
    workSpaceObject: BusinessObject = None
    extraProtectionInfos: List[ExtraProtectionInfo] = ()


@dataclass
class ExtraProtectionInfoResponse(TcBaseObj):
    """
    This structure contains list of extra protection reports one for of each of the given business objects for the
    given user.
    
    :var extraProtectionReports: List of extra protection report objects one for each of the given business objects.
    :var serviceData: Object that holds the partial errors occurred while deriving extra protection  information of any
    of the given business objects.
    """
    extraProtectionReports: List[ExtraProtectionInfoReport] = ()
    serviceData: ServiceData = None


@dataclass
class PrivNamesInfoResponse(TcBaseObj):
    """
    This structure holds the internal and display names of all the Teamcenter access privileges.
    
    :var privNameInfos: A list of DisplayNameInfo objects that holds internal name and display names of each Teamcenter
    privilege objects.
    :var serviceData: Object that holds any of the partial errors that occurred while getting the display names of the
    privileges in Teamcenter. But in fact this operation will not result in any errors as it is returning the names of
    existing privileges. Scope for any errors is very less.
    """
    privNameInfos: List[DisplayNameInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AccessorTypesResponse(TcBaseObj):
    """
    This structure contains the internal names and corresponding display values for all the Accessor Types in
    Teamcenter.
    
    :var accessorTypeNameInfos: List of DisplayNameInfo objects containing the internal name and corresponding display
    name for each of the Accessor Types in Teamcenter.
    :var serviceData: Object that holds any partial errors that occur while getting the display names of the Accessor
    Types in Teamcenter.
    """
    accessorTypeNameInfos: List[DisplayNameInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ACLInfo(TcBaseObj):
    """
    Structure to hold the ACE information for a single row in the effective ACL table like granted privileges, revoked
    privileges, Accessor Type name, Accessor Id and the ACL name. This structure holds both internal names and
    corresponding display values for the names of Accessor Type, Named ACL, Privilege and Accessor ID that constitutes
    a single ACE.
    
    :var grantedPrivsInfo: A list of objects containing the internal and display names of the access privileges that
    are granted to the user on a given business object.
    :var revokedPrivsInfo: A list of  objects containing the internal and display names of the access privileges that
    are revoked to the user on a given business object.
    :var accessorTypeNameInfo: Object containing the internal and display names of the accessor type in the ACE that is
    applicable to the given business object and to the user.
    :var accessorIdInfo: Object containing the internal and display names of the accessor id in the ACE that is
    applicable to the given business object and to the user.
    :var aclNameInfo: Object containing the internal and display names of the ACL in the ACE that is applicable to the
    given business object and to the user.
    """
    grantedPrivsInfo: List[DisplayNameInfo] = ()
    revokedPrivsInfo: List[DisplayNameInfo] = ()
    accessorTypeNameInfo: DisplayNameInfo = None
    accessorIdInfo: DisplayNameInfo = None
    aclNameInfo: DisplayNameInfo = None


@dataclass
class ACLInfoResponse(TcBaseObj):
    """
    This structure holds the list of effective ACL reports for each of the given business objects.  Each effective ACL
    report contains the business object and corresponding effective ACL information.
    
    :var aclInfosList: List of derived Effective ACL reports for each of the given business objects.
    :var serviceData: Object that holds the partial errors that occurred while deriving the effective ACL information
    for any of the given business objects.
    """
    aclInfosList: List[ACLInfos] = ()
    serviceData: ServiceData = None


@dataclass
class DisplayNameInfo(TcBaseObj):
    """
    DisplayNameInfo structure holds the internal name and corresponding display name of objects like privilege, named
    ACL, Accessor type and Accessor Id.
    
    :var internalName: String representing the internal name of an access privilege or a named ACL or an accessor type
    or an accessor.
    :var displayName: String representing the display name of an access privilege or a named ACL or an accessor type or
    an accessor.
    """
    internalName: str = ''
    displayName: str = ''
