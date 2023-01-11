## $Id: hostel.py 15944 2020-01-23 12:27:12Z henrik $
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
These are the hostels.
"""
import grok
from zope.event import notify
from zope.component import getUtility, createObject
from zope.component.interfaces import IFactory, ComponentLookupError
from zope.catalog.interfaces import ICatalog
from zope.catalog.field import FieldIndex
from datetime import datetime
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.hostels.vocabularies import NOT_OCCUPIED
from waeup.kofa.hostels.interfaces import IHostel, IBed
from waeup.kofa.students.interfaces import IBedTicket
from waeup.kofa.interfaces import IKofaUtils, IKofaPluggable
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.helpers import now, reindex_cat

class Hostel(grok.Container):
    """This is a hostel.
    """
    grok.implements(IHostel)
    grok.provides(IHostel)

    @property
    def bed_statistics(self):
        total = len(self.keys())
        booked = 0
        for value in self.values():
            if value.owner != NOT_OCCUPIED:
                booked += 1
        return {'booked':booked, 'total':total}

    def clearHostel(self):
        """Remove all beds
        """
        keys = [i for i in self.keys()] # create deep copy
        for bed in keys:
            del self[bed]
        return

    def addBed(self, bed):
        """Add a bed.
        """
        if not IBed.providedBy(bed):
            raise TypeError(
                'Hostels contain only IBed instances')
        self[bed.bed_id] = bed
        return

    def updateBeds(self):
        """Fill hostel with beds or update beds.
        """
        added_counter = 0
        modified_counter = 0
        removed_counter = 0
        modified_beds = u''

        # Remove all empty beds. Occupied beds remain in hostel!
        keys = list(self.keys()) # create list copy
        for key in keys:
            if self[key].owner == NOT_OCCUPIED:
                del self[key]
                self._p_changed = True
                removed_counter += 1
            else:
                self[key].bed_number = 9999
        remaining = len(keys) - removed_counter

        blocks_for_female = getattr(self,'blocks_for_female',[])
        blocks_for_male = getattr(self,'blocks_for_male',[])
        beds_for_fresh = getattr(self,'beds_for_fresh',[])
        beds_for_pre = getattr(self,'beds_for_pre',[])
        beds_for_returning = getattr(self,'beds_for_returning',[])
        beds_for_final = getattr(self,'beds_for_final',[])
        beds_for_all = getattr(self,'beds_for_all',[])
        all_blocks = blocks_for_female + blocks_for_male
        all_beds = (beds_for_pre + beds_for_fresh +
            beds_for_returning + beds_for_final + beds_for_all)
        floor_base = 100
        if self.rooms_per_floor > 99:
            floor_base = 1000
        for block in all_blocks:
            sex = 'male'
            if block in blocks_for_female:
                sex = 'female'
            for floor in range(1,int(self.floors_per_block)+1):
                for room in range(1,int(self.rooms_per_floor)+1):
                    for bed in all_beds:
                        room_nr = floor*floor_base + room
                        bt = 'all'
                        if bed in beds_for_fresh:
                            bt = 'fr'
                        elif bed in beds_for_pre:
                            bt = 'pr'
                        elif bed in beds_for_final:
                            bt = 'fi'
                        elif bed in beds_for_returning:
                            bt = 're'
                        bt = u'%s_%s_%s' % (self.special_handling,sex,bt)
                        uid = u'%s_%s_%d_%s' % (
                            self.hostel_id,block,room_nr,bed)
                        if uid in self:
                            bed = self[uid]
                            # Renumber remaining bed
                            bed.bed_number = len(self) + 1 - remaining
                            remaining -= 1
                            if bed.bed_type != bt:
                                bed.bed_type = bt
                                modified_counter += 1
                                modified_beds += '%s, ' % uid
                                notify(grok.ObjectModifiedEvent(bed))
                        else:
                            bed = createObject(u'waeup.Bed')
                            bed.bed_id = uid
                            bed.bed_type = bt
                            bed.bed_number = len(self) + 1 - remaining
                            bed.owner = NOT_OCCUPIED
                            self.addBed(bed)
                            added_counter +=1
        return removed_counter, added_counter, modified_counter, modified_beds

    def writeLogMessage(self, view, message):
        ob_class = view.__implemented__.__name__.replace('waeup.kofa.','')
        self.__parent__.logger.info(
            '%s - %s - %s' % (ob_class, self.__name__, message))
        return

Hostel = attrs_to_fields(Hostel)

class Bed(grok.Container):
    """This is a bed.
    """
    grok.implements(IBed)
    grok.provides(IBed)

    @property
    def coordinates(self):
        """Determine the coordinates from the bed_id.
        """
        return self.bed_id.split('_')

    # The following property attributes are only needed
    # for the exporter to ease evaluation with Excel.

    @property
    def hall(self):
        return self.coordinates[0]

    @property
    def block(self):
        return self.coordinates[1]

    @property
    def room(self):
        return self.coordinates[2]

    @property
    def bed(self):
        return self.coordinates[3]

    @property
    def special_handling(self):
        return self.bed_type.split('_')[0]

    @property
    def sex(self):
        return self.bed_type.split('_')[1]

    @property
    def bt(self):
        return self.bed_type.split('_')[2]


    def bookBed(self, student_id):
        if self.owner == NOT_OCCUPIED:
            self.owner = student_id
            notify(grok.ObjectModifiedEvent(self))
            return None
        else:
            return self.owner

    def switchReservation(self):
        """Reserves or unreserve bed respectively.
        """
        sh, sex, bt = self.bed_type.split('_')
        hostel_id, block, room_nr, bed = self.coordinates
        hostel = self.__parent__
        beds_for_fresh = getattr(hostel,'beds_for_fresh',[])
        beds_for_pre = getattr(hostel,'beds_for_pre',[])
        beds_for_returning = getattr(hostel,'beds_for_returning',[])
        beds_for_final = getattr(hostel,'beds_for_final',[])
        bed_string = u'%s_%s_%s' % (block, room_nr, bed)
        if bt == 'reserved':
            bt = 'all'
            if bed in beds_for_fresh:
                bt = 'fr'
            elif bed in beds_for_pre:
                bt = 'pr'
            elif bed in beds_for_final:
                bt = 'fi'
            elif bed in beds_for_returning:
                bt = 're'
            bt = u'%s_%s_%s' % (sh, sex, bt)
            message = _(u'unreserved')
        else:
            bt = u'%s_%s_reserved' % (sh, sex)
            message = _(u'reserved')
        self.bed_type = bt
        notify(grok.ObjectModifiedEvent(self))
        return message

    def releaseBed(self):
        """Release bed.
        """
        if self.owner == NOT_OCCUPIED:
            return
        old_owner = self.owner
        self.owner = NOT_OCCUPIED
        notify(grok.ObjectModifiedEvent(self))
        accommodation_session = grok.getSite()[
            'hostels'].accommodation_session
        try:
            bedticket = grok.getSite()['students'][old_owner][
                          'accommodation'][str(accommodation_session)]
        except KeyError:
            return '%s without bed ticket' % old_owner
        bedticket.bed = None
        tz = getUtility(IKofaUtils).tzinfo
        timestamp = now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        bedticket.bed_coordinates = u'-- booking cancelled on %s --' % (
            timestamp,)
        return old_owner

    def releaseBedIfMaintenanceNotPaid(self, n=7):
        """Release bed if maintenance fee has not been paid on time or
        if bed ticket does not exist. Reserve bed so that it cannot be
        automatically booked by someone else.
        """
        if self.owner == NOT_OCCUPIED:
            return
        accommodation_session = grok.getSite()[
            'hostels'].accommodation_session
        try:
            bedticket = grok.getSite()['students'][self.owner][
                          'accommodation'][str(accommodation_session)]
        except KeyError:
            old_owner = self.owner
            self.owner = NOT_OCCUPIED
            sh, sex, bt = self.bed_type.split('_')
            bt = u'%s_%s_reserved' % (sh, sex)
            self.bed_type = bt
            notify(grok.ObjectModifiedEvent(self))
            ##: Add logging message
            return "%s wob" % old_owner # owner without bed ticket
        if bedticket.maint_payment_made:
            return
        jetzt = datetime.utcnow()
        days_ago = getattr(jetzt - bedticket.booking_date, 'days')
        if days_ago >= n:
            old_owner = self.owner
            self.owner = NOT_OCCUPIED
            sh, sex, bt = self.bed_type.split('_')
            bt = u'%s_%s_reserved' % (sh, sex)
            self.bed_type = bt
            notify(grok.ObjectModifiedEvent(self))
            bedticket.bed = None
            tz = getUtility(IKofaUtils).tzinfo
            timestamp = now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            bedticket.bed_coordinates = u'-- booking expired (%s) --' % (
                timestamp,)
            return old_owner
        return

    def writeLogMessage(self, view, message):
        ob_class = view.__implemented__.__name__.replace('waeup.kofa.','')
        self.__parent__.__parent__.logger.info(
            '%s - %s - %s' % (ob_class, self.__name__, message))
        return

Bed = attrs_to_fields(Bed)

class HostelFactory(grok.GlobalUtility):
    """A factory for hostels.

    We need this factory for the hostel processor.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.Hostel')
    title = u"Create a new hostel.",
    description = u"This factory instantiates new hostel instances."

    def __call__(self, *args, **kw):
        return Hostel()

    def getInterfaces(self):
        return implementedBy(Hostel)

class BedFactory(grok.GlobalUtility):
    """A factory for  beds.

    We need this factory to ease customization.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.Bed')
    title = u"Create a new bed.",
    description = u"This factory instantiates new bed instances."

    def __call__(self, *args, **kw):
        return Bed()

    def getInterfaces(self):
        return implementedBy(Bed)

class HostelsPlugin(grok.GlobalUtility):
    """A plugin to update beds_catalog
    """
    grok.implements(IKofaPluggable)
    grok.name('hostels')
    log_prefix = 'HostelsPlugin'

    def setup(self, site, name, logger):
        return

    def update(self, site, name, logger):
        site_name = getattr(site, '__name__', '<Unnamed Site>')
        nothing_to_do = True
        # Add bed_id index
        try:
            cat = getUtility(ICatalog, name='beds_catalog')
            if 'bed_id' not in cat.keys():
                nothing_to_do = False
                # replace original `updateIndex` method
                def updateIndexReplacement(index):
                    reindex_cat(cat)
                cat._updateIndex = cat.updateIndex
                cat.updateIndex = updateIndexReplacement
                # setup catalog
                cat[u'bed_id'] = FieldIndex(field_name=u'bed_id')
                cat.updateIndex = cat._updateIndex  # undo changes
                logger.info(
                    '%s: bed_id index added to beds_catalog.'
                    % self.log_prefix)
                reindex_cat(cat)
                logger.info(
                    '%s: beds_catalog updated.'
                    % self.log_prefix)
        except ComponentLookupError: # in unit tests
            pass
        if nothing_to_do:
            logger.info(
                '%s: Updating site at %s: Nothing to do.' % (
                    self.log_prefix, site_name,)
                )
        return


@grok.subscribe(IBedTicket, grok.IObjectRemovedEvent)
def handle_bedticket_removed(bedticket, event):
    """If a bed ticket is deleted, we make sure that also the owner attribute
    of the bed is cleared (set to NOT_OCCUPIED).
    """
    if bedticket.bed != None:
        bedticket.bed.owner = NOT_OCCUPIED
        notify(grok.ObjectModifiedEvent(bedticket.bed))

@grok.subscribe(IBed, grok.IObjectRemovedEvent)
def handle_bed_removed(bed, event):
    """If a bed is deleted, we make sure that the bed object is
    removed also from the owner's bed ticket.
    """
    if bed.owner == NOT_OCCUPIED:
        return
    accommodation_session = grok.getSite()['hostels'].accommodation_session
    try:
        bedticket = grok.getSite()['students'][bed.owner][
                      'accommodation'][str(accommodation_session)]
    except KeyError:
        return
    bedticket.bed = None
