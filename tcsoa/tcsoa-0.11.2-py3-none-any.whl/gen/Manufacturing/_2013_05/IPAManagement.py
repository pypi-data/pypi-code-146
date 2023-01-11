from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FileTicketDetails(TcBaseObj):
    """
    The details of the file ticket.
    
    :var fileName: The name of the log file.
    :var fileTicket: The file management server ticket of the file.
    """
    fileName: str = ''
    fileTicket: str = ''


@dataclass
class AppPathRootWindowDetails(TcBaseObj):
    """
    The apperance path root window and its type.
    
    :var productWindowAppPathRoot: The appearance path root window.
    :var appPathRootType: The type of appearance path root window.
    """
    productWindowAppPathRoot: BusinessObject = None
    appPathRootType: BusinessObject = None


@dataclass
class GenerateIPATreeResponse(TcBaseObj):
    """
    ServiceData element, appearance path root window along with its type which was generated during the operation and
    the log file details and its ticket. The newly created occurrence groups from the process strcture and appearance
    path root of the product strcuture is added to the Created object list of ServiceData. Partial errors occurred in
    the operation are added to ServiceData.
    
    :var serviceData: The Service Data.
    :var productWindowAppPathRoot: The appearance window which was created.
    :var appPathRootType: The type of appearance window which was created.
    :var logFileTicket: The details of the log file ticket.
    """
    serviceData: ServiceData = None
    productWindowAppPathRoot: BusinessObject = None
    appPathRootType: BusinessObject = None
    logFileTicket: FileTicketDetails = None


@dataclass
class IPAExistResponse(TcBaseObj):
    """
    ServiceData element, flag indicating whether IPA tree exists for the process structure and ticket of configuration
    file if the IPA tree exists for the structure. Partial errors occurred in Teamcenter internal APIs during the
    operation are returned in ServiceData.
    
    :var serviceData: The Service Data.
    :var isIPAExist: The flag indicating whether IPA tree exists for the process structure.
    :var configFileTicket: The ticket of configuration file. This file is saved as an attachment on the top-level
    process element on which the assembly tree was generated/updated. This file contains information about all the
    configured product structures consumed in the process structure.
    """
    serviceData: ServiceData = None
    isIPAExist: bool = False
    configFileTicket: FileTicketDetails = None


@dataclass
class IPATreeInput(TcBaseObj):
    """
    All the details for IPA generation that includes the name of the IPA, process types, consumption types, occurrence
    group type, effectivity, email notification details etc.
    
    :var configDetails: The configuration details about the IPA generation which includes details of process structure,
    consumption types, occurrence group types and effectivity details.
    :var emailDetails: The e-mail notification details like recipients of the e-mail, subject and content of the
    message.
    """
    configDetails: ConfigDetails = None
    emailDetails: EmailNotificationDetails = None


@dataclass
class LocalUpdateIPATreeResponse(TcBaseObj):
    """
    ServiceData element, the log file name and its ticket. The updated occurrence groups from the process structure and
    appearance path root of the product structure is added to the Updated object list of ServiceData. Partial errors
    occurred in the operation are added to ServiceData.
    
    :var serviceData: The Service Data.
    :var logFileticket: The details about the log file ticket.
    """
    serviceData: ServiceData = None
    logFileticket: FileTicketDetails = None


@dataclass
class CleanIPATreeResponse(TcBaseObj):
    """
    ServiceData element, appearance path root window along with its type which was deleted during the operation and the
    log file details and its ticket. The deleted occurrence groups from the process structure and deleted appearance
    path root of the product structure is added to the Deleted object list of ServiceData. Partial errors occurred in
    the operation are added to ServiceData.
    
    :var serviceData: The Service Data.
    :var appPathRootWindows: List of appearance windows deleted by the operation. These windows corressponds to product
    structures consumed in the process strcuture to be cleaned.
    :var logFileTicket: The details of the log file ticket.
    """
    serviceData: ServiceData = None
    appPathRootWindows: List[AppPathRootWindowDetails] = ()
    logFileTicket: FileTicketDetails = None


@dataclass
class ConfigDetails(TcBaseObj):
    """
    The configuration details about the IPA generation which includes details of process structure, consumption types,
    occurrence group types and effectivity details.
    
    :var processWindow: The window of the process structure in which items are consumed from a product structure.
    :var ipaName: The name of the IPA to be processed.
    :var occGrpType: The type of occurrence group to be generated for the assembly tree.
    :var processTypes: List of process types for which an assembly tree is generated.
    :var consumptionOccTypes: List of consumed occurrence types considered for generation of the assembly tree.
    :var effectivityDetails: The effectivity details for the IPA generation like end item, its revision, range and/or
    unit of effectivity.
    """
    processWindow: BusinessObject = None
    ipaName: str = ''
    occGrpType: str = ''
    processTypes: List[str] = ()
    consumptionOccTypes: List[str] = ()
    effectivityDetails: EffectivityDetails = None


@dataclass
class EffectivityDetails(TcBaseObj):
    """
    The effectivity details for the IPA generation like end item, its revision, range and/or unit of effectivity.
    
    :var effectivityEndItem: The end item of generated assembly tree to which the effectivity is associated.
    :var effectivityEndItemRev: The end item revision of generated assembly tree to which the effectivity is associated.
    :var effectivityUnitRange: The unit range of effectivity associated with IPA generated occurrence.
    :var effectivityDateRange: The date range of effectivity associated with IPA generated occurrence.
    """
    effectivityEndItem: BusinessObject = None
    effectivityEndItemRev: BusinessObject = None
    effectivityUnitRange: str = ''
    effectivityDateRange: str = ''


@dataclass
class EmailNotificationDetails(TcBaseObj):
    """
    The e-mail notification details like recipients of the e-mail, subject and content of the message.
    
    :var logFileName: This is name of the report on errors and problems during the operation. This report contains all
    the problems or conflicts that occurred during generate/update that need to be addressed, for example, missing
    targets, locked nodes, or checked out nodes.
    This file is saved as an attachment on the top-level process element on which the assembly tree was
    generated/updated. 
    
    :var isLogFileNeeded:  This flag is used to create a run-time statistic log for IPA generation.
    :var mailToReceivers: List of recipients to be added in 'To' list of the e-mail notification.
    :var mailCcReceivers: List of recipients to be added in 'Cc' list of the e-mail notification.
    :var mailSubject: The subject of the e-mail notification.
    :var mailMessage: The message content of the e-mail notification.
    """
    logFileName: str = ''
    isLogFileNeeded: bool = False
    mailToReceivers: List[str] = ()
    mailCcReceivers: List[str] = ()
    mailSubject: str = ''
    mailMessage: str = ''
