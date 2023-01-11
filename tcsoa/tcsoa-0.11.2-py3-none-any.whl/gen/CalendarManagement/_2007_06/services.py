from __future__ import annotations

from tcsoa.gen.CalendarManagement._2007_06.CalendarManagement import CalendarUpdate, CreateCalendarResponse, CalendarContainer
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class CalendarManagementService(TcService):

    @classmethod
    def updateCalendars(cls, tccalendarUpdates: List[CalendarUpdate]) -> ServiceData:
        """
        Updates the specified calendars and their events.
        This includes creating, modifying and deleting events associated with specified calendars
        """
        return cls.execute_soa_method(
            method_name='updateCalendars',
            library='CalendarManagement',
            service_date='2007_06',
            service_name='CalendarManagement',
            params={'tccalendarUpdates': tccalendarUpdates},
            response_cls=ServiceData,
        )

    @classmethod
    def createCalendars(cls, newTCCalendars: List[CalendarContainer]) -> CreateCalendarResponse:
        """
        Creates new calendars based on the provided input parameters
        """
        return cls.execute_soa_method(
            method_name='createCalendars',
            library='CalendarManagement',
            service_date='2007_06',
            service_name='CalendarManagement',
            params={'newTCCalendars': newTCCalendars},
            response_cls=CreateCalendarResponse,
        )
