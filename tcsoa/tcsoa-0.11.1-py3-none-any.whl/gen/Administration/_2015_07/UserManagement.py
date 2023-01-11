from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Fnd0CustomUserProfile, Person
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class UserObjectStructure(TcBaseObj):
    """
    The output structure for createOrUpdateUser operation. It contains created or updated User with its Person and
    Fnd0CustomUserProfile objects.
    
    :var user: The User object.
    :var person: The Person object of corresponding User.
    :var profile: The Fnd0CustomUserProfile object of corresponding User.
    """
    user: User = None
    person: Person = None
    profile: Fnd0CustomUserProfile = None


@dataclass
class CreateOrUpdateUserInputs(TcBaseObj):
    """
    Input structure to create or update User object.
    
    :var userId: User ID of the User object which need to be created or updated.
    :var person: Name of the Person this User belongs to.
    :var password: Password of the User in plain text.
    :var defaultGroup: Default group of the User.
    :var newOwner: The user ID of the new owning user of objects owned by the user to be deactivated.  It should be set
    only if the current user is going to be deactivated.
    :var newOwningGroup: The name of new owning group of objects owned by the user to be deactivated. It should be set
    only if the current user is going to be deactivated.
    :var userPropertyMap: Property map (string/list of strings) with property name of User and list of values in string
    format. The calling client is responsible for converting the different property types (int, float, date .etc) to a
    string using the appropriate functions in the SOA client framework&rsquo;s Property class.
    :var userAddlPropertyMap: Property map (string/list of strings) with property name of Fnd0CustomUserProfile and
    list of values in string format. The calling client is responsible for converting the different property types
    (int, float, date .etc) to a string using the appropriate functions in the SOA client framework&rsquo;s Property
    class.
    """
    userId: str = ''
    person: str = ''
    password: str = ''
    defaultGroup: str = ''
    newOwner: str = ''
    newOwningGroup: str = ''
    userPropertyMap: UserPropertyData = None
    userAddlPropertyMap: UserPropertyData = None


@dataclass
class CreateOrUpdateUserResponse(TcBaseObj):
    """
    Response structure of creteOrUpdateUser operation.
    
    :var userObjectMap: User Id and its corresponding UserObjectStructure which contains User, Person and
    Fnd0CustomUserProfile objects.
    :var serviceData: The Service Data with partial errors if any.
    """
    userObjectMap: UserObjectsMap = None
    serviceData: ServiceData = None


"""
Map of User Id and corersponding User objects.
"""
UserObjectsMap = Dict[str, UserObjectStructure]


"""
A map of property names and desired values (string/string) of User object.
"""
UserPropertyData = Dict[str, List[str]]
