## $Id: batching.py 13434 2015-11-11 07:54:44Z henrik $
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
"""Batch processing components for hostels.

"""
import grok
from zope.interface import Interface
from zope.component import getUtility
from zope.catalog.interfaces import ICatalog
from waeup.kofa.interfaces import IBatchProcessor, IGNORE_MARKER
from waeup.kofa.utils.batching import BatchProcessor
from waeup.kofa.hostels.interfaces import IHostel, IBed
from waeup.kofa.hostels.vocabularies import NOT_OCCUPIED
from waeup.kofa.interfaces import MessageFactory as _

class HostelProcessor(BatchProcessor):
    """The Hostel Procesor imports hostels, i.e. the container objects of
    beds. It does not import beds. There is nothing special about this
    processor.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'hostelprocessor'
    grok.name(util_name)

    name = _('Hostel Processor')
    iface = IHostel

    location_fields = ['hostel_id',]
    factory_name = 'waeup.Hostel'

    mode = None

    def parentsExist(self, row, site):
        return 'hostels' in site.keys()

    def entryExists(self, row, site):
        return row['hostel_id'] in site['hostels'].keys()

    def getParent(self, row, site):
        return site['hostels']

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        parent = self.getParent(row, site)
        return parent.get(row['hostel_id'])

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent.addHostel(obj)
        return

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = super(HostelProcessor, self).updateEntry(
            obj, row, site, filename)
        # Log actions...
        location_field = self.location_fields[0]
        grok.getSite()['hostels'].logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, row[location_field], items_changed))
        return


class BedProcessor(BatchProcessor):
    """The Bed Procesor update beds. It allocates students
    to empty beds and switches the reservation status of beds. ``1``
    means reserved and ``0`` unreserved. Beds cannot be released
    by import.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'bedupdater'
    grok.name(util_name)

    name = _('Bed Processor (update only)')
    iface = IBed

    location_fields = ['hostel_id', 'bed_id']
    factory_name = None

    mode = None

    @property
    def available_fields(self):
        return self.location_fields + ['reserved', 'owner']

    def parentsExist(self, row, site):
        if not 'hostels' in site.keys():
            return False
        return row['hostel_id'] in site['hostels']

    def entryExists(self, row, site):
        if not self.parentsExist(row, site):
            return False
        parent = self.getParent(row, site)
        return row['bed_id'] in parent.keys()

    def getParent(self, row, site):
        return site['hostels'][row['hostel_id']]

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        parent = self.getParent(row, site)
        return parent.get(row['bed_id'])

    def checkUpdateRequirements(self, obj, row, site):
        """Checks requirements the bed must fulfill
        before being updated.
        """
        # Check if bed is occupied
        if row.get('owner') and obj.owner != NOT_OCCUPIED:
            return 'Bed is occupied.'

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        inv_errs = ''
        conv_dict = {}
        errs = []
        reserved = row.get('reserved')
        if reserved not in (None, IGNORE_MARKER, '', '0', '1'):
            errs.append(('reserved','invalid value'))
        owner = row.get('owner')
        if owner not in (None, '', IGNORE_MARKER):
            if owner == NOT_OCCUPIED:
                errs.append(('owner','bed cannot be released by import'))
                return errs, inv_errs, conv_dict
            beds_cat = getUtility(ICatalog, name='beds_catalog')
            results = list(beds_cat.searchResults(owner=(owner, owner)))
            if len(results) > 0:
                errs.append((
                    'owner','student already resides in %s'
                    % results[0].bed_id))
                return errs, inv_errs, conv_dict
            students_cat = getUtility(ICatalog, name='students_catalog')
            results = list(students_cat.searchResults(student_id=(owner, owner)))
            if len(results) != 1:
                errs.append(('owner','student does not exist'))
        return errs, inv_errs, conv_dict

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        changed = []
        owner = row.get('owner')
        if owner not in (None, '', IGNORE_MARKER):
            obj.bookBed(owner)
            changed.append('owner=%s' % owner)
        reserved = row.get('reserved')
        sh, sex, bt = obj.bed_type.split('_')
        if (reserved == '1' and bt != 'reserved') or \
            (reserved == '0'and bt == 'reserved'):
            message = obj.switchReservation()
            changed.append(message)
        # Log actions...
        if changed:
            items_changed = ', '.join(changed)
        else:
            items_changed = 'nothing'
        location_field = self.location_fields[1]
        grok.getSite()['hostels'].logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, row[location_field], items_changed))
        return