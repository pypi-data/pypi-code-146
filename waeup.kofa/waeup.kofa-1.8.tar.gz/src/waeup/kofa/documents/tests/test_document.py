## $Id: test_document.py 12438 2015-01-11 08:27:37Z henrik $
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
Tests for documents.
"""
import shutil
import tempfile
from StringIO import StringIO
from zope.interface.verify import verifyClass, verifyObject
from zope.component import createObject, queryUtility
from hurry.workflow.interfaces import (
    IWorkflowInfo, IWorkflowState, InvalidTransitionError)
from waeup.kofa.interfaces import (
    IObjectHistory, IFileStoreNameChooser, IFileStoreHandler)
from waeup.kofa.imagestorage import DefaultStorage
from waeup.kofa.documents.interfaces import (
    IDocumentsContainer, IPublicDocument, IPDFDocument,
    IHTMLDocument, IRESTDocument)
from waeup.kofa.documents.container import DocumentsContainer
from waeup.kofa.documents.document import (
    PDFDocument, HTMLDocument, RESTDocument,
    DocumentFileNameChooser, DocumentFileStoreHandler)
from waeup.kofa.testing import (FunctionalLayer, FunctionalTestCase)

class DocumentsContainerTestCase(FunctionalTestCase):

    layer = FunctionalLayer

    def test_interfaces(self):
        # Make sure the correct interfaces are implemented.
        self.assertTrue(
            verifyClass(
                IDocumentsContainer, DocumentsContainer)
            )
        self.assertTrue(
            verifyObject(
                IDocumentsContainer, DocumentsContainer())
            )
        self.assertTrue(
            verifyClass(
                IPDFDocument, PDFDocument)
            )
        self.assertTrue(
            verifyObject(
                IPDFDocument, PDFDocument())
            )
        self.assertTrue(
            verifyClass(
                IHTMLDocument, HTMLDocument)
            )
        self.assertTrue(
            verifyObject(
                IHTMLDocument, HTMLDocument())
            )
        self.assertTrue(
            verifyClass(
                IRESTDocument, RESTDocument)
            )
        self.assertTrue(
            verifyObject(
                IRESTDocument, RESTDocument())
            )
        return

    def test_addDocument(self):
        container = DocumentsContainer()
        document = createObject(u'waeup.HTMLDocument')
        document.document_id = u'DOC'
        container.addDocument(document)
        self.assertEqual(container[document.document_id], document)
        self.assertRaises(TypeError, container.addDocument, object())
        self.assertEqual(document.document_id, 'DOC')
        return

    def test_document_workflow(self):
        document = createObject(u'waeup.HTMLDocument')
        IWorkflowInfo(document).fireTransition('create')
        self.assertEqual(IWorkflowState(document).getState(), 'created')
        return

    def test_document_history(self):
        doc = createObject(u'waeup.HTMLDocument')
        IWorkflowInfo(doc).fireTransition('create')
        messages = ' '.join(doc.history.messages)
        self.assertTrue('Document created by system' in messages)
        return


class DocumentFileTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(DocumentFileTests, self).setUp()
        self.workdir = tempfile.mkdtemp()
        return

    def tearDown(self):
        super(DocumentFileTests, self).tearDown()
        shutil.rmtree(self.workdir)
        return

    def test_file_store_handler_util_accessible(self):
        # we can get an IFileStoreHandler utility for documents
        handler = queryUtility(IFileStoreHandler, name='file-document')
        self.assertTrue(
            isinstance(handler, DocumentFileStoreHandler))
        return

    def test_file_store_handler(self):
        store = DefaultStorage()
        handler = queryUtility(IFileStoreHandler, name='file-document')
        result = handler.pathFromFileID(
            store, '/fake-root', '__any_marker__sample.jpg')
        self.assertEqual(
            result, '/fake-root/documents/sample')
        return

    def test_file_store_handler_create(self):
        # we can create files in image store with the document file
        # store handler
        store = DefaultStorage(self.workdir)
        handler = queryUtility(IFileStoreHandler, name='file-document')
        file_obj, path, waeup_file = handler.createFile(
            store, store.root, 'sample.jpg', '__file_document__sample',
            StringIO('I am a JPG file'))
        self.assertEqual(path[-20:], 'documents/sample.jpg')
        return

    def test_iface(self):
        # make sure we implement promised interfaces
        obj = DocumentFileNameChooser(None) # needs a context normally
        verifyClass(IFileStoreNameChooser, DocumentFileNameChooser)
        verifyObject(IFileStoreNameChooser, obj)
        return

    def test_name_chooser_available(self):
        # we can get a name chooser for document objects as adapter
        doc = PDFDocument()
        chooser = IFileStoreNameChooser(doc)
        self.assertTrue(chooser is not None)
        return

    def test_name_chooser_document(self):
        # we can get an image filename for documents not in a container
        doc = PDFDocument()
        doc.document_id = u'DOC'
        chooser = IFileStoreNameChooser(doc)
        result = chooser.chooseName('sample.jpg')
        # the file would be stored in a ``_default`` directory.
        self.assertEqual(
            result, '__file-document__sample_DOC.jpg')
        return
