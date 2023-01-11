# Tests for the async module of waeup.kofa
import os
import re
import shutil
import tempfile
import transaction
import zc.async.configure
import zc.async.ftesting
import zc.async.queue
from zc.async.interfaces import IJob
from ZODB import DB, FileStorage
from zope.component import getUtility, provideAdapter
from zope.component.hooks import setSite
from zope.container.interfaces import IContainer
from zope.interface import verify
from zope.site.folder import rootFolder
from zope.site.testing import createSiteManager
from waeup.kofa.interfaces import (
    WAEUP_KEY, IProgressable, IJobManager, IJobContainer
    )
from waeup.kofa.testing import FunctionalTestCase, FunctionalLayer
from waeup.kofa.async import (
    get_job_id, AsyncJob, ProgressableJob, JobManager, JobContainer,
    JobManagerTraverser, JobContainerInstaller,
    )

def fake_async_func1():
    return 23

def fake_async_func2():
    return 42

class FunctionalAsyncTestCase(FunctionalTestCase):
    """A functional test case that additionally sets up asynchronous
    machinery.

    These type of test case takes _much_ more time than regular
    functional tests! So, only use it if really neccessary.
    """

    def setUp(self):
        super(FunctionalAsyncTestCase, self).setUp()
        zc.async.configure.base()
        provideAdapter(zc.async.queue.getDefaultQueue)
        connection = self.getRootFolder()._p_jar
        zc.async.ftesting.setUp(connection=connection)
        return

    def tearDown(self):
        zc.async.ftesting.tearDown()
        super(FunctionalAsyncTestCase, self).tearDown()
        return

class CommonAsyncFunctionalTests(FunctionalTestCase):

    layer = FunctionalLayer

    def test_iface_async_job(self):
        # AsyncJob implements the promised interfaces
        job = AsyncJob(fake_async_func1)
        verify.verifyClass(IJob, AsyncJob)
        verify.verifyObject(IJob, job)
        return

    def test_iface_progressable_job(self):
        # ProgressableJob implements the promised interfaces
        job = ProgressableJob(fake_async_func1)
        verify.verifyClass(IJob, ProgressableJob)
        verify.verifyClass(IProgressable, ProgressableJob)
        verify.verifyObject(IJob, job)
        verify.verifyObject(IProgressable, job)
        return

    def test_get_job_id(self):
        # for persisted jobs we can get an oid as job id
        job = AsyncJob(fake_async_func1)
        self.getRootFolder()['myjob'] = job
        transaction.commit()
        oid = job.__repr__().split(' ')[2][:-1]
        result = get_job_id(job)
        self.assertEqual(result, oid)
        return

class JobContainerTests(FunctionalTestCase):

    layer = FunctionalLayer

    def test_iface_job_container(self):
        # JobContainers implement the promised interfaces
        container = JobContainer()
        verify.verifyClass(IContainer, JobContainer)
        verify.verifyObject(IContainer, container)
        verify.verifyClass(IJobContainer, JobContainer)
        verify.verifyObject(IJobContainer, container)
        return

class JobManagerTests(FunctionalAsyncTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(JobManagerTests, self).setUp()
        self.root_folder = self.getRootFolder()
        self.root = self.root_folder._p_jar.root()

    def set_site(self):
        # helper to set a site 'externally'.
        # This is a bit complicated under the given limited setup conditions.
        # Returns a persisted site.
        site = rootFolder()
        self.root_folder['application'] = site
        createSiteManager(site, setsite=True)
        transaction.commit()
        return site

    def test_iface_job_manager(self):
        # JobManager implements the promised interfaces
        manager = JobManager()
        verify.verifyClass(IJobManager, JobManager)
        verify.verifyObject(IJobManager, manager)
        return

    def test_get_job_manager_as_util(self):
        # we can get a job manager as global, unnamed utility
        manager = getUtility(IJobManager)
        self.assertTrue(isinstance(manager, JobManager))
        return

    def test_get_site_no_site(self):
        # if no site is around, we get a lookup error
        manager = getUtility(IJobManager)
        self.assertRaises(LookupError, manager._get_site, None)
        return

    def test_get_site_invalid_site(self):
        # if we pass an invalid site, we get a lookup error
        manager = getUtility(IJobManager)
        self.assertRaises(LookupError, manager._get_site, object())
        return

    def test_get_site_valid_site(self):
        # if we pass a valid site, that will be respected
        manager = getUtility(IJobManager)
        result = manager._get_site(self.root_folder)
        self.assertEqual(result, self.root_folder)
        return

    def test_get_site_ext_set_none_given(self):
        # with an externally set site we don't have to pass in a site
        manager = getUtility(IJobManager)
        site = self.set_site()
        result = manager._get_site(None)
        self.assertEqual(result, site)
        return

    def test_get_site_ext_set_valid_site(self):
        # with an externally set site we can pass in this site
        manager = getUtility(IJobManager)
        site = self.set_site()
        result = manager._get_site(site)
        self.assertEqual(result, site)
        return

    def test_get_site_ext_set_invalid_site(self):
        # with an externally set site we can pass in invalid sites
        manager = getUtility(IJobManager)
        site = self.set_site()
        result = manager._get_site(object())
        self.assertEqual(result, site)
        return

    def test_get_site_ext_set_valid_obj(self):
        # valid persisted objects override externally set sites
        manager = getUtility(IJobManager)
        site = self.set_site()
        result = manager._get_site(self.root_folder)
        self.assertEqual(result, self.root_folder)
        return

    def test_put(self):
        # we can put jobs into the manager
        myjob = AsyncJob(fake_async_func1)
        manager = getUtility(IJobManager)
        job_id = manager.put(myjob, site=self.root_folder)
        # the returned job_id should be a string with a bunch of numbers
        self.assertTrue(re.match('^\d+$', job_id))
        # the job is also in the (new) jobs container
        self.assertTrue(job_id in self.root[WAEUP_KEY].keys())
        # the job is really stored
        stored_job =self.root[WAEUP_KEY][job_id]
        self.assertEqual(myjob, stored_job)
        return

    def test_put_no_site(self):
        # if no site is around we cannot store jobs
        myjob = AsyncJob(fake_async_func1)
        manager = getUtility(IJobManager)
        self.assertRaises(LookupError, manager.put, myjob)
        return

    def test_get(self):
        # we can get a job back with a valid job_id
        manager = getUtility(IJobManager)
        myjob = AsyncJob(fake_async_func1)
        job_id = manager.put(myjob, site=self.root_folder)
        stored_job = manager.get(job_id, site=self.root_folder)
        self.assertEqual(myjob, stored_job)
        return

    def test_get_no_site(self):
        # if no site is around we cannot retrieve jobs
        manager = getUtility(IJobManager)
        self.assertRaises(LookupError, manager.get, 'some_id')
        return

    def test_get_invalid_jobid(self):
        # invalid job_ids will result in `None` (if site is valid)
        manager = getUtility(IJobManager)
        result = manager.get('not-a-valid-job-id', site=self.root_folder)
        self.assertEqual(result, None)
        return

    def test_jobs(self):
        # we can get all jobs contained
        manager = getUtility(IJobManager)
        myjob1 = AsyncJob(fake_async_func1)
        job_id1 = manager.put(myjob1, site=self.root_folder)
        myjob2 = AsyncJob(fake_async_func2)
        job_id2 = manager.put(myjob2, site=self.root_folder)
        result = sorted(list(manager.jobs(site=self.root_folder)))
        self.assertEqual(
            result,
            [(job_id1, myjob1), (job_id2, myjob2)]
            )
        return

    def test_remove(self):
        # we can remove jobs from the job container
        manager = getUtility(IJobManager)
        myjob = AsyncJob(fake_async_func1)
        job_id = manager.put(myjob, site=self.root_folder)
        container = self.root[WAEUP_KEY]
        self.assertEqual(len(container), 1)
        manager.remove(job_id, site=self.root_folder)
        self.assertEqual(len(container), 0)
        return

    def test_start_test_job(self):
        # we can start a test job
        manager = getUtility(IJobManager)
        job_id = manager.start_test_job(duration=1, site=self.root_folder)
        container = self.root[WAEUP_KEY]
        self.assertEqual(len(container), 1)
        self.assertTrue(job_id is not None)
        return

class JobManagerTraverserTests(FunctionalAsyncTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(JobManagerTraverserTests, self).setUp()
        self.root_folder = self.getRootFolder()
        self.root = self.root_folder._p_jar.root()
        self.manager = getUtility(IJobManager)
        setSite(self.getRootFolder())

    def tearDown(self):
        setSite(None)
        super(JobManagerTraverserTests, self).tearDown()

    def test_no_jobs(self):
        # the traverser returns None if no job is available
        traverser = JobManagerTraverser(self.manager, None)
        result = traverser.traverse('123')
        self.assertTrue(result is None)
        return

    def test_valid_job(self):
        # the traverser returns the appropriate job if available
        myjob = AsyncJob(fake_async_func1)
        job_id = self.manager.put(myjob, site=self.root_folder)
        traverser = JobManagerTraverser(self.manager, None)
        result = traverser.traverse(job_id)
        self.assertEqual(myjob, result)
        return

class FakeEvent(object):
    # A faked DatabaseOpenedEvent as triggered at instance startup.
    # The only attribute we need here is `database` which should
    # return a valid ZODB.

    _storage = None
    _db = None

    def __init__(self, workdir, db_name=None):
        # workdir is the place to create a ZODB in, db_name its name.
        self.workdir = workdir
        self.db_name = db_name

    @property
    def database(self):
        if self._storage is None:
            # storage not created yet. Do it now.
            path = os.path.join(self.workdir, 'testdb.fs')
            self._storage = FileStorage.FileStorage(path)
            self._db = DB(self._storage, database_name=self.db_name)
        return self._db

class FakeDB(object):

    closed = False

    def open(self, transaction_manager=None):
        return self

    def close(self):
        self.closed = True
        return

class JobContainerInstallerTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(JobContainerInstallerTests, self).setUp()
        # setup two ZODBs, one unnamed, one named...
        self.workdir1 = tempfile.mkdtemp()
        self.workdir2 = tempfile.mkdtemp()
        self.fake_event1 = FakeEvent(self.workdir1)
        self.fake_event2 = FakeEvent(self.workdir2, 'mytestdb')
        self.tm1 = transaction.TransactionManager()
        self.tm2 = transaction.TransactionManager()
        self.db1 = self.fake_event1.database
        self.db2 = self.fake_event2.database
        self.conn1 = self.db1.open(self.tm1)
        self.conn2 = self.db2.open(self.tm2)

    def tearDown(self):
        self.tm1.abort()
        self.tm2.abort()
        shutil.rmtree(self.workdir1)
        shutil.rmtree(self.workdir2)
        super(JobContainerInstallerTests, self).tearDown()

    def reopen(self):
        # reopen connections to the ZODBs (for retrieving fresh data)...
        self.conn1.close()
        self.conn2.close()
        self.conn1 = self.db1.open(self.tm1)
        self.conn2 = self.db2.open(self.tm2)
        return

    @property
    def root1(self):
        # get root of first (unnamed) database
        self.reopen()
        return self.conn1.root()

    @property
    def root2(self):
        # get root of second (named 'mytestdb') database
        self.reopen()
        return self.conn2.root()

    def test_new_container(self):
        # we can install a job container if none is available yet
        installer = JobContainerInstaller()
        self.assertTrue(WAEUP_KEY not in self.root1)
        installer(self.fake_event1)
        self.assertTrue(WAEUP_KEY in self.root1)
        self.assertTrue(IJobContainer.providedBy(self.root1[WAEUP_KEY]))
        return

    def test_existing_container(self):
        # we won't try to install a new container if one is already present
        installer = JobContainerInstaller()
        self.assertTrue(WAEUP_KEY not in self.root1)
        installer(self.fake_event1)
        self.assertTrue(WAEUP_KEY in self.root1)
        self.assertTrue(IJobContainer.providedBy(self.root1[WAEUP_KEY]))
        container = self.root1[WAEUP_KEY]
        installer(self.fake_event1)
        self.assertTrue(WAEUP_KEY in self.root1)
        self.assertTrue(self.root1[WAEUP_KEY] is container)
        return

    def test_named_db(self):
        # we can also install containers in named dbs
        installer = JobContainerInstaller(db_name='mytestdb')
        self.assertTrue(WAEUP_KEY not in self.root1)
        self.assertTrue(WAEUP_KEY not in self.root2)
        installer(self.fake_event2)
        # now the job container is in database2 (but not database1)
        self.assertTrue(WAEUP_KEY not in self.root1)
        self.assertTrue(WAEUP_KEY in self.root2)
        self.assertTrue(IJobContainer.providedBy(self.root2[WAEUP_KEY]))
        return

    def test_broken_db(self):
        # if writing to db fails, we close the connection anyway...
        installer = JobContainerInstaller()
        self.conn1.close()
        # create a fake db
        db = FakeDB()
        self.fake_event1._storage = 'dummy'
        self.fake_event1._db = db
        self.assertEqual(db.closed, False)
        self.assertRaises(AttributeError, installer, self.fake_event1)
        self.assertEqual(db.closed, True)
        return
