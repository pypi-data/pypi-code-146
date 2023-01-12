from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class NameAuthorizationList(TcBaseObj):
    """
    This structure holds the accessibility information for the given user and group combinations on the given
    applications or utilities.
    
    :var output: A list of NameAuthorizationResponse objects one for each of the given application or utility.
    :var partialErrors: Object that holds the partial errors that occurred while getting the accessibility on any of
    the given application or utility.
    """
    output: List[NameAuthorizationResponse] = ()
    partialErrors: ServiceData = None


@dataclass
class NameAuthorizationResponse(TcBaseObj):
    """
    This structure contains the name of the given application or utility, rule domain name and the derived verdict that
    indicates whether the user and group combination have accessibility on the application or utility or not.  True
    value for the verdict indicates the user have authorization access on the application or the utility. False value
    for the verdict indicates the user doesn't have authorization access on the application or the utility.
    
    :var name: Name of the application or the utility.
    :var ruleDomain: Rule domain name.
    :var verdict: Derived verdict for the given user and group combination on the application or utility.
    """
    name: str = ''
    ruleDomain: str = ''
    verdict: bool = False


@dataclass
class NameInfo(TcBaseObj):
    """
    This structure contains the name of the application or utility and the rule domain that indicates whether the name
    is that of an application or that of a utility.
    
    :var name: Name of an application or a utility whose accessibility for the given user need to be determined.
    :var ruleDomain: The name of the rule domain. Valid rule domain  name is either Utility or Application.
    """
    name: str = ''
    ruleDomain: str = ''
