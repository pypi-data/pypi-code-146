# -*- coding: utf-8 -*-
## $Id: test_browser.py 17261 2023-01-09 21:16:28Z henrik $
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
"""
Test the student-related UI components.
"""
import shutil
import tempfile
import pytz
import base64
from datetime import datetime, timedelta, date
from StringIO import StringIO
import os
import grok
import logging
from zc.async.testing import wait_for_result
from zope.event import notify
from zope.component import createObject, queryUtility, getUtility
from zope.component.hooks import setSite, clearSite
from zope.catalog.interfaces import ICatalog
from zope.security.interfaces import Unauthorized
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.testbrowser.testing import Browser
from zope.interface import implementedBy
from zope.schema.fieldproperty import FieldProperty
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.app import University
from waeup.kofa.interfaces import IFileStoreNameChooser, IExtFileStore
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.students.payments import StudentOnlinePayment
from waeup.kofa.students.student import Student
from waeup.kofa.students.studylevel import StudentStudyLevel
from waeup.kofa.university.faculty import Faculty
from waeup.kofa.university.department import Department
from waeup.kofa.interfaces import IUserAccount, IJobManager, VALIDATED, CREATED
from waeup.kofa.authentication import LocalRoleSetEvent
from waeup.kofa.hostels.hostel import Hostel, Bed, NOT_OCCUPIED
from waeup.kofa.applicants.container import ApplicantsContainer
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase
from waeup.kofa.browser.tests.test_pdf import samples_dir
from waeup.kofa.tests.test_authentication import SECRET

PH_LEN = 15911  # Length of placeholder file

SAMPLE_IMAGE = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
SAMPLE_IMAGE_BMP = os.path.join(os.path.dirname(__file__), 'test_image.bmp')
URL_LECTURER_LANDING = 'http://localhost/app/my_courses'

curr_year = datetime.now().year

def lookup_submit_value(name, value, browser):
    """Find a button with a certain value."""
    for num in range(0, 100):
        try:
            button = browser.getControl(name=name, index=num)
            if button.value.endswith(value):
                return button
        except IndexError:
            break
    return None


class StudentsFullSetup(FunctionalTestCase):
    # A test case that only contains a setup and teardown
    #
    # Complete setup for students handlings is rather complex and
    # requires lots of things created before we can start. This is a
    # setup that does all this, creates a university, creates PINs,
    # etc.  so that we do not have to bother with that in different
    # test cases.

    layer = FunctionalLayer

    def setUp(self):
        super(StudentsFullSetup, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        # we add the site immediately after creation to the
        # ZODB. Catalogs and other local utilities are not setup
        # before that step.
        self.app = self.getRootFolder()['app']
        # Set site here. Some of the following setup code might need
        # to access grok.getSite() and should get our new app then
        setSite(app)

        # Add student with subobjects
        student = createObject('waeup.Student')
        student.firstname = u'Anna'
        student.lastname = u'Tester'
        student.reg_number = u'123'
        student.matric_number = u'234'
        student.sex = u'm'
        student.email = 'aa@aa.ng'
        student.phone = u'1234'
        student.date_of_birth = date(1981, 2, 4)
        self.app['students'].addStudent(student)
        self.student_id = student.student_id
        self.student = self.app['students'][self.student_id]

        # Set password
        IUserAccount(
            self.app['students'][self.student_id]).setPassword('spwd')

        self.login_path = 'http://localhost/app/login'
        self.container_path = 'http://localhost/app/students'
        self.manage_container_path = self.container_path + '/@@manage'
        self.add_student_path = self.container_path + '/addstudent'
        self.student_path = self.container_path + '/' + self.student_id
        self.manage_student_path = self.student_path + '/manage_base'
        self.trigtrans_path = self.student_path + '/trigtrans'
        self.clearance_path = self.student_path + '/view_clearance'
        self.personal_path = self.student_path + '/view_personal'
        self.edit_clearance_path = self.student_path + '/cedit'
        self.manage_clearance_path = self.student_path + '/manage_clearance'
        self.edit_personal_path = self.student_path + '/edit_personal'
        self.manage_personal_path = self.student_path + '/manage_personal'
        self.studycourse_path = self.student_path + '/studycourse'
        self.payments_path = self.student_path + '/payments'
        self.acco_path = self.student_path + '/accommodation'
        self.history_path = self.student_path + '/history'

        # Create 5 access codes with prefix'PWD'
        pin_container = self.app['accesscodes']
        pin_container.createBatch(
            datetime.utcnow(), 'some_userid', 'PWD', 9.99, 5)
        pins = pin_container['PWD-1'].values()
        self.pwdpins = [x.representation for x in pins]
        self.existing_pwdpin = self.pwdpins[0]
        parts = self.existing_pwdpin.split('-')[1:]
        self.existing_pwdseries, self.existing_pwdnumber = parts
        # Create 5 access codes with prefix 'CLR'
        pin_container.createBatch(
            datetime.now(), 'some_userid', 'CLR', 9.99, 5)
        pins = pin_container['CLR-1'].values()
        pins[0].owner = u'Hans Wurst'
        self.existing_clrac = pins[0]
        self.existing_clrpin = pins[0].representation
        parts = self.existing_clrpin.split('-')[1:]
        self.existing_clrseries, self.existing_clrnumber = parts
        # Create 2 access codes with prefix 'HOS'
        pin_container.createBatch(
            datetime.now(), 'some_userid', 'HOS', 9.99, 2)
        pins = pin_container['HOS-1'].values()
        self.existing_hosac = pins[0]
        self.existing_hospin = pins[0].representation
        parts = self.existing_hospin.split('-')[1:]
        self.existing_hosseries, self.existing_hosnumber = parts

        # Populate university
        self.certificate = createObject('waeup.Certificate')
        self.certificate.code = u'CERT1'
        self.certificate.application_category = 'basic'
        self.certificate.study_mode = 'ug_ft'
        self.certificate.start_level = 100
        self.certificate.end_level = 500
        self.certificate.school_fee_1 = 40000.0
        self.certificate.school_fee_2 = 20000.0
        self.app['faculties']['fac1'] = Faculty(code=u'fac1')
        self.app['faculties']['fac1']['dep1'] = Department(code=u'dep1')
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate)
        self.course = createObject('waeup.Course')
        self.course.code = 'COURSE1'
        self.course.semester = 1
        self.course.credits = 10
        self.course.passmark = 40
        self.app['faculties']['fac1']['dep1'].courses.addCourse(
            self.course)
        self.app['faculties']['fac1']['dep1'].certificates[
            'CERT1'].addCertCourse(self.course, level=100)

        # Configure university and hostels
        self.app['hostels'].accommodation_states = ['admitted']
        self.app['hostels'].accommodation_session = 2004
        delta = timedelta(days=10)
        self.app['hostels'].startdate = datetime.now(pytz.utc) - delta
        self.app['hostels'].enddate = datetime.now(pytz.utc) + delta
        self.app['configuration'].carry_over = True
        configuration = createObject('waeup.SessionConfiguration')
        configuration.academic_session = 2004
        configuration.clearance_fee = 3456.0
        configuration.transcript_fee = 4567.0
        configuration.booking_fee = 123.4
        configuration.maint_fee = 987.0
        configuration.transfer_fee = 456.0
        configuration.late_registration_fee = 345.0
        self.app['configuration'].addSessionConfiguration(configuration)

        # Create a hostel with two beds
        hostel = Hostel()
        hostel.hostel_id = u'hall-1'
        hostel.hostel_name = u'Hall 1'
        hostel.maint_fee = 876.0
        self.app['hostels'].addHostel(hostel)
        bed = Bed()
        bed.bed_id = u'hall-1_A_101_A'
        bed.bed_number = 1
        bed.owner = NOT_OCCUPIED
        bed.bed_type = u'regular_male_fr'
        self.app['hostels'][hostel.hostel_id].addBed(bed)
        bed = Bed()
        bed.bed_id = u'hall-1_A_101_B'
        bed.bed_number = 2
        bed.owner = NOT_OCCUPIED
        bed.bed_type = u'regular_female_fr'
        self.app['hostels'][hostel.hostel_id].addBed(bed)

        # Set study course attributes of test student
        self.student['studycourse'].certificate = self.certificate
        self.student['studycourse'].current_session = 2004
        self.student['studycourse'].entry_session = 2004
        self.student['studycourse'].current_verdict = 'A'
        self.student['studycourse'].current_level = 100
        # Update the catalog
        notify(grok.ObjectModifiedEvent(self.student))

        # Put the prepopulated site into test ZODB and prepare test
        # browser
        self.browser = Browser()
        self.browser.handleErrors = False

    def tearDown(self):
        super(StudentsFullSetup, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)


class StudentsContainerUITests(StudentsFullSetup):
    # Tests for StudentsContainer class views and pages

    layer = FunctionalLayer

    def setUp(self):
        super(StudentsContainerUITests, self).setUp()
        self.setup_logging()
        return

    def setup_logging(self):
        # setup a log-handler that catches all fake mailer output
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        logger = logging.getLogger('test.smtp')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return

    def get_fake_smtp_output(self):
        # get output generated by fake mailer
        self.stream.flush()
        self.stream.seek(0)
        return self.stream.read()

    def test_anonymous_access(self):
        # Anonymous users can't access students containers
        self.assertRaises(
            Unauthorized, self.browser.open, self.container_path)
        self.assertRaises(
            Unauthorized, self.browser.open, self.manage_container_path)
        return

    def test_manage_access(self):
        # Managers can access the view page of students
        # containers and can perform actions
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.container_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.container_path)
        self.browser.getLink("Manage students section").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.manage_container_path)
        return

    def test_add_search_delete_students(self):
        # Managers can add search and remove students
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_container_path)
        self.browser.getLink("Add student").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.add_student_path)
        self.browser.getControl(name="form.firstname").value = 'Bob'
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.reg_number").value = '123'
        self.browser.getControl("Create student").click()
        self.assertTrue(
            'Registration number exists already' in self.browser.contents)
        self.browser.getControl(name="form.reg_number").value = '1234'
        self.browser.getControl("Create student").click()
        self.assertTrue('Student record created' in self.browser.contents)

        # Registration and matric numbers must be unique
        self.browser.getLink("Manage").click()
        self.browser.getControl(name="form.reg_number").value = '123'
        self.browser.getControl("Save").click()
        self.assertMatches('...Registration number exists...',
                           self.browser.contents)
        self.browser.getControl(name="form.reg_number").value = '789'
        self.browser.getControl(name="form.matric_number").value = '234'
        self.browser.getControl("Save").click()
        self.assertMatches('...Matriculation number exists...',
                           self.browser.contents)

        # We can find a student with a certain student_id
        self.browser.open(self.container_path)
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Empty search string' in self.browser.contents)
        self.browser.getControl(name="searchtype").value = ['student_id']
        self.browser.getControl(name="searchterm").value = self.student_id
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)

        # We can find a student in a certain session
        self.browser.open(self.container_path)
        self.browser.getControl(name="searchtype").value = ['current_session']
        self.browser.getControl(name="searchterm").value = '2004'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        # Session fileds require integer values
        self.browser.open(self.container_path)
        self.browser.getControl(name="searchtype").value = ['current_session']
        self.browser.getControl(name="searchterm").value = '2004/2005'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Only year dates allowed' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['current_session']
        self.browser.getControl(name="searchterm").value = '2004/2005'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Only year dates allowed' in self.browser.contents)

        # We can find a student in a certain study_mode
        self.browser.open(self.container_path)
        self.browser.getControl(name="searchtype").value = ['current_mode']
        self.browser.getControl(name="searchterm").value = 'ug_ft'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)

        # We can find a student in a certain department
        self.browser.open(self.container_path)
        self.browser.getControl(name="searchtype").value = ['depcode']
        self.browser.getControl(name="searchterm").value = 'dep1'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)

        # We can find a student by searching for all kind of name parts
        self.browser.open(self.manage_container_path)
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Empty search string' in self.browser.contents)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'Anna Tester'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'Anna'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'Tester'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'An'
        self.browser.getControl("Find student(s)").click()
        self.assertFalse('Anna Tester' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'An*'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'tester'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'Tester Ana'
        self.browser.getControl("Find student(s)").click()
        self.assertFalse('Anna Tester' in self.browser.contents)
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'Tester Anna'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        # The old searchterm will be used again
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)

        # We can find suspended students
        self.student.suspended = True
        notify(grok.ObjectModifiedEvent(self.student))
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['suspended']
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.browser.open(self.container_path)
        self.browser.getControl(name="searchtype").value = ['suspended']
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)

        # The catalog is informed when studycourse objects have been
        # edited
        self.browser.open(self.studycourse_path + '/manage')
        self.browser.getControl(name="form.current_session").value = ['2010']
        self.browser.getControl(name="form.entry_session").value = ['2010']
        self.browser.getControl(name="form.entry_mode").value = ['ug_ft']
        self.browser.getControl("Save").click()

        # We can find the student in the new session
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['current_session']
        self.browser.getControl(name="searchterm").value = '2010'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)

        ctrl = self.browser.getControl(name='entries')
        ctrl.getControl(value=self.student_id).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)
        self.browser.getControl(name="searchtype").value = ['student_id']
        self.browser.getControl(name="searchterm").value = self.student_id
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('No student found' in self.browser.contents)

        self.browser.open(self.container_path)
        self.browser.getControl(name="searchtype").value = ['student_id']
        self.browser.getControl(name="searchterm").value = self.student_id
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('No student found' in self.browser.contents)
        return

    def test_send_bulk_emails(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_container_path)
        self.browser.getLink("Add student").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.add_student_path)
        self.browser.getControl(name="form.firstname").value = 'Bob'
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.reg_number").value = '1234'
        self.browser.getControl("Create student").click()
        self.assertTrue('Student record created' in self.browser.contents)
        self.browser.getLink("Manage").click()
        self.browser.getControl(name="form.email").value = 'uli@uni.ng'
        self.browser.getControl(name="form.sex").value = ['m']
        self.browser.getControl("Save").click()
        # We can find Anna and Bob
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['student_id']
        self.browser.getControl(name="searchterm").value = '*'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.assertTrue('Bob Tester' in self.browser.contents)
        # We can send bulk emails
        ctrl = self.browser.getControl(name='entries')
        ctrl.getControl(value='K1000000').selected = True
        ctrl.getControl(value='K1000001').selected = True
        self.browser.getControl("Send bulk", index=0).click()
        self.assertTrue("[('aa@aa.ng', u'K1000000'), ('uli@uni.ng', u'K1000001')]"
            in self.browser.contents)
        self.browser.getControl(name="form.subject").value = 'Test'
        self.browser.getControl(name="form.body").value = 'Hello world'
        self.browser.getControl("Send message").click()
        self.assertTrue('Your message has been sent' in self.browser.contents)
        self.assertMatches(
        u'Sending email from no-reply@waeup.org to contact@waeup.org, aa@aa.ng, uli@uni.ng:\n'
        u'Message:\n'
        u'msg: MIME-Version: 1.0\n'
        u'msg: Content-Type: text/plain; charset="us-ascii"\n'
        u'msg: Content-Transfer-Encoding: 7bit\n'
        u'msg: From: Manager <no-reply@waeup.org>\n'
        u'msg: To: Manager <contact@waeup.org>\n'
        u'msg: Bcc: K0000000 <aa@aa.ng>\n'
        u'msg: Bcc: K0000001 <uli@uni.ng>\n'
        u'msg: Reply-To: Manager <contact@waeup.org>\n'
        u'msg: Subject: Test\n'
        u'msg: \n'
        u'msg: Hello world\n'
        u'msg: \n'
        u'msg: ---\n'
        u'msg: Manager (id: zope.mgr)\n'
        u'msg: Sample University\n'
        u'msg: \n',
            self.get_fake_smtp_output()
            )

    def test_add_graduated_students(self):
        # Managers can add search and remove students
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_container_path)
        self.browser.getLink("Add student").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.add_student_path)
        self.browser.getControl(name="form.firstname").value = 'Bob'
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.reg_number").value = '1234'
        self.browser.getControl("Create graduated student").click()
        self.assertTrue('Graduated student record created' in self.browser.contents)
        self.assertEqual(self.app['students']['K1000001'].state, 'graduated')
        self.browser.open("http://localhost/app/students/K1000001/history")
        self.assertTrue("State 'graduated' set by Manager" in self.browser.contents)
        return


class OfficerUITests(StudentsFullSetup):
    # Tests for Student class views and pages

    def setUp(self):
        super(OfficerUITests, self).setUp()
        self.setup_logging()
        return

    def tearDown(self):
        super(OfficerUITests, self).tearDown()
        self.teardown_logging()
        return

    def setup_logging(self):
        # setup a log-handler that catches all fake mailer output
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        logger = logging.getLogger('test.smtp')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return

    def get_fake_smtp_output(self):
        # get output generated by fake mailer
        self.stream.flush()
        self.stream.seek(0)
        return self.stream.read()

    def teardown_logging(self):
        # remove the log handler for fake mailer output
        logger = logging.getLogger('test.smtp')
        handlers = [x for x in logger.handlers]
        for handler in handlers:
            logger.removeHandler(handler)
        return

    def test_student_properties(self):
        self.student['studycourse'].current_level = 100
        self.assertEqual(self.student.current_level, 100)
        self.student['studycourse'].current_session = 2011
        self.assertEqual(self.student.current_session, 2011)
        self.student['studycourse'].current_verdict = 'A'
        self.assertEqual(self.student.current_verdict, 'A')
        return

    def test_studylevelmanagepage(self):
        studylevel = StudentStudyLevel()
        studylevel.level = 100
        cert = self.app['faculties']['fac1']['dep1'].certificates['CERT1']
        self.student['studycourse'].addStudentStudyLevel(cert, studylevel)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.studycourse_path + '/100/manage')
        self.assertEqual(
            self.browser.url, self.studycourse_path + '/100/manage')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')

    def test_basic_auth(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app')
        self.browser.getLink("Logout").click()
        self.assertTrue('You have been logged out' in self.browser.contents)
        # But we are still logged in since we've used basic
        # authentication here.  Wikipedia says: Existing browsers
        # retain authentication information until the tab or browser
        # is closed or the user clears the history.  HTTP does not
        # provide a method for a server to direct clients to discard
        # these cached credentials. This means that there is no
        # effective way for a server to "log out" the user without
        # closing the browser. This is a significant defect that
        # requires browser manufacturers to support a "logout" user
        # interface element ...
        self.assertTrue('Manager' in self.browser.contents)

    def test_basic_auth_base64(self):
        auth_token = base64.b64encode('mgr:mgrpw')
        self.browser.addHeader('Authorization', 'Basic %s' % auth_token)
        self.browser.open(self.manage_container_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')

    def test_manage_access(self):
        # Managers can access the pages of students
        # and can perform actions
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.student_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.student_path)
        self.browser.getLink("Trigger").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        # Managers can trigger transitions
        self.browser.getControl(name="transition").value = ['admit']
        self.browser.getControl("Save").click()
        # Managers can edit base
        self.browser.open(self.student_path)
        self.browser.getLink("Manage").click()
        self.assertEqual(self.browser.url, self.manage_student_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.getControl(name="form.firstname").value = 'John'
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.reg_number").value = '345'
        self.browser.getControl(name="password").value = 'secret'
        self.browser.getControl(name="control_password").value = 'secret'
        self.browser.getControl("Save").click()
        self.assertMatches('...Form has been saved...',
                           self.browser.contents)
        self.browser.open(self.student_path)
        self.browser.getLink("Clearance Data").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.clearance_path)
        self.browser.getLink("Manage").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.manage_clearance_path)
        self.browser.getControl(name="form.date_of_birth").value = '09/10/1961'
        self.browser.getControl("Save").click()
        self.assertMatches('...Form has been saved...',
                           self.browser.contents)

        self.browser.open(self.student_path)
        self.browser.getLink("Personal Data").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.personal_path)
        self.browser.getLink("Manage").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.manage_personal_path)
        self.browser.open(self.personal_path)
        self.assertTrue('Updated' in self.browser.contents)
        self.browser.getLink("Edit").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.edit_personal_path)
        self.browser.getControl("Save").click()
        # perm_address is required in IStudentPersonalEdit
        self.assertMatches('...Required input is missing...',
                           self.browser.contents)
        self.browser.getControl(name="form.perm_address").value = 'My address!'
        self.browser.getControl("Save").click()
        self.assertMatches('...Form has been saved...',
                           self.browser.contents)

        # Managers can browse all subobjects
        self.browser.open(self.student_path)
        self.browser.getLink("Payments").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.payments_path)
        self.browser.open(self.student_path)
        self.browser.getLink("Accommodation").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        # We have been redirected to the manage page
        self.assertEqual(self.browser.url, self.acco_path + '/manage')
        self.browser.open(self.student_path)
        self.browser.getLink("History").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.history_path)
        self.assertMatches('...Admitted by Manager...',
                           self.browser.contents)
        # Only the Application Slip does not exist
        self.assertFalse('Application Slip' in self.browser.contents)
        return

    def test_upload_files(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_student_path)
        self.browser.getControl(name="form.firstname").value = 'John'
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.reg_number").value = '345'
        self.browser.getControl(name="password").value = 'secret'
        self.browser.getControl(name="control_password").value = 'secret'
        self.browser.getControl("Save").click()
        self.assertMatches('...Form has been saved...',
                           self.browser.contents)
        ctrl = self.browser.getControl(name='passportuploadmanage')
        file_obj = open(SAMPLE_IMAGE, 'rb')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file_obj, filename='my_photo.jpg')
        self.browser.getControl(
            name='upload_passportuploadmanage').click()
        self.assertTrue(
            'src="http://localhost/app/students/K1000000/passport.jpg"'
            in self.browser.contents)
        ctrl = self.browser.getControl(name='signatureuploadmanage')
        file_obj = open(SAMPLE_IMAGE, 'rb')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file_obj, filename='my_signature.jpg')
        self.browser.getControl(
            name='upload_signatureuploadmanage').click()
        self.assertTrue(
            'src="http://localhost/app/students/K1000000/signature.jpg"'
            in self.browser.contents)
        return

    def test_flash_notice(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.student_path)
        self.assertFalse('alert alert-warning' in self.browser.contents)
        self.student.flash_notice = u'Happy Birthday!'
        self.browser.open(self.student_path)
        self.assertTrue(
            '<div><div class="alert alert-warning">Happy Birthday!</div>'
            in self.browser.contents)
        return

    def test_manage_contact_student(self):
        # Managers can contact student
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        # Remove required FieldProperty attribute first ...
        delattr(Student, 'email')
        # ... and replace by None
        self.student.email = None
        # Now we have to add  the FieldProperty attribute again. Otherwise
        # many other tests below will fail.
        iface = list(implementedBy(Student))[0]
        field_property = FieldProperty(iface['email'])
        setattr(Student, 'email', field_property)
        self.browser.open(self.student_path)
        self.browser.getLink("Send email").click()
        self.browser.getControl(
            name="form.subject").value = 'Important subject'
        self.browser.getControl(name="form.body").value = 'Hello!'
        self.browser.getControl("Send message now").click()
        self.assertTrue(
            'An smtp server error occurred' in self.browser.contents)
        self.student.email = 'xx@yy.zz'
        self.browser.getControl("Send message now").click()
        self.assertTrue('Your message has been sent' in self.browser.contents)
        self.assertMatches(
            'Sending email from no-reply@waeup.org to xx@yy.zz:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0'
            '\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Manager <no-reply@waeup.org>'
            '\nmsg: To: Anna Tester <xx@yy.zz>'
            '\nmsg: Reply-To: Manager <contact@waeup.org>'
            '\nmsg: Subject: Important subject'
            '\nmsg:'
            '\nmsg: Hello!'
            '\nmsg:'
            '\nmsg: ---'
            '\nmsg: Manager (id: zope.mgr)'
            '\nmsg: Sample University'
            '\nmsg:',
            self.get_fake_smtp_output()
            )
        return

    def test_manage_remove_department(self):
        # Lazy student is studying CERT1
        lazystudent = Student()
        lazystudent.firstname = u'Lazy'
        lazystudent.lastname = u'Student'
        self.app['students'].addStudent(lazystudent)
        student_id = lazystudent.student_id
        student_path = self.container_path + '/' + student_id
        lazystudent['studycourse'].certificate = self.certificate
        notify(grok.ObjectModifiedEvent(lazystudent))
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(student_path + '/studycourse')
        self.assertTrue('CERT1' in self.browser.contents)
        # After some years the department is removed
        del self.app['faculties']['fac1']['dep1']
        # So CERT1 does no longer exist and lazy student's
        # certificate reference is removed too
        self.browser.open(student_path + '/studycourse')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, student_path + '/studycourse')
        self.assertFalse('CERT1' in self.browser.contents)
        self.assertMatches('...<div>--</div>...',
                           self.browser.contents)

    def test_manage_upload_file(self):
        # Managers can upload a file via the StudentClearanceManageFormPage
        # The image is stored even if form has errors
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_clearance_path)
        # No birth certificate has been uploaded yet
        # Browsing the link shows a placerholder image
        self.browser.open('birth_certificate')
        self.assertEqual(
            self.browser.headers['content-type'], 'image/jpeg')
        self.assertEqual(len(self.browser.contents), PH_LEN)
        # Create a pseudo image file and select it to be uploaded in form
        # as birth certificate
        self.browser.open(self.manage_clearance_path)
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='birthcertificateupload')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='my_birth_certificate.jpg')
        # The Save action does not upload files
        self.browser.getControl("Save").click()  # submit form
        self.assertFalse(
            '<a target="image" href="birth_certificate">'
            in self.browser.contents)
        # ... but the correct upload submit button does
        image = open(SAMPLE_IMAGE)
        ctrl = self.browser.getControl(name='birthcertificateupload')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='my_birth_certificate.jpg')
        self.browser.getControl(
            name='upload_birthcertificateupload').click()
        # There is a correct <img> link included
        self.assertTrue(
            'href="http://localhost/app/students/K1000000/birth_certificate"'
            in self.browser.contents)
        # Browsing the link shows a real image
        self.browser.open('birth_certificate')
        self.assertEqual(
            self.browser.headers['content-type'], 'image/jpeg')
        self.assertEqual(len(self.browser.contents), 2787)
        # We can't reupload a file. The existing file must be deleted first.
        self.browser.open(self.manage_clearance_path)
        self.assertFalse(
            'upload_birthcertificateupload' in self.browser.contents)
        # File must be deleted first
        self.browser.getControl(name='delete_birthcertificateupload').click()
        self.assertTrue(
            'birth_certificate deleted' in self.browser.contents)
        # Uploading a file which is bigger than 250k will raise an error
        big_image = StringIO(open(SAMPLE_IMAGE, 'rb').read() * 100)
        ctrl = self.browser.getControl(name='birthcertificateupload')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(big_image, filename='my_birth_certificate.jpg')
        self.browser.getControl(
            name='upload_birthcertificateupload').click()
        self.assertTrue(
            'Uploaded file is too big' in self.browser.contents)
        # we do not rely on filename extensions given by uploaders
        image = open(SAMPLE_IMAGE, 'rb')  # a jpg-file
        ctrl = self.browser.getControl(name='birthcertificateupload')
        file_ctrl = ctrl.mech_control
        # tell uploaded file is bmp
        file_ctrl.add_file(image, filename='my_birth_certificate.bmp')
        self.browser.getControl(
            name='upload_birthcertificateupload').click()
        self.assertTrue(
            # jpg file was recognized
            'File birth_certificate.jpg uploaded.' in self.browser.contents)
        # Delete file again
        self.browser.getControl(name='delete_birthcertificateupload').click()
        self.assertTrue(
            'birth_certificate deleted' in self.browser.contents)
        # File names must meet several conditions
        bmp_image = open(SAMPLE_IMAGE_BMP, 'rb')
        ctrl = self.browser.getControl(name='birthcertificateupload')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(bmp_image, filename='my_birth_certificate.bmp')
        self.browser.getControl(
            name='upload_birthcertificateupload').click()
        self.assertTrue(
            'Only the following extensions are allowed'
            in self.browser.contents)

        # Managers can upload a file via the StudentBaseManageFormPage
        self.browser.open(self.manage_student_path)
        image = open(SAMPLE_IMAGE_BMP, 'rb')
        ctrl = self.browser.getControl(name='passportuploadmanage')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='my_photo.bmp')
        self.browser.getControl(
            name='upload_passportuploadmanage').click()
        self.assertTrue(
            'jpg file format expected' in self.browser.contents)
        ctrl = self.browser.getControl(name='passportuploadmanage')
        file_ctrl = ctrl.mech_control
        image = open(SAMPLE_IMAGE, 'rb')
        file_ctrl.add_file(image, filename='my_photo.jpg')
        self.browser.getControl(
            name='upload_passportuploadmanage').click()
        self.assertTrue(
            'src="http://localhost/app/students/K1000000/passport.jpg"'
            in self.browser.contents)
        # We remove the passport file again
        self.browser.open(self.manage_student_path)
        self.browser.getControl('Delete').click()
        self.browser.open(self.student_path + '/clearance_slip.pdf')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        # We want to see the signature fields.
        IWorkflowState(self.student).setState('cleared')
        self.browser.open(self.student_path + '/clearance_slip.pdf')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        path = os.path.join(samples_dir(), 'clearance_slip.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF clearance_slip.pdf written to %s" % path

    def test_manage_course_lists(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.student_path)
        self.browser.getLink("Study Course").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.studycourse_path)
        self.assertTrue('Undergraduate Full-Time' in self.browser.contents)
        self.browser.getLink("Manage").click()
        self.assertTrue('Manage study course' in self.browser.contents)
        # Before we can select a level, the certificate must
        # be selected and saved
        self.browser.getControl(name="form.certificate").value = ['CERT1']
        self.browser.getControl(name="form.current_session").value = ['2004']
        self.browser.getControl(name="form.current_verdict").value = ['A']
        self.browser.getControl(name="form.entry_mode").value = ['ug_ft']
        self.browser.getControl("Save").click()
        # Now we can save also the current level which depends on start and end
        # level of the certificate
        self.browser.getControl(name="form.current_level").value = ['100']
        self.browser.getControl("Save").click()
        # Managers can add and remove any study level (course list)
        self.browser.getControl(name="addlevel").value = ['100']
        self.browser.getControl("Add study level").click()
        self.assertMatches(
            '...You must select a session...', self.browser.contents)
        self.browser.getControl(name="addlevel").value = ['100']
        self.browser.getControl(name="level_session").value = ['2004']
        self.browser.getControl("Add study level").click()
        self.assertMatches('...<span>100</span>...', self.browser.contents)
        self.assertEqual(self.student['studycourse']['100'].level, 100)
        self.assertEqual(
            self.student['studycourse']['100'].level_session, 2004)
        self.browser.getControl(name="addlevel").value = ['100']
        self.browser.getControl(name="level_session").value = ['2004']
        self.browser.getControl("Add study level").click()
        self.assertMatches('...This level exists...', self.browser.contents)
        self.browser.getControl("Remove selected").click()
        self.assertMatches(
            '...No study level selected...', self.browser.contents)
        self.browser.getControl(name="val_id").value = ['100']
        self.browser.getControl(name="level_session").value = ['2004']
        self.browser.getControl("Remove selected").click()
        self.assertMatches('...Successfully removed...', self.browser.contents)
        # Removing levels is properly logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.StudyCourseManageFormPage '
            '- K1000000 - removed: 100' in logcontent)
        # Add level again
        self.browser.getControl(name="addlevel").value = ['100']
        self.browser.getControl(name="level_session").value = ['2004']
        self.browser.getControl("Add study level").click()

        # Managers can view and manage course lists
        self.browser.getLink("100").click()
        self.assertMatches(
            '...: 100 (Year 1)...', self.browser.contents)
        self.browser.getLink("Manage").click()
        self.browser.getControl(name="form.level_session").value = ['2002']
        self.browser.getControl("Save").click()
        self.browser.getControl("Remove selected").click()
        self.assertMatches('...No ticket selected...', self.browser.contents)
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value='COURSE1').selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)
        # Removing course tickets is properly logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.StudyLevelManageFormPage '
            '- K1000000 - level 100 - removed: COURSE1' in logcontent)
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.course.credits = 100
        self.browser.getControl("Add course ticket").click()
        self.assertMatches(
            '...Maximum credits exceeded...', self.browser.contents)
        self.course.credits = 10
        self.browser.getControl("Add course ticket").click()
        self.assertTrue('Successfully added' in self.browser.contents)
        # We can do the same by adding the course on the manage page directly
        del self.student['studycourse']['100']['COURSE1']
        self.browser.getControl(name="course").value = 'COURSE1'
        self.browser.getControl("Add course ticket").click()
        self.assertTrue('Successfully added' in self.browser.contents)
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.browser.getControl("Add course ticket").click()
        self.assertTrue('The ticket exists' in self.browser.contents)
        self.browser.getControl("Cancel").click()
        self.browser.getLink("COURSE1").click()
        self.browser.getLink("Manage").click()
        self.browser.getControl("Save").click()
        self.assertTrue('Form has been saved' in self.browser.contents)
        # Grade and weight have been determined
        self.browser.open(self.studycourse_path + '/100/COURSE1')
        self.assertFalse('Grade' in self.browser.contents)
        self.assertFalse('Weight' in self.browser.contents)
        self.student['studycourse']['100']['COURSE1'].score = 55
        self.browser.open(self.studycourse_path + '/100/COURSE1')
        self.assertTrue('Grade' in self.browser.contents)
        self.assertTrue('Weight' in self.browser.contents)
        self.assertEqual(
            self.student['studycourse']['100']['COURSE1'].grade, 'C')
        self.assertEqual(
            self.student['studycourse']['100']['COURSE1'].weight, 3)
        # We add another ticket to check if GPA will be correctly
        # calculated (and rounded)
        courseticket = createObject('waeup.CourseTicket')
        courseticket.code = 'ANYCODE'
        courseticket.title = u'Any TITLE'
        courseticket.credits = 13
        courseticket.score = 66
        courseticket.semester = 1
        courseticket.dcode = u'ANYDCODE'
        courseticket.fcode = u'ANYFCODE'
        self.student['studycourse']['100']['COURSE2'] = courseticket
        self.browser.open(self.student_path + '/studycourse/100')
        # total credits
        self.assertEqual(
            self.student['studycourse']['100'].gpa_params_rectified[1], 23)
        # weigheted credits = 3 * 10 + 4 * 13
        self.assertEqual(
            self.student['studycourse']['100'].gpa_params_rectified[2], 82.0)
        # sgpa = 82 / 23
        self.assertEqual(
            self.student['studycourse']['100'].gpa_params_rectified[0],
            3.5652173913043477)
        # Carry-over courses will be collected when next level is created
        self.browser.open(self.student_path + '/studycourse/manage')
        # Add next level
        self.student['studycourse']['100']['COURSE1'].score = 10
        self.browser.getControl(name="addlevel").value = ['200']
        self.browser.getControl(name="level_session").value = ['2005']
        self.browser.getControl("Add study level").click()
        self.browser.getLink("200").click()
        self.assertMatches(
            '...: 200 (Year 2)...', self.browser.contents)
        # Since COURSE1 has score 10 it becomes a carry-over course
        # in level 200
        self.assertEqual(
            sorted(self.student['studycourse']['200'].keys()), [u'COURSE1'])
        self.assertTrue(
            self.student['studycourse']['200']['COURSE1'].carry_over)
        # Passed and failed courses have been counted
        self.assertEqual(
            self.student['studycourse']['100'].passed_params,
            (1, 1, 13, 10, 'COURSE1 ', '', 'ANYCODE '))
        self.assertEqual(
            self.student['studycourse']['200'].passed_params,
            (0, 0, 0, 0, '', 'COURSE1 ', ''))
        # And also cumulative params can be calculated. Meanwhile we have the
        # following courses: COURSE1 and COURSE2 in level 100 and
        # COURSE1 as carry-over course in level 200.
        self.assertEqual(
            self.student['studycourse']['100'].cumulative_params,
            (2.260869565217391, 23, 52.0, 23, 13))
        # COURSE1 in level 200 is not taken into consideration
        # when calculating the gpa.
        self.assertEqual(
            self.student['studycourse']['200'].cumulative_params,
            (2.260869565217391, 23, 52.0, 33, 13))
        return

    def test_gpa_calculation_with_carryover(self):
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 100
        studylevel.level_session = 2005
        self.student['studycourse'].entry_mode = 'ug_ft'
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)
        # First course has been added automatically.
        # Set score above passmark.
        studylevel['COURSE1'].score = studylevel['COURSE1'].passmark + 1
        # GPA is 1.
        self.assertEqual(
            self.student['studycourse']['100'].gpa_params_rectified[0], 1.0)
        # Set score below passmark.
        studylevel['COURSE1'].score = studylevel['COURSE1'].passmark - 1
        # GPA is still 0.
        self.assertEqual(
            self.student['studycourse']['100'].gpa_params_rectified[0], 0.0)
        studylevel2 = createObject(u'waeup.StudentStudyLevel')
        studylevel2.level = 200
        studylevel2.level_session = 2006
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel2)
        # Carry-over course has been autonatically added.
        studylevel2['COURSE1'].score = 66
        # The score of the carry-over course is now used for calculation of the
        # GPA at level 100 ...
        self.assertEqual(
            self.student['studycourse']['100'].gpa_params_rectified[0], 4.0)
        # ... but not at level 200
        self.assertEqual(
            self.student['studycourse']['200'].gpa_params_rectified[0], 0.0)
        return

    def test_manage_payments(self):
        # Managers can add online school fee payment tickets
        # if certain requirements are met
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.payments_path)
        IWorkflowState(self.student).setState('cleared')
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...Amount Authorized...',
                           self.browser.contents)
        self.assertEqual(self.student['payments'][value].amount_auth, 40000.0)
        payment_url = self.browser.url
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            ' zope.mgr - students.browser.OnlinePaymentAddFormPage - '
            'K1000000 - added: %s' % value
            in logcontent)
        # The pdf payment slip can't yet be opened
        #self.browser.open(payment_url + '/payment_slip.pdf')
        #self.assertMatches('...Ticket not yet paid...',
        #                   self.browser.contents)

        # The same payment (with same p_item, p_session and
        # p_category) can be initialized a second time if the former
        # ticket is not yet paid.
        self.browser.open(self.payments_path)
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...Payment ticket created...',
                           self.browser.contents)

        # The ticket can be found in the payments_catalog
        cat = queryUtility(ICatalog, name='payments_catalog')
        results = list(cat.searchResults(p_state=('unpaid', 'unpaid')))
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0] is self.student['payments'][value])
        # Managers can approve the payment
        # If, by some reason, the state has already changed,
        # an access code is created after approval.
        IWorkflowState(self.student).setState('school fee paid')
        self.assertEqual(len(self.app['accesscodes']['SFE-0']), 0)
        self.browser.open(payment_url)
        self.browser.getLink("Approve payment").click()
        self.assertMatches(
            '...Payment approved...', self.browser.contents)
        # Approval is logged in students.log ...
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.OnlinePaymentApproveView '
            '- K1000000 - schoolfee payment approved'
            in logcontent)
        # ... and in payments.log
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'payments.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            '"zope.mgr",K1000000,%s,schoolfee,40000.0,AP,,,,,,\n' % value
            in logcontent)
        # The authorized amount has been stored in the new access code
        self.assertEqual(
            self.app['accesscodes']['SFE-0'].values()[0].cost, 40000.0)

        # The catalog has been updated
        results = list(cat.searchResults(p_state=('unpaid', 'unpaid')))
        self.assertTrue(len(results), 0)
        results = list(cat.searchResults(p_state=('paid', 'paid')))
        self.assertTrue(len(results), 1)
        self.assertTrue(results[0] is self.student['payments'][value])

        # Payments can't be approved twice
        self.browser.open(payment_url + '/approve')
        self.assertMatches('...This ticket has already been paid...',
                          self.browser.contents)

        # Now the first ticket is paid and no more ticket of same type
        # (with same p_item, p_session and p_category) can be added.
        # First we have to reset the workflow state.
        IWorkflowState(self.student).setState('cleared')
        self.browser.open(self.payments_path)
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.assertMatches(
            '...This type of payment has already been made...',
            self.browser.contents)

        # Managers can open the pdf payment slip
        self.browser.open(payment_url)
        self.browser.getLink("Download payment slip").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')

        # Managers can remove online school fee payment tickets
        self.browser.open(self.payments_path)
        self.browser.getControl("Remove selected").click()
        self.assertMatches('...No payment selected...', self.browser.contents)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        ctrl.getControl(value=value).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)

        # Managers can add online clearance payment tickets
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['clearance']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)

        # Managers can approve the payment
        self.assertEqual(len(self.app['accesscodes']['CLR-0']),0)
        self.browser.open(self.browser.url + '/approve')
        self.assertMatches('...Payment approved...',
                          self.browser.contents)
        expected = '''...
        <td>
          <span>Paid</span>
        </td>...'''
        self.assertMatches(expected,self.browser.contents)
        # The new CLR-0 pin has been created
        self.assertEqual(len(self.app['accesscodes']['CLR-0']),1)
        pin = self.app['accesscodes']['CLR-0'].keys()[0]
        ac = self.app['accesscodes']['CLR-0'][pin]
        self.assertEqual(ac.owner, self.student_id)
        self.assertEqual(ac.cost, 3456.0)

        # Managers can add online transcript payment tickets
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['transcript']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)

        # Managers can approve the payment
        self.assertEqual(len(self.app['accesscodes']['TSC-0']),0)
        self.browser.open(self.browser.url + '/approve')
        self.assertMatches('...Payment approved...',
                          self.browser.contents)
        expected = '''...
        <td>
          <span>Paid</span>
        </td>...'''
        self.assertMatches(expected,self.browser.contents)
        # The new CLR-0 pin has been created
        self.assertEqual(len(self.app['accesscodes']['TSC-0']),1)
        pin = self.app['accesscodes']['TSC-0'].keys()[0]
        ac = self.app['accesscodes']['TSC-0'][pin]
        self.assertEqual(ac.owner, self.student_id)
        self.assertEqual(ac.cost, 4567.0)
        return

    def test_add_transfer_payment(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.payments_path)
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['transfer']
        self.browser.getControl(name="new_programme").value = 'my new study course'
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...my new study course...',
                           self.browser.contents)
        self.assertEqual(self.student['payments'][value].p_item, u'my new study course')

    def test_manage_payments_bypass_ac_creation(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.payments_path)
        IWorkflowState(self.student).setState('cleared')
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        payment_url = self.browser.url
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        # The ticket can be found in the payments_catalog
        cat = queryUtility(ICatalog, name='payments_catalog')
        results = list(cat.searchResults(p_state=('unpaid', 'unpaid')))
        self.assertTrue(len(results), 1)
        self.assertTrue(results[0] is self.student['payments'][value])
        # Managers can approve the payment
        self.browser.open(payment_url)
        self.browser.getLink("Approve payment").click()
        self.assertMatches('...Payment approved...',
                          self.browser.contents)
        # Approval is logged in students.log ...
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.OnlinePaymentApproveView '
            '- K1000000 - schoolfee payment approved'
            in logcontent)
        # ... and in payments.log
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'payments.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            '"zope.mgr",K1000000,%s,schoolfee,40000.0,AP,,,,,,\n' % value
            in logcontent)
        # Student is in state school fee paid, no activation
        # code was necessary.
        self.assertEqual(self.student.state, 'school fee paid')
        self.assertEqual(len(self.app['accesscodes']['SFE-0']),0)
        return

    def test_payment_disabled(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.payments_path)
        IWorkflowState(self.student).setState('cleared')
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.app['configuration']['2004'].payment_disabled = ['sf_all']
        self.browser.open(self.payments_path)
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...This category of payments has been disabled...',
                           self.browser.contents)
        return

    def test_manage_balance_payments(self):

        # Login
        #self.browser.open(self.login_path)
        #self.browser.getControl(name="form.login").value = self.student_id
        #self.browser.getControl(name="form.password").value = 'spwd'
        #self.browser.getControl("Login").click()

        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.payments_path)

        # Managers can add balance school fee payment tickets in any state.
        IWorkflowState(self.student).setState('courses registered')
        self.browser.open(self.payments_path)
        self.browser.getLink("Add balance payment ticket").click()

        # Balance payment form is provided
        self.assertEqual(self.student.current_session, 2004)
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl(name="form.balance_session").value = ['2004']
        self.browser.getControl(name="form.balance_level").value = ['300']
        self.browser.getControl(name="form.balance_amount").value = '-567.8'
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...Amount must be greater than 0...',
                           self.browser.contents)
        self.browser.getControl(name="form.balance_amount").value = '0'
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...Amount must be greater than 0...',
                           self.browser.contents)
        self.browser.getControl(name="form.balance_amount").value = '567.8'
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...Amount Authorized...',
                           self.browser.contents)
        self.assertEqual(self.student['payments'][value].amount_auth, 567.8)
        # Payment attributes are properly set
        self.assertEqual(self.student['payments'][value].p_session, 2004)
        self.assertEqual(self.student['payments'][value].p_level, 300)
        self.assertEqual(self.student['payments'][value].p_item, u'Balance')
        self.assertEqual(self.student['payments'][value].p_category, 'schoolfee')
        # Adding payment tickets is logged.
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue('zope.mgr - students.browser.BalancePaymentAddFormPage '
                        '- K1000000 - added: %s' % value in logcontent)

    def test_manage_accommodation(self):
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        # Managers can add online booking fee payment tickets and open the
        # callback view (see test_manage_payments)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.payments_path)
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['bed_allocation']
        # If student is not in accommodation session, payment cannot be processed
        self.app['hostels'].accommodation_session = 2011
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...Your current session does not allow...',
                           self.browser.contents)
        self.app['hostels'].accommodation_session = 2004
        self.browser.getControl(name="form.p_category").value = ['bed_allocation']
        self.browser.getControl("Create ticket").click()
        self.browser.open(self.browser.url + '/approve')
        # The new HOS-0 pin has been created
        self.assertEqual(len(self.app['accesscodes']['HOS-0']),1)
        pin = self.app['accesscodes']['HOS-0'].keys()[0]
        ac = self.app['accesscodes']['HOS-0'][pin]
        self.assertEqual(ac.owner, self.student_id)
        parts = pin.split('-')[1:]
        sfeseries, sfenumber = parts
        # Managers can use HOS code and book a bed space with it
        self.browser.open(self.acco_path)
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...You are in the wrong...',
                           self.browser.contents)
        IWorkflowInfo(self.student).fireTransition('admit')
        # An existing HOS code can only be used if students
        # are in accommodation session
        self.student['studycourse'].current_session = 2003
        self.browser.getControl("Book accommodation").click()
        self.assertMatches(
            '...Your current session does not allow to book accommodation...',
            self.browser.contents)
        self.student['studycourse'].current_session = 2004
        # All requirements are met and ticket can be created
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...Activation Code:...',
                           self.browser.contents)
        self.browser.getControl(name="ac_series").value = sfeseries
        self.browser.getControl(name="ac_number").value = sfenumber
        self.browser.getControl("Create bed ticket").click()
        self.assertMatches('...Hall 1, Block A, Room 101, Bed A...',
                           self.browser.contents)
        # Bed has been allocated
        bed1 = self.app['hostels']['hall-1']['hall-1_A_101_A']
        self.assertTrue(bed1.owner == self.student_id)
        # BedTicketAddPage is now blocked
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...You already booked a bed space...',
            self.browser.contents)
        # The bed ticket displays the data correctly
        self.browser.open(self.acco_path + '/2004')
        self.assertMatches('...Hall 1, Block A, Room 101, Bed A...',
                           self.browser.contents)
        self.assertMatches('...2004/2005...', self.browser.contents)
        self.assertMatches('...regular_male_fr...', self.browser.contents)
        self.assertMatches('...%s...' % pin, self.browser.contents)
        # Booking is properly logged
        logcontent = open(logfile).read()
        self.assertTrue('zope.mgr - students.browser.BedTicketAddPage '
            '- K1000000 - booked: hall-1_A_101_A' in logcontent)
        # Managers can relocate students if the student's bed_type has changed
        self.browser.getLink("Relocate student").click()
        self.assertMatches(
            "...Student can't be relocated...", self.browser.contents)
        self.student.sex = u'f'
        self.browser.getLink("Relocate student").click()
        self.assertMatches(
            "...Hall 1, Block A, Room 101, Bed B...", self.browser.contents)
        self.assertTrue(bed1.owner == NOT_OCCUPIED)
        bed2 = self.app['hostels']['hall-1']['hall-1_A_101_B']
        self.assertTrue(bed2.owner == self.student_id)
        self.assertTrue(self.student['accommodation'][
            '2004'].bed_type == u'regular_female_fr')
        # Relocation is properly logged
        logcontent = open(logfile).read()
        self.assertTrue('zope.mgr - students.accommodation.BedTicket '
            '- K1000000 - relocated: hall-1_A_101_B' in logcontent)
        # The payment object still shows the original payment item
        payment_id = self.student['payments'].keys()[0]
        payment = self.student['payments'][payment_id]
        self.assertTrue(payment.p_item == u'regular_male_fr')
        # Managers can relocate students if the bed's bed_type has changed
        bed1.bed_type = u'regular_female_fr'
        bed2.bed_type = u'regular_male_fr'
        notify(grok.ObjectModifiedEvent(bed1))
        notify(grok.ObjectModifiedEvent(bed2))
        self.browser.getLink("Relocate student").click()
        self.assertMatches(
            "...Student relocated...", self.browser.contents)
        self.assertMatches(
            "... Hall 1, Block A, Room 101, Bed A...", self.browser.contents)
        self.assertMatches(bed1.owner, self.student_id)
        self.assertMatches(bed2.owner, NOT_OCCUPIED)
        # Managers can't relocate students if bed is reserved
        self.student.sex = u'm'
        bed1.bed_type = u'regular_female_reserved'
        notify(grok.ObjectModifiedEvent(bed1))
        self.browser.getLink("Relocate student").click()
        self.assertMatches(
            "...Students in reserved beds can't be relocated...",
            self.browser.contents)
        # Managers can relocate students if booking has been cancelled but
        # other bed space has been manually allocated after cancellation
        old_owner = bed1.releaseBed()
        self.assertMatches(old_owner, self.student_id)
        bed2.owner = self.student_id
        self.browser.open(self.acco_path + '/2004')
        self.assertMatches(
            "...booking cancelled...", self.browser.contents)
        self.browser.getLink("Relocate student").click()
        # We didn't informed the catalog therefore the new owner is not found
        self.assertMatches(
            "...There is no free bed in your category regular_male_fr...",
            self.browser.contents)
        # Now we fire the event properly
        notify(grok.ObjectModifiedEvent(bed2))
        self.browser.getLink("Relocate student").click()
        self.assertMatches(
            "...Student relocated...", self.browser.contents)
        self.assertMatches(
            "... Hall 1, Block A, Room 101, Bed B...", self.browser.contents)
          # Managers can delete bed tickets
        self.browser.open(self.acco_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        ctrl.getControl(value=value).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertMatches('...Successfully removed...', self.browser.contents)
        # The bed has been properly released by the event handler
        self.assertMatches(bed1.owner, NOT_OCCUPIED)
        self.assertMatches(bed2.owner, NOT_OCCUPIED)
        return

    def test_manage_workflow(self):
        # Managers can pass through the whole workflow
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        student = self.app['students'][self.student_id]
        self.browser.open(self.trigtrans_path)
        self.assertTrue(student.clearance_locked)
        self.browser.getControl(name="transition").value = ['admit']
        self.browser.getControl("Save").click()
        self.assertTrue(student.clearance_locked)
        self.browser.getControl(name="transition").value = ['start_clearance']
        self.browser.getControl("Save").click()
        self.assertFalse(student.clearance_locked)
        self.browser.getControl(name="transition").value = ['request_clearance']
        self.browser.getControl("Save").click()
        self.assertTrue(student.clearance_locked)
        self.browser.getControl(name="transition").value = ['clear']
        self.browser.getControl("Save").click()
        # Managers approve payment, they do not pay
        self.assertFalse('pay_first_school_fee' in self.browser.contents)
        self.browser.getControl(
            name="transition").value = ['approve_first_school_fee']
        self.browser.getControl("Save").click()
        self.browser.getControl(name="transition").value = ['reset6']
        self.browser.getControl("Save").click()
        # In state returning the pay_school_fee transition triggers some 
        # changes of attributes
        self.browser.getControl(name="transition").value = ['approve_school_fee']
        self.browser.getControl("Save").click()
        self.assertEqual(student['studycourse'].current_session, 2005) # +1
        self.assertEqual(student['studycourse'].current_level, 200) # +100
        self.assertEqual(student['studycourse'].current_verdict, '0') # 0 = Zero = not set
        self.assertEqual(student['studycourse'].previous_verdict, 'A')
        self.browser.getControl(name="transition").value = ['register_courses']
        self.browser.getControl("Save").click()
        self.browser.getControl(name="transition").value = ['validate_courses']
        self.browser.getControl("Save").click()
        self.browser.getControl(name="transition").value = ['return']
        self.browser.getControl("Save").click()
        return

    def test_manage_pg_workflow(self):
        # Managers can pass through the whole workflow
        IWorkflowState(self.student).setState('school fee paid')
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.trigtrans_path)
        self.assertTrue('<option value="reset6">' in self.browser.contents)
        self.assertTrue('<option value="register_courses">' in self.browser.contents)
        self.assertTrue('<option value="reset5">' in self.browser.contents)
        self.certificate.study_mode = 'pg_ft'
        self.browser.open(self.trigtrans_path)
        self.assertFalse('<option value="reset6">' in self.browser.contents)
        self.assertFalse('<option value="register_courses">' in self.browser.contents)
        self.assertTrue('<option value="reset5">' in self.browser.contents)
        return

    def test_manage_import(self):
        # Managers can import student data files
        datacenter_path = 'http://localhost/app/datacenter'
        # Prepare a csv file for students
        open('students.csv', 'wb').write(
"""firstname,lastname,reg_number,date_of_birth,matric_number,email,phone,sex,password
Aaren,Pieri,1,1990-01-02,100000,aa@aa.ng,1234,m,mypwd1
Claus,Finau,2,1990-01-03,100001,aa@aa.ng,1234,m,mypwd1
Brit,Berson,3,1990-01-04,100001,aa@aa.ng,1234,m,mypwd1
""")
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(datacenter_path)
        self.browser.getLink('Upload data').click()
        filecontents = StringIO(open('students.csv', 'rb').read())
        filewidget = self.browser.getControl(name='uploadfile:file')
        filewidget.add_file(filecontents, 'text/plain', 'students.csv')
        self.browser.getControl(name='SUBMIT').click()
        self.browser.getLink('Process data').click()
        self.browser.getLink("Switch maintenance mode").click()
        button = lookup_submit_value(
            'select', 'students_zope.mgr.csv', self.browser)
        button.click()
        importerselect = self.browser.getControl(name='importer')
        modeselect = self.browser.getControl(name='mode')
        importerselect.getControl('Student Processor').selected = True
        modeselect.getControl(value='create').selected = True
        self.browser.getControl('Proceed to step 3').click()
        self.assertTrue('Header fields OK' in self.browser.contents)
        self.browser.getControl('Perform import').click()
        self.assertTrue('Processing of 1 rows failed' in self.browser.contents)
        self.assertTrue('Successfully processed 2 rows' in self.browser.contents)
        self.assertTrue('Batch processing finished' in self.browser.contents)
        open('studycourses.csv', 'wb').write(
"""reg_number,matric_number,certificate,current_session,current_level
1,,CERT1,2008,100
,100001,CERT1,2008,100
,100002,CERT1,2008,100
""")
        self.browser.open(datacenter_path)
        self.browser.getLink('Upload data').click()
        filecontents = StringIO(open('studycourses.csv', 'rb').read())
        filewidget = self.browser.getControl(name='uploadfile:file')
        filewidget.add_file(filecontents, 'text/plain', 'studycourses.csv')
        self.browser.getControl(name='SUBMIT').click()
        self.browser.getLink('Process data').click()
        # Meanwhile maintenance mode is disabled again.
        self.browser.getLink("Switch maintenance mode").click()
        button = lookup_submit_value(
            'select', 'studycourses_zope.mgr.csv', self.browser)
        button.click()
        importerselect = self.browser.getControl(name='importer')
        modeselect = self.browser.getControl(name='mode')
        importerselect.getControl(
            'StudentStudyCourse Processor',index=0).selected = True
        modeselect.getControl(value='update').selected = True
        #self.browser.getControl('Proceed to step 3').click()
        #self.assertTrue('Update mode only' in self.browser.contents)
        self.browser.getControl('Proceed to step 3').click()
        self.assertTrue('Header fields OK' in self.browser.contents)
        self.browser.getControl('Perform import').click()
        self.assertTrue('Processing of 1 rows failed' in self.browser.contents)
        self.assertTrue('Successfully processed 2 rows'
                        in self.browser.contents)
        # The students are properly indexed and we can
        # thus find a student in  the department
        self.browser.open(self.manage_container_path)
        self.browser.getControl(name="searchtype").value = ['depcode']
        self.browser.getControl(name="searchterm").value = 'dep1'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Aaren Pieri' in self.browser.contents)
        # We can search for a new student by name ...
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'Claus'
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Claus Finau' in self.browser.contents)
        # ... and check if the imported password has been properly set
        ctrl = self.browser.getControl(name='entries')
        value = ctrl.options[0]
        claus = self.app['students'][value]
        self.assertTrue(IUserAccount(claus).checkPassword('mypwd1'))
        return

    def init_clearance_officer(self):
        # Create clearance officer
        self.app['users'].addUser('mrclear', SECRET)
        self.app['users']['mrclear'].email = 'mrclear@foo.ng'
        self.app['users']['mrclear'].title = 'Carlo Pitter'
        # Clearance officers need not necessarily to get
        # the StudentsOfficer site role
        #prmglobal = IPrincipalRoleManager(self.app)
        #prmglobal.assignRoleToPrincipal('waeup.StudentsOfficer', 'mrclear')
        # Assign local ClearanceOfficer role
        self.department = self.app['faculties']['fac1']['dep1']
        prmlocal = IPrincipalRoleManager(self.department)
        prmlocal.assignRoleToPrincipal('waeup.local.ClearanceOfficer', 'mrclear')
        IWorkflowState(self.student).setState('clearance started')
        # Add another student for testing
        other_student = Student()
        other_student.firstname = u'Dep2'
        other_student.lastname = u'Student'
        self.app['students'].addStudent(other_student)
        self.other_student_path = (
            'http://localhost/app/students/%s' % other_student.student_id)
        # Login as clearance officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrclear'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()

    def test_handle_clearance_by_co(self):
        self.init_clearance_officer()
        self.assertMatches('...You logged in...', self.browser.contents)
        # CO is landing on index page.
        self.assertEqual(self.browser.url, 'http://localhost/app/index')
        # CO can see his roles
        self.browser.getLink("My Roles").click()
        self.assertMatches(
            '...<div>Academics Officer (view only)</div>...',
            self.browser.contents)
        # But not his local role ...
        self.assertFalse('Clearance Officer' in self.browser.contents)
        # ... because we forgot to notify the department that the local role
        # has changed.
        notify(LocalRoleSetEvent(
            self.department, 'waeup.local.ClearanceOfficer', 'mrclear',
            granted=True))
        self.browser.open('http://localhost/app/users/mrclear/my_roles')
        self.assertTrue('Clearance Officer' in self.browser.contents)
        self.assertMatches(
            '...<a href="http://localhost/app/faculties/fac1/dep1">...',
            self.browser.contents)
        # CO can view the student ...
        self.browser.open(self.clearance_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.clearance_path)
        # ... but not other students.
        self.assertRaises(
            Unauthorized, self.browser.open, self.other_student_path)
        # Clearance is disabled for this session.
        self.browser.open(self.clearance_path)
        self.assertFalse('Clear student' in self.browser.contents)
        self.browser.open(self.student_path + '/clear')
        self.assertTrue('Clearance is disabled for this session'
            in self.browser.contents)
        self.app['configuration']['2004'].clearance_enabled = True
        # Only in state clearance requested the CO does see the 'Clear' button.
        self.browser.open(self.clearance_path)
        self.assertFalse('Clear student' in self.browser.contents)
        self.browser.open(self.student_path + '/clear')
        self.assertTrue('Student is in wrong state.'
            in self.browser.contents)
        IWorkflowInfo(self.student).fireTransition('request_clearance')
        self.browser.open(self.clearance_path)
        self.assertTrue('Clear student' in self.browser.contents)
        self.browser.getLink("Clear student").click()
        self.assertTrue('Student has been cleared' in self.browser.contents)
        self.assertTrue('cleared' in self.browser.contents)
        self.browser.open(self.history_path)
        self.assertTrue('Cleared by Carlo Pitter' in self.browser.contents)
        # Hide real name.
        self.app['users']['mrclear'].public_name = 'My Public Name'
        self.browser.open(self.clearance_path)
        self.browser.getLink("Reject clearance").click()
        self.assertEqual(
            self.browser.url, self.student_path + '/reject_clearance')
        # Type comment why.
        self.browser.getControl(name="form.officer_comment").value = (
            'Dear Student,\n'
            'You did not fill properly.')
        self.browser.getControl("Save comment").click()
        self.assertTrue('Clearance has been annulled' in self.browser.contents)
        url = ('http://localhost/app/students/K1000000/'
              'contactstudent?body=Dear+Student%2C%0AYou+did+not+fill+properly.'
              '&subject=Clearance+has+been+annulled.')
        # CO does now see the prefilled contact form and can send a message.
        self.assertEqual(self.browser.url, url)
        self.assertTrue('clearance started' in self.browser.contents)
        self.assertTrue('name="form.subject" size="20" type="text" '
            'value="Clearance has been annulled."'
            in self.browser.contents)
        self.assertTrue('name="form.body" rows="10" >Dear Student,'
            in self.browser.contents)
        self.browser.getControl("Send message now").click()
        self.assertTrue('Your message has been sent' in self.browser.contents)
        # The comment has been stored ...
        self.assertEqual(self.student.officer_comment,
            u'Dear Student,\nYou did not fill properly.')
        # ... and logged.
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'INFO - mrclear - students.browser.StudentRejectClearancePage - '
            'K1000000 - comment: Dear Student,<br>You did not fill '
            'properly.\n' in logcontent)
        self.browser.open(self.history_path)
        self.assertTrue("Reset to 'clearance started' by My Public Name" in
            self.browser.contents)
        IWorkflowInfo(self.student).fireTransition('request_clearance')
        self.browser.open(self.clearance_path)
        self.browser.getLink("Reject clearance").click()
        self.browser.getControl("Save comment").click()
        self.assertTrue('Clearance request has been rejected'
            in self.browser.contents)
        self.assertTrue('clearance started' in self.browser.contents)
        # The CO can't clear students if not in state
        # clearance requested.
        self.browser.open(self.student_path + '/clear')
        self.assertTrue('Student is in wrong state'
            in self.browser.contents)
        # The CO can go to his department throug the my_roles page ...
        self.browser.open('http://localhost/app/users/mrclear/my_roles')
        self.browser.getLink("http://localhost/app/faculties/fac1/dep1").click()
        # ... and view the list of students.
        self.browser.getLink("Show students").click()
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['200']
        self.browser.getControl("Show").click()
        self.assertFalse(self.student_id in self.browser.contents)
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Show").click()
        self.assertTrue(self.student_id in self.browser.contents)
        # The comment is indicated by 'yes'.
        self.assertTrue('<td><span>yes</span></td>' in self.browser.contents)
        # Check if the enquiries form is not pre-filled with officer_comment
        # (regression test).
        self.browser.getLink("Logout").click()
        self.browser.open('http://localhost/app/enquiries')
        self.assertFalse(
            'You did not fill properly'
            in self.browser.contents)
        # When a student is cleared the comment is automatically deleted
        IWorkflowInfo(self.student).fireTransition('request_clearance')
        IWorkflowInfo(self.student).fireTransition('clear')
        self.assertEqual(self.student.officer_comment, None)
        return

    def test_handle_temp_clearance_by_co(self):
        self.app['configuration']['2004'].clearance_enabled = True
        self.init_clearance_officer()
        # Hide real name.
        self.app['users']['mrclear'].public_name = 'My Public Name'
        IWorkflowInfo(self.student).fireTransition('request_clearance')
        #notify(LocalRoleSetEvent(
        #    self.department, 'waeup.local.ClearanceOfficer', 'mrclear',
        #    granted=True))
        # CO can view the student ...
        self.browser.open(self.clearance_path)
        self.browser.getLink("Clear student temporarily").click()
        self.assertEqual(
            self.browser.url, self.student_path + '/temp_clearance')
        # Type comment why.
        self.browser.getControl(name="form.officer_comment").value = (
            'Dear Student,\n'
            'Your birth cert is missing.')
        self.browser.getControl(
            'Save comment and clear student temporarily now').click()
        self.assertTrue('Student has been temporarily cleared.'
            in self.browser.contents)
        url = ('http://localhost/app/students/K1000000/'
              'contactstudent?body=Dear+Student%2C%0AYour+birth+cert+is+missing.'
              '&subject=You+have+been+temporarily+cleared.')
        # CO does now see the prefilled contact form and can send a message.
        self.assertEqual(self.browser.url, url)
        self.assertTrue('clearance requested' in self.browser.contents)
        self.assertTrue('name="form.subject" size="20" type="text" '
            'value="You have been temporarily cleared."'
            in self.browser.contents)
        self.assertTrue('name="form.body" rows="10" >Dear Student,'
            in self.browser.contents)
        self.browser.getControl("Send message now").click()
        self.assertTrue('Your message has been sent' in self.browser.contents)
        # The comment has been stored ...
        self.assertEqual(self.student.officer_comment,
            'Temporarily cleared by My Public Name. Officer\'s comment:\n'
            'Dear Student,\nYour birth cert is missing.')
        # ... and logged.
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'INFO - mrclear - students.browser.StudentTempClearancePage - '
            'K1000000 - comment: Dear Student,<br>Your birth cert is '
            'missing.\n' in logcontent)
        # CO can view the student bus no longer see the temp clearance button ...
        self.browser.open(self.clearance_path)
        self.assertFalse('Clear student temporarily' in self.browser.contents)
        return

    def test_handle_mass_clearance_by_co(self):
        self.init_clearance_officer()
        # Additional setups according to test above
        notify(LocalRoleSetEvent(
            self.department, 'waeup.local.ClearanceOfficer', 'mrclear',
            granted=True))
        self.app['configuration']['2004'].clearance_enabled = True
        IWorkflowState(self.student).setState('clearance requested')
        # Update the catalog
        notify(grok.ObjectModifiedEvent(self.student))
        # The CO can go to the department and clear all students in department
        self.browser.open('http://localhost/app/faculties/fac1/dep1')
        self.browser.getLink("Clear all students").click()
        self.assertTrue('1 students have been cleared' in self.browser.contents)
        self.browser.open(self.history_path)
        self.assertTrue('Cleared by Carlo Pitter' in self.browser.contents)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'INFO - mrclear - K1000000 - Cleared' in logcontent)
        self.browser.open('http://localhost/app/faculties/fac1/dep1')
        self.browser.getLink("Clear all students").click()
        self.assertTrue('0 students have been cleared' in self.browser.contents)
        return

    #def test_remove_all_flash_notices(self):
    #    self.student.flash_notice = u'test'
    #    self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
    #    self.browser.open('http://localhost/app/faculties/fac1/dep1')
    #    self.browser.getLink("Remove all flash notices").click()
    #    self.assertTrue('1 flash notices have been removed' in self.browser.contents)
    #    self.assertEqual(self.student.flash_notice, '')
    #    return

    def test_edit_all_flash_notices(self):
        self.student.flash_notice = u'test'
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/faculties/fac1/dep1')
        self.browser.getLink("Edit all flash notices").click()
        self.browser.getControl(name="form.flash_notice").value = 'Hello'
        self.browser.getControl("Save flash notices").click()
        self.assertTrue('1 flash notices have been edited' in self.browser.contents)
        self.assertEqual(self.student.flash_notice, 'Hello')
        self.browser.getLink("Edit all flash notices").click()
        self.browser.getControl("Save flash notices").click()
        self.assertTrue('1 flash notices have been edited' in self.browser.contents)
        self.assertEqual(self.student.flash_notice, None)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.EditFlashNoticesFormPage - dep1 - '
            'saved flash notice: Hello' in logcontent)
        self.assertTrue(
            'zope.mgr - students.browser.EditFlashNoticesFormPage - dep1 - '
            'saved flash notice: None' in logcontent)
        return

    def test_handle_courses_by_ca(self):
        self.app['users'].addUser('mrsadvise', SECRET)
        self.app['users']['mrsadvise'].email = 'mradvise@foo.ng'
        self.app['users']['mrsadvise'].title = u'Helen Procter'
        # Assign local CourseAdviser100 role for a certificate
        cert = self.app['faculties']['fac1']['dep1'].certificates['CERT1']
        prmlocal = IPrincipalRoleManager(cert)
        prmlocal.assignRoleToPrincipal('waeup.local.CourseAdviser100', 'mrsadvise')
        IWorkflowState(self.student).setState('school fee paid')
        # Login as course adviser.
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrsadvise'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        # CO can see his roles.
        self.browser.getLink("My Roles").click()
        self.assertMatches(
            '...<div>Academics Officer (view only)</div>...',
            self.browser.contents)
        # But not his local role ...
        self.assertFalse('Course Adviser' in self.browser.contents)
        # ... because we forgot to notify the certificate that the local role
        # has changed.
        notify(LocalRoleSetEvent(
            cert, 'waeup.local.CourseAdviser100', 'mrsadvise', granted=True))
        self.browser.open('http://localhost/app/users/mrsadvise/my_roles')
        self.assertTrue('Course Adviser 100L' in self.browser.contents)
        self.assertMatches(
            '...<a href="http://localhost/app/faculties/fac1/dep1/certificates/CERT1">...',
            self.browser.contents)
        # CA can view the student ...
        self.browser.open(self.student_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.student_path)
        # ... but not other students.
        other_student = Student()
        other_student.firstname = u'Dep2'
        other_student.lastname = u'Student'
        self.app['students'].addStudent(other_student)
        other_student_path = (
            'http://localhost/app/students/%s' % other_student.student_id)
        self.assertRaises(
            Unauthorized, self.browser.open, other_student_path)
        # We add study level 110 to the student's studycourse.
        studylevel = StudentStudyLevel()
        studylevel.level = 110
        self.student['studycourse'].addStudentStudyLevel(
            cert,studylevel)
        L110_student_path = self.studycourse_path + '/110'
        # The CA can neither see the Validate nor the Edit button.
        self.browser.open(L110_student_path)
        self.assertFalse('Validate courses' in self.browser.contents)
        self.assertFalse('Edit' in self.browser.contents)
        IWorkflowInfo(self.student).fireTransition('register_courses')
        self.browser.open(L110_student_path)
        self.assertFalse('Validate courses' in self.browser.contents)
        self.assertFalse('Edit' in self.browser.contents)
        # Only in state courses registered and only if the current level
        # corresponds with the name of the study level object
        # the 100L CA does see the 'Validate' button but not
        # the edit button.
        self.student['studycourse'].current_level = 110
        self.browser.open(L110_student_path)
        self.assertFalse('Edit' in self.browser.contents)
        self.assertTrue('Validate courses' in self.browser.contents)
        # But a 100L CA does not see the button at other levels.
        studylevel2 = StudentStudyLevel()
        studylevel2.level = 200
        self.student['studycourse'].addStudentStudyLevel(
            cert,studylevel2)
        L200_student_path = self.studycourse_path + '/200'
        self.browser.open(L200_student_path)
        self.assertFalse('Edit' in self.browser.contents)
        self.assertFalse('Validate courses' in self.browser.contents)
        self.browser.open(L110_student_path)
        self.browser.getLink("Validate courses").click()
        self.assertTrue('Course list has been validated' in self.browser.contents)
        self.assertTrue('courses validated' in self.browser.contents)
        self.assertEqual(self.student['studycourse']['110'].validated_by,
            'Helen Procter')
        self.assertMatches(
            '<YYYY-MM-DD hh:mm:ss>',
            self.student['studycourse']['110'].validation_date.strftime(
                "%Y-%m-%d %H:%M:%S"))
        self.browser.getLink("Reject courses").click()
        self.assertTrue('Course list request has been annulled.'
            in self.browser.contents)
        urlmessage = 'Course+list+request+has+been+annulled.'
        self.assertEqual(self.browser.url, self.student_path +
            '/contactstudent?subject=%s' % urlmessage)
        self.assertTrue('school fee paid' in self.browser.contents)
        self.assertTrue(self.student['studycourse']['110'].validated_by is None)
        self.assertTrue(self.student['studycourse']['110'].validation_date is None)
        IWorkflowInfo(self.student).fireTransition('register_courses')
        self.browser.open(L110_student_path)
        self.browser.getLink("Reject courses").click()
        self.assertTrue('Course list has been unregistered'
            in self.browser.contents)
        self.assertTrue('school fee paid' in self.browser.contents)
        # CA does now see the contact form and can send a message.
        self.browser.getControl(name="form.subject").value = 'Important subject'
        self.browser.getControl(name="form.body").value = 'Course list rejected'
        self.browser.getControl("Send message now").click()
        self.assertTrue('Your message has been sent' in self.browser.contents)
        # The CA does now see the Edit button and can edit
        # current study level.
        self.browser.open(L110_student_path)
        self.browser.getLink("Edit").click()
        self.assertTrue('Edit course list of 100 (Year 1) on 1st probation'
            in self.browser.contents)
        # The CA can't validate courses if not in state
        # courses registered.
        self.browser.open(L110_student_path + '/validate_courses')
        self.assertTrue('Student is in the wrong state'
            in self.browser.contents)
        # The CA can go to his certificate through the my_roles page ...
        self.browser.open('http://localhost/app/users/mrsadvise/my_roles')
        self.browser.getLink(
            "http://localhost/app/faculties/fac1/dep1/certificates/CERT1").click()
        # ... and view the list of students.
        self.browser.getLink("Show students").click()
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Show").click()
        self.assertTrue(self.student_id in self.browser.contents)

    def test_change_current_mode(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.clearance_path)
        self.assertFalse('Employer' in self.browser.contents)
        self.browser.open(self.manage_clearance_path)
        self.assertFalse('Employer' in self.browser.contents)
        self.browser.open(self.edit_clearance_path)
        self.assertFalse('Employer' in self.browser.contents)
        # Now we change the study mode of the certificate and a different
        # interface is used by clearance views.
        self.certificate.study_mode = 'pg_ft'
        # Invariants are not being checked here?!
        self.certificate.end_level = 100
        self.browser.open(self.clearance_path)
        self.assertTrue('Employer' in self.browser.contents)
        self.browser.open(self.manage_clearance_path)
        self.assertTrue('Employer' in self.browser.contents)
        IWorkflowState(self.student).setState('clearance started')
        self.browser.open(self.edit_clearance_path)
        self.assertTrue('Employer' in self.browser.contents)

    def test_find_students_in_faculties(self):
        # Create local students manager in faculty
        self.app['users'].addUser('mrmanager', SECRET)
        self.app['users']['mrmanager'].email = 'mrmanager@foo.ng'
        self.app['users']['mrmanager'].title = u'Volk Wagen'
        # Assign LocalStudentsManager role for faculty
        fac = self.app['faculties']['fac1']
        prmlocal = IPrincipalRoleManager(fac)
        prmlocal.assignRoleToPrincipal(
            'waeup.local.LocalStudentsManager', 'mrmanager')
        notify(LocalRoleSetEvent(
            fac, 'waeup.local.LocalStudentsManager', 'mrmanager',
            granted=True))
        # Login as manager
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrmanager'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        # Manager can see his roles
        self.browser.getLink("My Roles").click()
        self.assertMatches(
            '...<span>Students Manager</span>...',
            self.browser.contents)
        # The manager can go to his faculty
        self.browser.getLink(
            "http://localhost/app/faculties/fac1").click()
        # and find students
        self.browser.getLink("Find students").click()
        self.browser.getControl("Find student").click()
        self.assertTrue('Empty search string' in self.browser.contents)
        self.browser.getControl(name="searchtype").value = ['student_id']
        self.browser.getControl(name="searchterm").value = self.student_id
        self.browser.getControl("Find student").click()
        self.assertTrue('Anna Tester' in self.browser.contents)

    def test_activate_deactivate_buttons(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.student_path)
        self.browser.getLink("Deactivate").click()
        self.assertTrue(
            'Student account has been deactivated.' in self.browser.contents)
        self.assertTrue(
            'Base Data (account deactivated)' in self.browser.contents)
        self.assertTrue(self.student.suspended)
        self.browser.getLink("Activate").click()
        self.assertTrue(
            'Student account has been activated.' in self.browser.contents)
        self.assertFalse(
            'Base Data (account deactivated)' in self.browser.contents)
        self.assertFalse(self.student.suspended)
        # History messages have been added ...
        self.browser.getLink("History").click()
        self.assertTrue(
            'Student account deactivated by Manager<br />' in self.browser.contents)
        self.assertTrue(
            'Student account activated by Manager<br />' in self.browser.contents)
        # ... and actions have been logged.
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue('zope.mgr - students.browser.StudentDeactivateView - '
                        'K1000000 - account deactivated' in logcontent)
        self.assertTrue('zope.mgr - students.browser.StudentActivateView - '
                        'K1000000 - account activated' in logcontent)

    def test_manage_student_transfer(self):
        # Add second certificate
        self.certificate2 = createObject('waeup.Certificate')
        self.certificate2.code = u'CERT2'
        self.certificate2.study_mode = 'ug_ft'
        self.certificate2.start_level = 999
        self.certificate2.end_level = 999
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate2)

        # Add study level to old study course
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 200
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 999
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)

        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.student_path)
        self.browser.getLink("Transfer").click()
        self.browser.getControl(name="form.certificate").value = ['CERT2']
        self.browser.getControl(name="form.current_session").value = ['2011']
        self.browser.getControl(name="form.current_level").value = ['200']
        self.browser.getControl("Transfer").click()
        self.assertTrue(
            'Current level does not match certificate levels'
            in self.browser.contents)
        self.browser.getControl(name="form.current_level").value = ['999']
        self.browser.getControl("Transfer").click()
        self.assertTrue('Successfully transferred' in self.browser.contents)
        # The catalog has been updated
        cat = queryUtility(ICatalog, name='students_catalog')
        results = list(
            cat.searchResults(
            certcode=('CERT2', 'CERT2')))
        self.assertTrue(results[0] is self.student)
        results = list(
            cat.searchResults(
            current_session=(2011, 2011)))
        self.assertTrue(results[0] is self.student)
        # Add study level to new study course
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 999
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)

        # Edit and add pages are locked for old study courses
        self.browser.open(self.student_path + '/studycourse/manage')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/manage')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        self.browser.open(self.student_path + '/studycourse/start_session')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/start_session')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        IWorkflowState(self.student).setState('school fee paid')
        self.browser.open(self.student_path + '/studycourse/add')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/add')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        self.browser.open(self.student_path + '/studycourse/999/manage')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/999/manage')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        self.browser.open(self.student_path + '/studycourse/999/validate_courses')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/999/validate_courses')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        self.browser.open(self.student_path + '/studycourse/999/reject_courses')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/999/reject_courses')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        self.browser.open(self.student_path + '/studycourse/999/add')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/999/add')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        self.browser.open(self.student_path + '/studycourse/999/edit')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse_1/999/edit')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        # Revert transfer
        self.browser.open(self.student_path + '/studycourse_1')
        self.browser.getLink("Reactivate").click()
        self.browser.getControl("Revert now").click()
        self.assertTrue('Previous transfer reverted' in self.browser.contents)
        results = list(
            cat.searchResults(
            certcode=('CERT1', 'CERT1')))
        self.assertTrue(results[0] is self.student)
        self.assertEqual([i for i in self.student.keys()],
            [u'accommodation', u'payments', u'studycourse'])

    def test_login_as_student(self):
        # StudentImpersonators can login as student
        # Create clearance officer
        self.app['users'].addUser('mrofficer', SECRET)
        self.app['users']['mrofficer'].email = 'mrofficer@foo.ng'
        self.app['users']['mrofficer'].title = 'Harry Actor'
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.StudentImpersonator', 'mrofficer')
        prmglobal.assignRoleToPrincipal('waeup.StudentsManager', 'mrofficer')
        # Login as student impersonator
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrofficer'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        self.browser.open(self.student_path)
        self.browser.getLink("Login as").click()
        self.browser.getControl("Set password now").click()
        temp_password = self.browser.getControl(name='form.password').value
        self.browser.getControl("Login now").click()
        self.assertMatches(
            '...You successfully logged in as...', self.browser.contents)
        # We are logged in as student and can see the 'My Data' tab
        self.assertMatches(
            '...<a href="#" class="dropdown-toggle" data-toggle="dropdown">...',
            self.browser.contents)
        self.assertMatches(
            '...My Data...',
            self.browser.contents)
        self.browser.getLink("Logout").click()
        # The student can't login with the original password ...
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...Your account has been temporarily deactivated...',
            self.browser.contents)
        # ... but with the temporary password
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = temp_password
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        # Creation of temp_password is properly logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'mrofficer - students.browser.LoginAsStudentStep1 - K1000000 - '
            'temp_password generated: %s' % temp_password in logcontent)

    def test_transcripts(self):
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 100
        studylevel.level_session = 2005
        self.student['studycourse'].entry_mode = 'ug_ft'
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)
        studylevel2 = createObject(u'waeup.StudentStudyLevel')
        studylevel2.level = 110
        studylevel2.level_session = 2006
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel2)
        # Add second course (COURSE has been added automatically)
        courseticket = createObject('waeup.CourseTicket')
        courseticket.code = 'ANYCODE'
        courseticket.title = u'Any TITLE'
        courseticket.credits = 13
        courseticket.score = 66
        courseticket.semester = 1
        courseticket.dcode = u'ANYDCODE'
        courseticket.fcode = u'ANYFCODE'
        self.student['studycourse']['110']['COURSE2'] = courseticket
        self.student['studycourse']['100']['COURSE1'].score = 55
        self.assertEqual(self.student['studycourse']['100'].gpa_params_rectified[0], 3.0)
        self.assertEqual(self.student['studycourse']['110'].gpa_params_rectified[0], 4.0)
        # Get transcript data
        td = self.student['studycourse'].getTranscriptData()
        self.assertEqual(td[0][0]['level_key'], '100')
        self.assertEqual(td[0][0]['sgpa'], 3.0)
        self.assertEqual(td[0][0]['level'].level, 100)
        self.assertEqual(td[0][0]['level'].level_session, 2005)
        self.assertEqual(td[0][0]['tickets_1'][0].code, 'COURSE1')
        self.assertEqual(td[0][1]['level_key'], '110')
        self.assertEqual(td[0][1]['sgpa'], 4.0)
        self.assertEqual(td[0][1]['level'].level, 110)
        self.assertEqual(td[0][1]['level'].level_session, 2006)
        self.assertEqual(td[0][1]['tickets_1'][0].code, 'ANYCODE')
        self.assertEqual(td[1], 3.5652173913043477)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.student_path + '/studycourse/transcript')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertTrue('Transcript' in self.browser.contents)
        # Officers can open the pdf transcript
        self.browser.open(self.student_path + '/studycourse/transcript.pdf')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'transcript.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF transcript.pdf written to %s" % path

    def test_process_transcript(self):
        IWorkflowState(self.student).setState('graduated')
        notify(grok.ObjectModifiedEvent(self.student))
        self.student['studycourse'].transcript_comment = (
            u'On 07/08/2013 08:59:54 UTC K1000000 wrote:\n\nComment line 1 \n'
            'Comment line2\n\nDispatch Address:\nAddress line 1 \n'
            'Address line2\n\n')
        # Create officer with both roles
        self.app['users'].addUser('mrtranscript', SECRET)
        self.app['users']['mrtranscript'].email = 'mrtranscript@foo.ng'
        self.app['users']['mrtranscript'].title = 'Ruth Gordon'
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.TranscriptOfficer', 'mrtranscript')
        prmglobal.assignRoleToPrincipal('waeup.StudentsManager', 'mrtranscript')
        prmglobal.assignRoleToPrincipal('waeup.TranscriptSignee', 'mrtranscript')
        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrtranscript'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        # Officer can request transcript for students
        self.browser.open(self.student_path)
        self.browser.getLink("Request transcript for student").click()
        self.browser.getControl("Request now").click()
        self.assertEqual(self.student.state, 'transcript requested')
        # Officer can see his roles
        self.browser.getLink("My Roles").click()
        self.assertMatches(
            '...<div>Transcript Officer</div>...',
            self.browser.contents)
        # Officer can search for students in state 'transcript requested'
        self.browser.open(self.container_path)
        self.browser.getControl(name="searchtype").value = [
            'transcript requested']
        self.browser.getControl("Find student(s)").click()
        self.assertTrue('Anna Tester' in self.browser.contents)
        self.browser.getLink("K1000000").click()
        self.assertFalse('Release transcript request' in self.browser.contents)
        # Officers can still edit studycourse, studylevel and course tickets.
        self.browser.open(self.studycourse_path + '/manage')
        self.assertTrue('Undergraduate Full-Time</option>'
            in self.browser.contents)
        self.browser.getControl(name="form.certificate").value = ['CERT1']
        self.browser.getControl(name="form.current_session").value = ['2004']
        self.browser.getControl(name="form.current_verdict").value = ['A']
        self.browser.getControl(name="form.entry_mode").value = ['ug_ft']
        self.browser.getControl("Save").click()
        self.browser.getControl(name="form.current_level").value = ['100']
        self.browser.getControl("Save").click()
        self.browser.getControl(name="addlevel").value = ['100']
        self.browser.getControl(name="level_session").value = ['2004']
        self.browser.getControl("Add study level").click()
        self.browser.getLink("100").click()
        self.browser.getLink("Manage").click()
        self.browser.getControl(name="form.level_session").value = ['2002']
        self.browser.getControl("Save").click()
        self.browser.getLink("COURSE1").click()
        self.browser.getLink("Manage").click()
        self.browser.getControl("Save").click()
        self.assertTrue('Form has been saved' in self.browser.contents)
        # Officer can edit transcript remarks and validate the transcript
        self.browser.open(self.studycourse_path + '/transcript')
        self.browser.getLink("Validate transcript").click()
        self.browser.getLink("Edit").click()
        self.assertEqual(
            self.browser.url, self.studycourse_path + '/100/remark')
        self.browser.getControl(
            name="form.transcript_remark").value = 'Oh, the student failed'
        self.browser.getControl(
            "Save remark and go and back to transcript validation page").click()
        self.assertEqual(
            self.browser.url,
            self.studycourse_path + '/validate_transcript#tab4')
        self.assertEqual(self.student['studycourse']['100'].transcript_remark,
            'Oh, the student failed')
        self.browser.getControl("Save comment and validate transcript").click()
        # After validation all manage forms are locked.
        self.browser.open(self.studycourse_path + '/manage')
        self.assertTrue('The requested form is locked' in self.browser.contents)
        self.assertFalse('Undergraduate Full-Time</option>'
            in self.browser.contents)
        self.browser.open(self.studycourse_path + '/100/manage')
        self.assertTrue('The requested form is locked' in self.browser.contents)
        self.browser.open(self.studycourse_path + '/100/COURSE1/manage')
        self.assertTrue('The requested form is locked' in self.browser.contents)
        self.browser.open(self.studycourse_path + '/100/remark')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        # Transcript can be signed if officer has the permission to sign
        #self.browser.open(self.studycourse_path + '/transcript')
        #self.assertFalse('Sign transcript' in self.browser.contents)
        #prmglobal = IPrincipalRoleManager(self.app)
        #prmglobal.assignRoleToPrincipal('waeup.TranscriptSignee', 'mrtranscript')

        self.browser.open(self.studycourse_path + '/transcript')
        self.browser.getLink("Sign transcript electronically").click()
        # Transcript signing has been logged ...
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'mrtranscript - students.browser.StudentTranscriptSignView - '
            'K1000000 - Transcript signed' in logcontent)
        # ... appears in the student's history ...
        self.browser.open(self.history_path)
        self.assertTrue('Transcript signed by Ruth Gordon'
            in self.browser.contents)
        # ... and is also stored in the transcript_signee attribute.
        self.assertTrue(
            u'Electronically signed by Ruth Gordon (mrtranscript) on '
            in self.student['studycourse'].transcript_signees)
        # Officer can release the transcript
        self.browser.open(self.studycourse_path + '/transcript')
        self.browser.getLink("Release transcript").click()
        self.assertTrue(' UTC K1000000 wrote:<br><br>Comment line 1 <br>'
        'Comment line2<br><br>Dispatch Address:<br>Address line 1 <br>'
        'Address line2<br><br></p>' in self.browser.contents)
        self.browser.getControl(name="comment").value = (
            'Hello,\nYour transcript has been sent to the address provided.')
        self.browser.getControl("Save comment and release transcript").click()
        self.assertTrue(
            'UTC mrtranscript wrote:\n\nHello,\nYour transcript has '
            'been sent to the address provided.\n\n'
            in self.student['studycourse'].transcript_comment)
        # The comment has been logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'mrtranscript - students.browser.StudentTranscriptReleaseFormPage - '
            'K1000000 - comment: Hello,<br>'
            'Your transcript has been sent to the address provided'
            in logcontent)
        # File has been stored in the file system
        # Check if transcript exists in the file system and is a PDF file
        storage = getUtility(IExtFileStore)
        file_id = IFileStoreNameChooser(
            self.student).chooseName(attr='final_transcript.pdf')
        pdf = storage.getFile(file_id).read()
        self.assertTrue(len(pdf) > 0)
        self.assertEqual(pdf[:8], '%PDF-1.4')
        # Copy the file to samples_dir
        path = os.path.join(samples_dir(), 'final_transcript.pdf')
        open(path, 'wb').write(pdf)
        print "Sample PDF final_transcript.pdf written to %s" % path
        # Check if there is an transcript pdf link in UI
        self.browser.open(self.student_path)
        self.assertTrue('Final Transcript' in self.browser.contents)
        self.browser.getLink("Final Transcript").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        # Transcript views are no longer accessible
        self.browser.open(self.studycourse_path)
        self.assertFalse('studycourse/transcript' in self.browser.contents)
        self.browser.open(self.studycourse_path + '/transcript')
        self.assertTrue('Forbidden!' in self.browser.contents)
        self.browser.open(self.studycourse_path + '/transcript.pdf')
        self.assertTrue('Forbidden!' in self.browser.contents)
        # If we reset the transcript process
        # (can't be done by transcript officer), the file will be deleted
        IWorkflowInfo(self.student).fireTransition('reset11')
        self.browser.open(self.student_path)
        self.assertFalse('Final Transcript' in self.browser.contents)
        # ... and transcript process information has been removed
        self.assertEqual(self.student['studycourse'].transcript_comment, None)
        self.assertEqual(self.student['studycourse'].transcript_signees, None)

    def createTranscriptApplications(self):
        # We create transcript application containers tscs1 and tscf2019
        applicantscontainer1 = ApplicantsContainer()
        applicantscontainer1.code = u'tscs1'
        applicantscontainer1.prefix = u'app'
        applicantscontainer1.year = 2020
        applicantscontainer1.title = u'This is the TSC container'
        applicantscontainer1.application_category = 'no'
        applicantscontainer1.mode = 'create'
        self.app['applicants']['tscs1'] = applicantscontainer1
        applicantscontainer2 = ApplicantsContainer()
        applicantscontainer2.code = u'tscf2020'
        applicantscontainer2.prefix = u'app'
        applicantscontainer2.year = 2020
        applicantscontainer2.title = u'This is the TSC container'
        applicantscontainer2.application_category = 'no'
        applicantscontainer2.mode = 'create'
        self.app['applicants']['tscf2020'] = applicantscontainer2
        # Add applicants
        self.applicant1 = createObject('waeup.Applicant')
        self.applicant1.firstname = u'Joanne'
        self.applicant1.lastname = u'Abba'
        self.applicant1.course_studied = self.certificate
        IWorkflowState(self.applicant1).setState('submitted')
        self.app['applicants']['tscs1'].addApplicant(self.applicant1)
        self.applicant2 = createObject('waeup.Applicant')
        self.applicant2.firstname = u'Josef'
        self.applicant2.lastname = u'Abba'
        self.applicant2.course_studied = self.certificate
        IWorkflowState(self.applicant2).setState('submitted')
        self.app['applicants']['tscf2020'].addApplicant(self.applicant2)

    def test_landingpage_transcript_officer(self):
        IWorkflowState(self.student).setState('transcript requested')
        notify(grok.ObjectModifiedEvent(self.student))
        # Create transcript officer
        self.app['users'].addUser('mrtranscript', SECRET)
        self.app['users']['mrtranscript'].email = 'mrtranscript@foo.ng'
        self.app['users']['mrtranscript'].title = 'Ruth Gordon'
        # We assign transcript officer role at faculty level
        fac = self.app['faculties']['fac1']
        prmlocal = IPrincipalRoleManager(fac)
        prmlocal.assignRoleToPrincipal(
            'waeup.local.TranscriptOfficer', 'mrtranscript')
        notify(LocalRoleSetEvent(
            fac, 'waeup.local.TranscriptOfficer', 'mrtranscript', granted=True))
        self.createTranscriptApplications()
        # Login as transcript officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrtranscript'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        # Officers do see the transcript applicants
        self.assertTrue(
            '<td>Josef Abba</td>' in self.browser.contents)
        self.assertTrue(
            '<td>Joanne Abba</td>' in self.browser.contents)
        # Officer is on landing page and does see the transcript link
        self.assertTrue(
            'http://localhost/app/students/K1000000/studycourse/transcript'
            in self.browser.contents)
        self.browser.getLink("K1000000").click()
        self.assertTrue(
            'Anna Tester: Transcript Data' in self.browser.contents)
        # Officer is on transcript page and can validate the transcript
        self.browser.getLink("Validate transcript").click()
        self.browser.getControl("Save comment and validate transcript").click()
        self.assertTrue(
            '<div class="alert alert-success">Transcript validated.</div>'
            in self.browser.contents)
        # Officer is still on transcript page and can release the transcript
        self.browser.getLink("Release transcript").click()
        self.browser.getControl("Save comment and release transcript").click()
        self.assertTrue(
            '<div class="alert alert-success">'
            'Transcript released and final transcript file saved.</div>'
            in self.browser.contents)

    def test_landingpage_transcript_signee(self):
        IWorkflowState(self.student).setState('transcript validated')
        notify(grok.ObjectModifiedEvent(self.student))
        # Create transcript signee
        self.app['users'].addUser('mrtranscript', SECRET)
        self.app['users']['mrtranscript'].email = 'mrtranscript@foo.ng'
        self.app['users']['mrtranscript'].title = 'Ruth Gordon'
        # We assign transcript officer role at faculty level
        fac = self.app['faculties']['fac1']
        prmlocal = IPrincipalRoleManager(fac)
        prmlocal.assignRoleToPrincipal(
            'waeup.local.TranscriptSignee', 'mrtranscript')
        notify(LocalRoleSetEvent(
            fac, 'waeup.local.TranscriptSignee', 'mrtranscript', granted=True))
        # Login as transcript officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrtranscript'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        # Officer is on landing page and does see the transcript link
        self.assertTrue(
            'http://localhost/app/students/K1000000/studycourse/transcript'
            in self.browser.contents)
        self.browser.getLink("K1000000").click()
        self.assertTrue(
            'Anna Tester: Transcript Data' in self.browser.contents)
        # Officer is on transcript page and can sign the transcript
        self.browser.getLink("Sign transcript").click()
        self.assertTrue(
            '<div class="alert alert-success">Transcript signed.</div>'
            in self.browser.contents)
        # Officer is still on transcript page
        self.assertTrue(
            'Anna Tester: Transcript Data' in self.browser.contents)
        # Officer can sign the transcript only once
        self.browser.getLink("Sign transcript").click()
        self.assertTrue(
            '<div class="alert alert-warning">'
            'You have already signed this transcript.</div>'
            in self.browser.contents)
        # Signature can be seen on transcript page
        self.assertTrue(
            'Electronically signed by Ruth Gordon (mrtranscript) on'
            in self.browser.contents)

    def test_update_coursetickets(self):
        IWorkflowState(self.student).setState('school fee paid')
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 100
        studylevel.level_session = 2015
        self.student['studycourse'].entry_mode = 'ug_ft'
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(
            'http://localhost/app/faculties/fac1/dep1/courses/COURSE1/')
        self.assertFalse(
            'Update session 2015/2016 credits' in self.browser.contents)
        self.app['configuration'].current_academic_session = 2015
        self.browser.open(
            'http://localhost/app/faculties/fac1/dep1/courses/COURSE1/')
        self.browser.getLink("Update session 2015/2016 credits").click()
        self.assertTrue(
            'No course ticket found.' in self.browser.contents)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - browser.pages.UpdateCourseTicketsView - '
            'course tickets updated: COURSE1' in logcontent)
        studylevel['COURSE1'].credits = 12
        self.browser.getLink("Update session 2015/2016 credits").click()
        self.assertTrue(
            'No course ticket found.' in self.browser.contents)
        studylevel.level_session = 2015
        self.student['studycourse'].current_session = 2015
        self.browser.getLink("Update session 2015/2016 credits").click()
        self.assertTrue(
            '1 course ticket(s) updated.' in self.browser.contents)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.utils.StudentsUtils - '
            'K1000000 100/COURSE1 credits updated (10->12)' in logcontent)
        return


class StudentUITests(StudentsFullSetup):
    # Tests for Student class views and pages

    def test_student_change_password(self):
        # Students can change the password
        self.student.personal_updated = datetime.utcnow()
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertEqual(self.browser.url, self.student_path)
        self.assertTrue('You logged in' in self.browser.contents)
        # Change password
        self.browser.getLink("Change password").click()
        self.browser.getControl(name="change_password").value = 'pw'
        self.browser.getControl(
            name="change_password_repeat").value = 'pw'
        self.browser.getControl("Save").click()
        self.assertTrue('Password must have at least' in self.browser.contents)
        self.browser.getControl(name="change_password").value = 'new_password'
        self.browser.getControl(
            name="change_password_repeat").value = 'new_passssword'
        self.browser.getControl("Save").click()
        self.assertTrue('Passwords do not match' in self.browser.contents)
        self.browser.getControl(name="change_password").value = 'new_password'
        self.browser.getControl(
            name="change_password_repeat").value = 'new_password'
        self.browser.getControl("Save").click()
        self.assertTrue('Password changed' in self.browser.contents)
        # We are still logged in. Changing the password hasn't thrown us out.
        self.browser.getLink("Base Data").click()
        self.assertEqual(self.browser.url, self.student_path)
        # We can logout
        self.browser.getLink("Logout").click()
        self.assertTrue('You have been logged out' in self.browser.contents)
        self.assertEqual(self.browser.url, 'http://localhost/app/index')
        # We can login again with the new password
        self.browser.getLink("Login").click()
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'new_password'
        self.browser.getControl("Login").click()
        self.assertEqual(self.browser.url, self.student_path)
        self.assertTrue('You logged in' in self.browser.contents)
        return

    def test_forbidden_name(self):
        self.student.lastname = u'<TAG>Tester</TAG>'
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.browser.getLink("Base Data").click()
        self.assertTrue('XXX: Base Data' in self.browser.contents)
        self.assertTrue('&lt;TAG&gt;Tester&lt;/TAG&gt;' in self.browser.contents)
        self.assertFalse('<TAG>Tester</TAG>' in self.browser.contents)
        return

    def test_setpassword(self):
        # Set password for first-time access
        student = Student()
        student.reg_number = u'123456'
        student.firstname = u'Klaus'
        student.lastname = u'Tester'
        self.app['students'].addStudent(student)
        setpassword_path = 'http://localhost/app/setpassword'
        student_path = 'http://localhost/app/students/%s' % student.student_id
        self.browser.open(setpassword_path)
        self.browser.getControl(name="ac_series").value = self.existing_pwdseries
        self.browser.getControl(name="ac_number").value = self.existing_pwdnumber
        self.browser.getControl(name="reg_number").value = '223456'
        self.browser.getControl("Set").click()
        self.assertMatches('...No student found...',
                           self.browser.contents)
        self.browser.getControl(name="reg_number").value = '123456'
        self.browser.getControl(name="ac_number").value = '999999'
        self.browser.getControl("Set").click()
        self.assertMatches('...Access code is invalid...',
                           self.browser.contents)
        self.browser.getControl(name="ac_number").value = self.existing_pwdnumber
        self.browser.getControl("Set").click()
        self.assertMatches('...Password has been set. Your Student Id is...',
                           self.browser.contents)
        self.browser.getControl("Set").click()
        self.assertMatches(
            '...Password has already been set. Your Student Id is...',
            self.browser.contents)
        existing_pwdpin = self.pwdpins[1]
        parts = existing_pwdpin.split('-')[1:]
        existing_pwdseries, existing_pwdnumber = parts
        self.browser.getControl(name="ac_series").value = existing_pwdseries
        self.browser.getControl(name="ac_number").value = existing_pwdnumber
        self.browser.getControl(name="reg_number").value = '123456'
        self.browser.getControl("Set").click()
        self.assertMatches(
            '...You are using the wrong Access Code...',
            self.browser.contents)
        # The student can login with the new credentials
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = student.student_id
        self.browser.getControl(
            name="form.password").value = self.existing_pwdnumber
        self.browser.getControl("Login").click()
        self.assertEqual(self.browser.url, student_path + '/edit_personal')
        self.assertTrue('You logged in' in self.browser.contents)
        return

    def test_student_login(self):
        # Student cant login if their password is not set
        self.student.password = None
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertTrue(
            'You entered invalid credentials.' in self.browser.contents)
        # We set the password again
        IUserAccount(
            self.app['students'][self.student_id]).setPassword('spwd')
        # Students can't login if their account is suspended/deactivated
        self.student.suspended = True
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...<div class="alert alert-warning">'
            'Your account has been deactivated.</div>...', self.browser.contents)
        # If suspended_comment is set this message will be flashed instead
        self.student.suspended_comment = u'Aetsch baetsch!'
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...<div class="alert alert-warning">Aetsch baetsch!</div>...',
            self.browser.contents)
        self.student.suspended = False
        # Students can't login if a temporary password has been set and
        # is not expired
        self.app['students'][self.student_id].setTempPassword(
            'anybody', 'temp_spwd')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...Your account has been temporarily deactivated...',
            self.browser.contents)
        # The student can login with the temporary password
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'temp_spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...You logged in...', self.browser.contents)
        # Student can view the base data
        self.browser.open(self.student_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.student_path)
        # When the password expires ...
        delta = timedelta(minutes=11)
        self.app['students'][self.student_id].temp_password[
            'timestamp'] = datetime.utcnow() - delta
        self.app['students'][self.student_id]._p_changed = True
        # ... the student will be automatically logged out
        self.assertRaises(
            Unauthorized, self.browser.open, self.student_path)
        # Then the student can login with the original password
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...You logged in...', self.browser.contents)

    def test_maintenance_mode(self):
        config = grok.getSite()['configuration']
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Student logged in.
        self.assertTrue('You logged in' in self.browser.contents)
        self.assertTrue("Anna Tester" in self.browser.contents)
        # If maintenance mode is enabled, student is immediately logged out.
        config.maintmode_enabled_by = u'any_user'
        self.assertRaises(
            Unauthorized, self.browser.open, 'http://localhost/app/faculties')
        self.browser.open('http://localhost/app/login')
        self.assertTrue('The portal is in maintenance mode' in self.browser.contents)
        # Student really can't login if maintenance mode is enabled.
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # A second warning is raised.
        self.assertTrue(
            'The portal is in maintenance mode. You can\'t login!'
            in self.browser.contents)
        return

    def test_student_studycourse_slip(self):
        IWorkflowState(self.student).setState('school fee paid')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Students can open study course base data slip
        # (no button available in base package)
        pdf_url = '%s/studycourse_slip.pdf' % self.studycourse_path
        self.browser.open(pdf_url)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'studycourse_slip.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF studycourse_slip.pdf written to %s" % path

    def test_student_personal_slip(self):
        IWorkflowState(self.student).setState('school fee paid')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Students can personal data slip
        # (no button available in base package)
        pdf_url = '%s/personal_slip.pdf' % self.student_path
        self.browser.open(pdf_url)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'personal_slip.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF personal_slip.pdf written to %s" % path

    def test_student_clearance(self):
        # Student cant login if their password is not set
        IWorkflowInfo(self.student).fireTransition('admit')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...You logged in...', self.browser.contents)
        # Admitted student can upload a passport picture
        self.browser.open(self.student_path + '/change_portrait')
        ctrl = self.browser.getControl(name='passportuploadedit')
        file_obj = open(SAMPLE_IMAGE, 'rb')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file_obj, filename='my_photo.jpg')
        self.browser.getControl(
            name='upload_passportuploadedit').click()
        self.assertTrue(
            'src="http://localhost/app/students/K1000000/passport.jpg"'
            in self.browser.contents)
        # Students can open admission letter
        self.browser.getLink("Base Data").click()
        self.browser.getLink("Download admission letter").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'admission_slip.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF admission_slip.pdf written to %s" % path
        # Student can view the clearance data
        self.browser.open(self.student_path)
        self.browser.getLink("Clearance Data").click()
        # Student can't open clearance edit form before starting clearance
        self.browser.open(self.student_path + '/cedit')
        self.assertMatches('...The requested form is locked...',
                           self.browser.contents)
        self.browser.getLink("Clearance Data").click()
        self.browser.getLink("Start clearance").click()
        self.student.phone = None
        # Uups, we forgot to fill the phone fields
        self.browser.getControl("Start clearance").click()
        self.assertMatches('...Phone number is missing...',
                           self.browser.contents)
        self.browser.open(self.student_path + '/edit_base')
        self.browser.getControl(name="form.phone.ext").value = '12345'
        self.browser.getControl("Save").click()
        self.browser.open(self.student_path + '/start_clearance')
        self.browser.getControl(name="ac_series").value = '3'
        self.browser.getControl(name="ac_number").value = '4444444'
        self.browser.getControl("Start clearance now").click()
        self.assertMatches('...Activation code is invalid...',
                           self.browser.contents)
        self.browser.getControl(name="ac_series").value = self.existing_clrseries
        self.browser.getControl(name="ac_number").value = self.existing_clrnumber
        # Owner is Hans Wurst, AC can't be invalidated
        self.browser.getControl("Start clearance now").click()
        self.assertMatches('...You are not the owner of this access code...',
                           self.browser.contents)
        # Set the correct owner
        self.existing_clrac.owner = self.student_id
        # clr_code might be set (and thus returns None) due importing
        # an empty clr_code column.
        self.student.clr_code = None
        self.browser.getControl("Start clearance now").click()
        self.assertMatches('...Clearance process has been started...',
                           self.browser.contents)
        self.browser.getControl(name="form.date_of_birth").value = '09/10/1961'
        self.browser.getControl("Save", index=0).click()
        # Student can view the clearance data
        self.browser.getLink("Clearance Data").click()
        # and go back to the edit form
        self.browser.getLink("Edit").click()
        # Students can upload documents
        ctrl = self.browser.getControl(name='birthcertificateupload')
        file_obj = open(SAMPLE_IMAGE, 'rb')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file_obj, filename='my_birth_certificate.jpg')
        self.browser.getControl(
            name='upload_birthcertificateupload').click()
        self.assertTrue(
            'href="http://localhost/app/students/K1000000/birth_certificate"'
            in self.browser.contents)
        # Students can open clearance slip
        self.browser.getLink("View").click()
        self.browser.getLink("Download clearance slip").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        # Students can request clearance
        self.browser.open(self.edit_clearance_path)
        self.browser.getControl("Save and request clearance").click()
        self.browser.getControl(name="ac_series").value = self.existing_clrseries
        self.browser.getControl(name="ac_number").value = self.existing_clrnumber
        self.browser.getControl("Request clearance now").click()
        self.assertMatches('...Clearance has been requested...',
                           self.browser.contents)
        # Student can't reopen clearance form after requesting clearance
        self.browser.open(self.student_path + '/cedit')
        self.assertMatches('...The requested form is locked...',
                           self.browser.contents)

    def test_student_course_registration(self):
        # Student cant login if their password is not set
        IWorkflowInfo(self.student).fireTransition('admit')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Student can't add study level if not in state 'school fee paid'
        self.browser.open(self.student_path + '/studycourse/add')
        self.assertMatches('...The requested form is locked...',
                           self.browser.contents)
        # ... and must be transferred first
        IWorkflowState(self.student).setState('school fee paid')
        # Now students can add the current study level
        self.browser.getLink("Study Course").click()
        self.student['studycourse'].current_level = None
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Your data are incomplete...',
                           self.browser.contents)
        self.student['studycourse'].current_level = 100
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 100 (Year 1)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        # A level with one course ticket was created
        self.assertEqual(self.student['studycourse']['100'].number_of_tickets, 1)
        self.browser.getLink("100").click()
        self.browser.getLink("Edit course list").click()
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.browser.getControl("Add course ticket").click()
        self.assertMatches('...The ticket exists...',
                           self.browser.contents)
        self.student['studycourse'].current_level = 200
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 200 (Year 2)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        self.browser.getLink("200").click()
        self.browser.getLink("Edit course list").click()
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.course.credits = 100
        self.browser.getControl("Add course ticket").click()
        self.assertMatches(
            '...Maximum credits exceeded...', self.browser.contents)
        self.course.credits = 10
        self.browser.getControl("Add course ticket").click()
        self.assertMatches('...The ticket exists...',
                           self.browser.contents)
        # Indeed the ticket exists as carry-over course from level 100
        # since its score was 0
        self.assertTrue(
            self.student['studycourse']['200']['COURSE1'].carry_over is True)
        self.assertTrue(
            self.student['studycourse']['200']['COURSE1'].course_category is None)
        # Students can open the pdf course registration slip
        self.browser.open(self.student_path + '/studycourse/200')
        self.browser.getLink("Download course registration slip").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'course_registration_slip.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF course_registration_slip.pdf written to %s" % path
        # Students can remove course tickets
        self.browser.open(self.student_path + '/studycourse/200/edit')
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('No ticket selected' in self.browser.contents)
        # No ticket can be selected since the carry-over course is a core course
        self.assertRaises(
            LookupError, self.browser.getControl, name='val_id')
        self.student['studycourse']['200']['COURSE1'].mandatory = False
        self.browser.open(self.student_path + '/studycourse/200/edit')
        # Course list can't be registered if total_credits exceeds max_credits
        self.student['studycourse']['200']['COURSE1'].credits = 60
        self.browser.getControl("Register course list").click()
        self.assertTrue('Maximum credits exceeded' in self.browser.contents)
        # Student can now remove the ticket
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value='COURSE1').selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)
        # Removing course tickets is properly logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue('K1000000 - students.browser.StudyLevelEditFormPage '
        '- K1000000 - level 200 - removed: COURSE1' in logcontent)
        # They can add the same ticket using the edit page directly.
        # We can do the same by adding the course on the manage page directly
        self.browser.getControl(name="course").value = 'COURSE1'
        self.browser.getControl("Add course ticket").click()
        # Adding course tickets is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue('K1000000 - students.browser.StudyLevelEditFormPage - '
            'K1000000 - level 200 - added: COURSE1|200|2004' in logcontent)
        # Course list can be registered
        self.browser.getControl("Register course list").click()
        self.assertTrue('Course list has been registered' in self.browser.contents)
        self.assertEqual(self.student.state, 'courses registered')
        # Course list can be unregistered
        self.browser.getLink("Unregister courses").click()
        self.assertEqual(self.student.state, 'school fee paid')
        self.assertTrue('Course list has been unregistered' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse/200/unregister_courses')
        self.assertTrue('You are in the wrong state' in self.browser.contents)
        # Students can view the transcript
        #self.browser.open(self.studycourse_path)
        #self.browser.getLink("Transcript").click()
        #self.browser.getLink("Academic Transcript").click()
        #self.assertEqual(self.browser.headers['Status'], '200 Ok')
        #self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        return

    def test_student_ticket_update(self):
        IWorkflowState(self.student).setState('school fee paid')
        self.student['studycourse'].current_level = 100
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Now students can add the current study level
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 100 (Year 1)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        # A level with one course ticket was created
        self.assertEqual(
            self.student['studycourse']['100'].number_of_tickets, 1)
        self.browser.getLink("100").click()
        self.assertTrue('<td>Unnamed Course</td>' in self.browser.contents)
        self.browser.getLink("Edit course list").click()
        self.browser.getControl("Update all tickets").click()
        self.assertTrue('All course tickets updated.' in self.browser.contents)
        # ... nothing has changed
        self.assertTrue('<td>Unnamed Course</td>' in self.browser.contents)
        # We change the title of the course
        self.course.title = u'New Title'
        self.browser.getControl("Update all tickets").click()
        self.assertTrue('<td>New Title</td>' in self.browser.contents)
        # We remove the course
        del self.app['faculties']['fac1']['dep1'].courses['COURSE1']
        self.browser.getControl("Update all tickets").click()
        self.assertTrue(' <td>New Title (course cancelled)</td>'
            in self.browser.contents)
        # Course ticket invalidation has been logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'K1000000 - students.browser.StudyLevelEditFormPage - '
            'K1000000 - level 100 - course tickets invalidated: COURSE1'
            in logcontent)
        return

    def test_student_course_already_passed(self):
        IWorkflowState(self.student).setState('school fee paid')
        self.student['studycourse'].current_level = 100
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Now students can add the current study level
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 100 (Year 1)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        # A level with one course ticket was created
        self.assertEqual(self.student['studycourse']['100'].number_of_tickets, 1)
        # We set the score above the passmark
        self.student['studycourse']['100'][
            'COURSE1'].score = self.student['studycourse']['100'][
                'COURSE1'].passmark + 1
        # We add a second level
        self.student['studycourse'].current_level = 200
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 200 (Year 2)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        self.browser.getLink("200").click()
        self.browser.getLink("Edit course list").click()
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.browser.getControl("Add course ticket").click()
        self.assertTrue(
            'Course has already been passed at previous level'
            in self.browser.contents)
        self.assertEqual(self.student['studycourse']['200'].number_of_tickets, 0)
        # We set the score below the passmark
        self.student['studycourse']['100'][
            'COURSE1'].score = self.student['studycourse']['100'][
                'COURSE1'].passmark - 1
        self.browser.getControl("Add course ticket").click()
        self.assertTrue(
            'Successfully added COURSE1' in self.browser.contents)
        self.assertEqual(self.student['studycourse']['200'].number_of_tickets, 1)
        return

    def test_student_course_registration_outstanding(self):
        self.course = createObject('waeup.Course')
        self.course.code = 'COURSE2'
        self.course.semester = 1
        self.course.credits = 45
        self.course.passmark = 40
        self.app['faculties']['fac1']['dep1'].courses.addCourse(
            self.course)
        IWorkflowState(self.student).setState('school fee paid')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.browser.open(self.student_path + '/studycourse/add')
        self.browser.getControl("Create course list now").click()
        self.assertEqual(self.student['studycourse']['100'].number_of_tickets, 1)
        self.student['studycourse'].current_level = 200
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 200 (Year 2)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        self.browser.getLink("200").click()
        self.browser.getLink("Edit course list").click()
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE2']
        self.browser.getControl("Add course ticket").click()
        # Carryover COURSE1 in level 200 already has 10 credits
        self.assertMatches(
            '...Maximum credits exceeded...', self.browser.contents)
        # If COURSE1 is outstanding, its credits won't be considered
        self.student['studycourse']['200']['COURSE1'].outstanding = True
        self.browser.getControl("Add course ticket").click()
        self.assertMatches(
            '...Successfully added COURSE2...', self.browser.contents)
        return

    def test_postgraduate_student_access(self):
        self.certificate.study_mode = 'pg_ft'
        self.certificate.start_level = 999
        self.certificate.end_level = 999
        self.student['studycourse'].current_level = 999
        IWorkflowState(self.student).setState('school fee paid')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertTrue(
            'You logged in as a student.' in self.browser.contents)
        # Now students can add the current study level
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level Postgraduate Level...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        self.assertTrue("You successfully created a new course list"
            in self.browser.contents)
        # A level with one course ticket was created
        self.assertEqual(self.student['studycourse']['999'].number_of_tickets, 0)
        self.browser.getLink("Edit course list").click()
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.browser.getControl("Add course ticket").click()
        self.assertMatches('...Successfully added COURSE1...',
                           self.browser.contents)
        # Postgraduate students can't register course lists
        self.browser.getControl("Register course list").click()
        self.assertTrue("your course list can't bee registered"
            in self.browser.contents)
        self.assertEqual(self.student.state, 'school fee paid')
        return

    def test_student_clearance_wo_clrcode(self):
        IWorkflowState(self.student).setState('clearance started')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.browser.open(self.edit_clearance_path)
        self.browser.getControl(name="form.date_of_birth").value = '09/10/1961'
        self.browser.getControl("Save and request clearance").click()
        self.assertMatches('...Clearance has been requested...',
                           self.browser.contents)

    def test_student_clearance_payment(self):
        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()

        # Students can add online clearance payment tickets
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['clearance']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)

        # Students can't approve the payment
        self.assertEqual(len(self.app['accesscodes']['CLR-0']),0)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        payment_url = self.browser.url
        self.assertRaises(
            Unauthorized, self.browser.open, payment_url + '/approve')
        # In the base package they can 'use' a fake approval view.
        # XXX: I tried to use
        # self.student['payments'][value].approveStudentPayment() instead.
        # But this function fails in
        # w.k.accesscodes.accesscode.create_accesscode.
        # grok.getSite returns None in tests.
        self.browser.open(payment_url + '/fake_approve')
        self.assertMatches('...Payment approved...',
                          self.browser.contents)
        expected = '''...
        <td>
          <span>Paid</span>
        </td>...'''
        expected = '''...
        <td>
          <span>Paid</span>
        </td>...'''
        self.assertMatches(expected,self.browser.contents)
        payment_id = self.student['payments'].keys()[0]
        payment = self.student['payments'][payment_id]
        self.assertEqual(payment.p_state, 'paid')
        self.assertEqual(payment.r_amount_approved, 3456.0)
        self.assertEqual(payment.r_code, 'AP')
        self.assertEqual(payment.r_desc, u'Payment approved by Anna Tester')
        # The new CLR-0 pin has been created
        self.assertEqual(len(self.app['accesscodes']['CLR-0']),1)
        pin = self.app['accesscodes']['CLR-0'].keys()[0]
        ac = self.app['accesscodes']['CLR-0'][pin]
        self.assertEqual(ac.owner, self.student_id)
        self.assertEqual(ac.cost, 3456.0)

        # Students can open the pdf payment slip
        self.browser.open(payment_url + '/payment_slip.pdf')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')

        # The new CLR-0 pin can be used for starting clearance
        # but they have to upload a passport picture first
        # which is only possible in state admitted
        self.browser.open(self.student_path + '/change_portrait')
        self.assertMatches('...form is locked...',
                          self.browser.contents)
        IWorkflowInfo(self.student).fireTransition('admit')
        self.browser.open(self.student_path + '/change_portrait')
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='passportuploadedit')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='my_photo.jpg')
        self.browser.getControl(
            name='upload_passportuploadedit').click()
        self.browser.open(self.student_path + '/start_clearance')
        parts = pin.split('-')[1:]
        clrseries, clrnumber = parts
        self.browser.getControl(name="ac_series").value = clrseries
        self.browser.getControl(name="ac_number").value = clrnumber
        self.browser.getControl("Start clearance now").click()
        self.assertMatches('...Clearance process has been started...',
                           self.browser.contents)

    def test_student_schoolfee_payment(self):
        configuration = createObject('waeup.SessionConfiguration')
        configuration.academic_session = 2005
        self.app['configuration'].addSessionConfiguration(configuration)
        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()

        # Students can add online school fee payment tickets.
        IWorkflowState(self.student).setState('returning')
        self.browser.open(self.payments_path)
        self.assertRaises(
            LookupError, self.browser.getControl, name='val_id')
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...Amount Authorized...',
                           self.browser.contents)
        self.assertEqual(self.student['payments'][value].amount_auth, 20000.0)
        # Payment session and will be calculated as defined
        # in w.k.students.utils because we set changed the state
        # to returning
        self.assertEqual(self.student['payments'][value].p_session, 2005)
        self.assertEqual(self.student['payments'][value].p_level, 200)

        # Student is the payer of the payment ticket.
        payer = IPayer(self.student['payments'][value])
        self.assertEqual(payer.payer, self.student)
        self.assertEqual(payer.display_fullname, 'Anna Tester')
        self.assertEqual(payer.id, self.student_id)
        self.assertEqual(payer.faculty, 'fac1')
        self.assertEqual(payer.department, 'dep1')

        # We simulate the approval
        self.assertEqual(len(self.app['accesscodes']['SFE-0']),0)
        self.browser.open(self.browser.url + '/fake_approve')
        self.assertMatches('...Payment approved...',
                          self.browser.contents)

        ## The new SFE-0 pin can be used for starting new session
        #self.browser.open(self.studycourse_path)
        #self.browser.getLink('Start new session').click()
        #pin = self.app['accesscodes']['SFE-0'].keys()[0]
        #parts = pin.split('-')[1:]
        #sfeseries, sfenumber = parts
        #self.browser.getControl(name="ac_series").value = sfeseries
        #self.browser.getControl(name="ac_number").value = sfenumber
        #self.browser.getControl("Start now").click()
        #self.assertMatches('...Session started...',
        #                   self.browser.contents)

        self.assertTrue(self.student.state == 'school fee paid')
        return

    def test_student_bedallocation_payment(self):
        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.browser.open(self.payments_path)
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['bed_allocation']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        # Students can remove only online payment tickets which have
        # not received a valid callback
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        ctrl.getControl(value=value).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed' in self.browser.contents)

    def test_student_maintenance_payment(self):
        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.browser.open(self.payments_path)
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['hostel_maintenance']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...You have not yet booked accommodation...',
                           self.browser.contents)
        # We continue this test in test_student_accommodation

    def test_student_previous_payments(self):
        configuration = createObject('waeup.SessionConfiguration')
        configuration.academic_session = 2000
        configuration.clearance_fee = 3456.0
        configuration.booking_fee = 123.4
        self.app['configuration'].addSessionConfiguration(configuration)
        configuration2 = createObject('waeup.SessionConfiguration')
        configuration2.academic_session = 2003
        configuration2.clearance_fee = 3456.0
        configuration2.booking_fee = 123.4
        self.app['configuration'].addSessionConfiguration(configuration2)
        configuration3 = createObject('waeup.SessionConfiguration')
        configuration3.academic_session = 2005
        configuration3.clearance_fee = 3456.0
        configuration3.booking_fee = 123.4
        self.app['configuration'].addSessionConfiguration(configuration3)
        self.student['studycourse'].entry_session = 2002

        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()

        # Students can add previous school fee payment tickets in any state.
        IWorkflowState(self.student).setState('courses registered')
        self.browser.open(self.payments_path)
        self.browser.getLink("Add previous session payment ticket").click()

        # Previous session payment form is provided
        self.assertEqual(self.student.current_session, 2004)
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl(name="form.p_session").value = ['2000']
        self.browser.getControl(name="form.p_level").value = ['300']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...The previous session must not fall below...',
                           self.browser.contents)
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl(name="form.p_session").value = ['2005']
        self.browser.getControl(name="form.p_level").value = ['300']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...This is not a previous session...',
                           self.browser.contents)

        # Students can pay current session school fee.
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl(name="form.p_session").value = ['2004']
        self.browser.getControl(name="form.p_level").value = ['300']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...Amount Authorized...',
                           self.browser.contents)
        self.assertEqual(self.student['payments'][value].amount_auth, 20000.0)

        # Ticket creation is logged.
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'K1000000 - students.browser.PreviousPaymentAddFormPage - '
            'K1000000 - added: %s' % value
            in logcontent)

        # Payment session is properly set
        self.assertEqual(self.student['payments'][value].p_session, 2004)
        self.assertEqual(self.student['payments'][value].p_level, 300)

        # We simulate the approval
        self.browser.open(self.browser.url + '/fake_approve')
        self.assertMatches('...Payment approved...',
                          self.browser.contents)

        # No AC has been created
        self.assertEqual(len(self.app['accesscodes']['SFE-0'].keys()), 0)
        self.assertTrue(self.student['payments'][value].ac is None)

        # Current payment flag is set False
        self.assertFalse(self.student['payments'][value].p_current)

        # Button and form are not available for students who are in
        # states up to cleared
        self.student['studycourse'].entry_session = 2004
        IWorkflowState(self.student).setState('cleared')
        self.browser.open(self.payments_path)
        self.assertFalse(
            "Add previous session payment ticket" in self.browser.contents)
        self.browser.open(self.payments_path + '/addpp')
        self.assertTrue(
            "No previous payment to be made" in self.browser.contents)
        return

    def test_postgraduate_student_payments(self):
        configuration = createObject('waeup.SessionConfiguration')
        configuration.academic_session = 2005
        self.app['configuration'].addSessionConfiguration(configuration)
        self.certificate.study_mode = 'pg_ft'
        self.certificate.start_level = 999
        self.certificate.end_level = 999
        self.student['studycourse'].current_level = 999
        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Students can add online school fee payment tickets.
        IWorkflowState(self.student).setState('cleared')
        self.browser.open(self.payments_path)
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...Amount Authorized...',
                           self.browser.contents)
        # Payment session and level are current ones.
        # Postgrads have to pay school_fee_1.
        self.assertEqual(self.student['payments'][value].amount_auth, 40000.0)
        self.assertEqual(self.student['payments'][value].p_session, 2004)
        self.assertEqual(self.student['payments'][value].p_level, 999)

        # We simulate the approval
        self.assertEqual(len(self.app['accesscodes']['SFE-0']),0)
        self.browser.open(self.browser.url + '/fake_approve')
        self.assertMatches('...Payment approved...',
                          self.browser.contents)

        ## The new SFE-0 pin can be used for starting session
        #self.browser.open(self.studycourse_path)
        #self.browser.getLink('Start new session').click()
        #pin = self.app['accesscodes']['SFE-0'].keys()[0]
        #parts = pin.split('-')[1:]
        #sfeseries, sfenumber = parts
        #self.browser.getControl(name="ac_series").value = sfeseries
        #self.browser.getControl(name="ac_number").value = sfenumber
        #self.browser.getControl("Start now").click()
        #self.assertMatches('...Session started...',
        #                   self.browser.contents)

        self.assertTrue(self.student.state == 'school fee paid')

        # Postgrad students do not need to register courses the
        # can just pay for the next session.
        self.browser.open(self.payments_path)
        # Remove first payment to be sure that we access the right ticket
        del self.student['payments'][value]
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['schoolfee']
        self.browser.getControl("Create ticket").click()
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        # Payment session has increased by one, payment level remains the same.
        # Returning Postgraduates have to pay school_fee_2.
        self.assertEqual(self.student['payments'][value].amount_auth, 20000.0)
        self.assertEqual(self.student['payments'][value].p_session, 2005)
        self.assertEqual(self.student['payments'][value].p_level, 999)

        # Student is still in old session
        self.assertEqual(self.student.current_session, 2004)

        # We do not need to pay the ticket if any other
        # SFE pin is provided
        pin_container = self.app['accesscodes']
        pin_container.createBatch(
            datetime.utcnow(), 'some_userid', 'SFE', 9.99, 1)
        pin = pin_container['SFE-1'].values()[0].representation
        sfeseries, sfenumber = pin.split('-')[1:]
        # The new SFE-1 pin can be used for starting new session
        self.browser.open(self.studycourse_path)
        self.browser.getLink('Start new session').click()
        self.browser.getControl(name="ac_series").value = sfeseries
        self.browser.getControl(name="ac_number").value = sfenumber
        self.browser.getControl("Start now").click()
        self.assertMatches('...Session started...',
                           self.browser.contents)
        self.assertTrue(self.student.state == 'school fee paid')
        # Student is in new session
        self.assertEqual(self.student.current_session, 2005)
        self.assertEqual(self.student['studycourse'].current_level, 999)
        return

    def test_student_accommodation(self):
        # Create a second hostel with one bed
        hostel = Hostel()
        hostel.hostel_id = u'hall-2'
        hostel.hostel_name = u'Hall 2'
        self.app['hostels'].addHostel(hostel)
        bed = Bed()
        bed.bed_id = u'hall-2_A_101_A'
        bed.bed_number = 1
        bed.owner = NOT_OCCUPIED
        bed.bed_type = u'regular_female_fr'
        self.app['hostels'][hostel.hostel_id].addBed(bed)
        self.app['hostels'].allocation_expiration = 7

        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Students can add online booking fee payment tickets and open the
        # callback view (see test_manage_payments).
        self.browser.getLink("Payments").click()
        self.browser.getLink("Add current session payment ticket").click()
        self.browser.getControl(name="form.p_category").value = ['bed_allocation']
        self.browser.getControl("Create ticket").click()
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.browser.open(self.browser.url + '/fake_approve')
        # The new HOS-0 pin has been created.
        self.assertEqual(len(self.app['accesscodes']['HOS-0']),1)
        pin = self.app['accesscodes']['HOS-0'].keys()[0]
        ac = self.app['accesscodes']['HOS-0'][pin]
        parts = pin.split('-')[1:]
        sfeseries, sfenumber = parts
        # Students can use HOS code and book a bed space with it ...
        self.browser.open(self.acco_path)
        # ... but not if booking period has expired ...
        self.app['hostels'].enddate = datetime.now(pytz.utc)
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...Outside booking period: ...',
                           self.browser.contents)
        self.app['hostels'].enddate = datetime.now(pytz.utc) + timedelta(days=10)
        # ... or student data are incomplete ...
        self.student['studycourse'].current_level = None
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...Your data are incomplete...',
            self.browser.contents)
        self.student['studycourse'].current_level = 100
        # ... or student is not the an allowed state ...
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...You are in the wrong...',
                           self.browser.contents)
        # Students can still not see the disired hostel selector.
        self.assertFalse('desired hostel' in self.browser.contents)
        IWorkflowInfo(self.student).fireTransition('admit')
        # Students can now see the disired hostel selector.
        self.browser.reload()
        self.browser.open(self.acco_path)
        self.assertTrue('desired hostel' in self.browser.contents)
        self.browser.getControl(name="hostel").value = ['hall-2']
        self.browser.getControl("Save").click()
        self.assertTrue('selection has been saved' in self.browser.contents)
        self.assertTrue('<option selected="selected" value="hall-2">'
            in self.browser.contents)
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...Activation Code:...',
                           self.browser.contents)
        # Student can't use faked ACs ...
        self.browser.getControl(name="ac_series").value = u'nonsense'
        self.browser.getControl(name="ac_number").value = sfenumber
        self.browser.getControl("Create bed ticket").click()
        self.assertMatches('...Activation code is invalid...',
                           self.browser.contents)
        # ... or ACs owned by somebody else.
        ac.owner = u'Anybody'
        self.browser.getControl(name="ac_series").value = sfeseries
        self.browser.getControl(name="ac_number").value = sfenumber
        # There is no free bed space and the bed selector does not appear
        self.assertFalse('<option value="hall-1_A_101_A">'
            in self.browser.contents)
        self.browser.getControl("Create bed ticket").click()
        # Hostel 2 has only a bed for women.
        self.assertTrue('There is no free bed in your category regular_male_fr.'
            in self.browser.contents)
        self.browser.getControl(name="hostel").value = ['hall-1']
        self.browser.getControl("Save").click()
        self.browser.getControl("Book accommodation").click()
        # Student can't use faked ACs ...
        self.browser.getControl(name="ac_series").value = sfeseries
        self.browser.getControl(name="ac_number").value = sfenumber
        self.browser.getControl("Create bed ticket").click()
        self.assertMatches('...You are not the owner of this access code...',
                           self.browser.contents)
        # The bed remains empty.
        bed = self.app['hostels']['hall-1']['hall-1_A_101_A']
        self.assertTrue(bed.owner == NOT_OCCUPIED)
        ac.owner = self.student_id
        self.browser.open(self.acco_path + '/add')
        self.browser.getControl(name="ac_series").value = sfeseries
        self.browser.getControl(name="ac_number").value = sfenumber
        # Bed can be selected
        self.browser.getControl(name="bed").value = ['hall-1_A_101_A']
        self.browser.getControl("Create bed ticket").click()
        self.assertTrue('Bed ticket created and bed booked'
            in self.browser.contents)
        # Bed has been allocated.
        self.assertTrue(bed.owner == self.student_id)
        # BedTicketAddPage is now blocked.
        self.browser.getControl("Book accommodation").click()
        self.assertMatches('...You already booked a bed space...',
            self.browser.contents)
        # The bed ticket displays the data correctly.
        self.browser.open(self.acco_path + '/2004')
        self.assertMatches('...Hall 1, Block A, Room 101, Bed A...',
                           self.browser.contents)
        self.assertMatches('...2004/2005...', self.browser.contents)
        self.assertMatches('...regular_male_fr...', self.browser.contents)
        self.assertMatches('...%s...' % pin, self.browser.contents)
        # Students can open the pdf slip.
        self.browser.open(self.browser.url + '/bed_allocation_slip.pdf')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'bed_allocation_slip.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF bed_allocation_slip.pdf written to %s" % path
        # Students can't relocate themselves.
        self.assertFalse('Relocate' in self.browser.contents)
        relocate_path = self.acco_path + '/2004/relocate'
        self.assertRaises(
            Unauthorized, self.browser.open, relocate_path)
        # Students can't see the Remove button and check boxes.
        self.browser.open(self.acco_path)
        self.assertFalse('Remove' in self.browser.contents)
        self.assertFalse('val_id' in self.browser.contents)
        # Students can pay maintenance fee now.
        self.browser.open(self.payments_path)
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['hostel_maintenance']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...Payment ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        # Maintennace fee is taken from the hostel object.
        self.assertEqual(self.student['payments'][value].amount_auth, 876.0)
        # If the hostel's maintenance fee isn't set, the fee is
        # taken from the session configuration object.
        self.app['hostels']['hall-1'].maint_fee = 0.0
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['hostel_maintenance']
        self.browser.getControl("Create ticket").click()
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[1]
        self.assertEqual(self.student['payments'][value].amount_auth, 987.0)
        # The bedticket is aware of successfull maintenance fee payment
        bedticket = self.student['accommodation']['2004']
        self.assertFalse(bedticket.maint_payment_made)
        self.student['payments'][value].approve()
        self.assertTrue(bedticket.maint_payment_made)
        return

    def test_change_password_request(self):
        self.browser.open('http://localhost/app/changepw')
        self.browser.getControl(name="form.identifier").value = '123'
        self.browser.getControl(name="form.email").value = 'aa@aa.ng'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('An email with' in self.browser.contents)

    def test_student_expired_personal_data(self):
        # Login
        IWorkflowState(self.student).setState('school fee paid')
        delta = timedelta(days=180)
        self.student.personal_updated = datetime.utcnow() - delta
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertEqual(self.browser.url, self.student_path)
        self.assertTrue(
            'You logged in' in self.browser.contents)
        # Students don't see personal_updated field in edit form
        self.browser.open(self.edit_personal_path)
        self.assertFalse('Updated' in self.browser.contents)
        self.browser.open(self.personal_path)
        self.assertTrue('Updated' in self.browser.contents)
        self.browser.getLink("Logout").click()
        delta = timedelta(days=181)
        self.student.personal_updated = datetime.utcnow() - delta
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertEqual(self.browser.url, self.edit_personal_path)
        self.assertTrue(
            'Your personal data record is outdated.' in self.browser.contents)

    def test_request_transcript(self):
        IWorkflowState(self.student).setState('graduated')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertMatches(
            '...You logged in...', self.browser.contents)
        # Create payment ticket
        self.browser.open(self.payments_path)
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['transcript']
        self.browser.getControl("Create ticket").click()
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...Amount Authorized...',
                           self.browser.contents)
        self.assertEqual(self.student['payments'][value].amount_auth, 4567.0)
        # Student is the payer of the payment ticket.
        payer = IPayer(self.student['payments'][value])
        self.assertEqual(payer.display_fullname, 'Anna Tester')
        self.assertEqual(payer.id, self.student_id)
        self.assertEqual(payer.faculty, 'fac1')
        self.assertEqual(payer.department, 'dep1')
        # We simulate the approval and fetch the pin
        self.assertEqual(len(self.app['accesscodes']['TSC-0']),0)
        self.browser.open(self.browser.url + '/fake_approve')
        self.assertMatches('...Payment approved...',
                          self.browser.contents)
        pin = self.app['accesscodes']['TSC-0'].keys()[0]
        parts = pin.split('-')[1:]
        tscseries, tscnumber = parts
        # Student can use the pin to send the transcript request
        self.browser.open(self.student_path)
        self.browser.getLink("Request transcript").click()
        self.browser.getControl(name="ac_series").value = tscseries
        self.browser.getControl(name="ac_number").value = tscnumber
        self.browser.getControl(name="comment").value = 'Comment line 1 \nComment line2'
        self.browser.getControl(name="address").value = 'Address line 1 \nAddress line2'
        self.browser.getControl("Request now").click()
        self.assertMatches('...Transcript processing has been started...',
                          self.browser.contents)
        self.assertEqual(self.student.state, 'transcript requested')
        self.assertMatches(
            '... UTC K1000000 wrote:\n\nComment line 1 \n'
            'Comment line2\n\nDispatch Address:\nAddress line 1 \n'
            'Address line2\n\n', self.student['studycourse'].transcript_comment)
        # The comment has been logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'K1000000 - students.browser.StudentTranscriptRequestPage - '
            'K1000000 - comment: Comment line 1 <br>Comment line2\n'
            in logcontent)

    def test_late_registration(self):
        # Login
        delta = timedelta(days=10)
        self.app['configuration'][
            '2004'].coursereg_deadline = datetime.now(pytz.utc) - delta
        IWorkflowState(self.student).setState('school fee paid')
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.browser.open(self.payments_path)
        self.browser.open(self.payments_path + '/addop')
        self.browser.getControl(name="form.p_category").value = ['late_registration']
        self.browser.getControl("Create ticket").click()
        self.assertMatches('...ticket created...',
                           self.browser.contents)
        self.browser.open(self.payments_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 100 (Year 1)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        self.browser.getLink("100").click()
        self.browser.getLink("Edit course list").click()
        self.browser.getControl("Register course list").click()
        self.assertTrue('Course registration has ended. Please pay' in self.browser.contents)
        self.student['payments'][value].approve()
        self.browser.getControl("Register course list").click()
        self.assertTrue('Course list has been registered' in self.browser.contents)
        self.assertEqual(self.student.state, 'courses registered')

    def test_former_course(self):
        IWorkflowState(self.student).setState('school fee paid')
        self.student['studycourse'].current_level = 100
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        # Now students can add the current study level
        self.browser.getLink("Study Course").click()
        self.browser.getLink("Add course list").click()
        self.assertMatches('...Add current level 100 (Year 1)...',
                           self.browser.contents)
        self.browser.getControl("Create course list now").click()
        # A level with one course ticket was created
        self.assertEqual(
            self.student['studycourse']['100'].number_of_tickets, 1)
        self.browser.getLink("100").click()
        self.assertTrue('<td>Unnamed Course</td>' in self.browser.contents)
        self.browser.getLink("Edit course list").click()
        del self.student['studycourse']['100']['COURSE1']
        # Course can be added again via CourseTicketAddFormPage2
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.browser.getControl("Add course ticket").click()
        self.assertTrue('Successfully added COURSE1' in self.browser.contents)
        self.assertEqual(len(self.student['studycourse']['100'].keys()),1)
        del self.student['studycourse']['100']['COURSE1']
        self.course.former_course = True
        self.browser.getLink("here").click()
        self.browser.getControl(name="form.course").value = ['COURSE1']
        self.browser.getControl("Add course ticket").click()
        self.assertTrue('Former courses can\'t be added.' in self.browser.contents)
        self.assertEqual(len(self.student['studycourse']['100'].keys()),0)
        # Course can be added again via StudyLevelEditFormPage
        self.browser.getLink("100").click()
        self.browser.getLink("Edit course list").click()
        self.browser.getControl(name="course").value = 'COURSE1'
        self.browser.getControl("Add course ticket").click()
        self.assertTrue('Former courses can\'t be added.' in
            self.browser.contents)
        self.assertEqual(len(self.student['studycourse']['100'].keys()),0)
        # but added if current course
        self.course.former_course = False
        self.browser.getControl(name="course").value = 'COURSE1'
        self.browser.getControl("Add course ticket").click()
        self.assertTrue('Successfully added COURSE1' in self.browser.contents)
        self.assertEqual(len(self.student['studycourse']['100'].keys()),1)
        return

class StudentRequestPWTests(StudentsFullSetup):
    # Tests for student registration

    layer = FunctionalLayer

    def test_request_pw(self):
        # Student with wrong number can't be found.
        self.browser.open('http://localhost/app/requestpw')
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.number").value = 'anynumber'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('No student record found.'
            in self.browser.contents)
        # Anonymous is not informed that lastname verification failed.
        # It seems that the record doesn't exist.
        self.browser.open('http://localhost/app/requestpw')
        self.browser.getControl(name="form.lastname").value = 'Johnny'
        self.browser.getControl(name="form.number").value = '123'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('No student record found.'
            in self.browser.contents)
        # Even with the correct lastname we can't register if a
        # password has been set and used.
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.number").value = '123'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('Your password has already been set and used.'
            in self.browser.contents)
        self.browser.open('http://localhost/app/requestpw')
        self.app['students'][self.student_id].password = None
        # The lastname field, used for verification, is not case-sensitive.
        self.browser.getControl(name="form.lastname").value = 'tESTer'
        self.browser.getControl(name="form.number").value = '123'
        self.browser.getControl(name="form.email").value = 'new@yy.zz'
        self.browser.getControl("Send login credentials").click()
        # Yeah, we succeded ...
        self.assertTrue('Your password request was successful.'
            in self.browser.contents)
        # We can also use the matric_number instead.
        self.browser.open('http://localhost/app/requestpw')
        self.browser.getControl(name="form.lastname").value = 'tESTer'
        self.browser.getControl(name="form.number").value = '234'
        self.browser.getControl(name="form.email").value = 'new@yy.zz'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('Your password request was successful.'
            in self.browser.contents)
        # ... and  student can be found in the catalog via the email address
        cat = queryUtility(ICatalog, name='students_catalog')
        results = list(
            cat.searchResults(
            email=('new@yy.zz', 'new@yy.zz')))
        self.assertEqual(self.student,results[0])
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertTrue('zope.anybody - students.browser.StudentRequestPasswordPage - '
                        '234 (K1000000) - new@yy.zz' in logcontent)
        return

    def test_student_locked_level_forms(self):

        # Add two study levels, one current and one previous
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 100
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = 200
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, studylevel)
        IWorkflowState(self.student).setState('school fee paid')
        self.student['studycourse'].current_level = 200

        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()

        self.browser.open(self.student_path + '/studycourse/200/edit')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse/100/edit')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        self.browser.open(self.student_path + '/studycourse/200/ctadd')
        self.assertFalse('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse/100/ctadd')
        self.assertTrue('The requested form is locked' in self.browser.contents)

        IWorkflowState(self.student).setState('courses registered')
        self.browser.open(self.student_path + '/studycourse/200/edit')
        self.assertTrue('The requested form is locked' in self.browser.contents)
        self.browser.open(self.student_path + '/studycourse/200/ctadd')
        self.assertTrue('The requested form is locked' in self.browser.contents)


class PublicPagesTests(StudentsFullSetup):
    # Tests for simple webservices

    layer = FunctionalLayer

    def test_paymentrequest(self):
        payment = createObject('waeup.StudentOnlinePayment')
        payment.p_category = u'schoolfee'
        payment.p_session = self.student.current_session
        payment.p_item = u'My Certificate'
        payment.p_id = u'anyid'
        self.student['payments']['anykey'] = payment
        # Request information about unpaid payment ticket
        self.browser.open('http://localhost/app/paymentrequest?P_ID=anyid')
        self.assertEqual(self.browser.contents, '-1')
        # Request information about paid payment ticket
        payment.p_state = u'paid'
        notify(grok.ObjectModifiedEvent(payment))
        self.browser.open('http://localhost/app/paymentrequest?P_ID=anyid')
        self.assertEqual(self.browser.contents,
            'FULL_NAME=Anna Tester&FACULTY=fac1&DEPARTMENT=dep1'
            '&PAYMENT_ITEM=My Certificate&PAYMENT_CATEGORY=School Fee'
            '&ACADEMIC_SESSION=2004/2005&MATRIC_NUMBER=234&REG_NUMBER=123'
            '&FEE_AMOUNT=0.0')
        self.browser.open('http://localhost/app/paymentrequest?NONSENSE=nonsense')
        self.assertEqual(self.browser.contents, '-1')
        self.browser.open('http://localhost/app/paymentrequest?P_ID=nonsense')
        self.assertEqual(self.browser.contents, '-1')

class StudentDataExportTests(StudentsFullSetup, FunctionalAsyncTestCase):
    # Tests for StudentsContainer class views and pages

    layer = FunctionalLayer

    def wait_for_export_job_completed(self):
        # helper function waiting until the current export job is completed
        manager = getUtility(IJobManager)
        job_id = self.app['datacenter'].running_exports[0][0]
        job = manager.get(job_id)
        wait_for_result(job)
        return job_id

    def add_payment(self, student):
        # get a payment with all fields set
        payment = StudentOnlinePayment()
        payment.creation_date = datetime(2012, 12, 13)
        payment.p_id = 'my-id'
        payment.p_category = u'schoolfee'
        payment.p_state = 'paid'
        payment.ac = u'666'
        payment.p_item = u'p-item'
        payment.p_level = 100
        payment.p_session = curr_year - 6
        payment.payment_date = datetime(2012, 12, 13)
        payment.amount_auth = 12.12
        payment.r_amount_approved = 12.12
        payment.r_code = u'r-code'
        # XXX: there is no addPayment method to give predictable names
        self.payment = student['payments']['my-payment'] = payment
        return payment

    def test_datacenter_export(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/datacenter/@@exportconfig')
        self.browser.getControl(name="exporter").value = ['bursary']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl(name="mode").value = ['ug_ft']
        self.browser.getControl(name="payments_start").value = '13/12/2012'
        self.browser.getControl(name="payments_end").value = '14/12/2012'
        self.browser.getControl("Create CSV file").click()

        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        # ... the csv file can be downloaded ...
        self.browser.open('http://localhost/app/datacenter/@@export')
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_bursary_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.app['datacenter'].running_exports[0][0]
        # ... and discarded
        self.browser.open('http://localhost/app/datacenter/@@export')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.DatacenterExportJobContainerJobConfig '
            '- exported: bursary (2004, 100, ug_ft, None, None, None, '
            '13/12/2012, 14/12/2012, all, all, all, all, all), job_id=%s'
            % job_id in logcontent
            )
        self.assertTrue(
            'zope.mgr - browser.pages.ExportCSVView '
            '- downloaded: WAeUP.Kofa_bursary_%s.csv, job_id=%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'zope.mgr - browser.pages.ExportCSVPage '
            '- discarded: job_id=%s' % job_id in logcontent
            )

    def test_datacenter_export_selected(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/datacenter/@@exportselected')
        self.browser.getControl(name="exporter").value = ['students']
        self.browser.getControl(name="students").value = 'K1000000'
        self.browser.getControl("Create CSV file").click()
        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        # ... the csv file can be downloaded ...
        self.browser.open('http://localhost/app/datacenter/@@export')
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_students_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertTrue(
            'adm_code,clr_code,date_of_birth,email,employer,'
            'firstname,flash_notice,lastname,matric_number,middlename,nationality,'
            'officer_comment,parents_email,perm_address,'
            'personal_updated,phone,reg_number,'
            'sex,student_id,suspended,suspended_comment,'
            'password,state,history,certcode,is_postgrad,'
            'current_level,current_session,entry_session\r\n'
            ',,1981-02-04#,aa@aa.ng,,Anna,,Tester,234,,,,,,,'
            '1234#,123,m,K1000000,0,,{SSHA}' in self.browser.contents)
        self.browser.open('http://localhost/app/datacenter/@@export')
        self.browser.getControl("Discard").click()

    def test_payment_dates(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/datacenter/@@exportconfig')
        self.browser.getControl(name="exporter").value = ['bursary']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl(name="mode").value = ['ug_ft']
        self.browser.getControl(name="payments_start").value = '13/12/2012'
        # If one payment date is missing, an error message appears
        self.browser.getControl(name="payments_end").value = ''
        self.browser.getControl("Create CSV file").click()
        self.assertTrue('Payment dates do not match format d/m/Y'
            in self.browser.contents)

    def test_faculties_export(self):
        self.add_payment(self.student)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        facs_path = 'http://localhost/app/faculties'
        self.browser.open(facs_path)
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        self.browser.getControl(name="exporter").value = ['bursary']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl(name="mode").value = ['ug_ft']
        self.browser.getControl(name="payments_start").value = '13/12/2012'
        self.browser.getControl(name="payments_end").value = '14/12/2012'
        self.browser.getControl(name="paycat").value = ['schoolfee']
        self.browser.getControl("Create CSV file").click()

        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        self.browser.open(facs_path + '/exports')
        # ... the csv file can be downloaded ...
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_bursary_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertTrue(
            '666,12.12,2012-12-13 00:00:00#,schoolfee,[],1,my-id,p-item,100,%s,'
            'paid,2012-12-13 00:00:00#,12.12,r-code,,K1000000,234,123,Anna,,'
            'Tester,m,created,2004,2004,,fac1,dep1,CERT1'
            %(curr_year-6) in self.browser.contents)
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.app['datacenter'].running_exports[0][0]
        # ... and discarded
        self.browser.open(facs_path + '/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.FacultiesExportJobContainerJobConfig '
            '- exported: bursary (2004, 100, ug_ft, None, None, None, '
            '13/12/2012, 14/12/2012, all, all, schoolfee, all, all), job_id=%s'
            % job_id in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_bursary_%s.csv, job_id=%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_id in logcontent
            )
        # Officer can also enter student id and gets the same export file
        self.browser.open(facs_path)
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Enter student ids or matric numbers").click()
        self.browser.getControl(name="exporter").value = ['bursary']
        self.browser.getControl(name="students").value = 'K1000000'
        self.browser.getControl("Create CSV file").click()
        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        # ... the csv file can be downloaded ...
        self.browser.open('http://localhost/app/faculties/exports')
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_bursary_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertTrue(
            '666,12.12,2012-12-13 00:00:00#,schoolfee,[],1,my-id,p-item,100,%s,'
            'paid,2012-12-13 00:00:00#,12.12,r-code,,K1000000,234,123,Anna,,'
            'Tester,m,created,2004,2004,,fac1,dep1,CERT1'
            %(curr_year-6) in self.browser.contents)

    def test_faculty_export(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        fac1_path = 'http://localhost/app/faculties/fac1'
        self.browser.open(fac1_path)
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        self.browser.getControl(name="exporter").value = ['students']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl(name="mode").value = ['ug_ft']
        # The testbrowser does not hide the payment period fields, but
        # values are ignored when using the students exporter.
        self.browser.getControl(name="payments_start").value = '13/12/2012'
        self.browser.getControl(name="payments_end").value = '14/12/2012'
        self.browser.getControl("Create CSV file").click()
        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        self.browser.open(fac1_path + '/exports')
        # ... the csv file can be downloaded ...
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_students_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertTrue(
            'adm_code,clr_code,date_of_birth,email,employer,'
            'firstname,flash_notice,lastname,matric_number,middlename,nationality,'
            'officer_comment,parents_email,perm_address,'
            'personal_updated,phone,reg_number,'
            'sex,student_id,suspended,suspended_comment,'
            'password,state,history,certcode,is_postgrad,'
            'current_level,current_session,entry_session\r\n'
            ',,1981-02-04#,aa@aa.ng,,Anna,,Tester,234,,,,,,,'
            '1234#,123,m,K1000000,0,,{SSHA}' in self.browser.contents)
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.app['datacenter'].running_exports[0][0]
        # ... and discarded
        self.browser.open(fac1_path + '/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.FacultyExportJobContainerJobConfig '
            '- exported: students (2004, 100, ug_ft, fac1, None, None, '
            '13/12/2012, 14/12/2012, all, all, all, all, all), job_id=%s'
            % job_id in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_students_%s.csv, job_id=%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_id in logcontent
            )
        # Officer can set export parameters but cannot enter student id
        # at faculty level
        self.browser.open(fac1_path + '/exports')
        self.assertTrue("Set export parameters"
                         in self.browser.contents)
        self.assertFalse("Enter student ids or matric numbers"
                         in self.browser.contents)

    def test_department_export(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        dep1_path = 'http://localhost/app/faculties/fac1/dep1'
        self.browser.open(dep1_path)
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        self.browser.getControl(name="exporter").value = ['students']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl(name="mode").value = ['ug_ft']
        # The testbrowser does not hide the payment period fields, but
        # values are ignored when using the students exporter.
        self.browser.getControl(name="payments_start").value = '13/12/2012'
        self.browser.getControl(name="payments_end").value = '14/12/2012'
        self.browser.getControl("Create CSV file").click()

        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        self.browser.open(dep1_path + '/exports')
        # ... the csv file can be downloaded ...
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_students_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.app['datacenter'].running_exports[0][0]
        # ... and discarded
        self.browser.open(dep1_path + '/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.DepartmentExportJobContainerJobConfig '
            '- exported: students (2004, 100, ug_ft, None, dep1, None, '
            '13/12/2012, 14/12/2012, all, all, all, all, all), job_id=%s'
            % job_id in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_students_%s.csv, job_id=%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_id in logcontent
            )

    def test_certificate_export(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        cert1_path = 'http://localhost/app/faculties/fac1/dep1/certificates/CERT1'
        self.browser.open(cert1_path)
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        self.browser.getControl(name="exporter").value = ['students']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Create CSV file").click()

        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        self.browser.open(cert1_path + '/exports')
        # ... the csv file can be downloaded ...
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_students_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.app['datacenter'].running_exports[0][0]
        # ... and discarded
        self.browser.open(cert1_path + '/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.CertificateExportJobContainerJobConfig '
            '- exported: students '
            '(2004, 100, None, None, None, CERT1, , , None, None, '
            'None, None, None), '
            'job_id=%s'
            % job_id in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_students_%s.csv, job_id=%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_id in logcontent
            )

    def deprecated_test_course_export_students(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        course1_path = 'http://localhost/app/faculties/fac1/dep1/courses/COURSE1'
        self.browser.open(course1_path)
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        self.browser.getControl(name="exporter").value = ['students']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Create CSV file").click()

        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        self.browser.open(course1_path + '/exports')
        # ... the csv file can be downloaded ...
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_students_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.app['datacenter'].running_exports[0][0]
        # ... and discarded
        self.browser.open(course1_path + '/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.CourseExportJobContainerJobConfig '
            '- exported: students (2004, 100, COURSE1), job_id=%s'
            % job_id in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_students_%s.csv, job_id=%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_id in logcontent
            )

    def test_course_export_lecturer(self):
        # We add study level 100 to the student's studycourse
        studylevel = StudentStudyLevel()
        studylevel.level = 100
        studylevel.level_session = 2004
        IWorkflowState(self.student).setState('courses validated')
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate,studylevel)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        course1_path = 'http://localhost/app/faculties/fac1/dep1/courses/COURSE1'
        self.browser.open(course1_path)
        self.browser.getLink("Export student data").click()
        # Disabled on 10/03/21
        #self.browser.getControl("Set export parameters").click()
        #self.assertTrue(
        #    'Academic session not set. Please contact the administrator.'
        #    in self.browser.contents)
        #self.app['configuration'].current_academic_session = 2004
        self.browser.getControl("Set export parameters").click()
        self.browser.getControl(name="exporter").value = ['lecturer']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Create CSV file").click()
        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        self.browser.open(course1_path + '/exports')
        # ... the csv file can be downloaded ...
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_lecturer_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        # ... and contains the course ticket COURSE1
        self.assertEqual(self.browser.contents,
            'matric_number,student_id,display_fullname,level,code,'
            'level_session,score\r\n234,K1000000,Anna Tester,'
            '100,COURSE1,2004,\r\n')
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.app['datacenter'].running_exports[0][0]
        # Thew job can be discarded
        self.browser.open(course1_path + '/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - students.browser.CourseExportJobContainerJobConfig '
            '- exported: lecturer (2004, 100, COURSE1), job_id=%s'
            % job_id in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_lecturer_%s.csv, job_id=%s'
            % (job_id, job_id) in logcontent
            )
        self.assertTrue(
            'zope.mgr - students.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_id in logcontent
            )

    def test_export_departmet_officers(self):
        # Create department officer
        self.app['users'].addUser('mrdepartment', SECRET)
        self.app['users']['mrdepartment'].email = 'mrdepartment@foo.ng'
        self.app['users']['mrdepartment'].title = 'Carlo Pitter'
        # Assign local role
        department = self.app['faculties']['fac1']['dep1']
        prmlocal = IPrincipalRoleManager(department)
        prmlocal.assignRoleToPrincipal('waeup.local.DepartmentOfficer', 'mrdepartment')
        # Login as department officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrdepartment'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        self.browser.open("http://localhost/app/faculties/fac1/dep1")
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        # Only the sfpaymentsoverview exporter is available for department officers
        self.assertFalse('<option value="students">' in self.browser.contents)
        self.assertTrue(
            '<option value="sfpaymentsoverview">' in self.browser.contents)
        self.browser.getControl(name="exporter").value = ['sfpaymentsoverview']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Create CSV file").click()
        self.assertTrue('Export started' in self.browser.contents)
        # Thew job can be discarded
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        self.wait_for_export_job_completed()
        self.browser.open("http://localhost/app/faculties/fac1/dep1/exports")
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)

    def test_export_bursary_officers(self):
        self.add_payment(self.student)
        # Create bursary officer
        self.app['users'].addUser('mrbursary', SECRET)
        self.app['users']['mrbursary'].email = 'mrbursary@foo.ng'
        self.app['users']['mrbursary'].title = 'Carlo Pitter'
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.BursaryOfficer', 'mrbursary')
        # Login as bursary officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrbursary'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        self.browser.getLink("Academics").click()
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        # Only the bursary exporter is available for bursary officers
        # not only at facultiescontainer level ...
        self.assertFalse('<option value="students">' in self.browser.contents)
        self.assertTrue('<option value="bursary">' in self.browser.contents)
        self.browser.getControl(name="exporter").value = ['bursary']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Create CSV file").click()
        self.assertTrue('Export started' in self.browser.contents)
        # ... but also at other levels
        self.browser.open('http://localhost/app/faculties/fac1/dep1')
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        self.assertFalse('<option value="students">' in self.browser.contents)
        self.assertTrue('<option value="bursary">' in self.browser.contents)
        # Thew job can be downloaded
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        job_id = self.wait_for_export_job_completed()
        self.browser.open('http://localhost/app/faculties/exports')
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_bursary_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertTrue(
            '666,12.12,2012-12-13 00:00:00#,schoolfee,[],1,my-id,p-item,100,%s,'
            'paid,2012-12-13 00:00:00#,12.12,r-code,,K1000000,234,123,Anna,,'
            'Tester,m,created,2004,2004,,fac1,dep1,CERT1'
            %(curr_year-6) in self.browser.contents)
        # ... and discarded
        self.browser.open('http://localhost/app/faculties/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # At Academics level bursary officers can also enter student ids
        self.browser.getLink("Academics").click()
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Enter student ids or matric numbers").click()
        self.assertFalse('<option value="students">' in self.browser.contents)
        self.browser.getControl(name="exporter").value = ['bursary']
        self.browser.getControl(name="students").value = 'K1000000'
        self.browser.getControl("Create CSV file").click()
        # When the job is finished and we reload the page...
        job_id = self.wait_for_export_job_completed()
        # ... the csv file can be downloaded ...
        self.browser.open('http://localhost/app/faculties/exports')
        self.browser.getLink("Download").click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_bursary_%s.csv' % job_id in
            self.browser.headers['content-disposition'])
        self.assertTrue(
            '666,12.12,2012-12-13 00:00:00#,schoolfee,[],1,my-id,p-item,100,%s,'
            'paid,2012-12-13 00:00:00#,12.12,r-code,,K1000000,234,123,Anna,,'
            'Tester,m,created,2004,2004,,fac1,dep1,CERT1'
            %(curr_year-6) in self.browser.contents)

    def test_export_accommodation_officers(self):
        # Create bursary officer
        self.app['users'].addUser('mracco', SECRET)
        self.app['users']['mracco'].email = 'mracco@foo.ng'
        self.app['users']['mracco'].title = 'Carlo Pitter'
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.AccommodationOfficer', 'mracco')
        # Login as bursary officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mracco'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.assertMatches('...You logged in...', self.browser.contents)
        self.browser.getLink("Academics").click()
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        # accommodationpayments and beds exporters are available
        # not only at facultiescontainer level ...
        self.assertFalse('<option value="students">' in self.browser.contents)
        self.assertTrue('<option value="accommodationpayments">'
            in self.browser.contents)
        self.assertTrue('<option value="bedtickets">' in self.browser.contents)
        self.browser.getControl(
            name="exporter").value = ['accommodationpayments']
        self.browser.getControl(name="session").value = ['2004']
        self.browser.getControl(name="level").value = ['100']
        self.browser.getControl("Create CSV file").click()
        self.assertTrue('Export started' in self.browser.contents)
        # ... but also at other levels
        self.browser.open('http://localhost/app/faculties/fac1/dep1')
        self.browser.getLink("Export student data").click()
        self.browser.getControl("Set export parameters").click()
        self.assertFalse('<option value="students">' in self.browser.contents)
        self.assertTrue('<option value="accommodationpayments">'
            in self.browser.contents)
        self.assertTrue('<option value="bedtickets">' in self.browser.contents)
        # Thew job can be discarded
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        self.wait_for_export_job_completed()
        self.browser.open('http://localhost/app/faculties/exports')
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)


UPLOAD_CSV_TEMPLATE = (
    'matric_number,student_id,display_fullname,level,code,level_session,'
    'score\r\n'
    '234,K1000000,Anna Tester,100,COURSE1,2004,%s\r\n')

class LecturerUITests(StudentsFullSetup):
    # Tests for UI actions when acting as lecturer.

    def login_as_lecturer(self):
        self.app['users'].addUser('mrslecturer', SECRET)
        self.app['users']['mrslecturer'].email = 'mrslecturer@foo.ng'
        self.app['users']['mrslecturer'].title = u'Mercedes Benz'
        # Add course ticket
        self.studylevel = createObject(u'waeup.StudentStudyLevel')
        self.studylevel.level = 100
        self.studylevel.level_session = 2004
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate, self.studylevel)
        # Assign local Lecturer role for a course.
        course = self.app['faculties']['fac1']['dep1'].courses['COURSE1']
        prmlocal = IPrincipalRoleManager(course)
        prmlocal.assignRoleToPrincipal('waeup.local.Lecturer', 'mrslecturer')
        notify(LocalRoleSetEvent(
            course, 'waeup.local.Lecturer', 'mrslecturer', granted=True))
        # Login as lecturer.
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrslecturer'
        self.browser.getControl(
            name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        # Store reused urls/paths
        self.course_url = (
            'http://localhost/app/faculties/fac1/dep1/courses/COURSE1')
        self.edit_scores_url = '%s/edit_scores' % self.course_url
        # Set standard parameters
        self.app['configuration'].current_academic_session = 2004
        self.app['faculties']['fac1']['dep1'].score_editing_disabled = False
        IWorkflowState(self.student).setState(VALIDATED)

    @property
    def stud_log_path(self):
        return os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')

    def test_lecturer_lands_on_landing_page(self):
        # lecturers can login and will be led to landing page.
        self.login_as_lecturer()
        self.assertTrue(
            'You logged in as a lecturer.' in self.browser.contents)
        self.assertEqual(self.browser.url, URL_LECTURER_LANDING)
        self.assertTrue(
            "<span>Unnamed Course (COURSE1)</span>"
            in self.browser.contents)

    def test_lecturer_department_role(self):
        # lecturers can login and will be led to landing page also if
        # role is assigned at department level.
        self.login_as_lecturer()
        # we remove the role granted above
        course = self.app['faculties']['fac1']['dep1'].courses['COURSE1']
        prmlocal = IPrincipalRoleManager(course)
        prmlocal.removeRoleFromPrincipal('waeup.local.Lecturer', 'mrslecturer')
        notify(LocalRoleSetEvent(
            course, 'waeup.local.Lecturer', 'mrslecturer', granted=False))
        self.browser.open(URL_LECTURER_LANDING)
        # no course appears
        self.assertFalse(
            "<span>Unnamed Course (COURSE1)</span>"
            in self.browser.contents)
        # we assign lecturer at department level
        dep = self.app['faculties']['fac1']['dep1']
        prmlocal = IPrincipalRoleManager(dep)
        prmlocal.assignRoleToPrincipal('waeup.local.Lecturer', 'mrslecturer')
        notify(LocalRoleSetEvent(
            dep, 'waeup.local.Lecturer', 'mrslecturer', granted=True))
        self.browser.open(URL_LECTURER_LANDING)
        # course appears again
        self.assertTrue(
            "<span>Unnamed Course (COURSE1)</span>"
            in self.browser.contents)

    def test_my_roles_link_works(self):
        # lecturers can see their roles
        self.login_as_lecturer()
        self.browser.getLink("My Roles").click()
        self.assertTrue(
            "<div>Academics Officer (view only)</div>"
            in self.browser.contents)
        self.assertTrue(
            '<a href="%s">' % self.course_url in self.browser.contents)

    def test_my_roles_page_contains_backlink(self):
        # we can get back from 'My Roles' view to landing page
        self.login_as_lecturer()
        self.browser.getLink("My Roles").click()
        self.browser.getLink("My Courses").click()
        self.assertEqual(self.browser.url, URL_LECTURER_LANDING)

    def test_lecturers_can_reach_their_courses(self):
        # lecturers get links to their courses on the landing page
        self.login_as_lecturer()
        self.browser.getLink("COURSE1").click()
        self.assertEqual(self.browser.url, self.course_url)

    def test_lecturers_student_access_is_restricted(self):
        # lecturers are not able to change other student data
        self.login_as_lecturer()
        # Lecturers can neither filter students ...
        self.assertRaises(
            Unauthorized, self.browser.open, '%s/students' % self.course_url)
        # ... nor access the student ...
        self.assertRaises(
            Unauthorized, self.browser.open, self.student_path)
        # ... nor the respective course ticket since editing course
        # tickets by lecturers is not feasible.
        self.assertTrue('COURSE1' in self.student['studycourse']['100'].keys())
        course_ticket_path = self.student_path + '/studycourse/100/COURSE1'
        self.assertRaises(
            Unauthorized, self.browser.open, course_ticket_path)

    def test_score_editing_requires_department_permit(self):
        # we get a warning if we try to update score while we are not allowed
        self.login_as_lecturer()
        self.app['faculties']['fac1']['dep1'].score_editing_disabled = True
        self.browser.open(self.course_url)
        self.browser.getLink("Update session 2004/2005 scores").click()
        self.assertTrue('Score editing disabled' in self.browser.contents)
        self.app['faculties']['fac1']['dep1'].score_editing_disabled = False
        self.browser.open(self.course_url)
        self.browser.getLink("Update session 2004/2005 scores").click()
        self.assertFalse('Score editing disabled' in self.browser.contents)

    def test_score_editing_requires_validated_students(self):
        # we can edit only scores of students whose courses have been
        # validated.
        self.login_as_lecturer()
        # set invalid student state
        IWorkflowState(self.student).setState(CREATED)
        self.browser.open(self.edit_scores_url)
        self.assertRaises(
            LookupError, self.browser.getControl, name="scores")
        # set valid student state
        IWorkflowState(self.student).setState(VALIDATED)
        self.browser.open(self.edit_scores_url)
        self.assertTrue(
            self.browser.getControl(name="scores:list") is not None)

    def test_score_editing_offers_only_current_scores(self):
        # only scores from current academic session can be edited
        self.login_as_lecturer()
        IWorkflowState(self.student).setState('courses validated')
        # with no academic session set
        self.app['configuration'].current_academic_session = None
        self.browser.open(self.edit_scores_url)
        self.assertRaises(
            LookupError, self.browser.getControl, name="scores")
        # with wrong academic session set
        self.app['configuration'].current_academic_session = 1999
        self.browser.open(self.edit_scores_url)
        self.assertRaises(
            LookupError, self.browser.getControl, name="scores")
        # with right academic session set
        self.app['configuration'].current_academic_session = 2004
        self.browser.reload()
        self.assertTrue(
            self.browser.getControl(name="scores:list") is not None)
        # if level_session of studycourse changes, catalog has been updated
        # and student disappears
        self.studylevel.level_session = 2005
        self.browser.reload()
        self.assertRaises(
            LookupError, self.browser.getControl, name="scores")

    def test_score_editing_can_change_scores(self):
        # we can really change scores via edit_scores view
        self.login_as_lecturer()
        self.assertEqual(
            self.student['studycourse']['100']['COURSE1'].score, None)
        self.browser.open(self.edit_scores_url)
        self.browser.getControl(name="scores:list", index=0).value = '55'
        self.browser.getControl("Update scores").click()
        # the new value is stored in data
        self.assertEqual(
            self.student['studycourse']['100']['COURSE1'].score, 55)
        # the new value is displayed on page/prefilled in form
        self.assertEqual(
            self.browser.getControl(name="scores:list", index=0).value, '55')
        # The change has been logged
        with open(self.stud_log_path, 'r') as fd:
            self.assertTrue(
                'mrslecturer - students.browser.EditScoresPage - '
                'K1000000 100/COURSE1 score updated (55)' in fd.read())

    def test_scores_editing_scores_must_be_integers(self):
        # Non-integer scores won't be accepted.
        self.login_as_lecturer()
        self.browser.open(self.edit_scores_url)
        self.browser.getControl(name="scores:list", index=0).value = 'abc'
        self.browser.getControl("Update scores").click()
        self.assertTrue(
            'Error: Score(s) of following students have not been updated '
            '(only integers are allowed): Anna Tester.'
            in self.browser.contents)

    def test_scores_editing_allows_score_removal(self):
        # we can remove scores, once they were set
        self.login_as_lecturer()
        # without a prior value, we cannot remove
        self.student['studycourse']['100']['COURSE1'].score = None
        self.browser.open(self.edit_scores_url)
        self.browser.getControl(name="scores:list", index=0).value = ''
        self.browser.getControl("Update scores").click()
        logcontent = open(self.stud_log_path, 'r').read()
        self.assertFalse('COURSE1 score updated (None)' in logcontent)
        # now retry with some value set
        self.student['studycourse']['100']['COURSE1'].score = 55
        self.browser.getControl(name="scores:list", index=0).value = ''
        self.browser.getControl("Update scores").click()
        logcontent = open(self.stud_log_path, 'r').read()
        self.assertTrue('COURSE1 score updated (None)' in logcontent)

    def test_lecturer_can_validate_courses(self):
        # the form is locked after validation
        self.login_as_lecturer()
        self.student['studycourse']['100']['COURSE1'].score = None
        self.browser.open(self.edit_scores_url)
        self.browser.getControl(name="scores:list", index=0).value = ''
        self.browser.getControl("Update scores").click()
        self.browser.getControl("Validate").click()
        self.assertTrue(
            'No score has been entered.' in self.browser.contents)
        self.browser.open(self.edit_scores_url)
        self.browser.getControl(name="scores:list", index=0).value = '66'
        self.browser.getControl("Update scores").click()
        self.browser.getControl("Validate").click()
        self.assertTrue(
            'You successfully validated the course results'
            in self.browser.contents)
        self.assertEqual(self.course.results_validation_session, 2004)
        self.assertEqual(self.course.results_validated_by, 'Mercedes Benz')
        self.assertEqual(self.browser.url, self.course_url)
        # Lecturer can't open edit_scores again
        self.browser.getLink("Update session 2004/2005 scores").click()
        self.assertEqual(self.browser.url, self.course_url)
        self.assertTrue(
            'Course results have already been validated'
            ' and can no longer be changed.'
            in self.browser.contents)
        # Also DownloadScoresView is blocked
        self.browser.open(self.browser.url + '/download_scores')
        self.assertEqual(self.browser.url, self.course_url)
        self.assertTrue(
            'Course results have already been validated'
            ' and can no longer be changed.'
            in self.browser.contents)
        # Students Manager can open page ...
        prmlocal = IPrincipalRoleManager(self.course)
        prmlocal.assignRoleToPrincipal(
            'waeup.local.LocalStudentsManager', 'mrslecturer')
        self.browser.getLink("Update session 2004/2005 scores").click()
        self.assertEqual(self.browser.url, self.edit_scores_url)
        self.browser.getLink("Download csv file").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'text/csv; charset=UTF-8')
        # ... but can't validate courses a second time
        self.browser.open(self.edit_scores_url)
        self.browser.getControl("Validate").click()
        self.assertTrue(
            'Course results have already been validated.'
            in self.browser.contents)

    def test_lecturers_can_download_course_tickets(self):
        # A course ticket slip can be downloaded
        self.course.title = (u'Lorem ipsum     dolor sit amet, consectetur     adipisici, '
                             u'sed         eiusmod tempor    incidunt ut  labore et dolore')
        self.login_as_lecturer()
        pdf_url = '%s/coursetickets.pdf' % self.course_url
        self.browser.open(pdf_url)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(
            self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'coursetickets.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF coursetickets.pdf written to %s" % path

    def test_lecturers_can_download_attendance_sheet(self):
        # A course ticket slip can be downloaded
        self.course.title = (u'Lorem ipsum     dolor sit amet, consectetur     adipisici, '
                             u'sed         eiusmod tempor    incidunt ut  labore et dolore')
        self.student.firstname = u'Emmanuella Woyengifigha Mercy Onosemudiana'
        self.student.lastname = u'OYAKEMIEGBEGHA'
        self.student.matric_number = u'hdk7gd62i872z27zt27ge'
        self.login_as_lecturer()
        pdf_url = '%s/attendance.pdf' % self.course_url
        self.browser.open(pdf_url)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(
            self.browser.headers['Content-Type'], 'application/pdf')
        path = os.path.join(samples_dir(), 'attendance.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF attendance.pdf written to %s" % path


    def test_lecturers_can_download_scores_as_csv(self):
        # Lecturers can download course scores as CSV.
        self.login_as_lecturer()
        self.browser.open(self.edit_scores_url)
        self.browser.getLink("Download csv file").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'text/csv; charset=UTF-8')
        self.assertEqual(self.browser.contents, 'matric_number,student_id,'
            'display_fullname,level,code,level_session,score\r\n234,'
            'K1000000,Anna Tester,100,COURSE1,2004,\r\n')

    def test_scores_csv_upload_available(self):
        # lecturers can upload a CSV file to set values.
        self.login_as_lecturer()
        # set value to change from
        self.student['studycourse']['100']['COURSE1'].score = 55
        self.browser.open(self.edit_scores_url)
        upload_ctrl = self.browser.getControl(name='uploadfile:file')
        upload_file = StringIO(UPLOAD_CSV_TEMPLATE % '65')
        upload_ctrl.add_file(upload_file, 'text/csv', 'myscores.csv')
        self.browser.getControl("Update editable scores from").click()
        # value changed
        self.assertEqual(
            self.student['studycourse']['100']['COURSE1'].score, 65)

    def test_scores_csv_upload_ignored(self):
        # for many type of file contents we simply ignore uploaded data
        self.login_as_lecturer()
        self.student['studycourse']['100']['COURSE1'].score = 55
        self.browser.open(self.edit_scores_url)
        for content, mimetype, name in (
                # empty file
                ('', 'text/foo', 'my.foo'),
                # plain ASCII text, w/o comma
                ('abcdef' * 200, 'text/plain', 'my.txt'),
                # plain UTF-8 text, with umlauts
                ('umlauts: äöü', 'text/plain', 'my.txt'),
                # csv file with only a header row
                ('student_id,score', 'text/csv', 'my.csv'),
                # csv with student_id column missing
                ('foo,score\r\nbar,66\r\n', 'text/csv', 'my.csv'),
                # csv with score column missing
                ('student_id,foo\r\nK1000000,bar\r\n', 'text/csv', 'my.csv'),
                # csv with non number as score value
                (UPLOAD_CSV_TEMPLATE % 'not-a-number', 'text/csv', 'my.csv'),
                ):
            upload_ctrl = self.browser.getControl(name='uploadfile:file')
            upload_ctrl.add_file(StringIO(content), mimetype, name)
            self.browser.getControl("Update scores").click()
            self.assertEqual(
                self.student['studycourse']['100']['COURSE1'].score, 55)
            self.assertFalse(
                'Uploaded file contains illegal data' in self.browser.contents)

    def test_scores_csv_upload_warn_illegal_chars(self):
        # for some types of files we issue a warning if upload data
        # contains illegal chars (and ignore the data)
        self.login_as_lecturer()
        self.student['studycourse']['100']['COURSE1'].score = 55
        self.browser.open(self.edit_scores_url)
        for content, mimetype, name in (
                # plain ASCII text, commas, control chars
                ('abv,qwe\n\r\r\t\b\n' * 20, 'text/plain', 'my.txt'),
                # image data (like a JPEG image)
                (open(SAMPLE_IMAGE, 'rb').read(), 'image/jpg', 'my.jpg'),
                ):
            upload_ctrl = self.browser.getControl(name='uploadfile:file')
            upload_ctrl.add_file(StringIO(content), mimetype, name)
            self.browser.getControl("Update editable scores").click()
            self.assertEqual(
                self.student['studycourse']['100']['COURSE1'].score, 55)
            self.assertTrue(
                'Uploaded file contains illegal data' in self.browser.contents)

class ParentsUITests(StudentsFullSetup):
    # Tests for UI actions when acting as parents.

    def test_request_ppw(self):
        self.app['students'][self.student_id].parents_email = 'par@yy.zz'
        self.browser.open('http://localhost/app/requestppw')
        self.browser.getControl(name="form.lastname").value = 'tESTer'
        self.browser.getControl(name="form.number").value = '123'
        self.browser.getControl(name="form.email").value = 'par@yy.zz'
        self.browser.getControl("Send temporary login credentials").click()
        self.assertTrue('Your password request was successful.'
            in self.browser.contents)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertTrue('zope.anybody - students.browser.RequestParentsPasswordPage - '
                        '123 (K1000000) - par@yy.zz' in logcontent)
        return

    def test_login_as_parents(self):
        # Student login still works after all the changes made
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertTrue('You logged in' in self.browser.contents)
        self.browser.open(self.edit_personal_path)
        self.browser.getLink("Logout").click()
        self.assertTrue('You have been logged out' in self.browser.contents)
        # We set parents password
        self.app['students'][self.student_id].setParentsPassword('ppwd')
        self.browser.open(self.login_path)
        # Student can't login with original password
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'spwd'
        self.browser.getControl("Login").click()
        self.assertEqual(self.browser.url, self.login_path)
        self.assertTrue('Your account has been temporarily deactivated '
            'because your parents have logged in.' in self.browser.contents)
        # Parents can login with their password
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = self.student_id
        self.browser.getControl(name="form.password").value = 'ppwd'
        self.browser.getControl("Login").click()
        self.assertTrue(
            'You logged in as a student.' in self.browser.contents)
        self.assertTrue(
            '<a href="http://localhost/app/students/K1000000">Base Data</a>'
            in self.browser.contents)
        # They do not see all links ...
        self.assertFalse(
            '<a href="http://localhost/app/students/K1000000/history">History</a>'
            in self.browser.contents)
        # ... and can't change anything
        self.assertRaises(
            Unauthorized, self.browser.open, self.edit_personal_path)
        # If the password has expired, parents are logged out and the
        # student can login again with the original password
        delta = timedelta(minutes=11)
        self.app['students'][self.student_id].parents_password[
            'timestamp'] = datetime.utcnow() - delta
        self.app['students'][self.student_id]._p_changed = True
        self.assertRaises(
            Unauthorized, self.browser.open, self.student_path)
        # Parents login is written to log file
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'K1000000 - browser.pages.LoginPage - K1000000 - Parents logged in'
            in logcontent)
