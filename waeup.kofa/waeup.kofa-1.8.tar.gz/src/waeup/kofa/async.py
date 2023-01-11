## $Id: async.py 12581 2015-02-10 14:13:17Z uli $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
"""Components for asynchronous job (task) handling, mainly based on
:mod:`zc.async`.
"""
import grok
import time
import transaction
import zc.async.dispatcher
import zc.async.utils
import zope.component
from zc.async.job import Job as AsyncJob
from zc.async.queue import getDefaultQueue
from zc.async.interfaces import IJob, ObjectAdded
from ZODB.utils import u64
from zope.component import getUtility, adapter
from zope.component.hooks import getSite
from zope.event import notify
from waeup.kofa.interfaces import (
    IJobManager, IProgressable, IJobContainer, WAEUP_KEY, IKofaUtils,
    )


def compute(num, duration=60):
    """A convenience function to test asynchronous jobs.

    `duration` gives the seconds, this job should (artificially) need
    for completing.
    """
    start = time.time()
    end = start + duration
    print "MyJob starts computation at ", start
    myjob = zc.async.local.getJob()
    print "MyJob's job: ", zc.async.local.getJob()
    print "MyJob's queue: ", zc.async.local.getQueue(), list(
        zc.async.local.getQueue())
    while True:
        if time.time() > end:
            break
        time.sleep(1)
        percent = (time.time() - start) * 100.0 / duration
        if percent > 100.0:
            percent = 100.0
        print "MyJob percent: ", percent
        zc.async.local.setLiveAnnotation('percent', percent)
        print "MyJob does something at %s of %s" % (
            time.time() - start, duration)
        print "MyJob's annotations: %r" % dict(myjob.annotations)
        print "MyJob's percent: %r" % zc.async.local.getLiveAnnotation(
            'percent')
    zc.async.local.setLiveAnnotation('percent', 100.0)
    return num * 2

#
# Content components
#
class ProgressableJob(AsyncJob):
    """A job that can indicate its progress via a `percent` attribute.
    """
    grok.implements(IJob, IProgressable)
    grok.provides(IJob)
    percent = None


def get_job_id(persisted_job):
    """Get the object id of an already persisted job.

    The `persisted_job` must provide a `_p_oid` attribute.
    """
    job_id = u64(persisted_job._p_oid)
    return "%s" % job_id

class JobContainer(grok.Container):
    """A container for :class:`IKofa` jobs.
    """
    grok.implements(IJobContainer)


class JobManager(grok.GlobalUtility):
    """A manager for asynchronous running jobs (tasks).

    Registered as a global utility for the
    `waeup.kofa.interfaces.IJobManager` interface.

    This is the central location for managing asynchronous running
    jobs/tasks.

    It works roughly like this: for usual tasks it looks up some
    JobContainer installed in a ZODB database root (the installation
    can happen during startup; see the respective installer classes
    and functions in this module) and then interacts with this
    JobContainer.

    The optional `site` parameter for most methods in here serves for
    finding the databases' roots. It is sufficient to pass any
    persisted object (or more precisely: some object with a valid
    ``_p_jar__`` attribte). As long as some site was already set (for
    instance during regular requests), the site is looked up
    automatically and you don't have to pass the `site` parameter
    then. So, in most cases you won't have to give a `site` parameter.
    """
    grok.implements(IJobManager)
    grok.provides(IJobManager)

    def _get_site(self, site):
        # in fact we get some persisted object if available.
        # As sites are normally persisted and easy to lookup, we use them
        # to get _some_ persisted object.
        if not hasattr(site, '_p_jar'):
            site = getSite()
            if site is None:
                raise LookupError('cannot find a valid site')
        return site

    def _get_jobs_container(self, site):
        # in fact we need _some_ persisted object, not necessarily a site
        return site._p_jar.root()[WAEUP_KEY]

    def put(self, job, site=None):
        """Start the `job` and store it in local `site`.

        The `job` must be an `IJob` instance.

        It will be put into the default queue and then stored in local
        site. The status of the job can be seen immediately in
        `job.status`.

        Please specify special treatments like `begin_after` or
        `begin_by` by setting the respectives attributes of the job
        itself.
        """
        site = self._get_site(site)
        if not getUtility(IKofaUtils).expensive_actions_allowed():
            return None
        container = self._get_jobs_container(site)
        transaction.begin()
        queue = getDefaultQueue(site)
        new_job = queue.put(job)
        job_id = get_job_id(new_job)
        container[job_id] = new_job
        transaction.commit()
        return job_id

    def get(self, job_id, site=None):
        """Get the job with `job_id` from local `site`.

        If `job_id` cannot be found, ``None`` is returned. This
        suitable e.g. when used with a traverser.
        """
        site = self._get_site(site)
        container = self._get_jobs_container(site)
        return container.get(job_id, None)

    def jobs(self, site=None):
        """Get all stored jobs as an iterable.

        Result provides tuples (JOB_ID, JOB_OBJECT).
        """
        site = self._get_site(site)
        container = self._get_jobs_container(site)
        for job_id, job in container.items():
            yield (job_id, job)

    def remove(self, job_id, site=None):
        """Remove job with `job_id` from local job container.

        If no such job can be found this is silently ignored.

        Please note: removing a job from the job container does not
        mean to stop its execution (if it wasn't started yet or is
        currently running).
        """
        site = self._get_site(site)
        container = self._get_jobs_container(site)
        if job_id in container.keys():
            del container[job_id]
        return

    def start_test_job(self, duration=60, site=None):
        """Start a test job.

        A method for testing the general asynchronous functionality of
        waeup.kofa. The test job started here executes the local
        :func:`compute` function with ``23`` as argument.
        """
        job = AsyncJob(compute, 23, duration)
        job_id = self.put(job, site=site)
        return job_id

class JobManagerTraverser(grok.Traverser):
    """A traverser for the global ``IJobManager``.

    Looks up jobs by job_id and returns the respective job if it
    can be found.
    """
    grok.context(IJobManager)

    def traverse(self, name):
        # ``None`` if name cannot be found.
        return self.context.get(name)

##
## configuration (permissions, subscribers, etc.) ...
##

class ViewJobs(grok.Permission):
    grok.name('waeup.viewJobs')

class ManageJobs(grok.Permission):
    grok.name('waeup.manageJobs')

class JobContainerInstaller(object):
    """Install a JobContainer in root of given DB.

    Instances of this installer can be called when a Zope instance
    comes up (i.e. when an IDatabaseOpenedEvent was triggered).

    It looks for some database named as in `db_name` and installs a
    job container in the root of this database (``None`` by default)
    if it does not exist already.
    """
    def __init__(self, db_name=None):
        # This IDatabaseOpenedEvent will be from zope.app.appsetup if that
        # package is around
        adapter(zc.async.interfaces.IDatabaseOpenedEvent)(self)
        self.db_name = db_name
        return

    def __call__(self, ev):
        db = ev.database
        tm = transaction.TransactionManager()
        conn = db.open(transaction_manager=tm)
        tm.begin()
        try:
            try:
                root = conn.root()
                if WAEUP_KEY in root:
                    return
                if self.db_name is not None:
                    other = conn.get_connection(self.db_name)
                    container = other.root()[WAEUP_KEY] = JobContainer()
                    other.add(container)
                else:
                    container = JobContainer()
                root[WAEUP_KEY] = container
                notify(ObjectAdded(container, root, WAEUP_KEY))
                tm.commit()
                zc.async.utils.log.info('job container added')
            except:
                tm.abort()
                raise
        finally:
            conn.close()
        return

#: Can be used as event subscriber from ZCML; installs a job container
#: in default database (named ``''``) root.
job_container_installer = JobContainerInstaller()

#: An installer instance that installs a job container in a ZODB
#: called ``async`` - this name is used in several components of the
#: `zc.async` package we don't want to reimplement here.
#:
#: To use this installer as an event subscriber by ZCML, make sure the
#: instance provides also a ZODB called `async`.
multidb_job_container_installer = JobContainerInstaller(db_name='async')
