## $Id: export.py 16431 2021-03-25 09:45:54Z henrik $
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
"""Exporters for applicant-related stuff.
"""
import grok
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from waeup.kofa.applicants.interfaces import (
    IApplicantBaseData, IApplicantsContainer, IApplicantOnlinePayment,
    IApplicantRefereeReport)
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.utils.helpers import iface_names

class ApplicantsContainerExporter(grok.GlobalUtility, ExporterBase):
    """The Applicants Container Exporter exports container data. It does not
    export applicants (application records) inside the container.
    """
    grok.implements(ICSVExporter)
    grok.name('applicantscontainers')

    fields = tuple(sorted(iface_names(IApplicantsContainer)))
    title = _(u'Applicants Containers')

    def mangle_value(self, value, name, context=None):
        return super(
            ApplicantsContainerExporter, self).mangle_value(
            value, name, context=context)

    def export(self, containers, filepath=None):
        """Export `containers`, an iterable, as CSV file.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for container in containers:
            self.write_item(container, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export applicantscontainer into filepath as CSV data.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        containers = site.get('applicants', {})
        return self.export(containers.values(), filepath)


class ApplicantExporter(grok.GlobalUtility, ExporterBase):
    """The Applicant Exporter exports application records (= applicants)
    stored in the database. In contrast to the exporters in the academic
    section this exporter does not iterate over the items of containers
    but searches the :class:`ApplicantsCatalog` instead.

    The exporter exports all applicants if started in the Data Center
    which means in the context of the `DataCenter` object. The exporter can also 
    be started 'locally' which means in the context of an `ApplicantsContainer`
    container. Then the :meth:`export_filtered()` instead of the 
    :meth:`export_all()` method is applied which searches for applicants
    in the respective container.
    """
    grok.implements(ICSVExporter)
    grok.name('applicants')

    fields = tuple(sorted(iface_names(IApplicantBaseData))) + (
        'password', 'state', 'history', 'container_code', 'application_number',
        'display_fullname', 'application_date')
    title = _(u'Applicants')

    def mangle_value(self, value, name, context=None):
        """The mangler determines the codes of the atributes `course1`,
        `course2` and `course_admitted`. It furthermore prepares the
        history messages and adds a hash symbol at the end of the phone number
        to avoid annoying automatic number transformation by Excel or Calc.
        """
        if name.startswith('course') and value is not None:
            value = value.code
        #elif name == 'school_grades':
        #    value = [eval(entry.to_string()) for entry in value]
        elif name == 'history':
            value = getattr(value, 'messages', None)
        elif name == 'phone' and value is not None:
            # Append hash '#' to phone numbers to circumvent
            # unwanted excel automatic
            value = str('%s#' % value)
        elif name == 'container_code':
            value = value.strip('+')
        return super(
            ApplicantExporter, self).mangle_value(
            value, name, context=context)

    def export(self, applicants, filepath=None):
        """Export `applicants`, an iterable, as CSV file.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for applicant in applicants:
            self.write_item(applicant, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export all applicants into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        Only used records are being exported.
        """
        catalog = queryUtility(
            ICatalog, context=site, name='applicants_catalog', default=None)
        if catalog is None:
            return self.export([], filepath)
        applicants = catalog.searchResults(
            # reg_num might not be set and then would not be found.
            # We therefore search for applicant_id.
            applicant_id=(None, None))
        used = [value for value in applicants
                if value.container_code.endswith('+')]
        return self.export(used, filepath=filepath)

    def export_filtered(self, site, filepath=None, **kw):
        """Export filtered applicants in container denoted by keywords (`kw`).
        If `filepath` is ``None``, a raw string with CSV data should
        be returned. Only used records are being exported.
        """
        container = grok.getSite()['applicants'][kw['container']]
        container_values = container.values()
        used = [value for value in container_values
                if value.container_code.endswith('+')]
        return self.export(used, filepath=filepath)


class ApplicantPaymentExporter(grok.GlobalUtility, ExporterBase):
    """The Applicant Payment Exporter exports all payments made by applicants.
    In other words, it exports payment tickets in state 'paid'. The exporter
    searches :class:`ApplicantsCatalog` and iterates over all payment tickets
    which are stored in an applicant (container).

    The exporter exports all applicant payments if started in the Data Center
    which means in the context of the `DataCenter` object. The exporter can also
    be started 'locally' which means in the context of an
    `ApplicantsContainer` container, see `ApplicantExporter` above.
    """
    grok.implements(ICSVExporter)
    grok.name('applicantpayments')

    fields = tuple(sorted(iface_names(
        IApplicantOnlinePayment,
        exclude_attribs=False,
        omit=['display_item', 'p_option']))) + (
              'applicant_id',
              'reg_number',
              'display_fullname',)
    title = _(u'Applicant Payments')

    def mangle_value(self, value, name, context=None):
        """The mangler determines the applicant's id.
        """
        if name in ('applicant_id', 'reg_number',
            'display_fullname',) and context is not None:
            applicant = context.__parent__
            value = getattr(applicant, name, None)
        return super(
            ApplicantPaymentExporter, self).mangle_value(
            value, name, context=context)

    def export(self, payments, filepath=None):
        """
        """
        writer, outfile = self.get_csv_writer(filepath)
        for payment in payments:
            self.write_item(payment, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """
        """
        catalog = queryUtility(
            ICatalog, context=site, name='applicants_catalog', default=None)
        if catalog is None:
            return self.export([], filepath)
        applicants = catalog.searchResults(
            # reg_num might not be set and then would not be found.
            # We therefore search for applicant_id.
            applicant_id=(None, None))
        used = [value for value in applicants
                if value.container_code.endswith('+')]
        payments = []
        for applicant in used:
            for payment in applicant.payments:
                if payment.p_state == 'paid':
                    payments.append(payment)
        return self.export(payments, filepath=filepath)

    def export_filtered(self, site, filepath=None, **kw):
        """
        """
        container = grok.getSite()['applicants'][kw['container']]
        container_values = container.values()
        used = [value for value in container_values
                if value.container_code.endswith('+')]
        payments = []
        for applicant in used:
            for payment in applicant.payments:
                if payment.p_state == 'paid':
                    payments.append(payment)
        return self.export(payments, filepath=filepath)

class ApplicantRefereeReportExporter(grok.GlobalUtility, ExporterBase):
    """The Applicant Referee Report Exporter exports all referee reports.
    The exportersearches :class:`ApplicantsCatalog` and iterates over all 
    referee reports which are stored in an applicant (container).

    The exporter exports all referee reports if started in the Data Center
    which means in the context of the `DataCenter` object. The exporter can also
    be started 'locally' which means in the context of an
    `ApplicantsContainer` container, see `ApplicantExporter` above.
    """
    grok.implements(ICSVExporter)
    grok.name('applicantrefereereports')

    fields = tuple(sorted(iface_names(
        IApplicantRefereeReport,
        exclude_attribs=False))) + (
              'applicant_id',
              'reg_number',
              'display_fullname',)
    title = _(u'Applicant Referee Reports')

    def mangle_value(self, value, name, context=None):
        """The mangler determines the applicant's id.
        """
        if name in ('applicant_id', 'reg_number',
            'display_fullname',) and context is not None:
            applicant = context.__parent__
            value = getattr(applicant, name, None)
        return super(
            ApplicantRefereeReportExporter, self).mangle_value(
            value, name, context=context)

    def export(self, refereereports, filepath=None):
        """
        """
        writer, outfile = self.get_csv_writer(filepath)
        for refereereport in refereereports:
            self.write_item(refereereport, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """
        """
        catalog = queryUtility(
            ICatalog, context=site, name='applicants_catalog', default=None)
        if catalog is None:
            return self.export([], filepath)
        applicants = catalog.searchResults(
            # reg_num might not be set and then would not be found.
            # We therefore search for applicant_id.
            applicant_id=(None, None))
        refereereports = []
        for applicant in applicants:
            for refereereport in applicant.refereereports:
                refereereports.append(refereereport)
        return self.export(refereereports, filepath=filepath)

    def export_filtered(self, site, filepath=None, **kw):
        """
        """
        container = grok.getSite()['applicants'][kw['container']]
        container_values = container.values()
        refereereports = []
        for applicant in container_values:
            for refereereport in applicant.refereereports:
                refereereports.append(refereereport)
        return self.export(refereereports, filepath=filepath)