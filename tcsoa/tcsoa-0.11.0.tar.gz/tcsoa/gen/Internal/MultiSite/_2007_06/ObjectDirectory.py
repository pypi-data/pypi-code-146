from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetODSVersionResponse(TcBaseObj):
    """
    'GetODSVersionResponse'  structure contains ODS version information and 'Servicedata'.
    
    :var serverReleaseVersion: Major release version of Teamcenter server hosting the ODS.
    :var serverMinorReleaseVersion: Minor release version of Teamcenter server hosting the ODS.
    :var serverServiceReleaseVersion: Service release version of Teamcenter server hosting the ODS.
    :var serverMaintPackVersion: Maintenance pack version of the server hosting the ODS.
    :var serverOdsMajorVersion: ODS server major version.
    :var serverOdsMinorVersion: ODS server minor version.
    :var clientRejected: Access to the requesting TcEnt client rejected/ accepted.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    serverReleaseVersion: int = 0
    serverMinorReleaseVersion: int = 0
    serverServiceReleaseVersion: int = 0
    serverMaintPackVersion: int = 0
    serverOdsMajorVersion: int = 0
    serverOdsMinorVersion: int = 0
    clientRejected: bool = False
    serviceData: ServiceData = None


@dataclass
class ItemIdRecordReturnStruct(TcBaseObj):
    """
    'ItemIdRecordReturnStruct' structure contains Item registration information.
    
    :var siteId: Owning siteid of input item.
    :var isRegistered: Flag for item registration status, whether input itemid is registered or not in the ItemId
    registry.
    """
    siteId: int = 0
    isRegistered: bool = False


@dataclass
class ItemIdRecordsProperties(TcBaseObj):
    """
    'ItemIdRecordsProperties' structure which contains item records to be registered in Item registry.
    
    :var itemId: The ID of the Item to be registered.
    :var context: Not being used.
    :var registrationSite: Siteid of the owning site of given itemId.
    """
    itemId: str = ''
    context: str = ''
    registrationSite: int = 0


@dataclass
class LocatePublishedObjectResponse(TcBaseObj):
    """
    'LocatePublishedObjectResponse' structure contains locating information for the input object and 'Servicedata'.
    
    :var owningSiteId: List of owning siteids for all the input Published Objects tag  strings.
    
    :var serviceData: The Service Data with failure message if any.
    """
    owningSiteId: List[int] = ()
    serviceData: ServiceData = None


@dataclass
class PublicationRecordProperties(TcBaseObj):
    """
    'PublicationRecordProperties' structure which contains attributes of Published object which is published to ODS.
    
    :var owningSiteId: Siteid of owning site of published object.
    :var objectTag: Tag of the published object.
    :var creationDate: Date of creation of published Object.
    :var pubDate: Date of publication of published Object.
    :var releaseStatus: Relase status if any of published Object is released.
    :var customAttributes: It is a string Map of custom attributes of published Object and ODS custom attribute.  This
    is used in case of extensible ODS feature.
    :var objectId: ID of the published object.
    :var revisionId: Revision id of the published object.
    :var objectName: Object name of published Object.
    :var objectDesc: Object description of published Object
    :var objectClass: Object class name of published Object.
    :var objectType: Object tyoe name of published Object.
    :var owningUserId: Owning user id of published Object.
    :var owningGroupName: Owning group name of published Object.
    """
    owningSiteId: int = 0
    objectTag: str = ''
    creationDate: datetime = None
    pubDate: datetime = None
    releaseStatus: List[str] = ()
    customAttributes: MapData = None
    objectId: str = ''
    revisionId: str = ''
    objectName: str = ''
    objectDesc: str = ''
    objectClass: str = ''
    objectType: str = ''
    owningUserId: str = ''
    owningGroupName: str = ''


@dataclass
class QueryItemIdRecordResponse(TcBaseObj):
    """
    'QueryItemIdRecordResponse' structure contains output query results in 'ItemIdRecordReturnStruct' object and
    'ServiceData'
    
    :var queryResults: List of 'ItemIdRecordReturnStruct' object which contains owning site id and flag for
    registration for each input itemid.
    :var serviceData: The Service Data with failure message if any.
    """
    queryResults: List[ItemIdRecordReturnStruct] = ()
    serviceData: ServiceData = None


@dataclass
class QueryPublicationRecordsResponse(TcBaseObj):
    """
    'QueryPublicationRecordsResponse' structure contains information returned from the query and 'ServiceData'.
    
    :var publishedObjTagAsString: List of published objects tag strings which returned as remote search results.
    :var serviceData: The Service Data with failure message if any.
    """
    publishedObjTagAsString: List[str] = ()
    serviceData: ServiceData = None


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
    :var clientServiceReleaseVersion: Teamcenter  release version of requesting client server.
    :var clientMaintPackVersion: Teamcenter  maintaince pack version of requesting client.
    :var clientOdsMajorVersion: Client ODS major version.
    :var clientOdsMinorVersion: Client ODS minor version.
    :var userId: Logged in userid of requesting client.
    """
    clientSiteId: int = 0
    targetServerSiteId: int = 0
    userName: str = ''
    osUserName: str = ''
    groupName: str = ''
    roleName: str = ''
    customAttributeNames: MapData = None
    clientNode: str = ''
    clientReleaseVersion: int = 0
    clientMinorReleaseVersion: int = 0
    clientServiceReleaseVersion: int = 0
    clientMaintPackVersion: int = 0
    clientOdsMajorVersion: int = 0
    clientOdsMinorVersion: int = 0
    userId: str = ''


@dataclass
class DescribePublicationRecordsResponse(TcBaseObj):
    """
    'DescribePublicationRecordsResponse' structure contains list of all PublicationRecord properties and Servicedata.
    
    :var records: List of 'PublicationRecordProperties' object for all the input PublishedObjects tag strings.
    :var serviceData: The 'ServiceData' with failure message if any.
    """
    records: List[PublicationRecordProperties] = ()
    serviceData: ServiceData = None


@dataclass
class DistributedAppProperties(TcBaseObj):
    """
    'DistributedAppProperties' structure contains required information to call the DIST ITK.
    
    :var clientReleaseVersion: Requesting client release version.
    :var clientIrmNumber: Teamcenter version release, phase number.
    :var appName: Application name for corressponding dist ITK.
    :var opCode: Method opcode to perform operation.
    :var appInputStringVal: List of input arguments which are in encoded form given to particular DIST itk call.
    """
    clientReleaseVersion: int = 0
    clientIrmNumber: int = 0
    appName: str = ''
    opCode: int = 0
    appInputStringVal: List[str] = ()


@dataclass
class DistributedAppResponse(TcBaseObj):
    """
    'DistributedAppResponse' structure is response from the distributed application contains 'Servicedata' and
    'DistributedAppReturnStruct' objects.
    
    :var appResponse: List of 'DistributedAppReturnStruct'  structure object.
    
    :var serviceData: The Service Data with failure message if any.
    """
    appResponse: List[DistributedAppReturnStruct] = ()
    serviceData: ServiceData = None


@dataclass
class DistributedAppReturnStruct(TcBaseObj):
    """
    'DistributedAppReturnStruct' structure is return structure of the distributed application contains output values.
    
    :var appOutputStringVal: List of required output values depend on user input.
    :var errorCodes: List of error code.
    :var errorTexts: List of corressponing error texts for error codes.
    """
    appOutputStringVal: List[str] = ()
    errorCodes: List[int] = ()
    errorTexts: List[str] = ()


"""
MapData
"""
MapData = Dict[str, str]
