from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, GroupMember
from typing import List
from tcsoa.gen.Server import Preferences, ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAvailableServicesResponse(TcBaseObj):
    """
    List of available services and operations.
    
    :var serviceNames: List of available services
    """
    serviceNames: List[str] = ()


@dataclass
class GetGroupMembershipResponse(TcBaseObj):
    """
    Info from 'getGroupMembership' operation.
    
    :var groupMembers: A list of all the valid GroupMember objects for the current session`s User.  A GroupMember holds
    identifiers for a User, Group, and Role and represents that the user belongs to a group with the particular role.
    :var serviceData: The plain list has all the GroupMembers, Groups and Roles for this User
    """
    groupMembers: List[GroupMember] = ()
    serviceData: ServiceData = None


@dataclass
class GetSessionGroupMemberResponse(TcBaseObj):
    """
    Information returned from the 'getSessionGroupMember' service operation.
    
    :var groupMember: The GroupMember object which represents the logged in user's, Group, and Role for the current
    session.
    :var serviceData: The GroupMember object is included in the plain list.
    """
    groupMember: GroupMember = None
    serviceData: ServiceData = None


@dataclass
class LoginResponse(TcBaseObj):
    """
    The  User and GroupMember objects for the user of this session. Partial errors are returned in the 'ServiceData'
    when the authentication is successful but requested role is not supported.
    
    :var user: The User of this session.
    :var groupMember: The GroupMember of this session.
    :var serviceData: The GroupMember and User are added to the plain object list.
    """
    user: User = None
    groupMember: GroupMember = None
    serviceData: ServiceData = None


@dataclass
class PrefSetting(TcBaseObj):
    """
    Info for setting preferences
    
    :var prefScope: The scope in which the preferences are to be set,
    "all", "site", "user", "group", or "role".
    :var prefName: The name of the preference.
    :var prefValues: The array of values for this perference.
    """
    prefScope: str = ''
    prefName: str = ''
    prefValues: List[str] = ()


@dataclass
class PreferencesResponse(TcBaseObj):
    """
    Info from get/setPreferences
    
    :var preferences: The requested preference name/values.
    :var serviceData: Any partial errors that may occur when filling this request.
    """
    preferences: Preferences = None
    serviceData: ServiceData = None
