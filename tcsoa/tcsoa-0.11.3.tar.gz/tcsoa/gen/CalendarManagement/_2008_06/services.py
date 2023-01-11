from __future__ import annotations

from tcsoa.gen.CalendarManagement._2008_06.CalendarManagement import CalendarUpdate, CalendarContainer
from tcsoa.gen.CalendarManagement._2007_06.CalendarManagement import CreateCalendarResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class CalendarManagementService(TcService):

    @classmethod
    def updateCalendars(cls, tccalendarUpdates: List[CalendarUpdate]) -> ServiceData:
        """
        This operation updates the list of specified calendars and their events based on the users request to the
        application interface. This includes creating, modifying and deleting events associated with list of specified
        calendars. The information needed to update calendars is specified in the 'CalendarUpdate' structure. It
        returns service data which contains the response data from the update request. Errors will be returned in the
        list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='updateCalendars',
            library='CalendarManagement',
            service_date='2008_06',
            service_name='CalendarManagement',
            params={'tccalendarUpdates': tccalendarUpdates},
            response_cls=ServiceData,
        )

    @classmethod
    def createCalendars(cls, newTCCalendars: List[CalendarContainer]) -> CreateCalendarResponse:
        """
        This operation creates a list of calendars based on the users request to the application interface.
         User, Resource, Schedule, Base Calendars can be created .
        The information needed to create Calendar are specified in the 'CalendarContainer' structure. It returns
        'CreateCalendarResponses'   which contains the response data from the create request .Errors will be returned
        in the list of partial errors in the 'ServiceData'.
        
        """
        return cls.execute_soa_method(
            method_name='createCalendars',
            library='CalendarManagement',
            service_date='2008_06',
            service_name='CalendarManagement',
            params={'newTCCalendars': newTCCalendars},
            response_cls=CreateCalendarResponse,
        )
