from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TCCalendarEvent, TCCalendar, Schedule
from tcsoa.gen.CalendarManagement._2007_06.CalendarManagement import ModifyCalendarEvent, RangeData, CalendarEventData
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


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
    :var timeZone: The timezone id (as specified in the Olson database eg, 'America/New_York' for US Eastern time)
    :var schedule: The schedule this calendar relates to (or null)
    :var source: The resource this calendar relates to (or null)
    :var baseCalendar: The parent BASE calendar (or null)
    :var type: The type of calendar (1-System Calendar, 2-Schedule Calendar, 3-User Calendar, 4-ScheduleMember Calendar)
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
    timeZone: str = ''
    schedule: Schedule = None
    source: BusinessObject = None
    baseCalendar: TCCalendar = None
    type: int = 0
    sunRanges: List[RangeData] = ()
    monRanges: List[RangeData] = ()
    tueRanges: List[RangeData] = ()
    wedRanges: List[RangeData] = ()


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
