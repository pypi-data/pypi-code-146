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
"""Exporters for access codes and access code batches.
"""
import grok
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.utils.helpers import iface_names
from waeup.kofa.accesscodes.interfaces import IAccessCode, IAccessCodeBatch

class AccessCodeBatchExporter(grok.GlobalUtility, ExporterBase):
    """The Access Code Batch Exporter exports container data. It does not
    export access codes inside the container.
    """
    grok.implements(ICSVExporter)
    grok.name('accesscodebatches')

    fields = tuple(sorted(iface_names(IAccessCodeBatch))) + ('batch_id',)
    title = _(u'Access Code Batches')

    def mangle_value(self, value, name, context=None):
        if name == 'batch_id' and context is not None:
            value = u'%s-%s' % (getattr(context, 'prefix', None),
                getattr(context, 'num', None))
        return super(
            AccessCodeBatchExporter, self).mangle_value(
            value, name, context=context)

    def export_all(self, site, filepath=None):
        """Export accesscode batches into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        accesscodebatches = site.get('accesscodes', {})
        for batch in accesscodebatches.values():
            self.write_item(batch, writer)
        return self.close_outfile(filepath, outfile)


class AccessCodeExporter(grok.GlobalUtility, ExporterBase):
    """The Access Code Exporter exports all access codes stored in the
    access code batch containers. The exporter iterates over all access code
    batches and over all access codes inside each batch container.
    """
    grok.implements(ICSVExporter)
    grok.name('accesscodes')

    fields = tuple(sorted(iface_names(IAccessCode)))
    title = _(u'Access Codes')

    def mangle_value(self, value, name, context=None):
        """The mangler adds a hash symbol at the end of ``random_num``
        to avoid annoying automatic number transformation by Excel or Calc.
        """
        if name == 'random_num' and value is not None:
            # Append hash '#' to numbers to circumvent
            # unwanted excel automatic
            value = str('%s#' % value)
        return super(
            AccessCodeExporter, self).mangle_value(
            value, name, context=context)

    def export_all(self, site, filepath=None):
        """Export accesscodes into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        accesscodebatches = site.get('accesscodes', {})
        for batch in accesscodebatches.values():
            for ac in batch.values():
                self.write_item(ac, writer)
        return self.close_outfile(filepath, outfile)

