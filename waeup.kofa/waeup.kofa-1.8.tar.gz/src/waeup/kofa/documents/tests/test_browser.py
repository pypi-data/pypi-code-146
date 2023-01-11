## $Id: test_browser.py 13263 2015-09-17 06:26:01Z henrik $
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
Test the customer-related UI components.
"""
import shutil
import tempfile
from datetime import datetime, timedelta, date
from StringIO import StringIO
import os
from zope.event import notify
from zope.component import createObject, queryUtility, getUtility
from zope.component.hooks import setSite, clearSite
from zope.schema.interfaces import ConstraintNotSatisfied
from zope.catalog.interfaces import ICatalog
from zope.security.interfaces import Unauthorized
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.testbrowser.testing import Browser
from hurry.workflow.interfaces import (
    IWorkflowInfo, IWorkflowState, InvalidTransitionError)
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.app import University
from waeup.kofa.interfaces import (
    IUserAccount, IJobManager,
    IFileStoreNameChooser, IExtFileStore, IFileStoreHandler)
from waeup.kofa.imagestorage import (
    FileStoreNameChooser, ExtFileStore, DefaultFileStoreHandler,
    DefaultStorage)
from waeup.kofa.authentication import LocalRoleSetEvent
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase
from waeup.kofa.browser.tests.test_pdf import samples_dir
from waeup.kofa.documents.workflow import PUBLISHED

PH_LEN = 15911  # Length of placeholder file

SAMPLE_IMAGE = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
#SAMPLE_IMAGE_BMP = os.path.join(os.path.dirname(__file__), 'test_image.bmp')
SAMPLE_PDF = os.path.join(os.path.dirname(__file__), 'test_pdf.pdf')

class FullSetup(FunctionalTestCase):
    # A test case that only contains a setup and teardown
    #
    # Complete setup for customers handlings is rather complex and
    # requires lots of things created before we can start. This is a
    # setup that does all this, creates a company etc.
    # so that we do not have to bother with that in different
    # test cases.

    layer = FunctionalLayer

    def setUp(self):
        super(FullSetup, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        # we add the site immediately after creation to the
        # ZODB. Catalogs and other local utilities are not setup
        # before that step.
        self.app = self.getRootFolder()['app']
        # Set site here. Some of the following setup code might need
        # to access grok.getSite() and should get our new app then
        setSite(app)

        self.login_path = 'http://localhost/app/login'
        self.container_path = 'http://localhost/app/documents'

        # Put the prepopulated site into test ZODB and prepare test
        # browser
        self.browser = Browser()
        self.browser.handleErrors = False

    def tearDown(self):
        super(FullSetup, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)


class DocumentUITests(FullSetup):
    # Tests for document related views and pages

    def test_manage_file_document(self):
        # Managers can access the pages of documentsconter
        # and can perform actions
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.getLink("Documents").click()
        self.assertEqual(self.browser.url, self.container_path)
        self.browser.getLink("Manage").click()
        self.browser.getControl("Add document").click()
        self.browser.getControl(name="doctype").value = ['PDFDocument']
        self.browser.getControl(name="form.title").value = 'My PDF Document'
        self.browser.getControl(name="form.document_id").value = 'DOC1'
        self.browser.getControl("Add document").click()
        self.assertTrue('PDF Document added.' in self.browser.contents)
        document = self.app['documents']['DOC1']

        # Document can be edited
        self.browser.getControl(name="form.title").value = 'My first doc'
        self.browser.getControl("Save").click()
        self.assertTrue('Form has been saved.' in self.browser.contents)
        self.browser.getLink("View").click()
        self.assertEqual(self.browser.url, self.container_path + '/DOC1/index')

        # File can be uploaded
        self.browser.getLink("Manage").click()
        # Create a pseudo image file and select it to be uploaded
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='pdfscanmanageupload')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='my_sample_scan.jpg')
        self.browser.getControl(
            name='upload_pdfscanmanageupload').click()
        self.assertTrue(
            'pdf file format expected' in self.browser.contents)
        ctrl = self.browser.getControl(name='pdfscanmanageupload')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='my_sample_scan.pdf')
        self.browser.getControl(
            name='upload_pdfscanmanageupload').click()
        self.assertTrue(
            'Could not determine file type' in self.browser.contents)
        pdf = open(SAMPLE_PDF, 'rb')
        ctrl = self.browser.getControl(name='pdfscanmanageupload')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pdf, filename='my_sample_scan.pdf')
        self.browser.getControl(
            name='upload_pdfscanmanageupload').click()
        # The file size is shown
        self.assertTrue(
            'href="http://localhost/app/documents/DOC1/file.pdf">DOC1.pdf (23.7 kB)</a>'
            in self.browser.contents)
        # Also on display page the file size is displayed.
        self.browser.open(self.container_path + '/DOC1')
        self.assertTrue(
            'href="http://localhost/app/documents/DOC1/file.pdf">DOC1.pdf (23.7 kB)</a>'
            in self.browser.contents)
        # The file can be found in the file system
        file = getUtility(IExtFileStore).getFileByContext(
            document, attr='file.pdf')
        file_content = file.read()
        pdf.seek(0)
        pdf_content = pdf.read()
        self.assertEqual(file_content, pdf_content)
        # Browsing the link shows a real pdf only if the document
        # has been published
        self.browser.getLink("DOC1.pdf").click()
        self.assertTrue(
            'The document requested has not yet been published'
            in self.browser.contents)
        IWorkflowState(document).setState(PUBLISHED)
        self.browser.open(self.container_path + '/DOC1/file.pdf')
        self.assertEqual(
            self.browser.headers['content-type'], 'application/pdf')
        # The name of the downloaded file will be different
        self.assertEqual(
            self.browser.headers['Content-Disposition'],
            'attachment; filename="DOC1.pdf')

        # Transitions can be performed
        self.assertEqual(document.state, 'published')
        self.browser.open(self.container_path + '/DOC1')
        self.browser.getLink("Transition").click()
        self.browser.getControl(name="transition").value = ['retract']
        self.browser.getControl("Apply now").click()
        self.assertEqual(document.state, 'created')

        # Documents can be removed
        self.browser.getLink("Documents").click()
        self.browser.getLink("Manage").click()
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value=document.document_id).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)

        # File has been removed too
        file = getUtility(IExtFileStore).getFileByContext(
            document, attr='file.pdf')
        self.assertTrue(file is None)

        # All actions are being logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()

        self.assertTrue(
            'INFO - zope.mgr - %s - Document created' % document.document_id
            in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - documents.browser.DocumentAddFormPage - added: PDF Document %s'
            % document.document_id in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - documents.browser.DocumentManageFormPage - %s - saved: title'
            % document.document_id in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - documents.browser.DocumentManageFormPage - %s - uploaded: file.pdf (my_sample_scan.pdf)'
            % document.document_id in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - %s - Document retracted' % document.document_id
            in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - documents.browser.DocumentsContainerManageFormPage - removed: %s'
            % document.document_id in logcontent)

    def test_manage_html_document(self):
        # Managers can access the pages of documentsconter
        # and can perform actions
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.getLink("Documents").click()
        self.assertEqual(self.browser.url, self.container_path)
        self.browser.getLink("Manage").click()
        self.browser.getControl("Add document").click()
        self.browser.getControl(name="doctype").value = ['HTMLDocument']
        self.browser.getControl(name="form.document_id").value = 'DOC2'
        self.browser.getControl(name="form.title").value = 'My HTML Document'
        self.browser.getControl("Add document").click()
        self.assertTrue('HTML Document added.' in self.browser.contents)
        document = self.app['documents']['DOC2']
        # All form action buttons are there
        self.assertTrue('value="Add local role"' in self.browser.contents)
        self.assertTrue('value="Save"' in self.browser.contents)
        self.assertTrue('value="Cancel"' in self.browser.contents)
        # Document can be edited
        self.browser.getControl(name="form.title").value = 'My second doc'
        self.browser.getControl(name="form.html_multilingual").value = """
<h1>Hello World</h1>
>>de<<
<h1>Hallo Welt</h1>
"""
        self.browser.getControl("Save").click()
        self.assertTrue('Form has been saved.' in self.browser.contents)
        self.browser.getLink("View").click()
        self.assertEqual(self.browser.url, self.container_path + '/DOC2/index')
        self.assertTrue(
            '<h1>Hello World</h1>' in self.browser.contents)
        self.assertFalse(
            '<h1>Hallo Welt</h1>' in self.browser.contents)
        self.browser.getLink("de", index=2).click()
        self.assertFalse(
            '<h1>Hello World</h1>' in self.browser.contents)
        self.assertTrue(
            '<h1>Hallo Welt</h1>' in self.browser.contents)
        # The content can't be rendered yet
        self.browser.open(self.container_path + '/DOC2/display')
        self.assertTrue(
            'The document requested has not yet been published'
            in self.browser.contents)
        # We have been redirected to the portal root
        self.assertEqual(self.browser.url, 'http://localhost/app')

        # Transitions can be performed
        self.browser.open(self.container_path + '/DOC2')
        self.browser.getLink("Transition").click()
        self.browser.getControl(name="transition").value = ['publish']
        self.browser.getControl("Apply now").click() # not yet translated
        self.assertEqual(document.state, 'published')

        # The content can be rendered
        self.browser.open(self.container_path + '/DOC2/display')
        self.assertTrue(
            '<h1>Hallo Welt</h1>' in self.browser.contents)

        # Documents can be removed
        self.browser.getLink("en", index=3).click()
        self.browser.getLink("Documents").click()
        self.browser.getLink("Manage").click()
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value=document.document_id).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)

        # All actions are being logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()

        self.assertTrue(
            'INFO - zope.mgr - %s - Document created' % document.document_id
            in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - documents.browser.DocumentAddFormPage - added: HTML Document %s'
            % document.document_id in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - documents.browser.HTMLDocumentManageFormPage - %s - saved: title + html_multilingual'
            % document.document_id in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - %s - Document published' % document.document_id
            in logcontent)
        self.assertTrue(
            'INFO - zope.mgr - documents.browser.DocumentsContainerManageFormPage - removed: %s'
            % document.document_id in logcontent)

    def test_manage_rest_document(self):
        # Managers can access the pages of documentsconter
        # and can perform actions
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.getLink("Documents").click()
        self.assertEqual(self.browser.url, self.container_path)
        self.browser.getLink("Manage").click()
        self.browser.getControl("Add document").click()
        self.browser.getControl(name="doctype").value = ['RESTDocument']
        self.browser.getControl(name="form.document_id").value = 'DOC3'
        self.browser.getControl(name="form.title").value = 'My REST Document'
        self.browser.getControl("Add document").click()
        self.assertTrue('REST Document added.' in self.browser.contents)
        document = self.app['documents']['DOC3']

        # Document can be edited
        self.browser.getControl(name="form.rest_multilingual").value = """
----------
Main Title
----------

Subtitle
========
>>de<<
----------
Haupttitel
----------

Untertitel
==========
"""
        self.browser.getControl("Save").click()
        self.assertTrue('Form has been saved.' in self.browser.contents)
        self.browser.getLink("View").click()
        self.assertEqual(self.browser.url, self.container_path + '/DOC3/index')
        self.assertTrue(
            '<h1 class="title">Main Title</h1>' in self.browser.contents)
        self.assertTrue(
            '<h2 class="subtitle" id="subtitle">Subtitle</h2>'
            in self.browser.contents)
        self.assertFalse(
            '<h1 class="title">Haupttitel</h1>' in self.browser.contents)
        self.browser.getLink("de", index=2).click()
        self.assertFalse(
            '<h1 class="title">Main Title</h1>' in self.browser.contents)
        self.assertTrue(
            '<h1 class="title">Haupttitel</h1>' in self.browser.contents)
        # The content can be rendered
        IWorkflowState(document).setState(PUBLISHED)
        self.browser.open(self.container_path + '/DOC3/display')
        self.assertTrue(
            '<h1 class="title">Haupttitel</h1>' in self.browser.contents)
        # The page label (object title) is not displayed
        self.assertFalse(
            '<h1 class="kofa-content-label">My REST Document</h1>'
            in self.browser.contents)
