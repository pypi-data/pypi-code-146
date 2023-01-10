from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OtSearchInfo(TcBaseObj):
    """
    It specifies criteria for searching briefcase transactions that include OT.
    
    :var transactionType: Type of briefcase transaction i.e. briefcase is exported or imported.
    :var siteId: Id of the site to which briefcase is exported to or is imported from.
    :var startDate: Earliest date and time breifcase transaction must have occured.
    :var endDate: Latest date and time briefcase transaction must have occured.
    :var briefcaseName: Name of the briefcase file.
    """
    transactionType: str = ''
    siteId: int = 0
    startDate: datetime = None
    endDate: datetime = None
    briefcaseName: str = ''


@dataclass
class OtTransactionInfo(TcBaseObj):
    """
    It contains information of a briefcase transaction (that include OT) like transaction id, transaction type, site
    id, user id, transaction date and briefcase name.
    
    :var transactionId: Identifier of the briefcase transaction that includes OT.
    :var transactionType: Type specifying briefcase is exported/imported.
    :var siteId: Current owning site of the briefcase.
    :var userId: Id of the user who exported/imported the briefcase.
    :var transactionDate: Date on which transaction occurred.
    :var briefcaseName: Name of the briefcase file.
    """
    transactionId: str = ''
    transactionType: str = ''
    siteId: int = 0
    userId: str = ''
    transactionDate: datetime = None
    briefcaseName: str = ''


@dataclass
class OtTransactionResponse(TcBaseObj):
    """
    Response for findOtTransactions operation. It contains list of briefcase transactions (that include OT) and errors
    if any.
    
    :var otTransactions: List of OtTransactionInfo objects.
    :var serviceData: Service data contains the errors if the operation fails.
    """
    otTransactions: List[OtTransactionInfo] = ()
    serviceData: ServiceData = None


@dataclass
class RecoverOwnershipResponse(TcBaseObj):
    """
    It holds the FMS ticket of report which has information about the status of recover ownership operation and errors
    if any.
    
    :var reportFmsTicket: FMS ticket of the report file listing the details of all objects for which ownership is
    recovered. The FMS ticket can be used to download the file from server to client.
    :var serviceData: Service data contains the errors if the operation fails.
    """
    reportFmsTicket: str = ''
    serviceData: ServiceData = None
