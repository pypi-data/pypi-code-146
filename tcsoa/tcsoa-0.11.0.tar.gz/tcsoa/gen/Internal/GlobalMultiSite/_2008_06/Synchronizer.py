from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetExportedObjectsResponse(TcBaseObj):
    """
    It holds list of objects that were exported to target site and errors if any.
    
    :var exportedObjectsList: A list of objects that were exported to target site
    :var serviceData: The service data
    """
    exportedObjectsList: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class NamesAndValues(TcBaseObj):
    """
    It holds name of session or transfer option and its value.
    
    :var name: The name of option
    :var value: The value of option
    """
    name: str = ''
    value: str = ''


@dataclass
class TransferFormula(TcBaseObj):
    """
    It has information about option set, list of options and their values that were overridden by user, session options
    and name of transfer mode, FMS ticket of xlst file that was used during transfer.
    
    :var optionSetName: Option set name
    :var optionSetUid: Option set UID [This parameter is ignored]
    :var optionOverrides: This is the list of options and values that user has overridden from the TransferOptionSet
    object specified above.
    
    :var sessionOptions: This is the list of session options and values (options which are not part of the option set )
    that user has specified.
    
    :var transferModeName: Transfer mode name
    :var transferModeUid: Transfer mode UID [This gets ignored]
    :var xsltFMSTicket:  FMS ticket of xslt file.
    :var reason: Reason for transfer
    """
    optionSetName: str = ''
    optionSetUid: str = ''
    optionOverrides: List[NamesAndValues] = ()
    sessionOptions: List[NamesAndValues] = ()
    transferModeName: str = ''
    transferModeUid: str = ''
    xsltFMSTicket: str = ''
    reason: str = ''
