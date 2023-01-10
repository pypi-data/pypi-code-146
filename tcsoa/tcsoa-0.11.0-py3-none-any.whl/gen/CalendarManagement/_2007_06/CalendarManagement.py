from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TCCalendarEvent, TCCalendar, Schedule
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ModifyCalendarEvent(TcBaseObj):
    """
    The information necessary to modify a calendar event.
    
    :var event: The event to modify
    :var eventAttributes: The new event data
    """
    event: TCCalendarEvent = None
    eventAttributes: CalendarEventData = None


@dataclass
class RangeData(TcBaseObj):
    """
    A single time range.  The startRange and endRange represent minutes since midnight.
    There is a special range (startRange=480 and endRange=480) which represents a non-working range.
    
    :var startRange: The starting offset.
    :var endRange: The ending offset.
    """
    startRange: int = 0
    endRange: int = 0


@dataclass
class CalendarContainer(TcBaseObj):
    """
    A container to hold the Calendar Events related to CalendarData
    
    :var tccalendarAttributes: The Calendar information
    :var newEvents: The event information
    """
    tccalendarAttributes: CalendarData = None
    newEvents: List[CalendarEventData] = ()


@dataclass
class CalendarData(TcBaseObj):
    """
    The information necessary to create a single TCCalendar including daily default ranges.
    
    :var name: The name of the calendar
    :var description: The description of the calendar
    :var thuRanges: The ranges for Thursday
    :var friRanges: The ranges for Friday
    :var satRanges: The ranges for Saturday
    :var schedule: The schedule this calendar relates to (or null)
    :var source: The resource this calendar relates to (or null)
    :var baseCalendar: The parent BASE calendar (or null)
    :var type: The type of calendar
    :var sunRanges: The ranges for Sunday
    :var monRanges: The ranges for Monday
    :var tueRanges: The ranges for Tuesday
    :var wedRanges: The ranges for Wednesday
    """
    name: str = ''
    description: str = ''
    thuRanges: List[RangeData] = ()
    friRanges: List[RangeData] = ()
    satRanges: List[RangeData] = ()
    schedule: Schedule = None
    source: BusinessObject = None
    baseCalendar: TCCalendar = None
    type: int = 0
    sunRanges: List[RangeData] = ()
    monRanges: List[RangeData] = ()
    tueRanges: List[RangeData] = ()
    wedRanges: List[RangeData] = ()


@dataclass
class CalendarEventData(TcBaseObj):
    """
    The information for a single CalendarEvent.
    
    :var firstRecurStart: The date of the event
    :var firstRecurEnd: Placeholder for recurring end date. (not currently used)
    :var eventExpiryDate: Placeholder for recurring event expiration. (not currently used)
    :var eventRanges: The time ranges for the event
    :var eventType: Placeholder for event type. (not currently used)
    :var numRecurrences: Placeholder number of recurrences. (not currently used)
    :var recurInterval: Placeholder for the recurring interval. (not currently used)
    :var recurDaysOfWeek: Placeholder for mask of days. (not currently used)
    :var recurWeeksOfMonth: Placeholder for mask of weeks. (not currently used)
    :var recurMonth: Placeholder for mask of months. (not currently used)
    """
    firstRecurStart: datetime = None
    firstRecurEnd: datetime = None
    eventExpiryDate: datetime = None
    eventRanges: List[RangeData] = ()
    eventType: int = 0
    numRecurrences: int = 0
    recurInterval: int = 0
    recurDaysOfWeek: int = 0
    recurWeeksOfMonth: int = 0
    recurMonth: int = 0


@dataclass
class CalendarResponse(TcBaseObj):
    """
    The response containing a created calendars and the events.
    
    :var calendar: The calendar
    :var calendarEvent: The events related to that calendar.
    """
    calendar: TCCalendar = None
    calendarEvent: List[TCCalendarEvent] = ()


@dataclass
class CalendarUpdate(TcBaseObj):
    """
    The information necessary to modify a calendar.
    
    :var calendar: The calendar to modify
    :var calendarAttributes: The basic calendar data to modify
    :var eventsToAdd: New calendar events to add
    :var eventsToDelete: Existing calendar events to delete
    :var eventsToUpdate: Calendar events to update.
    """
    calendar: TCCalendar = None
    calendarAttributes: CalendarData = None
    eventsToAdd: List[CalendarEventData] = ()
    eventsToDelete: List[TCCalendarEvent] = ()
    eventsToUpdate: List[ModifyCalendarEvent] = ()


@dataclass
class CreateCalendarResponse(TcBaseObj):
    """
    The container with ALL the CalendarResponse and the service data.
    
    :var serviceData: The service data
    :var calendarResponse: The calendars and events
    """
    serviceData: ServiceData = None
    calendarResponse: List[CalendarResponse] = ()
