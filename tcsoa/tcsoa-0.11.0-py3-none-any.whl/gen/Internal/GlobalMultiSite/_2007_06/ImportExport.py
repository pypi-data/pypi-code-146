from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportObjectsResponse(TcBaseObj):
    """
    The ExportObjectsResponse is used as a response for performing the 'exportObjects' operation.
    
    :var sitesResponse: A list of ExportObjectsSiteResponseInfo
    :var serviceData: serviceData
    """
    sitesResponse: List[ExportObjectsSiteResponseInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ExportObjectsSiteResponseInfo(TcBaseObj):
    """
    It is used for performing 'exportObjects' operation.
    
    :var siteId: Destination site id
    :var fileFmsTickets: A list of FMS ticket of output XML files.When there are a large number of exported objects,
    the export is broken up into multiple XML files
    :var logFmsTickets: A list of FMS ticket of output log files
    """
    siteId: int = 0
    fileFmsTickets: List[str] = ()
    logFmsTickets: List[str] = ()


@dataclass
class ImportObjectsResponse(TcBaseObj):
    """
    It is used as a response for performing 'importObjects' operation.
    
    :var fmsTicketOfFailedObjs: FMS ticket of file that contains a list of objects failed on import
    :var logFmsTicket: FMS ticket of log file
    :var servicedata: servicedata
    """
    fmsTicketOfFailedObjs: str = ''
    logFmsTicket: str = ''
    servicedata: ServiceData = None


@dataclass
class NamesAndValues(TcBaseObj):
    """
    The NamesAndValues structure represents a generic name-value pair.
    
    :var name: Name of the pair
    :var value: Value of the pair
    """
    name: str = ''
    value: str = ''


@dataclass
class OwningSiteAndObjs(TcBaseObj):
    """
    Vector of object and it's owning site.
    These objects need to be remote imported
    
    :var owningSiteId: owningSiteId
    :var objs: objs
    """
    owningSiteId: int = 0
    objs: List[BusinessObject] = ()


@dataclass
class StubReplicationInfo(TcBaseObj):
    """
    A stub is an object which acts as a place holder for actual object.This is used in multisite during data
    transfer,as sometimes we do not need all the dependent objects but it may not be possible to create the structure
    at target site without them.A stub serves the purpose in such situations.The StubReplicationInfo structure holds
    the stub objects that were replicated at masterSiteId site. The replicas are represented by by Global Service
    Identitiies  ( GSIdentites )in XML strings.
    
    
    :var masterSiteId: Master site id
    :var listOfGSIdentities: A list of objects were replicated
    """
    masterSiteId: int = 0
    listOfGSIdentities: List[str] = ()


@dataclass
class TransferFormula(TcBaseObj):
    """
    The TransferFormula structure contains the transfer options for performing an export.
    The transfer options can be TransferOptionSet, TransfferMode, list of options
    that override the ones specified in TransferOptionSet, and/or list of session options.
    Currently, the supported session options are 'OwnershipTransfer' and 'ContinueOnError'.
    
    :var optionSetName: Name of transfer option set.If option set is not specified TIEUnconfiguredExportDefault is used
    as default.
    :var optionSetUid: UID of transfer option set.If option set is not specified TIEExportDefaultTM transfer mode is
    used to export.
    :var optionOverrides: A list of override options.If the user wishes to change any default behaviour then these
    options are used to override.Example of a valid override option is
    - opt_entire_bom  False
    
    
    If the top item of an assembly is given as input, if the user does not want entire BOM to be processed then this is
    set to False.By default this value is set to True.
    :var sessionOptions: A list of session options.Some valid session options
    - ownership_transfer         yes or no
    - modified_objects_only     yes or no
    - revrule                         Latest Working or Any Status; Working or any rev rule name
    - svrule                         VariantRule Name
    - fastream                     yes
    - forceRetraverse             yes
    - ContinueOnError             yes
    
    
    :var transferModeName: Name of transfer mode.If not specified TIEExportDefaultTM will be taken as default.
    :var transferModeUid: UID of transfer mode.Name of transfer mode.No impact if this is not specified
    :var xsltFMSTicket: FMS ticket for the xsl file.No impact if this is not specified.
    :var reason: Reason for export.This is optional.
    """
    optionSetName: str = ''
    optionSetUid: str = ''
    optionOverrides: List[NamesAndValues] = ()
    sessionOptions: List[NamesAndValues] = ()
    transferModeName: str = ''
    transferModeUid: str = ''
    xsltFMSTicket: str = ''
    reason: str = ''


@dataclass
class CallToRemoteSiteResponse(TcBaseObj):
    """
    Remote exports objcets to specified sites. E-mail notification would be sent to
    current user if session option for email notification is set to true.
    
    :var msgIDs: msgIDs
    :var serviceData: serviceData
    """
    msgIDs: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class ChangeOwnershipInfo(TcBaseObj):
    """
    The ChangeOwnershipInfo has the list of objects whose ownership was transferred to replicaSiteId site.The
    transferred objects are represented by GSIdentites in XML strings.
    
    
    :var replicaSiteId: Replicated site id.Target site.
    :var listOfGSIdentities: A list of objects were transferred to replicaSiteId
    """
    replicaSiteId: int = 0
    listOfGSIdentities: List[str] = ()


@dataclass
class ConfirmExportResponse(TcBaseObj):
    """
    It is used as a response for performing confirmExport.
    
    :var ownershipChanges: A list of ChangeOwnershipInfo
    :var stubReplication: A list of stubReplication
    :var serviceData: serviceData
    """
    ownershipChanges: List[ChangeOwnershipInfo] = ()
    stubReplication: List[StubReplicationInfo] = ()
    serviceData: ServiceData = None


@dataclass
class DryRunExportResponse(TcBaseObj):
    """
    The dryRunExportResponse structure holds a string storing the File Management System(FMS) ticket of the report file
    which has information about the data that will be exported if real export was done.Any failure will be returned as
    partial errors.It is used as a response for performing 'dryRunExport'.
    
    :var fmsTicketForReport: FMS ticket of report file
    :var serviceData: serviceData
    """
    fmsTicketForReport: str = ''
    serviceData: ServiceData = None
