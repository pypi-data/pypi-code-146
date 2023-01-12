from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetReservationHistoryResponse(TcBaseObj):
    """
    GetReservationHistoryResponse
    
    :var histories: Reservation history.
    :var serviceData: Objects which are queried successfully are added to the ServiceData plain list.
    """
    histories: List[ReservationHistory] = ()
    serviceData: ServiceData = None


@dataclass
class ReservationHistory(TcBaseObj):
    """
    Reservation history.
    
    :var object: Object of reservation history.
    :var events: Sequence of history events, earliest first.
    """
    object: BusinessObject = None
    events: List[ReservationHistoryEvent] = ()


@dataclass
class ReservationHistoryEvent(TcBaseObj):
    """
    Single event in reservation history.
    
    :var dateTime: Date and time of event.
    :var user: User name.
    :var activity: Event type.  "Check-Out"/"Check-In"/"Cancel Check-Out".
    :var changeId: change id as provided during 'checkout' operation.
    :var comment: User comment
    """
    dateTime: str = ''
    user: str = ''
    activity: str = ''
    changeId: str = ''
    comment: str = ''
