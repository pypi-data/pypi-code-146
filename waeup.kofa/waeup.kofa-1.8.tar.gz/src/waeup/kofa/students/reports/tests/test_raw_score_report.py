import os
from zc.async.testing import wait_for_result
from zope.interface.verify import verifyClass, verifyObject
from zope.component import getUtility, createObject
from waeup.kofa.interfaces import IJobManager
from waeup.kofa.students.tests.test_catalog import CatalogTestSetup
from waeup.kofa.students.tests.test_browser import StudentsFullSetup
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.browser.tests.test_pdf import samples_dir
from waeup.kofa.students.reports.raw_score_report import (
    RawScoreReport, IRawScoreReport)


class RawScoreReportTests(CatalogTestSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(RawScoreReportTests, self).setUp()
        self.course = createObject('waeup.Course')
        self.course.code = 'Course1'
        self.course.credits = 25
        self.app['faculties']['fac1']['dep1'].courses.addCourse(
            self.course)
        self.app['faculties']['fac1']['dep1'].certificates[
            'CERT1'].addCertCourse(self.course, level=100)

    def test_iface(self):
        # ensure we fullfill interface contracts
        obj = RawScoreReport('fac1', 'dep1', 'CERT1', 2010, 100)
        verifyClass(IRawScoreReport, RawScoreReport)
        verifyObject(IRawScoreReport, obj)
        return

    def test_get_courses(self):
        # we can get a list with one course code
        rsr = RawScoreReport('fac1', 'dep1', 'CERT1', 2010, 100)
        result = rsr._get_courses('fac1', 'dep1', 'CERT1', 2010, 100)
        self.assertEqual(result, [self.certificate.values()[0]])
        self.assertEqual(
            result,
            [self.app['faculties']['fac1']['dep1'].certificates[
                'CERT1']['Course1_100']])
        return

    def test_get_students(self):
        # we can get a table with one student
        rsr = RawScoreReport('fac1', 'dep1', 'CERT1', 2010, 100)
        course_codes = rsr._get_courses('fac1', 'dep1', 'CERT1', 2010, 100)
        result = rsr._get_students(
            'fac1', 'dep1', 'CERT1', 2010, 100, course_codes)
        self.assertEqual(result,
            [(u'1234', u'Bob Tester', {'Course1': (70, 'A')})])
        self.student['studycourse']['100']['Course1'].score = None
        result = rsr._get_students(
            'fac1', 'dep1', 'CERT1', 2010, 100, course_codes)
        self.assertEqual(result,
            [(u'1234', u'Bob Tester', {'Course1': ('Nil', '')})])
        return

    def test_create_pdf(self):
        self.app['faculties']['fac1']['dep1'].certificates[
                'CERT1']['Course1_100'].course_category = 'xyz'
        self.course = createObject('waeup.Course')
        self.course.code = 'Course2'
        self.course.credits = 30
        self.app['faculties']['fac1']['dep1'].courses.addCourse(
            self.course)
        self.app['faculties']['fac1']['dep1'].certificates[
            'CERT1'].addCertCourse(self.course, level=100)
        studylevel = createObject('waeup.StudentStudyLevel')
        studylevel.level = 200
        studylevel.level_session = 2011
        self.student['studycourse']['200'] = studylevel
        ticket = createObject('waeup.CourseTicket')
        ticket.code = 'Course2'
        ticket.credits = 30
        ticket.score = 50
        ticket.ca = 10
        self.student['studycourse']['200']['Course2'] = ticket
        self.student.firstname = u'Osahenokese Tessy'
        self.student.lastname = u'Emwinyomwanru'
        report = RawScoreReport('fac1', 'dep1', 'CERT1', 2011, 200)
        result = report.create_pdf('JOB_ID')
        self.assertTrue(result.startswith('%PDF-'))
        path = os.path.join(samples_dir(), 'raw_score_report.pdf')
        open(path, 'wb').write(result)
        print "Sample raw_score_report.pdf written to %s" % path
        return
