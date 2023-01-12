from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import User, Fnd0CustomUserProfile
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class UserProfileProperties(TcBaseObj):
    """
    User and its Fnd0CustomUserProfile properties
    
    :var user: User object on which Fnd0CustomUserProfile properties need to be set.
    :var propertyMap: Property map with property name and list of values in string format. The calling client is
    responsible for converting the different property types (int, float, date .etc) to a string using the appropriate
    functions in the SOA client framework's Property class.
    """
    user: User = None
    propertyMap: PropertyNameValuesMap = None


@dataclass
class UserProfilePropertiesResponse(TcBaseObj):
    """
    A list of Fnd0CustomUserProfile objects, one for each of the given User object.
    
    :var userProfileMap: User and its corresponding Fnd0CustomUserProfile object.
    :var serviceData: The Service Data with partial errors if any.
    """
    userProfileMap: UserProfileMap = None
    serviceData: ServiceData = None


"""
A map of property names and desired values (string/string).
"""
PropertyNameValuesMap = Dict[str, List[str]]


"""
A map of User and its Fnd0CustomUserProfile object.
"""
UserProfileMap = Dict[User, Fnd0CustomUserProfile]
