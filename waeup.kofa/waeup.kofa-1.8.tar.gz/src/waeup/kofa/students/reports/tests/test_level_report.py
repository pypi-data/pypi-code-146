import os
from zc.async.testing import wait_for_result
from zope.event import notify
from zope.interface.verify import verifyClass, verifyObject
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.component import getUtility, createObject
from waeup.kofa.interfaces import IJobManager
from waeup.kofa.students.reports.level_report import (
    LevelReport, ILevelReport)
from waeup.kofa.students.tests.test_catalog import CatalogTestSetup
from waeup.kofa.students.tests.test_browser import StudentsFullSetup
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.authentication import LocalRoleSetEvent
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase
from waeup.kofa.browser.tests.test_pdf import samples_dir
from waeup.kofa.tests.test_authentication import SECRET

class LevelReportTests(CatalogTestSetup):

    layer = FunctionalLayer

    def test_iface(self):
        # ensure we fullfill interface contracts
        obj = LevelReport('fac1', 'dep1', 'CERT1', 2010, 100)
        verifyClass(ILevelReport, LevelReport)
        verifyObject(ILevelReport, obj)
        return

        # Credits counted (taken): 90
        # Credits passed: 60
        # Credits failed: 30
        # Credits registered (total_credits): 180
        # Course1 and Course3 are passed
        # Course2 is failed
        # Course4, Course5 and Course6 have not ben taken

    def _add_tickets(self):
        ticket = createObject('waeup.CourseTicket')
        ticket.code = 'Course2'
        ticket.credits = 30
        ticket.score = 30
        ticket.mandatory = True
        ticket.passmark = 40
        self.student['studycourse']['100']['Course2'] = ticket
        ticket = createObject('waeup.CourseTicket')
        ticket.code = 'Course3'
        ticket.credits = 30
        ticket.score = 30
        ticket.mandatory = False
        ticket.passmark = 40
        self.student['studycourse']['100']['Course3'] = ticket
        ticket = createObject('waeup.CourseTicket')
        ticket.code = 'Course4'
        ticket.credits = 30
        ticket.mandatory = False
        ticket.passmark = 40
        self.student['studycourse']['100']['Course4'] = ticket
        ticket = createObject('waeup.CourseTicket')
        ticket.code = 'Course5'
        ticket.credits = 30
        self.student['studycourse']['100']['Course5'] = ticket
        ticket = createObject('waeup.CourseTicket')
        ticket.code = 'Course6'
        ticket.credits = 30
        self.student['studycourse']['100']['Course6'] = ticket
        return

    def test_get_students(self):
        self._add_tickets()
         # we can get a table with one student
        lr =  LevelReport('fac1', 'dep1', 'CERT1', 2010, 100)
        result = lr._get_students('fac1', 'dep1', 'CERT1', 2010, 100)
        self.assertEqual(result,
            [(u'1234', u'Bob Tester', 90, 30, '1.666',
            'm_Course2_m Course3', 'Course4 Course5\nCourse6',
            90, 30, '1.666', '')])
        # same result when selecting all certificates
        result = lr._get_students('fac1', 'dep1', 'all', 2010, 100)
        self.assertEqual(result,
            [(u'1234', u'Bob Tester', 90, 30, '1.666',
            'm_Course2_m Course3', 'Course4 Course5\nCourse6',
            90, 30, '1.666', '')])
        return

    def test_create_pdf(self):
        self.student.firstname = u'Johnathan Emmanuel Amenaghawon'
        self.student.lastname = u'Ehissouria'
        self.student['studycourse']['100']['Course1'].passmark = 40
        self._add_tickets()
        report = LevelReport('fac1', 'dep1', 'all', 2010, 100)
        result = report.create_pdf('JOB_ID')
        self.assertTrue(result.startswith('%PDF-'))
        path = os.path.join(samples_dir(), 'level_report.pdf')
        open(path, 'wb').write(result)
        print "Sample level_report.pdf written to %s" % path
        return

class LevelReportUITests(StudentsFullSetup, FunctionalAsyncTestCase):

    layer = FunctionalLayer

    def wait_for_report_job_completed(self):
        # helper function waiting until the current export job is completed
        manager = getUtility(IJobManager)
        job_id = self.app['reports'].running_report_jobs[0][0]
        job = manager.get(job_id)
        wait_for_result(job)
        return job_id

    def stored_in_reports(self, job_id):
        # tell whether job_id is stored in reports's running jobs list
        for entry in list(self.app['reports'].running_report_jobs):
            if entry[0] == job_id:
                return True
        return False

    def trigger_report_creation(self):
        #self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        # Create reports officer
        self.app['users'].addUser('mrreport', SECRET)
        self.app['users']['mrreport'].email = 'mrreport@foo.ng'
        self.app['users']['mrreport'].title = 'Carlo Pitter'
        # Assign global reports officer role
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.ReportsOfficer', 'mrreport')
        # Assign local ReportsOfficer role which restricts the access to
        # certain faculties.
        self.department = self.app['faculties']['fac1']['dep1']
        prmlocal = IPrincipalRoleManager(self.department)
        prmlocal.assignRoleToPrincipal(
            'waeup.local.ReportsOfficer', 'mrreport')
        notify(LocalRoleSetEvent(
            self.department, 'waeup.local.ReportsOfficer', 'mrreport',
            granted=True))
        # Login as reports officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrreport'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.browser.open('http://localhost/app/reports')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.getLink("Create new report").click()
        self.browser.getControl(name="generator").value = ['level_report']
        self.browser.getControl("Configure").click()
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl(name="session").value = ['2010']
        self.browser.getControl(name="faccode_depcode_certcode").value = [
            'fac1_dep1_CERT1']
        self.browser.getControl("Create").click()
        return

    def test_report_download(self):
        # We can download a generated report
        self.trigger_report_creation()
        # When the job is finished and we reload the page...
        job_id = self.wait_for_report_job_completed()
        self.browser.open('http://localhost/app/reports')
        # ... the pdf file can be downloaded ...
        self.browser.getControl("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
                         'application/pdf')
        self.assertTrue(
            'filename="LevelReport_rno%s' % job_id in
            self.browser.headers['content-disposition'])
        self.assertEqual(len(self.app['reports'].running_report_jobs), 1)
        # ... and discarded
        self.browser.open('http://localhost/app/reports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['reports'].running_report_jobs), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'INFO - mrreport - students.reports.level_report.LevelReportGeneratorPage - '
            'report %s created: Level Report (faculty=fac1, department=dep1, '
            'certificate=CERT1, session=2010, level=100)'
            % job_id in logcontent
            )
        self.assertTrue(
            'INFO - mrreport - students.reports.level_report.LevelReportPDFView - '
            'report %s downloaded: LevelReport_rno%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'INFO - mrreport - browser.reports.ReportsContainerPage - '
            'report %s discarded' % job_id in logcontent
            )
        return