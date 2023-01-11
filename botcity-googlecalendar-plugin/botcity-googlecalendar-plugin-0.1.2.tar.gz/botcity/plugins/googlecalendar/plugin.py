from datetime import datetime
from enum import Enum
from typing import List

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
# from gcsa.recurrence import *
from gcsa.recurrence import (DAILY, FR, HOURLY, MO, MONTHLY, SA, SU, TH, TU,
                             WE, WEEKLY, Recurrence)


class EventRecurrence(Enum):
    HOURLY = HOURLY
    DAILY = DAILY
    WEEKLY = WEEKLY
    MONTHLY = MONTHLY


class EventDays(Enum):
    MONDAY = MO
    TUESDAY = TU
    WEDNESDAY = WE
    THURSDAY = TH
    FRIDAY = FR
    SATURDAY = SA
    SUNDAY = SU


class BotGoogleCalendarPlugin:
    def __init__(self, credentials_file_path: str, calendar: str = "primary") -> None:
        """
        BotGoogleCalendarPlugin

        Args:
            credentials_file_path (str): The path of the credentials json file obtained at Google Cloud Platform.
            calendar (str): The id of the calendar that will be used. Defaults to "primary".
        """
        self._calendar_service = GoogleCalendar(credentials_path=credentials_file_path, calendar=calendar)

    def get_events(self, date_min: datetime = None, date_max: datetime = None) -> List[Event]:
        """
        Get all calendar events that haven't happened yet.

        Args:
            date_min (datetime, optional): Events date is within or later than the specified date.
                Set this value if you want to return events that have already happened.
            date_max (datetime, optional): Events date is earlier or equal than the specified date.

        Returns:
            List[Event]: The list containing all the calendar events.
        """
        return list(self._calendar_service.get_events(time_min=date_min, time_max=date_max))

    def create_event(self, title: str, description: str, start_date: datetime,
                     end_date: datetime = None, attendees: List[str] = None) -> None:
        """
        Creates a new event on the calendar.

        Args:
            title (str): The title of the event.
            description (str): The description of the event. The text can be in HTML format.
            start_date (datetime): The starting date of the event.
            end_date(datetime, optional): The ending date of the event. Defaults to 1 hour after the starting date.
            attendees (str, optional): The list of emails that are included in the event.
        """
        event = Event(
            summary=title,
            description=description,
            start=start_date,
            end=end_date,
            attendees=attendees
        )
        self._calendar_service.add_event(event)

    def create_recurring_event(
        self,
        title: str,
        description: str,
        start_date: datetime,
        end_date: datetime = None,
        attendees: List[str] = None,
        recurrence: EventRecurrence = EventRecurrence.DAILY,
        recurrence_freq: int = None,
        recurrence_count: int = None,
        recurrence_days: List[EventDays] = [],
        recurrence_until_date: datetime = None
                               ) -> None:
        """
        Creates a new recurring event on the calendar.

        Args:
            title (str): The title of the event.
            description (str): The description of the event. The text can be in HTML format.
            start_date (datetime): The starting date of the event.
            end_date(datetime, optional): The ending date of the event. Defaults to 1 hour after the starting date.
            attendees (str, optional): The list of emails that are included in the event.
            recurrence (EventRecurrence): The recurrence period of the event. Usage: EventRecurrence.<PERIOD>
            recurrence_freq (int, optional): Positive integer representing how often the recurrence rule repeats.
            recurrence_count (int, optional): Maximum number of events created.
            recurrence_days (List[EventDays]): Specific days for event creation. Usage: EventDays.<DAY>
            recurrence_until_date (datetime, optional): The end date of the event recurrence.
        """
        recurrence_rule = Recurrence.rule(
            freq=recurrence.value,
            interval=recurrence_freq,
            count=recurrence_count,
            by_week_day=[day.value for day in recurrence_days],
            until=recurrence_until_date
        )

        event = Event(
            summary=title,
            description=description,
            start=start_date,
            end=end_date,
            attendees=attendees,
            recurrence=recurrence_rule
        )
        self._calendar_service.add_event(event)

    def move_event(self, event: Event, destination_calendar: str) -> None:
        """
        Move a event from the calendar to another calendar.

        Args:
            Event (Event): The event to be moved.
            Destination_calendar (str): The id of the destination calendar.
            To see the id of a calendar, go to the "Integrate Calendar" tab in the calendar settings.
        """
        self._calendar_service.move_event(event, destination_calendar)

    def delete_event(self, event: Event) -> None:
        """
        Delete a event from the calendar.

        Args:
            event (Event): The event to be deleted.
        """
        self._calendar_service.delete_event(event)
