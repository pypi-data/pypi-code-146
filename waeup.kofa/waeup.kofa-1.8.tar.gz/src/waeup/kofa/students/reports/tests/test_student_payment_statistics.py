# Tests for student related reports
import os
from zc.async.testing import wait_for_result
from zope.interface.verify import verifyClass, verifyObject
from zope.component import getUtility
from waeup.kofa.interfaces import IJobManager
from waeup.kofa.students.reports.student_payment_statistics import (
    get_student_payment_stats,
    StudentPaymentStatisticsReport,
    IStudentPaymentStatisticsReport)
from waeup.kofa.students.tests.test_catalog import CatalogTestSetup
from waeup.kofa.students.tests.test_browser import StudentsFullSetup
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase
from waeup.kofa.browser.tests.test_pdf import samples_dir

class StudentPaymentStatisticsReportTests(CatalogTestSetup):

    layer = FunctionalLayer

    def test_iface(self):
        # ensure we fullfill interface contracts
        obj = StudentPaymentStatisticsReport(
            2010, 'Undergraduate Full-Time', 0, 0, 0, 'faccode')
        verifyClass(IStudentPaymentStatisticsReport, StudentPaymentStatisticsReport)
        verifyObject(IStudentPaymentStatisticsReport, obj)
        return

    def test_get_student_payment_stats_session_simple(self):
        # we can get a table with one student
        result1 = get_student_payment_stats(
            2010, 'Undergraduate Full-Time', 0, 0, 0, 'faccode')
        result2 = get_student_payment_stats(
            2009, 'Undergraduate Full-Time', 0, 0, 0, 'faccode')
        self.assertEqual(
            result1,
            ((u'fac1', u'Total'),
             ['Acceptance Fee', 'Gown Hire Fee',
              'Hostel Maintenance Fee', 'School Fee',
              'Total'],
              ((0, 0, 0, 0, 0, 0, 1, 12345.678, 1, 12345.678),
              (0, 0, 0, 0, 0, 0, 1, 12345.678, 1, 12345.678)))
            )
        self.assertEqual(
            result2,
            ((u'fac1', u'Total'),
             ['Acceptance Fee', 'Gown Hire Fee',
              'Hostel Maintenance Fee', 'School Fee',
              'Total'],
              ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
              (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
            )
        return

    def test_create_pdf_1(self):
        report = StudentPaymentStatisticsReport(
            2010, 'Undergraduate Full-Time', 0, 0, 0, 'faccode')
        result = report.create_pdf('JOB_ID')
        self.assertTrue(result.startswith('%PDF-'))
        path = os.path.join(samples_dir(), 'student_payment_statistics_faccode.pdf')
        open(path, 'wb').write(result)
        print "Sample PDF student_statistics_faccode.pdf written to %s" % path
        return

    def test_create_pdf_2(self):
        report = StudentPaymentStatisticsReport(
            2010, 'Undergraduate Full-Time', 0, 0, 0, 'depcode')
        result = report.create_pdf('JOB_ID')
        self.assertTrue(result.startswith('%PDF-'))
        path = os.path.join(samples_dir(), 'student_payment_statistics_depcode.pdf')
        open(path, 'wb').write(result)
        print "Sample PDF student_statistics_depcode.pdf written to %s" % path
        return

class StudentPaymentStatisticsReportUITests(StudentsFullSetup, FunctionalAsyncTestCase):

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
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/reports')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.getLink("Create new report").click()
        self.browser.getControl(name="generator").value = ['student_payment_stats']
        self.browser.getControl("Configure").click()
        self.browser.getControl(name="breakdown").value = ['depcode']
        self.browser.getControl(name="mode").value = ['All']
        self.browser.getControl(name="session").value = ['2004']
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
            'filename="StudentPaymentStatisticsReport_rno%s' % job_id in
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
            'INFO - zope.mgr - students.reports.student_payment_statistics.StudentPaymentStatisticsReportGeneratorPage - '
            'report %s created: Student Payment Statistics '
            '(session=2004, mode=All, level=0, entry_session=0, '
            'p_session=0, breakdown=depcode)'
            % job_id in logcontent
            )
        self.assertTrue(
            'INFO - zope.mgr - students.reports.student_payment_statistics.StudentPaymentStatisticsReportPDFView - '
            'report %s downloaded: StudentPaymentStatisticsReport_rno%s_'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'INFO - zope.mgr - browser.reports.ReportsContainerPage - '
            'report %s discarded' % job_id in logcontent
            )
        return
