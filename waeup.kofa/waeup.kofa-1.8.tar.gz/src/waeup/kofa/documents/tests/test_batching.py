# -*- coding: utf-8 -*-
## $Id: test_batching.py 12438 2015-01-11 08:27:37Z henrik $
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
"""Unit tests for document data processors.
"""
import os
import shutil
import tempfile
import unittest
import datetime
import grok
from time import time
from zope.event import notify
from zope.component import createObject, queryUtility
from zope.component.hooks import setSite, clearSite
from zope.catalog.interfaces import ICatalog
from zope.interface.verify import verifyClass, verifyObject
from zope.securitypolicy.interfaces import IPrincipalRoleManager

from waeup.kofa.app import University
from waeup.kofa.interfaces import IBatchProcessor, FatalCSVError, IUserAccount
from waeup.kofa.documents.batching import PDFDocumentProcessor
from waeup.kofa.documents.document import PDFDocument, HTMLDocument
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

DOCUMENT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_document_data.csv'),
    'rb').read()

DOCUMENT_HEADER_FIELDS = DOCUMENT_SAMPLE_DATA.split(
    '\n')[0].split(',')

DOCUMENT_SAMPLE_DATA_UPDATE = open(
    os.path.join(os.path.dirname(__file__), 'sample_document_data_update.csv'),
    'rb').read()

DOCUMENT_HEADER_FIELDS_UPDATE = DOCUMENT_SAMPLE_DATA_UPDATE.split(
    '\n')[0].split(',')

class DocumentImportExportSetup(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(DocumentImportExportSetup, self).setUp()
        self.dc_root = tempfile.mkdtemp()
        self.workdir = tempfile.mkdtemp()
        app = University()
        app['datacenter'].setStoragePath(self.dc_root)
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(app)

        self.logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        return

    def tearDown(self):
        super(DocumentImportExportSetup, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def setup_for_export(self):
        document1 = PDFDocument()
        document1.document_id = u'DOC1'
        self.app['documents'].addDocument(document1)
        self.pdfdocument = document1
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        role_manager = IPrincipalRoleManager(document1)
        role_manager.assignRoleToPrincipal(u'johnsrole', u'john')

        document2 = HTMLDocument()
        document2.document_id = u'DOC2'
        self.app['documents'].addDocument(document2)
        self.htmldocument = document2
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        role_manager = IPrincipalRoleManager(document2)
        role_manager.assignRoleToPrincipal(u'johnsrole', u'john')
        return


class PDFDocumentProcessorTest(DocumentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(PDFDocumentProcessorTest, self).setUp()

        # Add document
        document = PDFDocument()
        document.document_id = u'DOC1'
        self.app['documents'].addDocument(document)
        document.title = u'Our PDF Document'
        notify(grok.ObjectModifiedEvent(document))
        self.document = self.app['documents'][document.document_id]

        self.processor = PDFDocumentProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_document_data.csv')
        self.csv_file_update = os.path.join(
            self.workdir, 'sample_document_data_update.csv')
        open(self.csv_file, 'wb').write(DOCUMENT_SAMPLE_DATA)
        open(self.csv_file_update, 'wb').write(DOCUMENT_SAMPLE_DATA_UPDATE)

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, PDFDocumentProcessor) is True

    def test_parentsExist(self):
        self.assertFalse(self.processor.parentsExist(None, dict()))
        self.assertTrue(self.processor.parentsExist(None, self.app))

    def test_entryExists(self):
        assert self.processor.entryExists(
            dict(document_id='ID_NONE'), self.app) is False
        assert self.processor.entryExists(
            dict(document_id=self.document.document_id), self.app) is True

    def test_getParent(self):
        parent = self.processor.getParent(None, self.app)
        assert parent is self.app['documents']

    def test_getEntry(self):
        assert self.processor.getEntry(
            dict(document_id='ID_NONE'), self.app) is None
        assert self.processor.getEntry(
            dict(document_id=self.document.document_id), self.app) is self.document

    def test_addEntry(self):
        new_document = PDFDocument()
        new_document.document_id = u'DOC2'
        self.processor.addEntry(
            new_document, {}, self.app)
        assert len(self.app['documents'].keys()) == 2
        self.assertEqual(self.app['documents']['DOC2'].document_id, 'DOC2')

    def test_checkConversion(self):
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(document_id='DOC4', class_name='PDFDocument'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(document_id='id with spaces', class_name='PDFDocument'))
        self.assertEqual(len(errs),1)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(document_id='DOC4', class_name='WrongDocument'), mode='create')
        self.assertEqual(len(errs),1)

    def test_delEntry(self):
        assert self.document.document_id in self.app['documents'].keys()
        self.processor.delEntry(
            dict(document_id=self.document.document_id), self.app)
        assert self.document.document_id not in self.app['documents'].keys()

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, DOCUMENT_HEADER_FIELDS)
        self.assertEqual(num_warns,2)
        self.assertEqual(len(self.app['documents']), 4)
        self.assertEqual(self.app['documents']['ABC'].title,'ABC title')
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry
        self.assertTrue(
            'INFO - system - Public PDF Document Processor - sample_document_data - '
            'EFG - updated: document_id=EFG, title=EFG title\n'
            in logcontent)
        failcontent = open(fail_file).read()
        self.assertTrue(
            'PDFDocument,ABC,Duplicate document,This object already exists.'
            in failcontent)
        self.assertTrue(
            'HTMLDocument,HIJ,HIJ title,class_name: wrong processor'
            in failcontent)
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_update(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, DOCUMENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update, DOCUMENT_HEADER_FIELDS_UPDATE, 'update')
        self.assertEqual(num_warns,1)
        # title has changed
        self.assertEqual(self.app['documents']['ABC'].title,'ABC new title')
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry
        self.assertTrue(
            'INFO - system - Public PDF Document Processor - sample_document_data_update - '
            'ABC - updated: document_id=ABC, title=ABC new title\n'
            in logcontent)
        failcontent = open(fail_file).read()
        self.assertTrue(
            'XYZ,Non-existing document,Cannot update: no such entry'
            in failcontent)
        shutil.rmtree(os.path.dirname(fin_file))
