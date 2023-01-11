## $Id: test_batching.py 12516 2015-01-27 08:31:34Z henrik $
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
import doctest
import logging
import os
import shutil
import tempfile
import unittest
from zc.async.interfaces import IJob
from zope import schema
from zope.component import provideUtility, getGlobalSiteManager, getUtility
from zope.component.factory import Factory
from zope.component.hooks import clearSite, setSite
from zope.component.interfaces import IFactory
from zope.interface import Interface, implements, verify
from waeup.kofa.app import University
from waeup.kofa.interfaces import (
    ICSVExporter, IBatchProcessor, IExportJobContainer, IJobManager,
    IExportJob, IExportContainerFinder)
from waeup.kofa.testing import (
    FunctionalLayer, FunctionalTestCase, FakeJob, FakeJobManager)
from waeup.kofa.utils.batching import (
    ExporterBase, BatchProcessor, export_job, AsyncExportJob,
    ExportJobContainer, VirtualExportJobContainer, ExportContainerFinder)

optionflags = (
    doctest.REPORT_NDIFF + doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)


class ICave(Interface):
    """A cave."""
    id_num = schema.TextLine(
        title = u'internal id',
        default = u'default',
        required = True,
        readonly = True,
        )
    name = schema.TextLine(
        title = u'Cave name',
        default = u'Unnamed',
        required = True)
    dinoports = schema.Int(
        title = u'Number of DinoPorts (tm)',
        required = False,
        default = 1)
    owner = schema.TextLine(
        title = u'Owner name',
        required = True,
        missing_value = 'Fred Estates Inc.')
    taxpayer = schema.Bool(
        title = u'Payes taxes',
        required = True,
        default = False)

class Cave(object):
    implements(ICave)
    def __init__(self, name=u'Unnamed', dinoports=2,
                 owner='Fred Estates Inc.', taxpayer=False):
        self.name = name
        self.dinoports = 2
        self.owner = owner
        self.taxpayer = taxpayer

stoneville = dict

SAMPLE_DATA = """name,dinoports,owner,taxpayer
Barneys Home,2,Barney,1
Wilmas Asylum,1,Wilma,1
Freds Dinoburgers,10,Fred,0
Joeys Drive-in,110,Joey,0
"""

SAMPLE_FILTERED_DATA = """name,dinoports,owner,taxpayer
Barneys Home,2,Barney,1
Wilmas Asylum,1,Wilma,1
"""

class CaveProcessor(BatchProcessor):
    util_name = 'caveprocessor'
    name = 'Cave Processor'
    iface = ICave
    location_fields = ['name']
    factory_name = 'Lovely Cave'

    def parentsExist(self, row, site):
        return True

    def getParent(self, row, site):
        return stoneville

    def entryExists(self, row, site):
        return row['name'] in stoneville.keys()

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        return stoneville[row['name']]

    def delEntry(self, row, site):
        del stoneville[row['name']]

    def addEntry(self, obj, row, site):
        stoneville[row['name']] = obj

class BatchProcessorTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setupLogger(self):

        self.logger = logging.getLogger('stoneville')
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.logfile = os.path.join(self.workdir, 'stoneville.log')
        self.handler = logging.FileHandler(self.logfile, 'w')
        self.logger.addHandler(self.handler)

    def setUp(self):
        global stoneville
        super(BatchProcessorTests, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']

        self.workdir = tempfile.mkdtemp()
        factory = Factory(Cave)
        provideUtility(factory, IFactory, 'Lovely Cave')

        # Provide sample data
        self.newcomers_csv = os.path.join(self.workdir, 'newcomers.csv')
        open(self.newcomers_csv, 'wb').write(SAMPLE_DATA)
        self.setupLogger()
        self.stoneville = stoneville
        stoneville = dict()
        self.resultpath = None
        return

    def tearDown(self):
        super(BatchProcessorTests, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        self.logger.removeHandler(self.handler)
        clearSite()
        if not isinstance(self.resultpath, list):
            self.resultpath = [self.resultpath]
        for path in self.resultpath:
            if not isinstance(path, basestring):
                continue
            if not os.path.isdir(path):
                path = os.path.dirname(path)
            if os.path.exists(path):
                shutil.rmtree(path)
        return

    def test_iface(self):
        # make sure we fullfill interface contracts
        obj = BatchProcessor()
        verify.verifyClass(IBatchProcessor, BatchProcessor)
        verify.verifyObject(IBatchProcessor, obj)
        return

    def test_import(self):
        processor = CaveProcessor()
        result = processor.doImport(
            self.newcomers_csv,
            ['name', 'dinoports', 'owner', 'taxpayer'],
            mode='create', user='Bob', logger=self.logger)
        num_succ, num_fail, finished_path, failed_path = result
        self.resultpath = [finished_path, failed_path]
        assert num_succ == 4
        assert num_fail == 0
        assert finished_path.endswith('/newcomers.finished.csv')
        assert failed_path is None

    def test_import_stoneville(self):
        processor = CaveProcessor()
        result = processor.doImport(
            self.newcomers_csv,
            ['name', 'dinoports', 'owner', 'taxpayer'],
            mode='create', user='Bob', logger=self.logger)
        num_succ, num_fail, finished_path, failed_path = result
        self.resultpath = [finished_path, failed_path]
        assert len(self.stoneville) == 4
        self.assertEqual(
            sorted(self.stoneville.keys()),
            [u'Barneys Home', u'Freds Dinoburgers',
             u'Joeys Drive-in', u'Wilmas Asylum'])

    def test_import_correct_type(self):
        processor = CaveProcessor()
        result = processor.doImport(
            self.newcomers_csv,
            ['name', 'dinoports', 'owner', 'taxpayer'],
            mode='create', user='Bob', logger=self.logger)
        num_succ, num_fail, finished_path, failed_path = result
        self.resultpath = [finished_path, failed_path]
        assert isinstance(self.stoneville['Barneys Home'].dinoports, int)


    def test_log(self):
        """
           >>> print log_contents
           processed: /.../newcomers.csv, create mode, 4 lines (4 successful/ 0 failed), ... s (... s/item)

        """
        processor = CaveProcessor()
        result = processor.doImport(
            self.newcomers_csv,
            ['name', 'dinoports', 'owner', 'taxpayer'],
            mode='create', user='Bob', logger=self.logger)
        num_succ, num_fail, finished_path, failed_path = result
        self.resultpath = [finished_path, failed_path]
        log_contents = open(self.logfile, 'rb').read()
        doctest.run_docstring_examples(
            self.test_log, locals(), False, 'test_log', None, optionflags)
        return

class ExporterBaseTests(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.workfile = os.path.join(self.workdir, 'testfile.csv')
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_iface(self):
        # ExporterBase really implements the promised interface.
        obj = ExporterBase()
        verify.verifyClass(ICSVExporter, ExporterBase)
        verify.verifyObject(ICSVExporter, obj)
        return

    def test_unimplemented(self):
        # make sure the not implemented methods signal that.
        exporter = ExporterBase()
        self.assertRaises(NotImplementedError, exporter.export_all, None)
        self.assertRaises(NotImplementedError, exporter.export, None)
        return

    def test_mangle_value(self):
        # some basic types are mangled correctly
        exporter = ExporterBase()
        result1 = exporter.mangle_value(True, 'foo')
        result2 = exporter.mangle_value(False, 'foo')
        result3 = exporter.mangle_value('string', 'foo')
        result4 = exporter.mangle_value(u'string', 'foo')
        result5 = exporter.mangle_value(None, 'foo')
        result6 = exporter.mangle_value(datetime.date(2012, 4, 1), 'foo')
        result7 = exporter.mangle_value(
            datetime.datetime(2012, 4, 1, 12, 1, 1), 'foo')
        self.assertEqual(
            (result1, result2, result3, result4, result5),
            ('1', '0', u'string', u'string', ''))
        self.assertEqual(type(result3), type('string'))
        self.assertEqual(type(result4), type('string'))
        # dates are formatted with trailing hash
        self.assertEqual(result6, '2012-04-01#')
        # datetimes are formatted as yyyy-mm-dd hh:mm:ss
        self.assertEqual(result7, '2012-04-01 12:01:01#')
        return

    def test_get_csv_writer(self):
        # we can get a CSV writer to a memory file
        exporter = ExporterBase()
        writer, outfile = exporter.get_csv_writer()
        writer.writerow(dict(code='A', title='B', title_prefix='C'))
        outfile.seek(0)
        self.assertEqual(
            outfile.read(),
            'code,title,title_prefix\r\nA,B,C\r\n')
        return

    def test_get_csv_writer_with_file(self):
        # we can get CSV writer that writes to a real file
        exporter = ExporterBase()
        writer, outfile = exporter.get_csv_writer(filepath=self.workfile)
        writer.writerow(dict(code='A', title='B', title_prefix='C'))
        outfile.close()
        resultfile = open(self.workfile, 'rb')
        self.assertEqual(
            resultfile.read(),
            'code,title,title_prefix\r\nA,B,C\r\n')
        return

    def test_write_item(self):
        # we can write items to opened exporter files.
        exporter = ExporterBase()
        writer, outfile = exporter.get_csv_writer()
        class Sample(object):
            code = 'A'
            title = u'B'
            title_prefix = True
        exporter.write_item(Sample(), writer)
        outfile.seek(0)
        self.assertEqual(
            outfile.read(),
            'code,title,title_prefix\r\nA,B,1\r\n')
        return

    def test_close_outfile(self):
        # exporters can help to close outfiles.
        exporter = ExporterBase()
        writer, outfile = exporter.get_csv_writer()
        result = exporter.close_outfile(None, outfile)
        self.assertEqual(result, 'code,title,title_prefix\r\n')
        return

    def test_close_outfile_real(self):
        # we can also close outfiles in real files.
        exporter = ExporterBase()
        writer, outfile = exporter.get_csv_writer(filepath=self.workfile)
        result = exporter.close_outfile(self.workfile, outfile)
        self.assertEqual(result, None)
        return

    def test_export_filtered(self):
        # we can pass in positional and keyword args
        exporter = ExporterBase()
        self.assertRaises(NotImplementedError, exporter.export_filtered,
                          'foo', bar='bar')

    def test_export_selected(self):
        # we can pass in a list of identifiers
        exporter = ExporterBase()
        self.assertRaises(NotImplementedError, exporter.export_selected,
                          'foo', selected=[])
        return

class CaveExporter(ExporterBase):
    # A minimal fake exporter suitable to be called by export_jobs
    fields = ('name', 'dinoports', 'owner', 'taxpayer')
    title = u'Dummy cave exporter'

    def export_all(self, site, filepath=None):
        if filepath is None:
            return SAMPLE_DATA
        open(filepath, 'wb').write(SAMPLE_DATA)
        return

    def export_filtered(self, site, filepath=None, foo=None, bar=None):
        if foo or bar:
            open(filepath, 'wb').write(SAMPLE_FILTERED_DATA)
            return
        self.export_all(site, filepath=filepath)
        return

    def export_selected(self, site, filepath=None, selected=None):
        if selected:
            open(filepath, 'wb').write(SAMPLE_FILTERED_DATA)
            return
        self.export_all(site, filepath=filepath)
        return

class ExportJobTests(unittest.TestCase):
    # Test asynchronous export functionality (simple cases)

    def setUp(self):
        # register a suitable ICSVExporter as named utility
        self.exporter = CaveExporter()
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(
            self.exporter, ICSVExporter, name='cave_exporter')

    def tearDown(self):
        self.gsm.unregisterUtility(self.exporter)

    def test_export_job_func(self):
        # the export_job func does really export data...
        result_path = export_job(None, 'cave_exporter')
        self.assertTrue(os.path.isfile(result_path))
        contents = open(result_path, 'rb').read()
        shutil.rmtree(os.path.dirname(result_path))
        self.assertEqual(contents, SAMPLE_DATA)
        return

    def test_export_job_interfaces(self):
        # the AsyncExportJob implements promised interfaces correctly...
        job = AsyncExportJob(None, None)
        verify.verifyClass(IJob, AsyncExportJob)
        verify.verifyObject(IJob, job)
        verify.verifyClass(IExportJob, AsyncExportJob)
        verify.verifyObject(IExportJob, job)
        return

    def test_export_job_with_args(self):
        # we export filtered sets
        result_path = export_job(None, 'cave_exporter', foo='foo')
        contents = open(result_path, 'rb').read()
        shutil.rmtree(os.path.dirname(result_path))
        self.assertEqual(contents, SAMPLE_FILTERED_DATA)
        return

    def test_export_job_selected(self):
        # we export subsets
        result_path = export_job(None, 'cave_exporter', selected=['foo'])
        contents = open(result_path, 'rb').read()
        shutil.rmtree(os.path.dirname(result_path))
        self.assertEqual(contents, SAMPLE_FILTERED_DATA)
        return


class FakeJobWithResult(FakeJob):

    def __init__(self):
        self.dir_path = tempfile.mkdtemp()
        self.result = os.path.join(self.dir_path, 'fake.csv')
        open(self.result, 'wb').write('a fake result')
        return

class ExportJobContainerTests(unittest.TestCase):
    # Test ExportJobContainer

    TestedClass = ExportJobContainer

    def setUp(self):
        # register a suitable ICSVExporter as named utility
        self.exporter = CaveExporter()
        self.job_manager = FakeJobManager()
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(
            self.exporter, ICSVExporter, name='cave_exporter')
        self.gsm.registerUtility(
            self.job_manager, IJobManager)

    def tearDown(self):
        self.gsm.unregisterUtility(self.exporter)
        self.gsm.unregisterUtility(self.job_manager, IJobManager)

    def test_export_job_interfaces(self):
        # the ExportJobContainer implements promised interfaces correctly...
        container = self.TestedClass()
        verify.verifyClass(IExportJobContainer, self.TestedClass)
        verify.verifyObject(IExportJobContainer, container)
        return

    def test_start_export_job(self):
        # we can start jobs
        container = self.TestedClass()
        container.start_export_job('cave_exporter', 'bob')
        result = self.job_manager._jobs.values()[0]
        self.assertTrue(IJob.providedBy(result))
        self.assertEqual(
            container.running_exports,
            [('1', 'cave_exporter', 'bob')]
            )
        return

    def test_get_running_export_jobs_all(self):
        # we can get export jobs of all users
        container = self.TestedClass()
        container.start_export_job('cave_exporter', 'bob')
        container.start_export_job('cave_exporter', 'alice')
        result = container.get_running_export_jobs()
        self.assertEqual(
            result,
            [('1', 'cave_exporter', 'bob'),
             ('2', 'cave_exporter', 'alice')]
            )
        return

    def test_get_running_export_jobs_user(self):
        # we can get the export jobs running for a certain user
        container = self.TestedClass()
        container.start_export_job('cave_exporter', 'bob')
        container.start_export_job('cave_exporter', 'alice')
        result1 = container.get_running_export_jobs(user_id='alice')
        result2 = container.get_running_export_jobs(user_id='foo')
        self.assertEqual(
            result1, [('2', 'cave_exporter', 'alice')])
        self.assertEqual(
            result2, [])
        return

    def test_get_running_export_jobs_only_if_exist(self):
        # we get only jobs that are accessible through the job manager...
        container = self.TestedClass()
        container.start_export_job('cave_exporter', 'bob')
        container.start_export_job('cave_exporter', 'bob')
        self.assertTrue(
            ('2', 'cave_exporter', 'bob') in container.running_exports)
        # we remove the second entry from job manager
        del self.job_manager._jobs['2']
        result = container.get_running_export_jobs(user_id='bob')
        self.assertEqual(
            result, [('1', 'cave_exporter', 'bob')])
        self.assertTrue(
            ('2', 'cave_exporter', 'bob') not in container.running_exports)
        return

    def test_get_export_job_status(self):
        # we can get the stati of jobs...
        container = self.TestedClass()
        container.start_export_job('cave_exporter', 'alice')
        container.start_export_job('cave_exporter', 'bob')
        container.start_export_job('cave_exporter', 'bob')
        result = container.get_export_jobs_status(user_id='bob')
        # we'll get the raw value, a translation and the title of the
        # exporter
        self.assertEqual(
            result,
            [('new', u'new', u'Dummy cave exporter'),
             ('completed', u'completed', u'Dummy cave exporter')]
            )
        return

    def test_delete_export_entry(self):
        # we can remove export entries in local lists and the job
        # manager as well...
        container = self.TestedClass()
        container.start_export_job('cave_exporter', 'bob')
        entry = container.running_exports[0]
        container.delete_export_entry(entry)
        # both, running_exports list and job manager are empty now
        self.assertEqual(
            container.running_exports, [])
        self.assertEqual(
            self.job_manager._jobs, {})
        return

    def test_delete_export_entry_remove_file(self):
        # any result files of exports are deleted as well
        container = self.TestedClass()
        entry = ('4', 'cave_exporter', 'bob')
        container.running_exports = [entry]
        fake_job = FakeJobWithResult()
        self.job_manager._jobs['4'] = fake_job
        self.assertTrue(os.path.isfile(fake_job.result))
        container.delete_export_entry(entry)
        self.assertTrue(not os.path.exists(fake_job.result))
        return

    def test_entry_from_job_id(self):
        # we can get an entry for a job_id if the id exists
        container = self.TestedClass()
        entry = ('4', 'cave_exporter', 'bob')
        container.running_exports = [entry]
        fake_job = FakeJobWithResult()
        self.job_manager._jobs['4'] = fake_job
        result1 = container.entry_from_job_id(None)
        result2 = container.entry_from_job_id('4')
        result3 = container.entry_from_job_id('23')
        self.assertEqual(result1, None)
        self.assertEqual(result2, ('4', 'cave_exporter', 'bob'))
        self.assertEqual(result3, None)
        shutil.rmtree(fake_job.dir_path)
        return

class VirtualExportJobContainerTests(ExportJobContainerTests):
    # VirtualExportJobContainers should provide the
    # same functionality as regular ones.

    TestedClass = VirtualExportJobContainer

    def setUp(self):
        super(VirtualExportJobContainerTests, self).setUp()
        self.root_job_container = ExportJobContainer()
        def fake_finder():
            return self.root_job_container
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(fake_finder, IExportContainerFinder)
        return

class ExportContainerFinderTests(FunctionalTestCase):
    # Tests for export container finder.

    layer = FunctionalLayer

    def test_get_finder_as_util(self):
        # we can get a finder by utility lookup
        finder = getUtility(IExportContainerFinder)
        self.assertTrue(finder is not None)
        self.assertEqual(
            IExportContainerFinder.providedBy(finder),
            True)
        return

    def test_iface(self):
        # the finder complies with the promised interface
        finder = ExportContainerFinder()
        verify.verifyClass(IExportContainerFinder,
                           ExportContainerFinder)
        verify.verifyObject(IExportContainerFinder, finder)
        return

    def test_no_site(self):
        # a finder returns None if no site is available
        finder = ExportContainerFinder()
        self.assertEqual(
            finder(), None)
        return

    def test_active_site(self):
        # we get the datafinder if one is installed and site set
        self.getRootFolder()['app'] = University()
        finder = getUtility(IExportContainerFinder)
        setSite(self.getRootFolder()['app'])
        container = finder()
        self.assertTrue(container is not None)
        return

    def test_broken_site(self):
        # if the current site has no ExportContainer, we get None
        self.getRootFolder()['app'] = University()
        app = self.getRootFolder()['app']
        del app['datacenter'] # datacenter _is_ the export container
        setSite(app)
        finder = getUtility(IExportContainerFinder)
        container = finder()
        self.assertTrue(container is None)
        return
