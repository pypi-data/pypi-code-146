from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TCCalendarEvent, TCCalendar
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetTCCalendarData(TcBaseObj):
    """
    The query information for calendars
    
    :var type: The type of TCCalendar (1-System Calendar, 2-Schedule Calendar, 3-User Calendar, 4-ScheduleMember
    Calendar)
    :var schedule: The related schedule
    :var resource: The related resource
    """
    type: int = 0
    schedule: BusinessObject = None
    resource: BusinessObject = None


@dataclass
class NewTCCalendar(TcBaseObj):
    """
    Holder for new tccalendar and its events
    
    :var tccalendarAttributes: The calendar data
    :var newEvents: The calendar events.
    """
    tccalendarAttributes: TCCalendarData = None
    newEvents: List[TCCalendarEventData] = ()


@dataclass
class TCCalendarContainer(TcBaseObj):
    """
    Holder for TCCalendar and its events
    
    :var tccalendar: The TCCalendar
    :var events: The TCCalendarEvents for the TCCalendar.
    """
    tccalendar: TCCalendar = None
    events: List[TCCalendarEvent] = ()


@dataclass
class TCCalendarData(TcBaseObj):
    """
    Data for a calendar
    
    :var name: Name of the tccalendar
    :var description: Description of the tccalendar
    :var minsFri: Default minutes for Friday
    :var minsSat: Default minutes for Saturday
    :var schedule: Null indicates no schedule
    :var source: TCCalendar source(schedule/resource)
    :var type: Type of tccalendar
    :var minsSun: Default minutes for Sunday
    :var minsMon: Default minutes for Monday
    :var minsTue: Default minutes for Tuesday
    :var minsWed: Default minutes for Wednesday
    :var minsThu: Default minutes for Thursday
    """
    name: str = ''
    description: str = ''
    minsFri: int = 0
    minsSat: int = 0
    schedule: BusinessObject = None
    source: BusinessObject = None
    type: int = 0
    minsSun: int = 0
    minsMon: int = 0
    minsTue: int = 0
    minsWed: int = 0
    minsThu: int = 0


@dataclass
class TCCalendarEventData(TcBaseObj):
    """
    Data for a calendar event.
    
    :var eventDate: The date on which event occurs
    :var eventMin: The duration of the event in minutes
    """
    eventDate: datetime = None
    eventMin: int = 0


@dataclass
class TCCalendarModification(TcBaseObj):
    """
    Modification structure
    
    :var scheduleTCCalendar: TCCalendar to modify
    :var action: enumerated action
    """
    scheduleTCCalendar: TCCalendar = None
    action: ActionString = None


@dataclass
class TCCalendarResponse(TcBaseObj):
    """
    Standard response for most tccalendar calls
    
    :var tccalendars: The calendar containers
    :var serviceData: The service data
    """
    tccalendars: List[TCCalendarContainer] = ()
    serviceData: ServiceData = None


@dataclass
class TCCalendarUpdate(TcBaseObj):
    """
    A calendar update
    
    :var tccalendar: The calendar being updated
    :var updatedAttributes: The updated attributes
    :var eventsToDelete: Events to delete
    :var eventsToUpdate: Events to update
    :var eventAttributes: Corresponding updates for the EventsToUpdate
    :var newEvents: Events to create
    """
    tccalendar: TCCalendar = None
    updatedAttributes: TCCalendarData = None
    eventsToDelete: List[TCCalendarEvent] = ()
    eventsToUpdate: List[TCCalendarEvent] = ()
    eventAttributes: List[TCCalendarEventData] = ()
    newEvents: List[TCCalendarEventData] = ()


class ActionString(Enum):
    """
    ActionString
    """
    MergeSchedule = 'MergeSchedule'
    ResetSchedule = 'ResetSchedule'
