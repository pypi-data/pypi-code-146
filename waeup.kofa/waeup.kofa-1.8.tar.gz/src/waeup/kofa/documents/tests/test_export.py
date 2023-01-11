## $Id: test_export.py 12438 2015-01-11 08:27:37Z henrik $
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
"""
Test the document exporter.
"""
import os
import grok
import datetime
from cStringIO import StringIO
from zope.component import queryUtility, getUtility
from zope.event import notify
from zope.interface.verify import verifyObject, verifyClass
from waeup.kofa.interfaces import (
    ICSVExporter, IExtFileStore, IFileStoreNameChooser)
from waeup.kofa.documents.export import (
    PDFDocumentExporter, HTMLDocumentExporter)
from waeup.kofa.documents.document import PDFDocument, HTMLDocument
from waeup.kofa.documents.tests.test_batching import DocumentImportExportSetup
from waeup.kofa.testing import FunctionalLayer


class PDFDocumentExporterTest(DocumentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(PDFDocumentExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = PDFDocumentExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, PDFDocumentExporter)
        return

    def test_get_as_utility(self):
        # we can get an document exporter as utility
        result = queryUtility(ICSVExporter, name="pdfdocuments")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can really export a document
        exporter = PDFDocumentExporter()
        exporter.export([self.pdfdocument], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            'class_name,document_id,history,state,title,users_with_local_roles\r\n'
            'PDFDocument,DOC1,'
            '[u\'2014-12-21 16:55:16 UTC - Document created by system\'],'
            'created,,"[{\'user_name\': u\'john\', \'local_role\': u\'johnsrole\'}]"',
            result
            )
        return

    def test_export_all(self):
        # we can really export all documents
        exporter = PDFDocumentExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            'class_name,document_id,history,state,title,users_with_local_roles\r\n'
            'PDFDocument,DOC1,'
            '[u\'2014-12-21 16:55:16 UTC - Document created by system\'],'
            'created,,"[{\'user_name\': u\'john\', \'local_role\': u\'johnsrole\'}]"',
            result
            )
        return


class HTMLDocumentExporterTest(DocumentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(HTMLDocumentExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = HTMLDocumentExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, HTMLDocumentExporter)
        return

    def test_get_as_utility(self):
        # we can get an document exporter as utility
        result = queryUtility(ICSVExporter, name="htmldocuments")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can really export a document
        exporter = HTMLDocumentExporter()
        exporter.export([self.htmldocument], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            'class_name,document_id,history,html_dict,'
            'html_multilingual,state,title,users_with_local_roles\r\n'
            'HTMLDocument,DOC2,'
            '[u\'2014-12-21 16:50:28 UTC - Document created by system\'],'
            '{},,created,,"[{\'user_name\': u\'john\', \'local_role\': u\'johnsrole\'}]"',
            result
            )
        return

    def test_export_all(self):
        # we can really export all documents
        exporter = HTMLDocumentExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            'class_name,document_id,history,html_dict,'
            'html_multilingual,state,title,users_with_local_roles\r\n'
            'HTMLDocument,DOC2,'
            '[u\'2014-12-21 16:50:28 UTC - Document created by system\'],'
            '{},,created,,"[{\'user_name\': u\'john\', \'local_role\': u\'johnsrole\'}]"',
            result
            )
        return
