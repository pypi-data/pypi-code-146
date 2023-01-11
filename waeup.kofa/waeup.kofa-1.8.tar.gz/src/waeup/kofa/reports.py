## $Id: reports.py 14373 2017-01-06 22:40:30Z henrik $
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
"""Components for report generation.
"""
import grok
import zc.async.interfaces
from persistent.list import PersistentList
from zope import schema
from zope.component import getUtility, getUtilitiesFor
from zope.component.hooks import setSite
from zope.interface import implementer
from zope.interface import Interface, Attribute
from waeup.kofa.async import AsyncJob
from waeup.kofa.interfaces import (
    IJobManager, JOB_STATUS_MAP, IKofaPluggable, IKofaObject)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.helpers import now

class IReport(Interface):
    """A report.
    """
    args = Attribute("""The args passed to constructor""")

    kwargs = Attribute("""The keywords passed to constructor""")

    creation_dt = Attribute(
        """Datetime when a report was created. The datetime should """
        """reflect the point of time when the data was fetched, """
        """not when any output was created.""")

    def create_pdf(job_id):
        """Generate a PDF copy.
        """

class IReportGenerator(IKofaObject):
    """A report generator.
    """
    title = Attribute("""Human readable description of report type.""")

    def generate(site, args=[], kw={}):
        """Generate a report.

        `args` and `kw` are the parameters needed to create a specific
        report (if any).
        """

class IReportJob(zc.async.interfaces.IJob):

    finished = schema.Bool(
        title = u'`True` if the job finished.`',
        default = False,
        )

    failed = schema.Bool(
        title = u"`True` iff the job finished and didn't provide a report.",
        default = None,
        )

    def __init__(site, generator_name):
        """Create a report job via generator."""

class IReportJobContainer(Interface):
    """A component that contains (maybe virtually) report jobs.
    """
    def start_report_job(report_generator_name, user_id, args=[], kw={}):
        """Start asynchronous report job.

        `report_generator_name`
            is the name of a report generator utility to be used.

        `user_id`
            is the ID of the user that triggers the report generation.

        `args` and `kw`
            args and keywords passed to the generators `generate()`
            method.

        The job_id is stored along with exporter name and user id in a
        persistent list.

        Returns the job ID of the job started.
        """

    def get_running_report_jobs(user_id=None):
        """Get report jobs for user with `user_id` as list of tuples.

        Each tuples holds ``<job_id>, <generator_name>, <user_id>`` in
        that order. The ``<generator_name>`` is the utility name of the
        used report generator.

        If `user_id` is ``None``, all running report jobs are returned.
        """

    def get_report_jobs_status(user_id=None):
        """Get running/completed report jobs for `user_id` as list of tuples.

        Each tuple holds ``<raw status>, <status translated>,
        <generator title>`` in that order, where ``<status
        translated>`` and ``<generator title>`` are translated strings
        representing the status of the job and the human readable
        title of the report generator used.
        """

    def delete_report_entry(entry):
        """Delete the report job denoted by `entry`.

        Removes `entry` from the local `running_report_jobs` list and
        also removes the regarding job via the local job manager.

        `entry` is a tuple ``(<job id>, <generator name>, <user id>)``
        as created by :meth:`start_report_job` or returned by
        :meth:`get_running_report_jobs`.
        """

    def report_entry_from_job_id(job_id):
        """Get entry tuple for `job_id`.

        Returns ``None`` if no such entry can be found.
        """

class IReportsContainer(grok.interfaces.IContainer, IReportJobContainer,
                        IKofaObject):
    """A grok container that holds report jobs.
    """

class HandleReports(grok.Permission):
    """The HandleReports permission allows to add any kind of report
    and to view and remove own reports, i.e. reports which were created by
    the logged-in user.
    """
    grok.name('waeup.handleReports')

class ManageReports(grok.Permission):
    """The ManageReports permission allows to view, add and remove also
    the reports of other users. It requires the permission to handle reports.
    """
    grok.name('waeup.manageReports')

class ReportsOfficer(grok.Role):
    """The Reports Officer has the permission to view, add and remove
    **own** reports.
    """
    grok.name('waeup.ReportsOfficer')
    grok.title(u'Reports Officer')
    grok.permissions('waeup.handleReports')

class ReportsManager(grok.Role):
    """The Reports Manager has the permission to view, add and remove
    **all** reports.
    """
    grok.name('waeup.ReportsManager')
    grok.title(u'Reports Manager')
    grok.permissions('waeup.handleReports', 'waeup.manageReports')

def get_generators():
    """Get available report generators.

    Returns an iterator of tuples ``<NAME, GENERATOR>`` with ``NAME``
    being the name under which the respective generator was
    registered.
    """
    for name, util in getUtilitiesFor(IReportGenerator):
        yield name, util
    pass

@implementer(IReport)
class Report(object):
    """A base for reports.
    """
    creation_dt = None

    def __init__(self, args=[], kwargs={}):
        self.args = args
        self.kwargs = kwargs
        self.creation_dt = now()

    def create_pdf(self, job_id):
        raise NotImplementedError()

@implementer(IReportGenerator)
class ReportGenerator(object):
    """A base for report generators.
    """
    title = _("Unnamed Report")

    def generate(self, site, args=[], kw={}):
        result = Report()
        return result

def report_job(site, generator_name, args=[], kw={}):
    """Get a generator and perform report creation.

    `site`
        is the site for which the report should be created.
    `generator_name`
        the global utility name under which the desired generator is
        registered.
    `args` and `kw`
        Arguments and keywords to be passed to the `generate()` method of
        the desired generator. While `args` should be a list, `kw` should
        be a dictionary.
    """
    setSite(site)
    generator = getUtility(IReportGenerator, name=generator_name)
    report = generator.generate(site, *args, **kw)
    return report

@implementer(IReportJob)
class AsyncReportJob(AsyncJob):
    """An IJob that creates reports.

    `AsyncReportJob` instances are regular `AsyncJob` instances with a
    different constructor API. Instead of a callable to execute, you
    must pass a `site`, some `generator_name`, and additional args and
    keywords to create a report.

    The real work is done when an instance of this class is put into a
    queue. See :mod:`waeup.kofa.async` to learn more about
    asynchronous jobs.

    The `generator_name` must be the name under which an IReportGenerator
    utility was registered with the ZCA.

    The `site` must be a valid site  or ``None``.

    The result of an `AsyncReportJob` is an IReport object.
    """
    def __init__(self, site, generator_name, args=[], kw={}):
        self._generator_name = generator_name
        super(AsyncReportJob, self).__init__(
            report_job, site, generator_name, args=args, kw=kw)

    @property
    def finished(self):
        """A job is marked `finished` if it is completed.

        Please note: a finished report job does not neccessarily
        provide an IReport result. See meth:`failed`.
        """
        return self.status == zc.async.interfaces.COMPLETED

    @property
    def failed(self):
        """A report job is marked failed iff it is finished and the
        result does not provide IReport.

        While a job is unfinished, the `failed` status is ``None``.

        Failed jobs normally provide a `traceback` to examine reasons.
        """
        if not self.finished:
            return None
        if not IReport.providedBy(getattr(self, 'result', None)):
            return True
        return False

@implementer(IReportJobContainer)
class ReportJobContainer(object):
    """A mix-in that provides functionality for asynchronous report jobs.
    """
    running_report_jobs = PersistentList()

    def start_report_job(self, generator_name, user_id, args=[], kw={}):
        """Start asynchronous export job.

        `generator_name`
            is the name of a report generator utility to be used.

        `user_id`
            is the ID of the user that triggers the report generation.

        `args` and `kw`
            args and keywords passed to the generators `generate()`
            method.

        The job_id is stored along with exporter name and user id in a
        persistent list.

        Returns the job ID of the job started, `None` if the job could
        not be started.
        """
        site = grok.getSite()
        manager = getUtility(IJobManager)
        job = AsyncReportJob(site, generator_name, args=args, kw=kw)
        job_id = manager.put(job)
        if job_id is not None:
            # Make sure that the persisted list is stored in ZODB
            self.running_report_jobs = PersistentList(self.running_report_jobs)
            self.running_report_jobs.append((job_id, generator_name, user_id),)
        return job_id

    def get_running_report_jobs(self, user_id=None):
        """Get report jobs for user with `user_id` as list of tuples.

        Each tuples holds ``<job_id>, <generator_name>, <user_id>`` in
        that order. The ``<generator_name>`` is the utility name of the
        used report generator.

        If `user_id` is ``None``, all running report jobs are returned.
        """
        entries = []
        to_delete = []
        manager = getUtility(IJobManager)
        for entry in self.running_report_jobs:
            if user_id is not None and entry[2] != user_id:
                continue
            if manager.get(entry[0]) is None:
                to_delete.append(entry)
                continue
            entries.append(entry)
        if to_delete:
            self.running_report_jobs = PersistentList(
                [x for x in self.running_report_jobs if x not in to_delete])
        return entries

    def get_report_jobs_status(self, user_id=None):
        """Get running/completed report jobs for `user_id` as list of tuples.

        Each tuple holds ``<raw status>, <status translated>,
        <generator title>`` in that order, where ``<status
        translated>`` and ``<generator title>`` are translated strings
        representing the status of the job and the human readable
        title of the report generator used.
        """
        entries = self.get_running_report_jobs(user_id)
        result = []
        manager = getUtility(IJobManager)
        for entry in entries:
            job = manager.get(entry[0])
            status, status_translated = JOB_STATUS_MAP[job.status]
            generator = getUtility(IReportGenerator, name=entry[1])
            generator_name = getattr(generator, 'title', 'unnamed')
            result.append((status, status_translated, generator_name))
        return result

    def delete_report_entry(self, entry):
        """Delete the report job denoted by `entry`.

        Removes `entry` from the local `running_report_jobs` list and
        also removes the regarding job via the local job manager.

        `entry` is a tuple ``(<job id>, <generator name>, <user id>)``
        as created by :meth:`start_report_job` or returned by
        :meth:`get_running_report_jobs`.
        """
        manager = getUtility(IJobManager)
        manager.remove(entry[0], self)
        new_entries = [x for x in self.running_report_jobs
                       if x != entry]
        self.running_report_jobs = PersistentList(new_entries)
        return

    def report_entry_from_job_id(self, job_id):
        """Get entry tuple for `job_id`.

        Returns ``None`` if no such entry can be found.
        """
        for entry in self.running_report_jobs:
            if entry[0] == job_id:
                return entry
        return None

@implementer(IReportsContainer)
class ReportsContainer(grok.Container, ReportJobContainer):
    """A container for reports.
    """

@implementer(IKofaPluggable)
class ReportsContainerPlugin(grok.GlobalUtility):
    """A plugin that updates sites to contain a reports container.
    """

    grok.name('reports')

    deprecated_attributes = []

    def setup(self, site, name, logger):
        """Add a reports container for `site`.

        If there is such an object already, we install a fresh one.
        """
        if site.get('reports', None) is not None:
            del site['reports']
            logger.info('Removed reports container for site "%s"' % name)
        return self.update(site, name, logger)

    def update(self, site, name, logger):
        """Install a reports container in `site`.

        If one exists already, do nothing.
        """
        if site.get('reports', None) is not None:
            return
        site['reports'] = ReportsContainer()
        logger.info('Added reports container for site "%s"' % name)
        return
