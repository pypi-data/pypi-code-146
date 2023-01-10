from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AuthorizationInfo(TcBaseObj):
    """
    This structure contains the accessor object, rule domain name and list of applications or utilities.
    
    :var accessorTag: Group or Role in the Group to which authorization rules need to be set.
    :var ruleDomain: Rule domain name. Valid value is either "application" or "utiltiy".
    :var names: A list of application IDs or utility IDs.
    """
    accessorTag: BusinessObject = None
    ruleDomain: str = ''
    names: List[str] = ()


@dataclass
class AccessorAccessibleNamesList(TcBaseObj):
    """
    This structure contains a list of AccessorAccessibleNamesResponse objects one for each of the given accessors and
    ServiceData.
    
    :var output: List of AccessorAccessibleNamesResponse objects one for each of the given accessors.
    :var partialErrors: The object that contains any partial errors that occur while getting the authorization rules
    for any of the given accessor.
    """
    output: List[AccessorAccessibleNamesResponse] = ()
    partialErrors: ServiceData = None


@dataclass
class AccessorAccessibleNamesResponse(TcBaseObj):
    """
    This structure contains the given accessor and rule domain and corresponding accessible applications or utilities
    (authorization rules) retrieved. If the rule domain string is "application" then the accessibleNames contains the
    application names. If the domain string is "utility" then the accessibleNames will contain the utility names.
    
    :var accessorTag: Accessor whose authorization rules need to be retrieved. This object can be either a Group or a
    Role in the group.
    :var ruleDomain: Rule domain name. Valid values for this string are "utility" and "application".
    :var accessibleNames: List of accessible application names or utility names for the given accessor.
    """
    accessorTag: BusinessObject = None
    ruleDomain: str = ''
    accessibleNames: List[str] = ()


@dataclass
class AccessorInfo(TcBaseObj):
    """
    This structure contains the accessor tag and rule domain name.
    
    :var accessorTag: Group or Role in the group to which authorization rules need to be set.
    :var ruleDomain: Rule domain name. Valid value is either "application" or "utiltiy".
    """
    accessorTag: BusinessObject = None
    ruleDomain: str = ''
