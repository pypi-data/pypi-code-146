from __future__ import annotations

from tcsoa.gen.Internal.MultiSite._2007_06.ObjectDirectory import ItemIdRecordReturnStruct, PublicationRecordProperties
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LocatePublishedObjectResponse(TcBaseObj):
    """
    'LocatePublishedObjectResponse' structure contains locating information for the input object and 'Servicedata'.
    
    :var owningSiteId: List of owning siteids for all the input Published Objects tag strings.
    
    :var serverCorrelID: Server correlation ID.
    :var userDataInput: Added for future use.
    :var serviceData: The Service Data with failure message if any.
    """
    owningSiteId: List[int] = ()
    serverCorrelID: str = ''
    userDataInput: str = ''
    serviceData: ServiceData = None


@dataclass
class ODSOperationResponse(TcBaseObj):
    """
    'ODSOperationResponse' structure contains ODS response information and 'ServiceData'.
    
    :var serverCorrelID: Server correlation ID.
    :var userDataOutput: Added for future use.
    :var serviceData: The Service Data with failure message if any.
    """
    serverCorrelID: str = ''
    userDataOutput: str = ''
    serviceData: ServiceData = None


@dataclass
class QueryItemIdRecordResponse(TcBaseObj):
    """
    'QueryItemIdRecordResponse' structure contains output query results in 'ItemIdRecordReturnStruct' object and
    'ServiceData'.
    
    :var queryResults: List of 'ItemIdRecordReturnStruct' object which contains owning site id and flag for
    registration 
    for each input 'BoMfkInfo' object.
    :var serverCorrelID: Server correlation ID.
    :var userDataOutput: Added for future use.
    :var serviceData: The Service Data with failure message if any.
    """
    queryResults: List[ItemIdRecordReturnStruct] = ()
    serverCorrelID: str = ''
    userDataOutput: str = ''
    serviceData: ServiceData = None


@dataclass
class QueryPublicationRecordsResponse(TcBaseObj):
    """
    'QueryPublicationRecordsResponse' structure contains information returned from the query and 'ServiceData'.
    
    :var publishedObjTagAsString: List of published objects tag strings which returned as remote search results.
    
    :var serverCorrelID: Server correlation ID.
    :var userDataOutput: Added for future use.
    :var serviceData: The Service Data with failure message if any.
    """
    publishedObjTagAsString: List[str] = ()
    serverCorrelID: str = ''
    userDataOutput: str = ''
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
    
    :var clientCorrelID: Correlation Id of requesting client.
    :var userDataInput: Added for future use.
    :var customAttributeNames: String map of custom attributes of published Object and ODS custom attribute. This is
    used in case of extensible ODS feature.
    :var clientNode: Node name of requesting client.
    :var clientReleaseVersion: Teamcenter release version of requesting client.
    :var clientMinorReleaseVersion: Minor release version of requesting client.
    
    :var clientServiceReleaseVersion: Teamcenter release version of requesting client server.
    
    :var clientMaintPackVersion: Teamcenter maintaince pack version of requesting client.
    
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
    clientCorrelID: str = ''
    userDataInput: str = ''
    customAttributeNames: MapDataLogger = None
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
    'DescribePublicationRecordsResponse' structure object which has 'ServiceData' (contains failure with error message
    if any). It also contains vector of PublicationRecord properties.
    
    :var records: List of 'PublicationRecordProperties' object for all the input PublishedObjects tag strings.
    :var serverCorrelID: Server correlation ID.
    :var userDataOutput: Added for future use.
    :var serviceData: The 'ServiceData' with failure message if any.
    """
    records: List[PublicationRecordProperties] = ()
    serverCorrelID: str = ''
    userDataOutput: str = ''
    serviceData: ServiceData = None


"""
MapDataLogger
"""
MapDataLogger = Dict[str, str]
