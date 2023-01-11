## $Id: test_applicantcopier.py 16545 2021-07-13 14:08:06Z henrik $
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
Tests for the creation of student containers with data from admitted applicants.
"""
import os
import grok
from StringIO import StringIO
from datetime import datetime
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from zope.event import notify
from zope.component import getUtility
from zope.i18n import translate
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.interfaces import IExtFileStore, IFileStoreNameChooser
from waeup.kofa.applicants.tests.test_browser import ApplicantsFullSetup
from waeup.kofa.browser.tests.test_pdf import samples_dir

session = datetime.now().year - 2

class ApplicantCopierFunctionalTests(ApplicantsFullSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantCopierFunctionalTests, self).setUp()
        return

    def prepare_applicant(self):
        self.browser.open(self.manage_path)
        self.fill_correct_values()
        self.browser.getControl("Save").click()
        # Upload a passport picture
        ctrl = self.browser.getControl(name='form.passport')
        file_obj = open(
            os.path.join(os.path.dirname(__file__), 'test_image.jpg'),'rb')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file_obj, filename='my_photo.jpg')
        self.browser.getControl("Save").click() # submit form
        return

    def test_applicant_student_copier(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.prepare_applicant()
        storage = getUtility(IExtFileStore)
        # The stored image can be fetched
        file_id = IFileStoreNameChooser(self.applicant).chooseName()
        fd = storage.getFile(file_id)
        file_len_orig = len(fd.read())
        # We store a test pdf file
        dummy_file = StringIO('test file')
        testfile_id = IFileStoreNameChooser(
            self.applicant).chooseName(attr='testfile.jpg')
        test_file = storage.createFile(testfile_id, dummy_file)
        # The stored file can be fetched
        fd = storage.getFile(testfile_id)
        testfile_len_orig = len(fd.read())
        self.assertEqual(self.app['students']._curr_stud_id, 1000000)
        # Let's try to create the student
        (success, msg) = self.applicant.createStudent()
        self.assertTrue(msg == 'Applicant has not yet been admitted.')
        IWorkflowState(self.applicant).setState('admitted')
        (success, msg) = self.applicant.createStudent()
        # Current student_id has not changed.
        self.assertEqual(self.app['students']._curr_stud_id, 1000000)
        self.assertTrue(msg == 'No study course provided.')
        self.browser.open(self.manage_path)
        self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click()
        # Maybe the certificate has meanwhile been removed
        del self.app['faculties']['fac1']['dep1'].certificates['CERT1']
        (success, msg) = self.applicant.createStudent()
        self.assertFalse(success)
        self.assertTrue('ConstraintNotSatisfied: CERT1' in msg)
        # Current student_id has not changed.
        self.assertEqual(self.app['students']._curr_stud_id, 1000000)
        # Ok, lets add the certificate and try again
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate)
        # Managers are not allowed to trigger the create transition manually
        self.assertFalse('<option value="create">' in self.browser.contents)
        # Student can be created
        (success, msg) = self.applicant.createStudent()
        self.assertTrue('created' in msg)
        # Current student_id has not changed.
        self.assertEqual(self.app['students']._curr_stud_id, 1000001)
        # The applicant is locked
        self.assertTrue(self.applicant.locked)
        student_id = translate(msg, 'waeup.kofa').split()[1]
        # View student container just created
        student = self.app['students'][student_id]
        student_path = 'http://localhost/app/students/%s' % student_id
        self.browser.open(student_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, student_path)
        # Student is in state admitted
        self.assertEqual(student.state, 'admitted')
        # Attributes properly set?
        self.assertEqual(student.email, 'xx@yy.zz')
        self.assertEqual(student.firstname, 'John')
        self.assertEqual(student.middlename, 'Anthony')
        self.assertEqual(student.lastname, 'Tester')
        # student_id set in application record?
        self.assertEqual(self.applicant.student_id, student.student_id)
        # Check if passport image has been copied
        file_id = IFileStoreNameChooser(student).chooseName(attr='passport.jpg')
        fd = storage.getFile(file_id)
        file_len = len(fd.read())
        self.assertEqual(file_len_orig, file_len)
        # Check if test file has been copied too (new)
        file_id = IFileStoreNameChooser(student).chooseName(attr='testfile.jpg')
        fd = storage.getFile(file_id)
        file_len = len(fd.read())
        self.assertEqual(testfile_len_orig, file_len)
        # Check if application slip exists and is a PDF file
        file_id = IFileStoreNameChooser(
            student).chooseName(attr='application_slip.pdf')
        pdf = storage.getFile(file_id).read()
        self.assertTrue(len(pdf) > 0)
        self.assertEqual(pdf[:8], '%PDF-1.4')
        path = os.path.join(samples_dir(), 'application_slip.pdf')
        open(path, 'wb').write(pdf)
        print "Sample PDF application_slip.pdf written to %s" % path
        # Check if there is an application slip link in UI
        self.assertTrue('Application Slip' in self.browser.contents)
        self.browser.getLink("Application Slip").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        # Has the student been properly indexed?
        # Yes, we can find the student in department
        self.browser.open('http://localhost/app/students')
        self.browser.getControl(name="searchtype").value = ['depcode']
        self.browser.getControl(name="searchterm").value = 'dep1'
        self.browser.getControl("Find student(s)").click()
        self.assertMatches('...John Anthony Tester...', self.browser.contents)
        # Has the student studycourse the correct attributes?
        self.assertEqual(student['studycourse'].certificate.code, 'CERT1')
        self.assertEqual(student['studycourse'].entry_session, session)
        self.assertEqual(student['studycourse'].entry_mode, 'ug_ft')
        self.assertEqual(student['studycourse'].current_session, session)
        self.assertEqual(student['studycourse'].current_level, 100)

    def test_applicant_graduated_copier(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.prepare_applicant()
        storage = getUtility(IExtFileStore)
        # The stored image can be fetched
        file_id = IFileStoreNameChooser(self.applicant).chooseName()
        fd = storage.getFile(file_id)
        file_len_orig = len(fd.read())
        # We store a test pdf file
        dummy_file = StringIO('test file')
        testfile_id = IFileStoreNameChooser(
            self.applicant).chooseName(attr='testfile.pdf')
        test_file = storage.createFile(testfile_id, dummy_file)
        # The stored file can be fetched
        fd = storage.getFile(testfile_id)
        testfile_len_orig = len(fd.read())
        self.assertEqual(self.app['students']._curr_stud_id, 1000000)
        # Let's try to create the student
        (success, msg) = self.applicant.createStudent(graduated=True)
        self.assertTrue(msg == 'Applicant has not yet been processed.')
        IWorkflowState(self.applicant).setState('processed')
        (success, msg) = self.applicant.createStudent(graduated=True)
        # Current student_id has not changed.
        self.assertEqual(self.app['students']._curr_stud_id, 1000000)
        self.assertTrue(msg == 'No study course provided.')
        # The course_studied field is not used in the base package. Thus we
        # have to set the attribute manually.
        self.applicant.course_studied = self.certificate
        self.browser.open(self.manage_path)
        self.browser.getControl("Save").click()
        # Maybe the certificate has meanwhile been removed
        del self.app['faculties']['fac1']['dep1'].certificates['CERT1']
        (success, msg) = self.applicant.createStudent(graduated=True)
        self.assertFalse(success)
        self.assertTrue('ConstraintNotSatisfied: CERT1' in msg)
        # Current student_id has not changed.
        self.assertEqual(self.app['students']._curr_stud_id, 1000000)
        # Ok, lets add the certificate and try again
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate)
        # Managers are not allowed to trigger the create transition manually
        self.assertFalse('<option value="create">' in self.browser.contents)
        # Graduated student can be created
        (success, msg) = self.applicant.createStudent(graduated=True)
        self.assertTrue('created' in msg)
        # Current student_id has not changed.
        self.assertEqual(self.app['students']._curr_stud_id, 1000001)
        student_id = translate(msg, 'waeup.kofa').split()[1]
        # View student container just created
        student = self.app['students'][student_id]
        student_path = 'http://localhost/app/students/%s' % student_id
        self.browser.open(student_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, student_path)
        # Student is in state graduated
        self.assertEqual(student.state, 'graduated')
        # Attributes properly set?
        self.assertEqual(student.email, 'xx@yy.zz')
        self.assertEqual(student.firstname, 'John')
        self.assertEqual(student.middlename, 'Anthony')
        self.assertEqual(student.lastname, 'Tester')
        # student_id set in application record?
        self.assertEqual(self.applicant.student_id, student.student_id)
        # Check if passport image has been copied
        file_id = IFileStoreNameChooser(student).chooseName(attr='passport.jpg')
        fd = storage.getFile(file_id)
        file_len = len(fd.read())
        self.assertEqual(file_len_orig, file_len)
        # Check if test file has been copied too (new)
        file_id = IFileStoreNameChooser(student).chooseName(attr='testfile.jpg')
        fd = storage.getFile(file_id)
        file_len = len(fd.read())
        self.assertEqual(testfile_len_orig, file_len)
        # Check if application slip exists and is a PDF file
        file_id = IFileStoreNameChooser(
            student).chooseName(attr='application_slip.pdf')
        pdf = storage.getFile(file_id).read()
        self.assertTrue(len(pdf) > 0)
        self.assertEqual(pdf[:8], '%PDF-1.4')
        path = os.path.join(samples_dir(), 'application_slip.pdf')
        open(path, 'wb').write(pdf)
        print "Sample PDF application_slip.pdf written to %s" % path
        # Check if there is an application slip link in UI
        self.assertTrue('Application Slip' in self.browser.contents)
        self.browser.getLink("Application Slip").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        # Has the student been properly indexed?
        # Yes, we can find the student in department
        self.browser.open('http://localhost/app/students')
        self.browser.getControl(name="searchtype").value = ['depcode']
        self.browser.getControl(name="searchterm").value = 'dep1'
        self.browser.getControl("Find student(s)").click()
        self.assertMatches('...John Anthony Tester...', self.browser.contents)
        # Has the student studycourse the correct attributes?
        self.assertEqual(student['studycourse'].certificate.code, 'CERT1')
        self.assertEqual(student['studycourse'].entry_session, session)
        self.assertEqual(student['studycourse'].entry_mode, 'ug_ft')
        self.assertEqual(student['studycourse'].current_session, session)
        self.assertEqual(student['studycourse'].current_level, 100)

    def test_batch_copying(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.prepare_applicant()
        IWorkflowState(self.applicant).setState('admitted')
        self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click()
        self.browser.open(self.manage_container_path)
        self.browser.getControl("Create students from selected", index=0).click()
        self.assertTrue('No applicant selected' in self.browser.contents)
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value=self.applicant.application_number).selected = True
        self.browser.getControl("Create students from selected", index=0).click()
        self.assertTrue('1 students successfully created' in self.browser.contents)

    def test_hidden_batch_copying_container(self):
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.prepare_applicant()
        self.browser.open(self.container_path + '/createallstudents')
        self.assertTrue('No record found' in self.browser.contents)
        self.assertFalse('Failed records' in self.browser.contents)
        self.assertFalse('Successfully created records' in self.browser.contents)
        IWorkflowState(self.applicant).setState('admitted')
        notify(grok.ObjectModifiedEvent(self.applicant))
        self.browser.open(self.container_path + '/createallstudents')
        self.assertTrue('No study course provided' in self.browser.contents)
        self.assertFalse('Successfully created records' in self.browser.contents)
        self.assertTrue('Failed records' in self.browser.contents)
        self.browser.open(self.manage_path)
        self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click()
        # date_of_birth is not required for applicants but for students
        self.applicant.date_of_birth = None
        self.browser.open(self.container_path + '/createallstudents')
        self.assertTrue('RequiredMissing: date_of_birth' in self.browser.contents)
        self.assertTrue('Failed records' in self.browser.contents)
        self.assertFalse('Successfully created records' in self.browser.contents)
        self.browser.open(self.manage_path)
        self.browser.getControl(name="form.date_of_birth").value = '09/09/1988'
        self.browser.getControl("Save").click()
        self.browser.open(self.container_path + '/createallstudents')
        self.assertFalse('Failed records' in self.browser.contents)
        self.assertTrue('Successfully created records' in self.browser.contents)

    def test_hidden_batch_copying_all(self):
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.prepare_applicant()
        self.browser.open(self.manage_path)
        self.browser.getControl(name="form.date_of_birth").value = '09/09/1988'
        #self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click()
        IWorkflowState(self.applicant).setState('admitted')
        notify(grok.ObjectModifiedEvent(self.applicant))
        self.browser.open(self.root_path + '/createallstudents')
        self.assertTrue('No study course provided' in self.browser.contents)
        self.applicant.course_admitted = self.certificate
        self.browser.open(self.root_path + '/createallstudents')
        self.assertTrue('Successfully created records:' in self.browser.contents)

    def test_copier_wo_passport(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        self.fill_correct_values()
        # Let's try to create the student
        IWorkflowState(self.applicant).setState('admitted')
        self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click()
        (success, msg) = self.applicant.createStudent()
        self.assertTrue('created' in msg)

    def test_copier_with_defective_passport_image(self):
        IWorkflowState(self.applicant).setState('admitted')
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        self.fill_correct_values()
        self.browser.getControl("Save").click()
        # Upload a passport picture
        ctrl = self.browser.getControl(name='form.passport')
        # This file has really been uploaded by KwaraPoly student
        # Until 4/1/15 these files resulted a traceback when opening
        # the createallstudents page. The traceback is now catched.
        file_obj = open(
            os.path.join(os.path.dirname(__file__), 'fake_image.jpg'),'rb')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file_obj, filename='my_photo.jpg')
        self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click() # submit form
        (success, msg) = self.applicant.createStudent()
        self.assertTrue(msg == 'IOError: Application Slip could not be created.')
        # The same in the UI
        self.browser.open(self.manage_container_path)
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value=self.applicant.application_number).selected = True
        self.browser.getControl("Create students from selected", index=0).click()
        self.assertTrue('No student could be created.' in self.browser.contents)
        self.browser.open(self.container_path + '/createallstudents')
        self.assertTrue(
            'IOError: Application Slip could not be created.'
            in self.browser.contents)

    def disabled_test_delay(self):
        # Create portalmanager manager
        self.app['users'].addUser('mrportalmanager', 'mrportalmanagersecret')
        self.app['users']['mrportalmanager'].email = 'mrportalmanager@foo.ng'
        self.app['users']['mrportalmanager'].title = 'Carlos Portales'
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal(
            'waeup.PortalManager', 'mrportalmanager')
        # Login as portal manager
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrportalmanager'
        self.browser.getControl(name="form.password").value = 'mrportalmanagersecret'
        self.browser.getControl("Login").click()
        self.prepare_applicant()
        self.browser.open(self.manage_path)
        self.browser.getControl(name="form.date_of_birth").value = '09/09/1988'
        self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click()
        IWorkflowState(self.applicant).setState('admitted')
        notify(grok.ObjectModifiedEvent(self.applicant))
        start = datetime.now()
        self.browser.open(self.root_path + '/createallstudents')
        self.assertTrue('1 students successfully created' in self.browser.contents)
        self.assertTrue((datetime.now() - start).seconds >= 10)
