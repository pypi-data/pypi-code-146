# -*- coding: utf-8 -*-

## $Id: test_helpers.py 16818 2022-02-21 06:21:10Z henrik $
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

import datetime
import os
import pytz
import shutil
import tempfile
import unittest
import doctest
from cStringIO import StringIO
from zope import schema
from zope.interface import Interface, Attribute, implements, implementer
from zope.security.testing import Principal, Participation
from zope.security.management import newInteraction, endInteraction
from waeup.kofa.utils import helpers

class IFakeObject(Interface):
    """Some marker interface."""

class FakeObject(object):
    implements(IFakeObject)

class SimpleHelpersTestCase(unittest.TestCase):
    # Tests for simple functions in `helpers`.
    def test_product(self):
        # the product will return zero without input
        result1 = helpers.product([])
        result2 = helpers.product([1,2,3])
        result3 = helpers.product([], start=5)
        result4 = helpers.product([1,2,3], start=5)
        self.assertEqual(result1, 0)
        self.assertEqual(result2, 6)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 30)
        return

    def test_attrs_to_fields_properties(self):
        # we can omit single fields in order to retrieve properties
        class IMyInterface(Interface):
            attr1 = schema.Int(
                title = u'Attribute 1', readonly = True, default = 110,
                )

        @helpers.attrs_to_fields
        @implementer(IMyInterface)
        class MyClass1(object):
            @property
            def attr1(self):
                return 42

        @implementer(IMyInterface)
        class MyClass2(object):
            @property
            def attr1(self):
                return 42
        MyClass2 = helpers.attrs_to_fields(MyClass2, omit=['attr1'])

        obj1 = MyClass1()
        obj2 = MyClass2()

        self.assertEqual(obj1.attr1, 110)
        self.assertEqual(obj2.attr1, 42)
        return


class RemoveFileOrDirectoryTestCase(unittest.TestCase):

    def setUp(self):
        self.dirpath = tempfile.mkdtemp()
        self.filepath = os.path.join(self.dirpath, 'somefile')
        self.non_file = os.path.join(self.dirpath, 'nonfile')
        open(self.filepath, 'wb').write('Hi!')
        return

    def tearDown(self):
        if os.path.exists(self.dirpath):
            shutil.rmtree(self.dirpath)
        return

    def test_handle_not_existing_path(self):
        result = helpers.remove_file_or_directory(self.non_file)
        self.assertTrue(result is None)
        return

    def test_handle_dir(self):
        helpers.remove_file_or_directory(self.dirpath)
        self.assertFalse(
            os.path.exists(self.dirpath)
            )
        return

    def test_handle_file(self):
        helpers.remove_file_or_directory(self.filepath)
        self.assertFalse(
            os.path.exists(self.filepath)
            )
        return

class CopyFileSystemTreeTestCase(unittest.TestCase):
    # Test edge cases of copy_filesystem_tree().
    #
    # This is a typical case of tests not written as doctest as it is
    # normally not interesting for developers and we only want to make
    # sure everything works as expected.
    def setUp(self):
        self.existing_src = tempfile.mkdtemp()
        self.filepath = os.path.join(self.existing_src, 'somefile')
        open(self.filepath, 'wb').write('Hi!')
        self.existing_dst = tempfile.mkdtemp()
        self.not_existing_dir = tempfile.mkdtemp()
        shutil.rmtree(self.not_existing_dir)

        pass

    def tearDown(self):
        shutil.rmtree(self.existing_src)
        shutil.rmtree(self.existing_dst)
        pass

    def test_source_and_dst_existing(self):
        helpers.copy_filesystem_tree(self.existing_src, self.existing_dst)
        self.assertTrue(
            os.path.exists(
                os.path.join(self.existing_dst, 'somefile')
                )
            )
        return

    def test_source_not_existing(self):
        self.assertRaises(
            ValueError,
            helpers.copy_filesystem_tree,
            self.not_existing_dir,
            self.existing_dst
            )
        return

    def test_dest_not_existing(self):
        self.assertRaises(
            ValueError,
            helpers.copy_filesystem_tree,
            self.existing_src,
            self.not_existing_dir
            )
        return

    def test_src_not_a_dir(self):
        self.assertRaises(
            ValueError,
            helpers.copy_filesystem_tree,
            self.filepath,
            self.existing_dst
            )
        return

    def test_dst_not_a_dir(self):
        self.assertRaises(
            ValueError,
            helpers.copy_filesystem_tree,
            self.existing_src,
            self.filepath
            )
        return

class ReST2HTMLTestCase(unittest.TestCase):

    def setUp(self):
        self.expected = u'<div class="document">\n\n\n<p>Some '
        self.expected += u'test with \xfcmlaut</p>\n</div>'
        return

    def test_ascii_umlauts(self):
        # Make sure we convert umlauts correctly to unicode.
        source = 'Some test with ümlaut'
        result = helpers.ReST2HTML(source)
        self.assertEqual(result, self.expected)

    def test_unicode_umlauts(self):
        # Make sure we convert umlauts correctly to unicode.
        source = u'Some test with ümlaut'
        result = helpers.ReST2HTML(source)
        self.assertEqual(result, self.expected)

    def test_unicode_output_from_ascii(self):
        source = 'Some test with ümlaut'
        self.assertTrue(isinstance(helpers.ReST2HTML(source), unicode))

    def test_unicode_output_from_unicode(self):
        source = u'Some test with ümlaut'
        self.assertTrue(isinstance(helpers.ReST2HTML(source), unicode))


class FactoryBaseTestCase(unittest.TestCase):

    def test_ifaces(self):
        # We test all relevant parts in the docstring. But the interfaces
        # method has to be tested to please the coverage report as well.
        factory = helpers.FactoryBase()
        factory.factory = FakeObject
        self.assertTrue(factory.getInterfaces()(IFakeObject))
        return

class CurrentPrincipalTestCase(unittest.TestCase):

    def tearDown(test):
        endInteraction() # Just in case, one is still lingering around

    def test_existing_principal(self):
        # We can get the current principal if one is involved
        principal = Principal('myprincipal')
        newInteraction(Participation(principal))
        result = helpers.get_current_principal()
        self.assertTrue(result is principal)

    def test_no_participation(self):
        # Interactions without participation are handled correctly
        newInteraction()
        result = helpers.get_current_principal()
        self.assertTrue(result is None)

    def test_not_existing_principal(self):
        # Missing interactions do not raise errors.
        result = helpers.get_current_principal()
        self.assertTrue(result is None)

class CmpFilesTestCase(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workdir)

    def test_equal(self):
        p1 = os.path.join(self.workdir, 'sample1')
        p2 = os.path.join(self.workdir, 'sample2')
        open(p1, 'wb').write('Hi!')
        open(p2, 'wb').write('Hi!')
        assert helpers.cmp_files(open(p1, 'r'), open(p2, 'r')) is True

    def test_unequal(self):
        p1 = os.path.join(self.workdir, 'sample1')
        p2 = os.path.join(self.workdir, 'sample2')
        open(p1, 'wb').write('Hi!')
        open(p2, 'wb').write('Ho!')
        assert helpers.cmp_files(open(p1, 'r'), open(p2, 'r')) is False

class FileSizeTestCase(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workdir)

    def test_real_file(self):
        # we can get the size of real files
        path = os.path.join(self.workdir, 'sample.txt')
        open(path, 'wb').write('My content')
        self.assertEqual(
            int(helpers.file_size(open(path, 'rb'))), 10)
        return

    def test_stringio_file(self):
        # we can get the size of file-like objects
        self.assertEqual(
            helpers.file_size(StringIO('my sample content')), 17)

class IfaceNamesTestCase(unittest.TestCase):

    def test_iface_names(self):
        class I1(Interface):
            foo = Attribute("""Some Foo""")
            def bar(blah):
                pass
            i1_name = schema.TextLine(title=u'i1 name')
        class I2(I1):
            baz = schema.TextLine(title=u'some baz')
        class I3(I2):
            pass

        result1 = helpers.iface_names(I3)
        result2 = helpers.iface_names(I2)
        result3 = helpers.iface_names(I1)
        result4 = helpers.iface_names(I3, exclude_attribs=False)
        result5 = helpers.iface_names(I3, exclude_methods=False)
        result6 = helpers.iface_names(I3, omit='i1_name')
        self.assertEqual(sorted(result1), ['baz', 'i1_name'])
        self.assertEqual(sorted(result2), ['baz', 'i1_name'])
        self.assertEqual(sorted(result3), ['i1_name'])
        self.assertEqual(sorted(result4), ['baz', 'foo', 'i1_name'])
        self.assertEqual(sorted(result5), ['bar', 'baz', 'i1_name'])
        self.assertEqual(sorted(result6), ['baz'])
        return

class DateTimeHelpersTestCase(unittest.TestCase):

    def test_now(self):
        tz_berlin = pytz.timezone('Europe/Berlin')
        result1 = helpers.now()
        result2 = helpers.now(tz_berlin)
        self.assertEqual(result1.tzinfo, pytz.utc)
        self.assertFalse(result2.tzinfo == pytz.utc)
        self.assertFalse(result2.tzinfo is None)
        return

    def test_to_timezone(self):
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        tz_berlin = pytz.timezone('Europe/Berlin')
        tz_lagos = pytz.timezone('Africa/Lagos')
        dt1 = datetime.datetime(2012, 1, 1, 0, 0)
        dt2 = datetime.datetime(2012, 1, 1, 0, 0, tzinfo=tz_berlin)
        dt3 = datetime.datetime(2012, 6, 1, 0, 0, tzinfo=tz_lagos)
        dt4 = datetime.datetime(2012, 6, 1, 0, 0, tzinfo=tz_berlin)
        result1 = helpers.to_timezone(dt1)
        result2 = helpers.to_timezone(dt1, pytz.utc)
        result3 = helpers.to_timezone(dt2)
        result4 = helpers.to_timezone(dt2, tz_lagos)
        result5 = helpers.to_timezone(dt3, tz_berlin)
        result6 = helpers.to_timezone(dt4, tz_lagos)
        self.assertEqual(
            result1.strftime(fmt), '2012-01-01 00:00:00 UTC+0000')
        self.assertEqual(
            result2.strftime(fmt), '2012-01-01 00:00:00 UTC+0000')
        self.assertEqual(
            result3.strftime(fmt), '2011-12-31 23:00:00 UTC+0000')
        self.assertEqual(
            result4.strftime(fmt), '2012-01-01 00:00:00 WAT+0100')
        self.assertEqual(
            result5.strftime(fmt), '2012-06-01 01:46:00 CEST+0200')
        self.assertEqual(
            result6.strftime(fmt), '2012-06-01 00:00:00 WAT+0100')
        return

    def test_to_timezone_no_dt(self):
        # the to_timezone function copes with dates (!= datetimes)
        d = datetime.date(2012, 12, 1)
        result1 = helpers.to_timezone(d)
        result2 = helpers.to_timezone(d, pytz.utc)
        self.assertEqual(result1, d)
        self.assertEqual(result2, d)
        return

class GetFileFormatTestCase(unittest.TestCase):
    # Tests for the get_fileformat helper.

    def setUp(self):
        self.valid_jpg_path = os.path.join(
            os.path.dirname(__file__), 'sample_jpg_valid.jpg')
        self.valid_jpg = open(self.valid_jpg_path, 'rb').read()
        self.valid_png_path = os.path.join(
            os.path.dirname(__file__), 'sample_png_valid.png')
        self.valid_png = open(self.valid_png_path, 'rb').read()
        self.valid_pdf_path = os.path.join(
            os.path.dirname(__file__), 'sample_pdf_valid.pdf')
        self.valid_pdf = open(self.valid_pdf_path, 'rb').read()
        self.valid_fpm_path = os.path.join(
            os.path.dirname(__file__), 'sample_fpm_valid.fpm')
        self.valid_fpm = open(self.valid_fpm_path, 'rb').read()
        return

    def test_none(self):
        # ``None`` is not a file and not a valid file format
        self.assertEqual(helpers.get_fileformat(None), None)
        return

    def test_path_and_bytestream(self):
        # get_fileformat accepts bytestreams and paths as arg.
        self.assertEqual(
            helpers.get_fileformat(None, self.valid_jpg), 'jpg')
        self.assertEqual(
            helpers.get_fileformat(self.valid_jpg_path), 'jpg')
        # path is ignored when giving a bytestream
        self.assertEqual(
            helpers.get_fileformat('blah', self.valid_jpg), 'jpg')
        return

    def test_jpg(self):
        # we recognize jpeg images.
        self.assertEqual(
            helpers.get_fileformat(self.valid_jpg_path), 'jpg')
        self.assertEqual(
            helpers.get_fileformat(None, self.valid_jpg), 'jpg')
        return

    def test_png(self):
        # we recognize png images.
        self.assertEqual(
            helpers.get_fileformat(self.valid_png_path), 'png')
        self.assertEqual(
            helpers.get_fileformat(None, self.valid_png), 'png')
        return

    def test_pdf(self):
        # we recognize pdf documents.
        self.assertEqual(
            helpers.get_fileformat(self.valid_pdf_path), 'pdf')
        self.assertEqual(
            helpers.get_fileformat(None, self.valid_pdf), 'pdf')
        return

    def test_fpm(self):
        # we recognize fpm files.
        # fpm files are binary fingerprint data produced by libfprint.
        self.assertEqual(
            helpers.get_fileformat(self.valid_fpm_path), 'fpm')
        self.assertEqual(
            helpers.get_fileformat(None, self.valid_fpm), 'fpm')
        return

class MergeCSVFileTestCase(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.path1 = os.path.join(self.workdir, 'myfile1')
        self.path2 = os.path.join(self.workdir, 'myfile2')
        self.result_path = None
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        if self.result_path is not None and os.path.exists(self.result_path):
            os.unlink(self.result_path)
        return

    def test_basic(self):
        # we can merge very basic CSV files
        open(self.path1, 'wb').write('name,age\nManfred,32\n')
        open(self.path2, 'wb').write('name,age\nBarney,28\n')
        self.result_path = helpers.merge_csv_files(self.path1, self.path2)
        contents = open(self.result_path, 'r').read()
        self.assertEqual(
            contents,
            'age,name\r\n'
            '32,Manfred\r\n'
            '28,Barney\r\n')
        return

    def test_different_col_order(self):
        # if cols of both files have different order, that won't stop us
        open(self.path1, 'wb').write('name,age\nManfred,32\n')
        open(self.path2, 'wb').write('age,name\n28,Barney\n')
        self.result_path = helpers.merge_csv_files(self.path1, self.path2)
        contents = open(self.result_path, 'r').read()
        self.assertEqual(
            contents,
            'age,name\r\n'
            '32,Manfred\r\n'
            '28,Barney\r\n')
        return

    def test_different_cols_at_all(self):
        # also cols available only in one file will work.
        open(self.path1, 'wb').write('name,age\nManfred,32\n')
        open(self.path2, 'wb').write('name,age,buddy\nBarney,28,Manfred\n')
        self.result_path = helpers.merge_csv_files(self.path1, self.path2)
        contents = open(self.result_path, 'r').read()
        self.assertEqual(
            contents,
            'age,buddy,name\r\n'
            '32,,Manfred\r\n'
            '28,Manfred,Barney\r\n')
        return

    def test_one_empty_input(self):
        # we cope even with nearly empty input (one file with no data)
        open(self.path1, 'wb').write('\n')
        open(self.path2, 'wb').write('name,age\nManfred,32\n')
        self.result_path = helpers.merge_csv_files(self.path1, self.path2)
        contents = open(self.result_path, 'r').read()
        self.assertEqual(
            contents,
            'age,name\r\n'
            '32,Manfred\r\n')
        return

    def test_two_empty_inputs(self):
        # we cope even with empty input (two files with no data)
        open(self.path1, 'wb').write('\n')
        open(self.path2, 'wb').write('\n')
        self.result_path = helpers.merge_csv_files(self.path1, self.path2)
        contents = open(self.result_path, 'r').read()
        self.assertEqual(
            contents, '\r\n')
        return


class CheckCSVCharsetTestCase(unittest.TestCase):

    def test_valid_data1(self):
        csv = (
            'col1,col2,col3\n'
            'val1,val2,val3\n'
            ).splitlines()
        self.assertEqual(helpers.check_csv_charset(csv), None)

    def test_valid_data2(self):
        csv = (
            "code,title,title_prefix\n"
            "FAC1,Faculty 1,faculty\n"
            "FAC2,Faculty 2,institute\n"
            "FAC3,Fäcülty 3,school\n"
            ).splitlines()
        self.assertEqual(helpers.check_csv_charset(csv), None)

    def test_invalid_data1(self):
        csv = (
            'col1,col2,col3\n' +
            chr(0x92) + 'val1,val2,val3\n'
            ).splitlines()
        self.assertEqual(helpers.check_csv_charset(csv), 1)

    def test_invalid_data2(self):
        csv = (
            'some text that \n'
            '\n'      # this empty line will break
            'is not a csv file\n' + chr(0x92) + '\n'
            ).splitlines()
        self.assertEqual(helpers.check_csv_charset(csv), 2)


    def test_invalid_data3(self):
        csv = (
            "code,title,title_prefix\n"
            "FAC1,Faculty 1,faculty\n"
            "FAC2,Faculty 2 ,institute\n"
            "FAC3,Fäcülty 3,school\n"
            ).splitlines()
        self.assertEqual(helpers.check_csv_charset(csv), None)

class MemInfoTestCase(unittest.TestCase):

    def test_getsetattrs(self):
        # we can set/get attributes of MemInfos
        info = helpers.MemInfo()
        self.assertRaises(
            KeyError, info.__getattr__, 'foo')
        info['foo'] = 'bar'
        assert info.foo == 'bar'
        info.bar = 'baz'
        assert info.bar == 'baz'

    def test_getattrs(self):
        # we can del attributes
        info = helpers.MemInfo()
        info['foo'] = 'bar'
        del info['foo']
        self.assertRaises(
            KeyError, info.__getattr__, 'foo')
        info['bar'] = 'baz'
        del info.bar
        self.assertRaises(
            KeyError, info.__getattr__, 'bar')


class GetMemInfoTestCase(unittest.TestCase):

    @unittest.skipIf(
        not os.path.exists('/proc/meminfo'),
        reason="No /proc/meminfo found.")
    def test_system(self):
        info = helpers.get_meminfo()
        assert isinstance(info, helpers.MemInfo)

    def test_values(self):
        sample_meminfo = os.path.join(
            os.path.dirname(__file__), 'sample_meminfo')
        info = helpers.get_meminfo(src=sample_meminfo)
        assert info.Cached == 1013816

    def test_invalid_src(self):
        # we cope with invalid src files
        info = helpers.get_meminfo(src="nOt-ExIsTiNg-FiLe")
        assert info is None


class Html2dictTestCase(unittest.TestCase):

    def test_html2dict(self):
        assert helpers.html2dict(None) == {}
        assert helpers.html2dict() == {}
        assert helpers.html2dict(9) == {}
        assert helpers.html2dict('Hello world') == {
            'en': u'<div id="html">Hello world</div id="html">'}
        assert helpers.html2dict('Hello world>>de<<Hallo Welt') == {
            'de': u'<div id="html">Hallo Welt</div id="html">',
            'en': u'<div id="html">Hello world</div id="html">'}


class Rest2dictTestCase(unittest.TestCase):

    def test_rest2dict(self):
        assert helpers.rest2dict(None) == {}
        assert helpers.rest2dict() == {}
        assert helpers.rest2dict(9) == {}
        assert helpers.rest2dict('Hello world') == {
            'en': u'<div id="rest"><div class="document">\n\n\n<p>Hello world'
                   '</p>\n</div></div id="rest">'}
        assert helpers.rest2dict('Hello world>>de<<Hallo Welt') == {
            'de': u'<div id="rest"><div class="document">\n\n\n<p>Hallo Welt'
                   '</p>\n</div></div id="rest">',
            'en': u'<div id="rest"><div class="document">\n\n\n<p>Hello world'
                   '</p>\n</div></div id="rest">'}


def test_suite():
    suite = unittest.TestSuite()
    # Register local test cases...
    for testcase in [
        ReST2HTMLTestCase,
        FactoryBaseTestCase,
        CopyFileSystemTreeTestCase,
        RemoveFileOrDirectoryTestCase,
        CurrentPrincipalTestCase,
        CmpFilesTestCase,
        FileSizeTestCase,
        IfaceNamesTestCase,
        DateTimeHelpersTestCase,
        GetFileFormatTestCase,
        MergeCSVFileTestCase,
        SimpleHelpersTestCase,
        CheckCSVCharsetTestCase,
        MemInfoTestCase,
        GetMemInfoTestCase,
        Html2dictTestCase,
        Rest2dictTestCase,
        ]:
        suite.addTests(
            unittest.TestLoader().loadTestsFromTestCase(testcase)
            )
    # Add tests from docstrings in helpers.py...
    suite.addTests(
        doctest.DocTestSuite(
            helpers,
            optionflags = doctest.ELLIPSIS + doctest.REPORT_NDIFF,
            )
        )
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
