from __future__ import annotations

from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ItemIdRecordsProperties(TcBaseObj):
    """
    'ItemIdRecordsProperties' structure which contains itemids and MFK values to be registered in Item registry.
    
    :var itemId: The ID of the Item to be registered.
    :var context: Not being used.
    :var keyValue: MFK key value for a input item.
    :var domain: Domain name i.e. class name for a input item.
    :var registrationSite: Siteid of the owning site of given itemId.
    """
    itemId: str = ''
    context: str = ''
    keyValue: str = ''
    domain: str = ''
    registrationSite: int = 0


@dataclass
class PublicationRecordProperties(TcBaseObj):
    """
    'PublicationRecordProperties' structure which contains attributes of Published object which is published to ODS.
    
    :var owningSiteId: siteid of owning site of published object.
    :var objectTag: Tag of the published object.
    :var creationDate: Date of creation of published Object.
    :var pubDate: Date of publication of published Object.
    :var releaseStatus: Relase status if any of published Object is released.
    :var domainName: MFK domain name of published Object.
    :var keyValue: MFK value of published Object.
    :var customAttributes: It is a string Map of custom attributes of published Object and ODS custom attribute.  This
    is used in case of extensible ODS feature.
    :var l10NPropertiesInfo: List of localized attributes of published Object.
    :var l10NLocalizedValues: List of corressponding localized attribute values of published Object.
    :var localeCountStr: Formated string which contains value count of locales for each localized attribute.
    :var objectId: ID of the published object.
    :var revisionId: Revision id of the published object.
    :var objectName: Object name of published Object.
    :var objectDesc: Object description of published Object.
    :var objectClass: Object class name of published Object.
    :var objectType: Object type name of published Object.
    :var owningUserId: Owning user id of published Object.
    :var owningGroupName: Owning group name of published Object.
    """
    owningSiteId: int = 0
    objectTag: str = ''
    creationDate: datetime = None
    pubDate: datetime = None
    releaseStatus: List[str] = ()
    domainName: str = ''
    keyValue: str = ''
    customAttributes: MapDataMfk = None
    l10NPropertiesInfo: List[str] = ()
    l10NLocalizedValues: List[str] = ()
    localeCountStr: str = ''
    objectId: str = ''
    revisionId: str = ''
    objectName: str = ''
    objectDesc: str = ''
    objectClass: str = ''
    objectType: str = ''
    owningUserId: str = ''
    owningGroupName: str = ''


@dataclass
class BoMfkInfo(TcBaseObj):
    """
    'BoMfkInfo' structure contains mfk value for which item id record to be queried from the Item registry.
    
    
    :var itemId: The ID of the Item to be unregistered.
    :var keyValue: MFK key value for a input item to be unregistered.
    :var domain: Domain name of the MultifieldKey i.e. class name for a input item.
    """
    itemId: str = ''
    keyValue: str = ''
    domain: str = ''


@dataclass
class ClientInfoProperties(TcBaseObj):
    """
    'ClientInfoProperties' structure contains requesting ODS client information.
    
    :var clientSiteId: Requesting client siteid.
    :var targetServerSiteId: Target server siteid.
    :var userName: Logged in username of requesting client.
    :var osUserName: OS logged in username of requesting client node.
    
    :var groupName: Group name of userid of requesting client.
    
    :var roleName: Role name of userid of requesting client.
    
    :var customAttributeNames: String map of custom attributes of published Object and ODS custom attribute. This is
    used in case of extensible ODS feature.
    
    :var clientNode: Node name of requesting client.
    :var clientReleaseVersion: Teamcenter release version of requesting client.
    :var clientMinorReleaseVersion: Minor release version of requesting client.
    :var clientServiceReleaseVersion: Teamcenter release version of requesting client server.
    
    :var clientMaintPackVersion: Teamcenter maintaince pack version of requesting client.
    
    :var clientOdsMajorVersion: Client ODS major version.
    :var clientOdsMinorVersion: client ODS minor version.
    :var userId: Logged in userid of requesting client.
    """
    clientSiteId: int = 0
    targetServerSiteId: int = 0
    userName: str = ''
    osUserName: str = ''
    groupName: str = ''
    roleName: str = ''
    customAttributeNames: MapDataMfk = None
    clientNode: str = ''
    clientReleaseVersion: int = 0
    clientMinorReleaseVersion: int = 0
    clientServiceReleaseVersion: int = 0
    clientMaintPackVersion: int = 0
    clientOdsMajorVersion: int = 0
    clientOdsMinorVersion: int = 0
    userId: str = ''


"""
Map Data
"""
MapDataMfk = Dict[str, str]
