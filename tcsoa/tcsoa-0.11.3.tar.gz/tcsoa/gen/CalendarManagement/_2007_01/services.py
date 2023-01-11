from __future__ import annotations

from tcsoa.gen.CalendarManagement._2007_01.CalendarManagement import TCCalendarModification, TCCalendarResponse, TCCalendarUpdate, NewTCCalendar, GetTCCalendarData
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.BusinessObjects import TCCalendar
from tcsoa.base import TcService


class CalendarManagementService(TcService):

    @classmethod
    def getTCCalendars(cls, getTCCalendars: List[GetTCCalendarData]) -> TCCalendarResponse:
        """
        This operation gets the list of  calendars based on the user's request to the application interface. Multiple
        calendars can be obtained through this operation.
        The information needed to get TCCalendar  objects is specified in the 'GetTCCalendarData'  structure. It
        returns 'TCCalendarResponse' which contains response data from the 'getcalendar' request. Errors will be
        returned in the list of partial errors in the 'ServiceData'. 
        """
        return cls.execute_soa_method(
            method_name='getTCCalendars',
            library='CalendarManagement',
            service_date='2007_01',
            service_name='CalendarManagement',
            params={'getTCCalendars': getTCCalendars},
            response_cls=TCCalendarResponse,
        )

    @classmethod
    def modifyTCCalendars(cls, modifications: List[TCCalendarModification]) -> TCCalendarResponse:
        """
        Modifies the specified schedule calendars based on the action string.
        Reset: Reset the schedule calendar to the base calendar
        Merge: Merge the schedule calendar with the base calendar
        """
        return cls.execute_soa_method(
            method_name='modifyTCCalendars',
            library='CalendarManagement',
            service_date='2007_01',
            service_name='CalendarManagement',
            params={'modifications': modifications},
            response_cls=TCCalendarResponse,
        )

    @classmethod
    def updateTCCalendars(cls, tccalendarUpdates: List[TCCalendarUpdate]) -> TCCalendarResponse:
        """
        Updates the specified calendars and their events.
        This includes creating, modifying and deleting events associated with specified calendars
        """
        return cls.execute_soa_method(
            method_name='updateTCCalendars',
            library='CalendarManagement',
            service_date='2007_01',
            service_name='CalendarManagement',
            params={'tccalendarUpdates': tccalendarUpdates},
            response_cls=TCCalendarResponse,
        )

    @classmethod
    def createTCCalendars(cls, newTCCalendars: List[NewTCCalendar]) -> TCCalendarResponse:
        """
        Creates new calendars based on the input parameters
        """
        return cls.execute_soa_method(
            method_name='createTCCalendars',
            library='CalendarManagement',
            service_date='2007_01',
            service_name='CalendarManagement',
            params={'newTCCalendars': newTCCalendars},
            response_cls=TCCalendarResponse,
        )

    @classmethod
    def deleteTCCalendars(cls, tccalendarsToDelete: List[TCCalendar]) -> ServiceData:
        """
        This operation deletes the specified calendars and their calendar events based on the user's request to the
        application interface. Multiple calendars and its their events can be deleted   through this operation.
        Existing schedule, resource , and base calendars can be deleted through this operation.. 
        The information needed to delete a TCCalendar  object is specified in the TCCalendar structure. It returns 
        'ServiceData'  , which is  a common data structure used to return sets of Teamcenter data model objects from a
        service request. This structure holds lists of data model objects that were 'created', 'deleted', 'updated' or
        'plain' in the database with this service request. 'Plain' objects are simply objects that the service is
        returning where no changes have been made to the database object, i.e. e.g., 'GetHomeFolder' returns a list of
        objects that are contained in the user's home folder. Errors will be returned in the list of partial errors in
        the 'ServiceData'.   
        
        """
        return cls.execute_soa_method(
            method_name='deleteTCCalendars',
            library='CalendarManagement',
            service_date='2007_01',
            service_name='CalendarManagement',
            params={'tccalendarsToDelete': tccalendarsToDelete},
            response_cls=ServiceData,
        )
