## $Id: export.py 13144 2015-07-07 05:21:14Z henrik $
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
"""Exporters for documents.
"""
import grok
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.utils.helpers import iface_names
from waeup.kofa.documents.interfaces import (
    IPDFDocument, IHTMLDocument, IRESTDocument)


class DocumentExporterBase(grok.GlobalUtility, ExporterBase):
    """This is the exporter base class for all kinds of document exporters.
    Derived classes export all documents of type `class_name` inside the
    documents container.

    All schema fields and the property attributes
    `history`, `state`, `class_name` and `users_with_local_roles`
    are being exported.
    """
    grok.implements(ICSVExporter)
    grok.baseclass()
    class_name = None
    iface = None
    title = None

    @property
    def fields(self):
        return tuple(sorted(iface_names(self.iface, exclude_attribs=False,
            omit=['translated_state',
                  'formatted_transition_date',
                  'translated_class_name',
                  'form_fields_interface',
                  'filenames',
                  'local_roles',
                  ]
            ))) + (
            'users_with_local_roles',)

    def mangle_value(self, value, name, context=None):
        """The mangler prepares the history messages and computes the
        `users_with_local_roles` value which is a Python expression like:

        ``[{'user_name': u'bob', 'local_role': u'bobsrole'},
        {'user_name': u'anna', 'local_role': u'annasrole'}]``
        """
        if name == 'users_with_local_roles':
            value = []
            role_map = IPrincipalRoleMap(context)
            for local_role, user_name, setting in role_map.getPrincipalsAndRoles():
                value.append({'user_name':user_name,'local_role':local_role})
        if name == 'history':
            value = value.messages
        return super(DocumentExporterBase, self).mangle_value(
            value, name, context)

    def export(self, documents, filepath=None):
        """Export `documents`, an iterable, as CSV file.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for document in documents:
            self.write_item(document, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export documents in documentscontainer into filepath as CSV data.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        documents = site.get('documents', {}).values()
        documents = [doc for doc in documents
                     if doc.class_name == self.class_name]
        return self.export(documents, filepath)


class PDFDocumentExporter(DocumentExporterBase):
    """Exporter for documents.
    """
    grok.name('pdfdocuments')
    iface = IPDFDocument
    class_name = 'PDFDocument'
    title = _(u'Public PDF Documents')


class HTMLDocumentExporter(DocumentExporterBase):
    """Exporter for documents.
    """
    grok.name('htmldocuments')
    iface = IHTMLDocument
    class_name = 'HTMLDocument'
    title = _(u'Public HTML Documents')


class RESTDocumentExporter(DocumentExporterBase):
    """Exporter for documents.
    """
    grok.name('restdocuments')
    iface = IRESTDocument
    class_name = 'RESTDocument'
    title = _(u'Public REST Documents')