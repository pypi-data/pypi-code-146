import os
import shutil
import tempfile
import transaction
from zc.async.testing import wait_for_result
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.security.interfaces import Unauthorized
from zope.testbrowser.testing import Browser
from waeup.kofa.app import University
from waeup.kofa.async import AsyncJob, get_job_id
from waeup.kofa.interfaces import IJobManager
from waeup.kofa.testing import FunctionalLayer, expensive_actions
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase


def fake_get_export_jobs_status(user_id=None):
    return [('completed', 'Completed', 'my_exporter'), ]


def dummy_func():
    return 42


class AsyncBrowserTests(FunctionalAsyncTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(AsyncBrowserTests, self).setUp()
        self.workdir = tempfile.mkdtemp()
        self.storage = os.path.join(self.workdir, 'storage')
        os.mkdir(self.storage)
        app = University()
        app['datacenter'].setStoragePath(self.storage)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        # we add the site immediately after creation to the
        # ZODB. Catalogs and other local utilities are not setup
        # before that step.
        self.app = self.getRootFolder()['app']
        # Set site here. Some of the following setup code might need
        # to access grok.getSite() and should get our new app then
        setSite(app)
        self.browser = Browser()
        self.browser.handleErrors = False
        self.datacenter_path = 'http://localhost/app/datacenter'

    def tearDown(self):
        super(AsyncBrowserTests, self).tearDown()
        shutil.rmtree(self.workdir)


class JobViewTests(AsyncBrowserTests):
    # Tests for the view of single jobs
    overview_path = 'http://localhost/app/jobs'

    def setUp(self):
        super(JobViewTests, self).setUp()
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')

    def start_job(self):
        # helper that starts a job in background and returns the job
        manager = getUtility(IJobManager)
        job = AsyncJob(dummy_func)
        manager.put(job, site=self.getRootFolder())
        return job

    def test_get_job_view(self):
        # we can get a job on a view
        self.browser.open(self.overview_path)
        job = self.start_job()
        wait_for_result(job)
        self.browser.open(self.overview_path)
        job_id = get_job_id(job)
        link = self.browser.getLink(job_id)
        expected_url = 'http://localhost/app/jobs/%s' % job_id
        self.assertEqual(link.url, expected_url)
        link.click()
        self.assertEqual(self.browser.headers['status'], '200 Ok')
        return

    def test_anonymous_forbidden(self):
        # we need some permissions to get a job view
        transaction.commit()  # make sure the 'app' is stored in ZODB
        job = self.start_job()
        wait_for_result(job)
        job_id = get_job_id(job)
        link_url = 'http://localhost/app/jobs/%s' % job_id

        # get a new browser, where we're not authenticated
        browser = Browser()
        browser.handleErrors = False
        self.assertRaises(Unauthorized, browser.open, link_url)
        return


class JobOverviewTests(AsyncBrowserTests):
    # Tests for the job overview page of universities
    overview_path = 'http://localhost/app/jobs'

    def setUp(self):
        super(JobOverviewTests, self).setUp()
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')

    def start_job(self):
        # helper that start a job in background and returns the job
        manager = getUtility(IJobManager)
        job = AsyncJob(dummy_func)
        manager.put(job, site=self.getRootFolder())
        return job

    def test_job_high_load(self):
        # under high load, jobs won't start (None is returned then)
        manager = getUtility(IJobManager)
        job = AsyncJob(dummy_func)
        with expensive_actions() as utils:
            utils.expensive_actions_allowed = lambda: False
            result = manager.put(job, site=self.getRootFolder())
        self.assertTrue(result is None)

    def test_job_get(self):
        # we can get the overview page
        self.browser.open(self.overview_path)
        self.assertTrue("Running and Completed Jobs" in self.browser.contents)
        self.assertEqual(self.browser.headers['status'], '200 Ok')
        return

    def test_anonymous_forbidden(self):
        # anonymous user will be kept out
        browser = Browser()  # get a browser w/o credentials set
        browser.handleErrors = False
        self.assertRaises(Unauthorized, browser.open, self.overview_path)
        return

    def test_job_reload(self):
        # we can reload the overview page
        self.browser.open(self.overview_path)
        self.browser.getControl('reload').click()
        self.assertTrue("Running and Completed Jobs" in self.browser.contents)
        self.assertEqual(self.browser.headers['status'], '200 Ok')
        return

    def test_jobs_appear(self):
        # any job running will appear
        self.browser.open(self.overview_path)
        job = self.start_job()
        wait_for_result(job)
        self.browser.getControl('reload').click()
        self.assertEqual(self.browser.headers['status'], '200 Ok')
        self.assertTrue('status: Completed' in self.browser.contents)
        return

    def test_job_removal(self):
        # we can remove jobs via the overview page
        self.browser.open(self.overview_path)
        job = self.start_job()
        wait_for_result(job)
        self.browser.getControl('reload').click()
        self.assertEqual(len(list(getUtility(IJobManager).jobs())), 1)
        self.browser.getControl('Remove').click()
        self.assertEqual(self.browser.headers['status'], '200 Ok')
        self.assertTrue('Removed job' in self.browser.contents)
        self.assertEqual(len(list(getUtility(IJobManager).jobs())), 0)
        return


class DataCenterJSONTests(AsyncBrowserTests):

    def test_status_plain(self):
        # if no job was triggered, no need to update something.
        path = '%s/status' % self.datacenter_path
        self.browser.open(path)
        self.assertEqual(self.browser.headers['content-type'],
                         'application/json')
        self.assertEqual(self.browser.contents,
                         '{"reload": false, "interval": 0, "html": ""}')
        return

    def test_status_completed(self):
        # if all jobs are completed, we should reload the page
        self.app[
            'datacenter'].get_export_jobs_status = fake_get_export_jobs_status
        path = '%s/status' % self.datacenter_path
        self.browser.open(path)
        self.assertEqual(self.browser.contents,
                         '{"reload": true, "interval": 0, "html": ""}')
        return
