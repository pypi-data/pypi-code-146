from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetACLInfoResponse(TcBaseObj):
    """
    This structure holds the list of effective ACL reports for each of the given business objects.  Each effective ACL
    report contains the business object and corresponding effective ACL information.
    
    :var aclInfoList: List of derived Effective ACL reports for each of the given business objects.
    :var serviceData: Object that holds the partial errors that occurred while getting the effective ACL information
    for any of the given business objects.
    """
    aclInfoList: List[ACLInfos] = ()
    serviceData: ServiceData = None


@dataclass
class GetProtectionReportResponse(TcBaseObj):
    """
    This structure contains list of extra protection reports one for of each of the given business objects for the
    given user.
    
    :var protectionReports: List of extra protection report objects one for each of the given business objects.
    :var serviceData: Object that holds the partial errors occurred while deriving extra protection  information of any
    of the given business objects.
    """
    protectionReports: List[ProtectionReport] = ()
    serviceData: ServiceData = None


@dataclass
class Privilege(TcBaseObj):
    """
    This structure holds the name of the given privilege and its verdict that indicates if the privilege is granted or
    denied.
    
    :var privilegeName: The name of the access privilege.
    :var verdict: Value true means the privilege is granted and false means the privilege is denied.
    """
    privilegeName: str = ''
    verdict: bool = False


@dataclass
class PrivilegeReport(TcBaseObj):
    """
    This structure holds the business object for which access privileges are successfully evaluated and corresponding
    privileges information. Privilege information includes the privilege name and corresponding verdict for each of the
    given privileges.
    
    :var object: Business object on which access privileges are evaluated successfully  for the given groupMember.
    :var privilegeInfos: A list of evaluated access privileges and corresponding verdicts for the given groupMember on
    the business object.
    """
    object: BusinessObject = None
    privilegeInfos: List[Privilege] = ()


@dataclass
class PrivilegeSettingInput(TcBaseObj):
    """
    This structure holds the object on which access privileges need to be modified and the sets of granted, denied and
    unset privileges for the given accessor type.
    
    :var object: POM_application_object or a named ACL.
    :var grant: A list of access privilege names that need to be granted.
    :var revoke: A list of access privilege names that need to be denied.
    :var unset: A list of access privilege names that need to be unset.
    """
    object: BusinessObject = None
    grant: List[str] = ()
    revoke: List[str] = ()
    unset: List[str] = ()


@dataclass
class Protection(TcBaseObj):
    """
    This structure contains the derived extra protection information corresponding to a single access privilege on a
    given business object for the given user.
    
    :var privilege: The name of the access privilege.
    :var verdict: True or false. True means the privilege is granted and false means the privilege is denied.
    :var rules: A list of access rules evalued to arrive at the verdict for the privilege.
    :var ruleEvaluation: A list of access rule arrangements involved in arriving at the verdict.
    :var acl: The name of the named ACL that is used to determine the verdict for this privilege. For object ACLs the
    name is "OBJECT".
    :var accessorType: The accessor type name corresponding to the ACE that involved in arriving at the privilege
    verdict.
    :var accessorId: The name of the accessor that is used in the ACE that is used to determine the privilege.
    """
    privilege: str = ''
    verdict: bool = False
    rules: List[str] = ()
    ruleEvaluation: List[str] = ()
    acl: str = ''
    accessorType: str = ''
    accessorId: str = ''


@dataclass
class ProtectionReport(TcBaseObj):
    """
    This structure holds the business object and corresponding derived extra protection information for all the access
    privileges for the given user.
    
    :var object: POM_object on which extra protection information is derived for the given user.
    :var protections: The derived extra protection information corresponding to the single business object.
    """
    object: BusinessObject = None
    protections: List[Protection] = ()


@dataclass
class CheckAccessorPrivilegesResponse(TcBaseObj):
    """
    A list of privilegeReport objects for each of the given business objects and each given privilege. Each
    PrivilegeReport object contains the business object and verdicts for all the given privileges.
    
    :var privilegeReports: A list of PrivilegeReport objects one for each of the given business object.
    :var serviceData: Object that holds the partial errors that resulted while determining the privileges on a business
    object through access rules evaluation.
    """
    privilegeReports: List[PrivilegeReport] = ()
    serviceData: ServiceData = None


@dataclass
class ACLInfo(TcBaseObj):
    """
    Structure to hold the ACE information for a single row in the effective ACL table like granted privileges, revoked
    privileges, Accessor Type name, Accessor Id and the ACL name.
    
    :var grantedNames: Names access privilege that are granted to the user on a given object.
    :var revokedNames: Names access privilege that are revoked to the user on a given object.
    :var accessorType: The name of the accessor type in the ACE that is applicable to the given business object and to
    the user.
    :var accessorId: The name of the accessor id in the ACE that is applicable to the given business object and to the
    user.
    :var namedACL: The name of the name of the ACL in the ACE that is applicable to the given business object and to
    the user.  Name for the object ACL is "ORBJECT".
    """
    grantedNames: List[str] = ()
    revokedNames: List[str] = ()
    accessorType: str = ''
    accessorId: str = ''
    namedACL: str = ''


@dataclass
class ACLInfos(TcBaseObj):
    """
    This structure holds the business object and corresponding effective ACL information derived through access rule
    evaluation.  Each effective ACL contains a list of ACE objects. Each ACE object is a single row in the effective
    ACL table that contains information like granted privileges, revoked privileges, Accessor Type name, Accessor Id
    and the ACL name.
    
    :var object: The business object for which effective ACL was derived.
    :var aclInfos: List of ACE objects returned from the server that make up the effective ACL for the business object.
    """
    object: BusinessObject = None
    aclInfos: List[ACLInfo] = ()
