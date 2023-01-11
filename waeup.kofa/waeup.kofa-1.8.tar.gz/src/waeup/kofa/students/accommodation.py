## $Id: accommodation.py 15705 2019-10-28 09:18:21Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""
Student accommodation components.
"""
from datetime import datetime
import grok
from zope.component import getUtility, queryUtility
from zope.component.interfaces import IFactory
from zope.event import notify
from zope.i18n import translate
from zope.catalog.interfaces import ICatalog
from zope.interface import implementedBy
from waeup.kofa.interfaces import academic_sessions_vocab, IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.students.interfaces import (
    IStudentAccommodation, IStudentNavigation, IBedTicket, IStudentsUtils)
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.hostels.hostel import NOT_OCCUPIED


class StudentAccommodation(grok.Container):
    """This is a container for bed tickets.
    """
    grok.implements(IStudentAccommodation, IStudentNavigation)
    grok.provides(IStudentAccommodation)

    def __init__(self):
        super(StudentAccommodation, self).__init__()
        return

    def addBedTicket(self, bedticket):
        """Add a bed ticket object.
        """
        if not IBedTicket.providedBy(bedticket):
            raise TypeError(
                'StudentAccommodation containers contain only IBedTicket instances')
        try:
            self[str(bedticket.booking_session)] = bedticket
        except KeyError:
            if 'booking expired' in self[
                    str(bedticket.booking_session)].bed_coordinates:
                del self[str(bedticket.booking_session)]
        self[str(bedticket.booking_session)] = bedticket
        return

    @property
    def student(self):
        return self.__parent__

    def writeLogMessage(self, view, message):
        return self.__parent__.writeLogMessage(view, message)

StudentAccommodation = attrs_to_fields(StudentAccommodation)

class BedTicket(grok.Model):
    """This is a bed ticket which shows that the student has booked a bed.
    """
    grok.implements(IBedTicket, IStudentNavigation)
    grok.provides(IBedTicket)

    def __init__(self):
        super(BedTicket, self).__init__()
        self.booking_date = datetime.utcnow()
        self.bed = None
        return

    @property
    def student(self):
        try:
            return self.__parent__.__parent__
        except AttributeError:
            return None

    @property
    def display_coordinates(self):
        students_utils = getUtility(IStudentsUtils)
        return students_utils.getBedCoordinates(self)

    @property
    def maint_payment_made(self):
        try:
            if len(self.student['payments']):
                for ticket in self.student['payments'].values():
                    if ticket.p_category == 'hostel_maintenance' and \
                        ticket.p_session == self.booking_session and \
                        ticket.p_state == 'paid':
                            return True
        except TypeError: # in unit tests
            pass
        return False

    def relocateStudent(self):
        """Relocate student if student parameters have changed or the bed_type
        of the bed has changed.
        """
        if self.booking_session != grok.getSite()[
            'hostels'].accommodation_session:
            return False, _("Previous session bookings can't be changed.")
        student = self.student
        students_utils = getUtility(IStudentsUtils)
        acc_details  = students_utils.getAccommodationDetails(student)
        if self.bed != None and \
              'reserved' in self.bed.bed_type:
            return False, _("Students in reserved beds can't be relocated.")
        if acc_details['bt'] == self.bed_type and \
                self.bed != None and \
                self.bed.bed_type == self.bed_type and \
                self.bed.__parent__.__parent__:
            return False, _("Student can't be relocated.")
        # Search a bed
        cat = queryUtility(ICatalog, name='beds_catalog', default=None)
        entries = cat.searchResults(
            owner=(student.student_id,student.student_id))
        if len(entries) and self.bed == None:
            # If booking has been cancelled but other bed space has been
            # manually allocated after cancellation use this bed
            new_bed = [entry for entry in entries][0]
        else:
            # Search for other available beds
            entries = cat.searchResults(
                bed_type=(acc_details['bt'],acc_details['bt']))
            available_beds = [
                entry for entry in entries if entry.owner == NOT_OCCUPIED]
            desired_hostel = self.__parent__.desired_hostel
            if desired_hostel and desired_hostel != 'no':
                # Filter desired hostel beds
                filtered_beds = [bed for bed in available_beds
                                 if bed.bed_id.startswith(desired_hostel)]
                available_beds = filtered_beds
            if available_beds:
                new_bed = students_utils.selectBed(available_beds)
                new_bed.bookBed(student.student_id)
            else:
                return False, _('There is no free bed in your category ${a}.',
                                 mapping = {'a':acc_details['bt']})
        # Release old bed if exists
        if self.bed != None:
            self.bed.owner = NOT_OCCUPIED
            notify(grok.ObjectModifiedEvent(self.bed))
        # Designate new bed in ticket
        self.bed_type = acc_details['bt']
        self.bed = new_bed
        hall_title = new_bed.__parent__.hostel_name
        coordinates = new_bed.coordinates[1:]
        block, room_nr, bed_nr = coordinates
        bc = _('${a}, Block ${b}, Room ${c}, Bed ${d} (${e})', mapping = {
            'a':hall_title, 'b':block,
            'c':room_nr, 'd':bed_nr,
            'e':new_bed.bed_type})
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.bed_coordinates = translate(
            bc, 'waeup.kofa',target_language=portal_language)
        self.writeLogMessage(self, 'relocated: %s' % new_bed.bed_id)
        return True, _('Student relocated: ${a}',
                 mapping = {'a':self.display_coordinates})

    def writeLogMessage(self, view, message):
        return self.__parent__.__parent__.writeLogMessage(view, message)

    def getSessionString(self):
        return academic_sessions_vocab.getTerm(
            self.booking_session).title

BedTicket = attrs_to_fields(BedTicket, omit=['display_coordinates'])


# Bed tickets must be importable. So we might need a factory.
class BedTicketFactory(grok.GlobalUtility):
    """A factory for bed tickets.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.BedTicket')
    title = u"Create a new bed ticket.",
    description = u"This factory instantiates new bed ticket instances."

    def __call__(self, *args, **kw):
        return BedTicket()

    def getInterfaces(self):
        return implementedBy(BedTicket)
