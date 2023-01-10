from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetObjectsLockInfoResponse(TcBaseObj):
    """
    GetObjectsLockInfoResponse structure defines the response from getObjectsLockInfo operation. It contains the
    information of the found locks. It provides the errors if the operation fails too.
    
    :var lockInfo: The list of found lock information. It includes:
    1.    Business object UID.
    2.    Lock date and time.
    3.    Lock user id.
    4.    Lock node name.
    :var serviceData: Service data contains the errors if the operation fails.
    """
    lockInfo: List[MarkOTLockInfo] = ()
    serviceData: ServiceData = None


@dataclass
class MarkOTErrorInfo(TcBaseObj):
    """
    MarkOTErrorInfo structure represents the failure information for adding marks.
    
    :var objectUID: Business object UID.
    :var errorInfo: The error message for the business object. 
    It includes:
    1.    Error code from the server side.
    2.    Error message for the error code.
    """
    objectUID: str = ''
    errorInfo: List[NameAndValue] = ()


@dataclass
class MarkOTInfo(TcBaseObj):
    """
    MarkOTInfo structure represents the mark information for briefcase ownership transfer.
    
    :var objectUID: Business object UID.
    :var targetSiteId: Target site id for ownership transfer.
    :var userId: User id who locks the object.
    :var parentUID: The anchor business object. It is used by ItemRevision objects only and the value is its Item. The
    value is empty for other objects.
    """
    objectUID: str = ''
    targetSiteId: int = 0
    userId: str = ''
    parentUID: str = ''


@dataclass
class MarkOTLockInfo(TcBaseObj):
    """
    MarkOTLockInfo structure represents the lock information.
    
    :var objectUID: Business object UID.
    :var lockUserId: User id who locks the object.
    :var lockTime: Lock time.
    :var lockNodeName: Lock node name.
    """
    objectUID: str = ''
    lockUserId: str = ''
    lockTime: str = ''
    lockNodeName: str = ''


@dataclass
class NameAndValue(TcBaseObj):
    """
    NameAndValue structure represents a generic name-value pair.
    
    :var elementName: The name of the name-values pair.
    :var elementValue: The value of the name-values pair.
    """
    elementName: str = ''
    elementValue: str = ''


@dataclass
class QueryMarkOTResponse(TcBaseObj):
    """
    QueryMarkOTResponse structure defines the response from queryMarkOT operation. It contains the details of each
    marks. It provides errors if the operation fails too.
    
    :var markInfo: A list of found marks. 
    The information includes:
    1.    Business object UID.
    2.    Target site id.
    3.    Lock user id.
    4.    The anchor business object. This is used by ItemRevision and the value is its Item.
    :var serviceData: Service data contains the errors if the operation fails.
    """
    markInfo: List[MarkOTInfo] = ()
    serviceData: ServiceData = None


@dataclass
class RemoveMarkOTResponse(TcBaseObj):
    """
    RemoveMarkOTResponse structure defines the response from removeMarkOTForCurrentUser operation. It contains the
    success and failure information of each objects for removing marks. It provides the errors if the operation fails
    too.
    
    :var successInfo: The list of the success business object UID.
    :var failureInfo: The list of failure information. It includes:
    1.    Business object.
    2.    Error code.
    3.    Error message.
    :var serviceData: Service data contains the errors if the operation fails.
    """
    successInfo: List[str] = ()
    failureInfo: List[MarkOTErrorInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AddMarkOTResponse(TcBaseObj):
    """
    AddMarkOTResponse structure defines the response from addMarkOTForCurrentUser operation. It contains the success
    and failure information of every objects for marks. It provides the errors if the operation fails too.
    
    :var successInfo: The list of the success information. It includes:
    1.    Business object UID.
    2.    Target site id.
    3.    Lock user id.
    4.    The anchor business object. It is used by ItemRevision objects only and the value is its Item. The value is
    empty for other objects.
    :var failureInfo: The list of failure information. It includes:
    1.    Business object UID.
    2.    Error code.
    3.    Error message.
    :var serviceData: Service data contains the errors if the operation fails.
    """
    successInfo: List[MarkOTInfo] = ()
    failureInfo: List[MarkOTErrorInfo] = ()
    serviceData: ServiceData = None
