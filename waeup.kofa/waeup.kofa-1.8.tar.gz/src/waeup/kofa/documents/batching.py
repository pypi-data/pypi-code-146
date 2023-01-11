## $Id: batching.py 13145 2015-07-07 05:36:46Z henrik $
##
## Copyright (C) 2014 Uli Fouquet & Henrik Bettermann
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
"""Batch processing components for document objects.

Batch processors eat CSV files to add, update or remove large numbers
of certain kinds of objects at once.
"""
import grok
import unicodecsv as csv  # XXX: csv ops should move to dedicated module.
from time import time
from datetime import datetime
from zope.i18n import translate
from zope.interface import Interface
from zope.schema import getFields
from zope.component import queryUtility, getUtility, createObject
from zope.event import notify
from zope.catalog.interfaces import ICatalog
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from waeup.kofa.interfaces import (
    IBatchProcessor, FatalCSVError, IObjectConverter, IUserAccount,
    IGNORE_MARKER)
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.documents.interfaces import (
    IPDFDocument, IHTMLDocument, IRESTDocument)
from waeup.kofa.utils.batching import BatchProcessor


class DocumentProcessorBase(BatchProcessor):
    """This is the base class for all kinds of document processors.
    The `checkConversion` method checks whether `class_name` in a row
    corresponds with the processor chosen. This is to avoid accidentally
    wrong imports.

    Document processors do not import workflow states or transitions which
    means, all imported documents will be unpublished after batch creation.
    In other words, publishing can't be done by import, it has do be done
    via the UI.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    grok.baseclass()

    util_name = None
    name = None
    iface = None

    location_fields = ['document_id',]
    additional_fields = ['class_name',]

    factory_name = None

    mode = None

    @property
    def available_fields(self):
        return sorted(list(set(
                    self.additional_fields +
                    getFields(self.iface).keys())))

    def parentsExist(self, row, site):
        return 'documents' in site.keys()

    def entryExists(self, row, site):
        document_id = row.get('document_id', None)
        cat = queryUtility(ICatalog, name='documents_catalog')
        results = list(cat.searchResults(document_id=(document_id, document_id)))
        if results:
            return True
        return False

    def getParent(self, row, site):
        return site['documents']

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        parent = self.getParent(row, site)
        return parent.get(row['document_id'])

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent.addDocument(obj)
        return

    def delEntry(self, row, site):
        document = self.getEntry(row, site)
        parent = self.getParent(row, site)
        if document is not None:
            grok.getSite().logger.info(
                '%s - Document removed' % document.document_id)
            del parent[document.document_id]
        return

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = super(DocumentProcessorBase, self).updateEntry(
            obj, row, site, filename)
        # Log actions...
        location_field = self.location_fields[0]
        grok.getSite().logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, row[location_field], items_changed))
        return

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        errs, inv_errs, conv_dict = super(
            DocumentProcessorBase, self).checkConversion(row, mode=mode)
        # We need to check if the class_name corresponds with the
        # processor chosen. This is to avoid accidentally wrong imports.
        if mode == 'create':
            class_name = row.get('class_name', None)
            if class_name != self.factory_name.strip('waeup.'):
                errs.append(('class_name','wrong processor'))
        return errs, inv_errs, conv_dict


class PDFDocumentProcessor(DocumentProcessorBase):
    """A batch processor for IPDFDocument objects.
    """
    util_name = 'pdfdocumentprocessor'
    grok.name(util_name)

    name = _('Public PDF Document Processor')
    iface = IPDFDocument

    factory_name = 'waeup.PDFDocument'


class HTMLDocumentProcessor(DocumentProcessorBase):
    """A batch processor for IHTMLDocument objects.
    """
    util_name = 'htmldocumentprocessor'
    grok.name(util_name)

    name = _('Public HTML Document Processor')
    iface = IHTMLDocument

    factory_name = 'waeup.HTMLDocument'


class RESTDocumentProcessor(DocumentProcessorBase):
    """A batch processor for IRESTDocument objects.
    """
    util_name = 'restdocumentprocessor'
    grok.name(util_name)

    name = _('Public REST Document Processor')
    iface = IRESTDocument

    factory_name = 'waeup.RESTDocument'
