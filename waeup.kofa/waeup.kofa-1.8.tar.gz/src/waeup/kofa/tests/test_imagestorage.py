## $Id: test_imagestorage.py 9286 2012-10-04 09:48:56Z uli $
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
import os
import tempfile
import shutil
import unittest
from StringIO import StringIO
from hurry.file import HurryFile
from hurry.file.interfaces import IFileRetrieval
from zope.component import (
    getUtility, provideUtility, queryUtility, provideAdapter)
from zope.component.hooks import setSite
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.app import University
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.imagestorage import (
    FileStoreNameChooser, ExtFileStore, DefaultFileStoreHandler,
    DefaultStorage)
from waeup.kofa.interfaces import (
    IFileStoreNameChooser, IExtFileStore, IFileStoreHandler,)

class FileStoreNameChooserTests(FunctionalTestCase):

    layer = FunctionalLayer

    def test_iface(self):
        # we provide the interfaces we promise to do
        obj = FileStoreNameChooser(None)
        verifyClass(IFileStoreNameChooser, FileStoreNameChooser)
        verifyObject(IFileStoreNameChooser, obj)
        return

    def test_accessible_as_adapter(self):
        # we can get a file name chooser via adapter
        chooser = IFileStoreNameChooser(object())
        self.assertTrue(
            isinstance(chooser, FileStoreNameChooser))
        return

    def test_check_name(self):
        # default file name choosers accept any string
        chooser = FileStoreNameChooser(object())
        self.assertEqual(chooser.checkName('Hi there!'), True)
        self.assertEqual(chooser.checkName(None), False)
        return

    def test_choose_name(self):
        # we get a simple string if we do not pass in a valid string
        chooser = FileStoreNameChooser(object())
        self.assertEqual(chooser.chooseName('myname'), 'myname')
        self.assertEqual(chooser.chooseName(None), u'unknown_file')
        return

class ExtFileStoreTests(unittest.TestCase):
    # Test external file store (non-functional mode)

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.root = None
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        if self.root is not None:
            shutil.rmtree(self.root)
        return

    def test_iface(self):
        obj = ExtFileStore(None)
        verifyClass(IExtFileStore, ExtFileStore)
        verifyObject(IExtFileStore, obj)
        self.root = obj.root # for cleanup
        return

    def test_root_setup_wo_site(self):
        # if no site is available we can use a temporary root
        fs = ExtFileStore()
        self.root = fs.root
        self.assertTrue(isinstance(self.root, basestring))
        self.assertTrue(os.path.exists(self.root))
        return

    def test_create_instance(self):
        # we can create file stores with or without a root dir set
        storage1 = ExtFileStore()
        storage2 = ExtFileStore(root=self.workdir)
        self.root = storage1.root
        self.assertTrue(storage1.root is not None)
        self.assertTrue(storage1.root != storage2.root)
        self.assertEqual(storage2.root, self.workdir)
        return

    def test_create_file(self):
        # We can store files
        storage = ExtFileStore(root=self.workdir)
        dummy_file = StringIO('sample file')
        image_file = storage.createFile('mysample', dummy_file)
        self.assertTrue('mysample' in os.listdir(storage.root))
        self.assertEqual('mysample', image_file.data)
        return

    def test_create_file_w_ext(self):
        # We can store files with filename extension
        storage = ExtFileStore(root=self.workdir)
        dummy_file = StringIO('sample file')
        image_file = storage.createFile('mysample.txt', dummy_file)
        self.assertTrue('mysample.txt' in os.listdir(storage.root))
        self.assertEqual('mysample.txt', image_file.data)
        return

    def test_get_file(self):
        # We can get files after having them stored
        storage = ExtFileStore(root=self.workdir)
        dummy_file = StringIO('sample file')
        image_file = storage.createFile('mysample', dummy_file)
        result = storage.getFile(image_file.data)
        self.assertEqual(result.read(), 'sample file')
        return

    def test_get_file_w_ext(self):
        # We can get files with filename extension after having them
        # stored
        storage = ExtFileStore(root=self.workdir)
        dummy_file = StringIO('sample file')
        image_file = storage.createFile('mysample.txt', dummy_file)
        result = storage.getFile('mysample')
        self.assertEqual(result.read(), 'sample file')
        return

    def test_replace_file_w_new_ext(self):
        # when we store a file with the same file_id but different
        # filename extension, the old file will be deleted
        storage = ExtFileStore(root=self.workdir)
        dummy_file = StringIO('sample_file')
        image_file = storage.createFile('mysample.jpg', dummy_file)
        file1_path = storage.getFile('mysample').name
        new_file = storage.createFile(
            'mysample.png', StringIO('new file'))
        file2 = storage.getFile('mysample')
        self.assertEqual(file2.name[-12:], 'mysample.png')
        self.assertEqual(file2.read(), 'new file')
        # the old file was deleted
        self.assertFalse(os.path.exists(file1_path))
        return

    def test_extract_marker(self):
        # file stores support extracting markers from filenames
        storage = ExtFileStore(root=self.workdir)
        result1 = storage.extractMarker(None)
        result2 = storage.extractMarker('')
        result3 = storage.extractMarker('no-marker')
        result4 = storage.extractMarker('no-marker.txt')
        result5 = storage.extractMarker('__MARKER__foo.jpg')
        result6 = storage.extractMarker('__MaRkEr__foo.jpg')
        result7 = storage.extractMarker('__THE_MARKER__foo.jpg')
        result8 = storage.extractMarker('__A_MARK__my__foo.jpg')

        self.assertEqual(result1, ('', '', '', ''))
        self.assertEqual(result2, ('', '', '', ''))
        self.assertEqual(result3, ('', 'no-marker', 'no-marker', ''))
        self.assertEqual(result4, ('', 'no-marker.txt', 'no-marker', '.txt'))
        self.assertEqual(result5, ('marker', 'foo.jpg', 'foo', '.jpg'))
        self.assertEqual(result6, ('marker', 'foo.jpg', 'foo', '.jpg'))
        self.assertEqual(result7, ('the_marker', 'foo.jpg', 'foo', '.jpg'))
        self.assertEqual(result8, ('a_mark', 'my__foo.jpg', 'my__foo', '.jpg'))
        return

class DefaultFileStoreHandlerTests(unittest.TestCase):

    def test_iface(self):
        obj = DefaultFileStoreHandler()
        verifyClass(IFileStoreHandler, DefaultFileStoreHandler)
        verifyObject(IFileStoreHandler, obj)
        return

class CustomizedFileHandler(object):
    def pathFromFileID(self, store, root, file_id):
        return os.path.join(root, file_id[12:])

    def createFile(self, store, root, filename, file_id, f):
        ext = os.path.splitext(filename)[1]
        path = self.pathFromFileID(store, root, file_id) + ext
        return f, path, HurryFile(filename, file_id + ext)

class CustomContext(object):
    pass

class CustomContextFileChooser(object):
    def __init__(self, context):
        self.context = context

    def chooseName(self, name=None, attr=None):
        # this name chooser returns different file ids depending on
        # the `attr` parameter, a simple string.
        if attr=='img':
            return '__mymarker__mysample_img.jpg'
        elif attr=='doc':
            return '__mymarker__mysample_doc.doc'
        return '__mymarker__mysample.txt'

class FunctionalExtFileStoreTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(FunctionalExtFileStoreTests, self).setUp()
        self.workdir = tempfile.mkdtemp()
        self.root = None
        self.samplefile = os.path.join(self.workdir, 'sample')
        self.otherfile = os.path.join(self.workdir, 'other')
        open(self.samplefile, 'wb').write('Hi there!')
        open(self.otherfile, 'wb').write('Hi from other!')
        self.fd = open(self.samplefile, 'r')
        self.fd2 = open(self.otherfile, 'r')
        self.getRootFolder()['app'] = University()
        self.app = self.getRootFolder()['app']
        self.app['datacenter'].setStoragePath(self.workdir)
        # register a custom filename mangler
        provideUtility(
            CustomizedFileHandler(), IFileStoreHandler, name=u'mymarker')
        # register a file chooser adapter for CustomContext
        provideAdapter(
            CustomContextFileChooser,
            (CustomContext,), IFileStoreNameChooser)
        return


    def tearDown(self):
        super(FunctionalExtFileStoreTests, self).tearDown()
        self.fd.close()
        self.fd2.close()
        shutil.rmtree(self.workdir)
        if self.root is not None and os.path.exists(self.root):
            shutil.rmtree(self.root)
        return

    def test_root_setup_w_site(self):
        # if a site is available we use it to determine the root dir
        fs = ExtFileStore()
        setSite(self.app)
        self.root = fs.root
        expected_root = os.path.join(
            self.app['datacenter'].storage, 'media')
        self.assertTrue(isinstance(self.root, basestring))
        self.assertEqual(self.root, expected_root)
        return

    def test_get_utility(self):
        # we can get an ExtFileStore by global utility lookup
        fs1 = getUtility(IExtFileStore)
        fs2 = getUtility(IExtFileStore)
        self.assertTrue(isinstance(fs1, ExtFileStore))
        self.assertTrue(fs1 is fs2)
        return

    def test_default_handler_create_file(self):
        # we can use the default handler to store files
        fs = ExtFileStore(root=self.workdir)
        result = fs.createFile('sample.txt', StringIO('sample text'))
        self.assertEqual(result.data, 'sample.txt')
        self.assertTrue('sample.txt' in os.listdir(fs.root))
        return

    def test_default_handler_get_file(self):
        # we can get files stored by the default handler
        fs = ExtFileStore(root=self.workdir)
        fs.createFile('sample.txt', StringIO('sample text'))
        result1 = fs.getFile('sample.txt')
        result2 = fs.getFile('not-existent')
        self.assertEqual(result1.read(), 'sample text')
        self.assertTrue(result2 is None)
        return

    def test_customized_handler_create_file(self):
        # we can use registered filename handlers
        fs = ExtFileStore(root=self.workdir)
        result = fs.createFile(
            '__MYMARKER__sample.txt', StringIO('sample text'))
        self.assertEqual(result.data, '__MYMARKER__sample.txt')
        self.assertTrue('sample.txt' in os.listdir(fs.root))
        return

    def test_customized_handler_create_file_w_ext(self):
        # when we create a file of img type, the filename ext is taken
        # from input file.
        fs = ExtFileStore(root=self.workdir)
        result = fs.createFile(
            '__MYMARKER__sample_img.png', StringIO('sample text'))
        self.assertEqual(result.data, '__MYMARKER__sample_img.png')
        self.assertTrue('sample_img.png' in os.listdir(fs.root))
        return

    def test_customized_handler_get_file(self):
        # we consider registered filename handlers when asking for
        # stored files.
        fs = ExtFileStore(root=self.workdir)
        fs.createFile('__MYMARKER__sample.txt', StringIO('sample text'))
        result1 = fs.getFile('__MYMARKER__sample.txt')
        result2 = fs.getFile('__MYMARKER__not-existent')
        result3 = fs.getFile('not-existent')
        self.assertEqual(result1.read(), 'sample text')
        self.assertTrue(result2 is None)
        self.assertTrue(result3 is None)
        return

    def test_get_file_by_context_w_attr(self):
        # if we register a file name chooser, we can also get a file
        # by context and attribute
        context = CustomContext()
        file_id1 = IFileStoreNameChooser(context).chooseName()
        file_id2 = IFileStoreNameChooser(context).chooseName(attr='img')
        file_id3 = IFileStoreNameChooser(context).chooseName(attr='doc')
        # create three files for a single context, each with different
        # content
        fs = ExtFileStore(root=self.workdir)
        fs.createFile(file_id1, StringIO('my sample 1'))
        fs.createFile(file_id2, StringIO('my sample 2'))
        fs.createFile(file_id3, StringIO('my sample 3'))
        # now get back all files indicated by different `attr` markers
        result1 = fs.getFileByContext(context)
        result2 = fs.getFileByContext(context, attr='img')
        result3 = fs.getFileByContext(context, attr='doc')
        # each file has a different file id
        self.assertEqual(file_id1, '__mymarker__mysample.txt')
        self.assertEqual(file_id2, '__mymarker__mysample_img.jpg')
        self.assertEqual(file_id3, '__mymarker__mysample_doc.doc')
        # each file has different content
        self.assertEqual(result1.read(), 'my sample 1')
        self.assertEqual(result2.read(), 'my sample 2')
        self.assertEqual(result3.read(), 'my sample 3')
        return

    def test_get_default_handler(self):
        # we can get a default handler
        result = queryUtility(IFileStoreHandler)
        self.assertTrue(
            isinstance(result, DefaultFileStoreHandler))
        return

    def test_get_default_file_retrieval(self):
        # we get a file store when requesting a file retrieval
        result = queryUtility(IFileRetrieval)
        self.assertTrue(
            isinstance(result, DefaultStorage))

    def test_delete_file(self):
        # we can remove stored files from storage
        fs = ExtFileStore(root=self.workdir)
        # First, we store a file in file store
        fs.createFile('sample.txt', StringIO('sample text'))
        # Then we delete it
        fs.deleteFile('sample.txt')
        # 'Deletion' means, next call to getFile should get None
        result = fs.getFile('sample.txt')
        self.assertTrue(result is None)
        # Hm, okay we can also check, whether it was really deleted
        self.assertTrue('sample.txt' not in os.listdir(fs.root))
        return

    def test_delete_file_by_context_w_attr(self):
        # if we register a file name chooser, we can also delete a file
        # by context and attribute
        fs = ExtFileStore(root=self.workdir)
        context = CustomContext()
        file_id1 = IFileStoreNameChooser(context).chooseName()
        file_id2 = IFileStoreNameChooser(context).chooseName(attr='img')
        file_id3 = IFileStoreNameChooser(context).chooseName(attr='doc')
        fs = ExtFileStore(root=self.workdir)
        # create three files for a single context, each which
        # different content
        fs.createFile(file_id1, StringIO('my sample 1'))
        fs.createFile(file_id2, StringIO('my sample 2'))
        fs.createFile(file_id3, StringIO('my sample 3'))
        # now delete first two of these files
        fs.deleteFileByContext(context)
        fs.deleteFileByContext(context, attr='img')
        # Following getFile calls should give None for two of the
        # files.
        result1 = fs.getFileByContext(context)
        result2 = fs.getFileByContext(context, attr='img')
        result3 = fs.getFileByContext(context, attr='doc')
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)
        self.assertEqual(result3.read(), 'my sample 3')
        return
