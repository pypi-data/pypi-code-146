from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetODSVersionResponse(TcBaseObj):
    """
    'GetODSVersionResponse' structure contains ODS version information and Servicedata
    
    :var serverReleaseVersion: Major release version of Teamcenter server hosting the ODS.
    :var serverMinorReleaseVersion: Minor release version of Teamcenter server hosting the ODS.
    :var serverServiceReleaseVersion: Service release version of Teamcenter server hosting the ODS.
    :var serverMaintPackVersion: Maintenance pack version of the server hosting the ODS.
    :var serverOdsMajorVersion: ODS services major version.
    :var serverOdsMinorVersion: ODS services minor version.
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
class QueryPublicationRecordsProperties(TcBaseObj):
    """
    'QueryPublicationRecordsProperties' structure holds the paramerters which needs to be queried with the ODS server.
    
    :var attributeName: Name of the attribute.
    :var attributeValue: Respective value for the attribute
    :var attributeType: Attribute type
    :var qryOperator: Standandard query operator.
    """
    attributeName: str = ''
    attributeValue: str = ''
    attributeType: str = ''
    qryOperator: str = ''


@dataclass
class QueryPublicationRecordsResponse(TcBaseObj):
    """
    'QueryPublicationRecordsResponse' structure holds the retrieved publication records.
    
    :var publishedObjTagAsString: List of PUIDs of the published object
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    publishedObjTagAsString: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class RepublishObjectInputProperties(TcBaseObj):
    """
    'RepublishObjectInputProperties'  structure contains list of property values which needs to be added in publication
    record.
    
    :var oldObjectTag: Unique id allocated to client site in the multisite federation
    :var pubRecProps: Object of 'TcEntPublicationRecordProperties' with the major attributes as object tag and owning
    site id.
    """
    oldObjectTag: str = ''
    pubRecProps: TcEntPublicationRecordProperties = None


@dataclass
class TcEntClientInfoProperties(TcBaseObj):
    """
    'TcEntClientInfoProperties' structure contains requesting ODS client information.
    
    :var clientSiteId: Unique id allocated to client TcEnt site.
    :var targetServerSiteId: ODS server site ID.
    :var clientNode: Machine name where TcEnterprise Server is running.
    :var clientReleaseVersion: TcEnterprise (ODS Client) server release version.
    :var clientServiceReleaseVersion: TcEnterprise (ODS Client) server release version.
    :var clientMaintPackVersion: TcEnterprise (ODS Client) server maintainace pack version.
    :var userName: Teamcenter user ID.
    :var groupName: Teamcenter group associated with the given user name.
    :var roleName: Teamcenter role associated with the given user name.
    :var customAttributeNames: The extra attributes added for the TcEnterprise (ODS Client) server client. This is used
    in case of extensible ODS feature.
    """
    clientSiteId: int = 0
    targetServerSiteId: int = 0
    clientNode: str = ''
    clientReleaseVersion: int = 0
    clientServiceReleaseVersion: int = 0
    clientMaintPackVersion: int = 0
    userName: str = ''
    groupName: str = ''
    roleName: str = ''
    customAttributeNames: MapData = None


@dataclass
class TcEntPublicationRecordProperties(TcBaseObj):
    """
    'TcEntPublicationRecordProperties' structure contains list of all PublicationRecord properties.
    
    :var owningSiteId: Unique id allocated to to client TcEnt site
    :var objectTag: Unique tag allocated to the object within session
    :var pubDate: Date of publication of Object
    :var creationDate: Date of creation of Object
    :var projectName: Project name, where object belongs
    :var releaseStatus: Object release status
    :var customAttributes: The extra attributes added for the TcEnterprise (ODS Client) server client. This is used in
    case of extensible ODS feature.
    :var objectId: Unique object id
    :var revisionId: Revision id of the published object
    :var objectName: Object name of published Object.
    :var objectDesc: Object Description if any, else the empty string
    :var objectClass: Classs of the Object
    :var objectType: Object type
    :var owningUserId: User id who owns the object
    :var owningGroupName: Groud name, where user belongs to
    """
    owningSiteId: int = 0
    objectTag: str = ''
    pubDate: datetime = None
    creationDate: datetime = None
    projectName: str = ''
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
class DescribePublicationRecordsResponse(TcBaseObj):
    """
    'DescribePublicationRecordsResponse' structure contains list of all PublicationRecord properties and 'Servicedata'.
    
    :var records: List of 'TcEntPublicationRecordProperties' object.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message
    """
    records: List[TcEntPublicationRecordProperties] = ()
    serviceData: ServiceData = None


"""
MapData
"""
MapData = Dict[str, str]
