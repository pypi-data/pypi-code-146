from tcsoa.gen.CalendarManagement._2007_06.services import CalendarManagementService as imp0
from tcsoa.gen.CalendarManagement._2008_06.services import CalendarManagementService as imp1
from tcsoa.gen.CalendarManagement._2007_01.services import CalendarManagementService as imp2
from tcsoa.base import TcService


class CalendarManagementService(TcService):
    createCalendars = imp0.createCalendars
    createCalendars2 = imp1.createCalendars
    createTCCalendars = imp2.createTCCalendars
    deleteTCCalendars = imp2.deleteTCCalendars
    getTCCalendars = imp2.getTCCalendars
    modifyTCCalendars = imp2.modifyTCCalendars
    updateCalendars = imp0.updateCalendars
    updateCalendars2 = imp1.updateCalendars
    updateTCCalendars = imp2.updateTCCalendars
