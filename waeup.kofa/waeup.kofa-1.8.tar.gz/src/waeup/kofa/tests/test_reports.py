import datetime
import grok
import logging
import pytz
import unittest
from cStringIO import StringIO
from grok.interfaces import IContainer
from zc.async.interfaces import IJob
from zc.async.testing import wait_for_result
from zope.component import getGlobalSiteManager, getUtility
from zope.component.hooks import setSite
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.interfaces import IJobManager, IKofaPluggable
from waeup.kofa.reports import (
    IReport, IReportGenerator, IReportJob, IReportJobContainer,
    IReportsContainer,)
from waeup.kofa.reports import (
    Report, ReportGenerator, get_generators, report_job, AsyncReportJob,
    ReportJobContainer, ReportsContainer, ReportsContainerPlugin)
from waeup.kofa.testing import FakeJob, FakeJobManager, FunctionalLayer
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase

class FakeReportGenerator(ReportGenerator):
    # fake report generator for tests.

    def __init__(self, name=None, perm_create=None, perm_view=None):
        self.title = 'Report 1'
        self.perm_create = perm_create
        self.perm_view = perm_view
        return

    def __eq__(self, obj):
        if getattr(obj, 'title', None) is None:
            return False
        return self.title == obj.title

    def generate(self, site, args=[], kw={}):
        result = Report()
        result.args = args
        result.kw = kw
        return result

class ReportTests(unittest.TestCase):

    def test_iface(self):
        # make sure we fullfill the promised contracts
        obj = Report()
        verifyClass(IReport, Report)
        verifyObject(IReport, obj)
        return

    def test_creation_dt(self):
        # a report sets a datetime timestamp when created
        report = Report()
        self.assertTrue(hasattr(report, 'creation_dt'))
        self.assertTrue(isinstance(report.creation_dt, datetime.datetime))
        # the datetime is set with UTC timezone info
        self.assertEqual(report.creation_dt.tzinfo, pytz.utc)
        return

    def test_args(self):
        # a report stores the args and kw used for generation
        report1 = Report()
        report2 = Report(args=[1, 2], kwargs=dict(a=1, b=2))
        self.assertEqual(report1.args, [])
        self.assertEqual(report1.kwargs, dict())
        self.assertEqual(report2.args, [1, 2])
        self.assertEqual(report2.kwargs, dict(a=1, b=2))
        return

    def test_create_pdf(self):
        # trying to create a pdf results in an error
        report = Report()
        self.assertRaises(NotImplementedError, report.create_pdf, 'JOB_ID')
        return

class ReportGeneratorTest(unittest.TestCase):
    def setUp(self):
        grok.testing.grok('waeup.kofa.reports') # register utils

    def test_iface(self):
        # make sure we fullfill the promised contracts
        obj = ReportGenerator()
        verifyClass(IReportGenerator, ReportGenerator)
        verifyObject(IReportGenerator, obj)
        return

    def test_generate(self):
        # the base report generator delivers reports
        obj = ReportGenerator()
        result = obj.generate(None)
        self.assertTrue(IReport.providedBy(result))
        return

class GeneratorRegistrar(object):
    # Mix-in providing report generator registrations
    def setUp(self):
        self.registered = []

    def tearDown(self):
        # unregister any previously registered report types
        gsm = getGlobalSiteManager()
        for report, name in self.registered:
            gsm.unregisterUtility(report, IReportGenerator, name=name)
        return

    def register_generator(self, name, perm_create=None, perm_view=None):
        # helper to register report generators as utils
        gsm = getGlobalSiteManager()
        generator = FakeReportGenerator(name)
        gsm.registerUtility(generator, provided=IReportGenerator, name=name)
        self.registered.append((generator, name),)
        return generator

class HelpersTests(GeneratorRegistrar, unittest.TestCase):
    # Tests for helper functions

    def setUp(self):
        grok.testing.grok('waeup.kofa.reports') # register utils
        super(HelpersTests, self).setUp()
        return

    def test_get_generators_none(self):
        # we get no generators if none was registered
        result = list(get_generators())
        self.assertEqual(result, [])
        return

    def test_get_generators_simple(self):
        # we get a single generator if one is registered
        self.register_generator('report1')
        result = list(get_generators())
        self.assertEqual(
            result, [('report1', FakeReportGenerator('report1'))])
        return

    def test_get_generators_multiple(self):
        # we also get multiple generators if available
        self.register_generator('report1')
        self.register_generator('report2')
        result = list(get_generators())
        self.assertEqual(
            result,
            [(u'report1', FakeReportGenerator('report1')),
             (u'report2', FakeReportGenerator('report2'))])
        return


class ReportJobTests(FunctionalAsyncTestCase, GeneratorRegistrar):
    # Test asynchronous report functionality (simple cases)

    layer = FunctionalLayer

    def setUp(self):
        super(ReportJobTests, self).setUp()
        GeneratorRegistrar.setUp(self)
        self.root_folder = self.getRootFolder()

    def test_report_job_func(self):
        # the report_job func really creates reports...
        self.register_generator('report1')
        report = report_job(None, 'report1')
        self.assertTrue(IReport.providedBy(report))
        self.assertTrue(isinstance(report, Report))

    def test_report_job_interfaces(self):
        # the AsyncReportJob implements promised interfaces correctly...
        job = AsyncReportJob(None, None)
        verifyClass(IJob, AsyncReportJob)
        verifyObject(IJob, job)
        verifyClass(IReportJob, AsyncReportJob)
        verifyObject(IReportJob, job)
        return

    def test_finished(self):
        # AsyncReportJobs signal with a bool whether they`re  finished
        job = AsyncReportJob(self.root_folder, None)
        setSite(self.root_folder)
        self.assertEqual(job.finished, False)
        manager = getUtility(IJobManager)
        manager.put(job)
        wait_for_result(job)
        self.assertEqual(job.finished, True)
        return

    def test_failed_true(self):
        # We can test whether a job failed
        job = AsyncReportJob(self.root_folder, None) # no report generator
        setSite(self.root_folder)
        # while a job is not finished, `failed` is ``None``
        self.assertTrue(job.failed is None)
        manager = getUtility(IJobManager)
        manager.put(job)
        wait_for_result(job)
        # the finished job failed
        self.assertEqual(job.failed, True)
        return

    def test_failed_false(self):
        # We can test whether a job failed
        self.register_generator('report1')
        job = AsyncReportJob(self.root_folder, 'report1')
        setSite(self.root_folder)
        # while a job is not finished, `failed` is ``None``
        self.assertTrue(job.failed is None)
        manager = getUtility(IJobManager)
        manager.put(job)
        wait_for_result(job)
        # the finished job failed
        self.assertEqual(job.failed, False)
        return

class FakeJobWithResult(FakeJob):

    def __init__(self, args=[], kw={}):
        self.result = Report()
        self.result.args = args
        self.result.kw = kw
        return

class ReportJobContainerTests(unittest.TestCase):
    # Test ReportJobContainer

    def setUp(self):
        # register a suitable ICSVExporter as named utility
        self.generator = FakeReportGenerator('report1')
        self.job_manager = FakeJobManager()
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(
            self.generator, IReportGenerator, name='report1')
        self.gsm.registerUtility(
            self.job_manager, IJobManager)

    def tearDown(self):
        self.gsm.unregisterUtility(
            self.generator, IReportGenerator, name='report1')
        self.gsm.unregisterUtility(self.job_manager, IJobManager)

    def test_report_job_interfaces(self):
        # the ExportJobContainer implements promised interfaces correctly...
        container = ReportJobContainer()
        verifyClass(IReportJobContainer, ReportJobContainer)
        verifyObject(IReportJobContainer, container)
        return

    def test_start_report_job(self):
        # we can start jobs
        container = ReportJobContainer()
        container.start_report_job('report3', 'bob')
        result = self.job_manager._jobs.values()[0]
        self.assertTrue(IJob.providedBy(result))
        self.assertEqual(
            container.running_report_jobs,
            [('1', 'report3', 'bob')]
            )
        return

    def test_get_running_report_jobs_all(self):
        # we can get report jobs of all users
        container = ReportJobContainer()
        container.start_report_job('report3', 'bob')
        container.start_report_job('report3', 'alice')
        result = container.get_running_report_jobs()
        self.assertEqual(
            result,
            [('1', 'report3', 'bob'),
             ('2', 'report3', 'alice')]
            )
        return

    def test_get_running_report_jobs_user(self):
        # we can get the report jobs running for a certain user
        container = ReportJobContainer()
        container.start_report_job('report3', 'bob')
        container.start_report_job('report3', 'alice')
        result1 = container.get_running_report_jobs(user_id='alice')
        result2 = container.get_running_report_jobs(user_id='foo')
        self.assertEqual(
            result1, [('2', 'report3', 'alice')])
        self.assertEqual(
            result2, [])
        return

    def test_get_running_report_jobs_only_if_exist(self):
        # we get only jobs that are accessible through the job manager...
        container = ReportJobContainer()
        container.start_report_job('report3', 'bob')
        container.start_report_job('report3', 'bob')
        self.assertTrue(
            ('2', 'report3', 'bob') in container.running_report_jobs)
        # we remove the second entry from job manager
        del self.job_manager._jobs['2']
        result = container.get_running_report_jobs(user_id='bob')
        self.assertEqual(
            result, [('1', 'report3', 'bob')])
        self.assertTrue(
            ('2', 'report3', 'bob') not in container.running_report_jobs)
        return

    def test_get_report_job_status(self):
        # we can get the stati of jobs...
        container = ReportJobContainer()
        container.start_report_job('report1', 'alice')
        container.start_report_job('report1', 'bob')
        container.start_report_job('report1', 'bob')
        result = container.get_report_jobs_status(user_id='bob')
        # we'll get the raw value, a translation and the title of the
        # exporter
        self.assertEqual(
            result,
            [('new', u'new', u'Report 1'),
             ('completed', u'completed', u'Report 1')]
            )
        return

    def test_delete_report_entry(self):
        # we can remove report entries in local lists and the job
        # manager as well...
        container = ReportJobContainer()
        container.start_report_job('report3', 'bob')
        entry = container.running_report_jobs[0]
        container.delete_report_entry(entry)
        # both, running_report_jobs list and job manager are empty now
        self.assertEqual(
            container.running_report_jobs, [])
        self.assertEqual(
            self.job_manager._jobs, {})
        return

    def test_report_entry_from_job_id(self):
        # we can get an report entry for a job_id if the id exists
        container = ReportJobContainer()
        entry = ('4', 'report3', 'bob')
        container.running_report_jobs = [entry]
        fake_job = FakeJobWithResult()
        self.job_manager._jobs['4'] = fake_job
        result1 = container.report_entry_from_job_id(None)
        result2 = container.report_entry_from_job_id('4')
        result3 = container.report_entry_from_job_id('23')
        self.assertEqual(result1, None)
        self.assertEqual(result2, ('4', 'report3', 'bob'))
        self.assertEqual(result3, None)
        return


class ReportsContainerTests(unittest.TestCase):
    # Tests for ReportsContainer

    def test_iface(self):
        # ReportsContainers really provide the promised interfaces
        obj = ReportsContainer()
        verifyClass(IReportsContainer, ReportsContainer)
        verifyClass(IContainer, ReportsContainer)
        verifyObject(IReportsContainer, obj)
        verifyObject(IContainer, obj)
        return

class ReportsContainerPluginTests(unittest.TestCase):
    # Tests for ReportsContainerPlugin

    def create_logger(self):
        # create a logger suitable for local tests.
        test_logger = logging.getLogger('waeup.kofa.reports.testlogger')
        log = StringIO()
        handler = logging.StreamHandler(log)
        handler.setLevel(logging.DEBUG)
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.DEBUG)
        self.logger = test_logger
        self.log = log
        self.handler = handler
        return self.logger

    def remove_logger(self):
        del self.handler
        del self.logger
        del self.log
        pass

    def get_log(self):
        self.log.seek(0)
        return self.log.read()

    def setUp(self):
        self.create_logger()
        return

    def tearDown(self):
        self.remove_logger()
        return

    def test_iface(self):
        # make sure we fullfill the promised interfaces
        obj = ReportsContainerPlugin()
        verifyClass(IKofaPluggable, ReportsContainerPlugin)
        verifyObject(IKofaPluggable, obj)
        return

    def test_get_as_utility(self):
        # make sure we can get the plugin as utility
        grok.testing.grok('waeup.kofa.reports')
        util = getUtility(IKofaPluggable, name='reports')
        self.assertTrue(util is not None)
        return

    def test_update_no_container(self):
        # we can update an existing site
        fake_site = grok.Container()
        plugin = ReportsContainerPlugin()
        plugin.update(fake_site, 'app', self.logger)
        log = self.get_log()
        self.assertEqual(
            log, 'Added reports container for site "app"\n')
        self.assertTrue('reports' in fake_site.keys())
        self.assertTrue(IReportsContainer.providedBy(fake_site['reports']))
        return

    def test_update_uptodate_site(self):
        # we leave already existing reports containers in place
        fake_site = grok.Container()
        plugin = ReportsContainerPlugin()
        fake_site['reports'] = ReportsContainer()
        plugin.update(fake_site, 'app', self.logger)
        log = self.get_log()
        self.assertEqual(log, '') # no log message
        return

    def test_setup_new_site(self):
        # if we setup a site, we always install a fresh reports container
        fake_site = grok.Container()
        plugin = ReportsContainerPlugin()
        plugin.setup(fake_site, 'app', self.logger)
        log1 = self.get_log()
        result1 = fake_site.get('reports', None)
        plugin.setup(fake_site, 'app', self.logger) # replace old container
        log2 = self.get_log()
        result2 = fake_site.get('reports', None)
        self.assertTrue(result1 is not result2)
        self.assertEqual(log1,
                         'Added reports container for site "app"\n')
        self.assertEqual(log2,
                         'Added reports container for site "app"\n'
                         'Removed reports container for site "app"\n'
                         'Added reports container for site "app"\n')
        return
