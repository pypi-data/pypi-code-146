## $Id: export.py 12859 2015-04-16 18:49:08Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
"""Exporters for hostels and beds.
"""
import grok
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.utils.helpers import iface_names
from waeup.kofa.hostels.interfaces import IBed, IHostel

class HostelExporter(grok.GlobalUtility, ExporterBase):
    """The Hostel Exporter exports container data. It does not
    export beds inside the container.
    """
    grok.implements(ICSVExporter)
    grok.name('hostels')

    fields = tuple(sorted(iface_names(IHostel))) 
    title = _(u'Hostels')

    def export_all(self, site, filepath=None):
        """Export hostels into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        hostels = site.get('hostels', {})
        for hostel in hostels.values():
            self.write_item(hostel, writer)
        return self.close_outfile(filepath, outfile)


class BedExporter(grok.GlobalUtility, ExporterBase):
    """The Bed Exporter exports all beds stored in the
    hostel containers. The exporter iterates over all hostels
    and over all beds inside each hostel container.
    """
    grok.implements(ICSVExporter)
    grok.name('beds')

    fields = tuple(sorted(iface_names(IBed))) + (
        'hall', 'block', 'room', 'bed', 'special_handling', 'sex', 'bt')
    title = _(u'Beds')

    def export_all(self, site, filepath=None):
        """Export beds into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        hostels = site.get('hostels', {})
        for hostel in hostels.values():
            for bed in hostel.values():
                self.write_item(bed, writer)
        return self.close_outfile(filepath, outfile)

