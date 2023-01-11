import grok
from zc.async.interfaces import COMPLETED, NEW
from zope.interface import Interface
from waeup.kofa.async import IJob, IJobManager
from waeup.kofa.browser.layout import KofaPage
from waeup.kofa.interfaces import IKofaObject, IDataCenter
from waeup.kofa.interfaces import MessageFactory as _

grok.templatedir('templates')
grok.context(IKofaObject)

loadingbar_template = '''
<input id="status_url" type="hidden" name="status_url" value="%s" />
<div id="loadbar">%%s</div>
'''

class LoadingBar(grok.ViewletManager):
    grok.name('loadingbar')

class LoadingBarViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(LoadingBar)

    _running_exports = None

    def getRunningExports(self):
        """Returns running exports as list of tuples.

        Only exports triggered by the current user (identified by
        principal.id) are returned.

        Each tuple has the form (<STATUS>, <STATUS_TITLE>, <EXPORTER_NAME>).

        ``STATUS``:
           the status as machine readable string (something like
           ``'completed'``)

        ``STATUS_TITLE``:
           status of export as translated string.

        ``EXPORTER_NAME``:
           string representing the exporter title used when triggering
           the export job.
        """
        result = self.context.get_export_jobs_status(self.user_id)
        return result

    def update(self):
        self.user_id = self.request.principal.id
        self.exports = self.getRunningExports()
        self.uncompleted = [x for x in self.exports if x[0] != 'completed']

    def render(self):
        status_url = self.view.url('status')
        template = loadingbar_template % (status_url,)
        content = ''
        return template % content

class DataCenterJSON(grok.JSON):
    grok.context(IDataCenter)

    def status(self):
        """Get status of currently handled export jobs for users.

        The result is a set of valus useful for JavaScript handlers to
        update some page handling data center exports.

        Returns a mapping::

          {html=<string>, interval=<int>, reload=<bool>}

        where `html` is some HTML code that might be shown in a
        loading bar section.

        `interval` is the time in microseconds after which the loading
        bar should be reloaded (by a new JSON call). If the value is
        zero, then the loading bar should not be renewed and further
        JSON calls be canceled.

        `reload` is a hint to tell, whether the complete page should
        be reloaded or not. Reloading is neccessary, if the export
        file creation finished and download buttons or similar should
        appear.
        """
        user_id = self.request.principal.id
        jobs = self.context.get_export_jobs_status(user_id)
        uncompleted = [x for x in jobs if x[0] != 'completed']
        result = dict(
            html='', interval=0, reload=False)
        if len(uncompleted):
            html = '<em>%s</em>' % (_("Please wait..."),)
            result.update(interval=500, html=html)
        else:
            if len(jobs):
                result.update(reload=True)
        return result


class JobManagerView(KofaPage):
    """The main view for the job container.
    """
    grok.name('index.html')
    grok.context(IJobManager)
    grok.template('virtjobscontainerindex')
    grok.require('waeup.manageJobs')

    def jobs(self):
        for job_id, job in sorted(self.context.jobs(),
                                  cmp=lambda x, y: cmp(int(x[0]), int(y[0]))):
            link = self.url(self.context, job_id)
            removable = job.status in (COMPLETED, NEW)
            yield dict(
                job_id = job_id,
                job = job,
                link = link,
                status = job.status,
                begin_after = job.begin_after,
                begin_by = job.begin_by,
                annotations = '%r' % [
                    (x, y) for x, y in job.annotations.items()],
                removable = removable,
                failure = '%r' % getattr(job, 'traceback', None),
                )

    def update(self, START_NEW=None, REMOVE=None, job_id=None):
        if REMOVE and job_id:
            self.context.remove(job_id)
            self.flash('Removed job "%s"' % job_id)
        if START_NEW:
            self.context.start_test_job()                    #pragma NO COVER
            self.flash('Started new test job "%s"' % job_id) #pragma NO COVER
        return

class JobView(grok.View):
    grok.name('index.html')
    grok.context(IJob)
    grok.template('jobindex')
    grok.require('waeup.manageJobs')

    def percent(self):
        value = self.context.annotations.get('percent', None)
        if not value:
            return
        value = int(value+0.5)
        return min(value, 100)

    def update(self):
        pass
