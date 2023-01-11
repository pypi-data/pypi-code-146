## $Id: test_student.py 16827 2022-02-22 12:48:36Z henrik $
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
"""Tests for students and related.
"""
import os
import re
import unittest
import grok
from cStringIO import StringIO
from datetime import tzinfo
from zope.component import getUtility, queryUtility, createObject
from zope.catalog.interfaces import ICatalog
from zope.component.interfaces import IFactory
from zope.event import notify
from zope.interface import verify
from zope.schema.interfaces import RequiredMissing
from hurry.workflow.interfaces import IWorkflowState
from waeup.kofa.interfaces import IExtFileStore, IFileStoreNameChooser
from waeup.kofa.students.student import (
    Student, StudentFactory, handle_student_removed, path_from_studid)
from waeup.kofa.students.studycourse import StudentStudyCourse
from waeup.kofa.students.studylevel import StudentStudyLevel, CourseTicket
from waeup.kofa.students.payments import StudentPaymentsContainer
from waeup.kofa.students.accommodation import StudentAccommodation, BedTicket
from waeup.kofa.students.interfaces import (
    IStudent, IStudentStudyCourse, IStudentPaymentsContainer,
    IStudentAccommodation, IStudentStudyLevel, ICourseTicket, IBedTicket,
    IStudentNavigation, IStudentsUtils)
from waeup.kofa.students.tests.test_batching import StudentImportExportSetup
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.university.department import Department

class HelperTests(unittest.TestCase):
    # Tests for helper functions in student module.

    def test_path_from_studid(self):
        # make sure we get predictable paths from student ids.
        self.assertEqual(
            path_from_studid('K1000000'), u'01000/K1000000')
        self.assertEqual(
            path_from_studid('K1234567'), u'01234/K1234567')
        self.assertEqual(
            path_from_studid('K12345678'), u'12345/K12345678')
        # The algorithm works also for overlong numbers, just to be
        # sure.
        self.assertEqual(
            path_from_studid('K123456789'), u'123456/K123456789')
        # low numbers (< 10**6) are treated special: they get max. of
        # 10,000 entries. That's mainly because of old students
        # migrated into our portal.
        self.assertEqual(
            path_from_studid('KM123456'), u'00120/KM123456')
        return

class StudentTest(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentTest, self).setUp()
        self.student = Student()
        self.student.firstname = u'Anna'
        self.student.lastname = u'Tester'
        self.studycourse = StudentStudyCourse()
        self.studylevel = StudentStudyLevel()
        self.studylevel.level_session = 2015
        self.courseticket = CourseTicket()
        self.payments = StudentPaymentsContainer()
        self.accommodation = StudentAccommodation()
        self.bedticket = BedTicket()
        return

    def tearDown(self):
        super(StudentTest, self).tearDown()
        return

    def test_interfaces(self):
        verify.verifyClass(IStudent, Student)
        verify.verifyClass(IStudentNavigation, Student)
        verify.verifyObject(IStudent, self.student)
        verify.verifyObject(IStudentNavigation, self.student)

        verify.verifyClass(IStudentStudyCourse, StudentStudyCourse)
        verify.verifyClass(IStudentNavigation, StudentStudyCourse)
        verify.verifyObject(IStudentStudyCourse, self.studycourse)
        verify.verifyObject(IStudentNavigation, self.studycourse)

        verify.verifyClass(IStudentStudyLevel, StudentStudyLevel)
        verify.verifyClass(IStudentNavigation, StudentStudyLevel)
        verify.verifyObject(IStudentStudyLevel, self.studylevel)
        verify.verifyObject(IStudentNavigation, self.studylevel)

        verify.verifyClass(ICourseTicket, CourseTicket)
        verify.verifyClass(IStudentNavigation, CourseTicket)
        verify.verifyObject(ICourseTicket, self.courseticket)
        verify.verifyObject(IStudentNavigation, self.courseticket)

        verify.verifyClass(IStudentPaymentsContainer, StudentPaymentsContainer)
        verify.verifyClass(IStudentNavigation, StudentPaymentsContainer)
        verify.verifyObject(IStudentPaymentsContainer, self.payments)
        verify.verifyObject(IStudentNavigation, self.payments)

        verify.verifyClass(IStudentAccommodation, StudentAccommodation)
        verify.verifyClass(IStudentNavigation, StudentAccommodation)
        verify.verifyObject(IStudentAccommodation, self.accommodation)
        verify.verifyObject(IStudentNavigation, self.accommodation)

        verify.verifyClass(IBedTicket, BedTicket)
        verify.verifyClass(IStudentNavigation, BedTicket)
        verify.verifyObject(IBedTicket, self.bedticket)
        verify.verifyObject(IStudentNavigation, self.bedticket)
        return

    def test_base(self):
        department = Department()
        studycourse = StudentStudyCourse()
        self.assertRaises(
            TypeError, studycourse.addStudentStudyLevel, department)
        studylevel = StudentStudyLevel()
        self.assertRaises(
            TypeError, studylevel.addCourseTicket, department, department)

    def test_booking_date(self):
        isinstance(self.bedticket.booking_date.tzinfo, tzinfo)
        self.assertEqual(self.bedticket.booking_date.tzinfo, None)
        return

    def test_maint_payment_made(self):
        self.assertFalse(self.bedticket.maint_payment_made)
        return


class StudentRemovalTests(StudentImportExportSetup):
    # Test handle_student_removed
    #
    # This is a complex action updating several CSV files and moving
    # stored files to a backup location.
    #
    # These tests make no assumptions about the CSV files except that
    # they contain a deletion timestamp at end of each data row

    layer = FunctionalLayer

    def setUp(self):
        super(StudentRemovalTests, self).setUp()
        self.setup_for_export()
        self.certificate2 = createObject('waeup.Certificate')
        self.certificate2.code = 'CERT2'
        self.certificate2.application_category = 'basic'
        self.certificate2.start_level = 200
        self.certificate2.end_level = 500
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate2)
        return

    def create_passport_img(self, student):
        # create some passport file for `student`
        storage = getUtility(IExtFileStore)
        image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        self.image_contents = open(image_path, 'rb').read()
        file_id = IFileStoreNameChooser(student).chooseName(
            attr='passport.jpg')
        storage.createFile(file_id, StringIO(self.image_contents))

    def test_backup_single_student_data(self):
        # when a single student is removed, the data is backed up.
        self.setup_student(self.student)
        # Add a fake image
        self.create_passport_img(self.student)
        handle_student_removed(self.student, None)
        del_dir = self.app['datacenter'].deleted_path
        del_img_path = os.path.join(
            del_dir, 'media', 'students', '00110', 'A111111',
            'passport_A111111.jpg')
        # The image was copied over
        self.assertTrue(os.path.isfile(del_img_path))
        self.assertEqual(
            open(del_img_path, 'rb').read(),
            self.image_contents)
        # The student data were put into CSV files
        STUDENT_BACKUP_EXPORTER_NAMES = getUtility(
            IStudentsUtils).STUDENT_BACKUP_EXPORTER_NAMES
        for name in STUDENT_BACKUP_EXPORTER_NAMES:
            if name[-2:-1] == '_':
                continue
            csv_path = os.path.join(del_dir, '%s.csv' % name)
            self.assertTrue(os.path.isfile(csv_path))
            contents = open(csv_path, 'rb').read().split('\r\n')
            # We expect 3 lines output including a linebreak at end of file.
            self.assertEqual(len(contents), 3)
        return

    def test_backup_single_graduated_data(self):
        # when a single graduated student is removed, the data is backed up
        # somewhere else
        self.setup_student(self.student)
        IWorkflowState(self.student).setState('graduated')
        # Add a fake image
        self.create_passport_img(self.student)
        handle_student_removed(self.student, None)
        del_dir = self.app['datacenter'].graduated_path
        del_img_path = os.path.join(
            del_dir, 'media', 'students', '00110', 'A111111',
            'passport_A111111.jpg')
        # The image was copied over
        self.assertTrue(os.path.isfile(del_img_path))
        self.assertEqual(
            open(del_img_path, 'rb').read(),
            self.image_contents)
        # The student data were put into CSV files
        STUDENT_BACKUP_EXPORTER_NAMES = getUtility(
            IStudentsUtils).STUDENT_BACKUP_EXPORTER_NAMES
        for name in STUDENT_BACKUP_EXPORTER_NAMES:
            if name[-2:-1] == '_':
                continue
            csv_path = os.path.join(del_dir, '%s.csv' % name)
            self.assertTrue(os.path.isfile(csv_path))
            contents = open(csv_path, 'rb').read().split('\r\n')
            # We expect 3 lines output including a linebreak at end of file.
            self.assertEqual(len(contents), 3)
        return

    def test_backup_single_graduated_transferred_data(self):
        del_dir = self.app['datacenter'].graduated_path
        # when a single graduated student is removed, the data is backed up
        # somewhere else including previous study courses
        self.setup_student(self.student)
        error = self.student.transfer(self.certificate2, current_session=2013)
        self.assertTrue(error == None)
        IWorkflowState(self.student).setState('graduated')
        handle_student_removed(self.student, None)
        # The previous study course data were put into CSV files
        name = 'studentstudycourses_1'
        csv_path = os.path.join(del_dir, '%s.csv' % name)
        self.assertTrue(os.path.isfile(csv_path))
        contents = open(csv_path, 'rb').read().split('\r\n')
        # We expect 3 lines output including a linebreak at end of file.
        self.assertEqual(len(contents), 3)
        name = 'studentstudycourses_2'
        csv_path = os.path.join(del_dir, '%s.csv' % name)
        self.assertTrue(os.path.isfile(csv_path))
        contents = open(csv_path, 'rb').read().split('\r\n')
        # We expect only 2 lines output including a linebreak at end of file.
        self.assertEqual(len(contents), 2)
        name = 'studentstudylevels_1'
        csv_path = os.path.join(del_dir, '%s.csv' % name)
        self.assertTrue(os.path.isfile(csv_path))
        contents = open(csv_path, 'rb').read().split('\r\n')
        # We expect 3 lines output including a linebreak at end of file.
        self.assertEqual(len(contents), 3)
        name = 'coursetickets_1'
        csv_path = os.path.join(del_dir, '%s.csv' % name)
        self.assertTrue(os.path.isfile(csv_path))
        contents = open(csv_path, 'rb').read().split('\r\n')
        # We expect 3 lines output including a linebreak at end of file.
        self.assertEqual(len(contents), 3)
        return

    def test_backup_append_csv(self):
        # when several students are removed, existing CSVs are appended
        self.setup_student(self.student)
        # Add a fake image
        self.create_passport_img(self.student)
        del_dir = self.app['datacenter'].deleted_path
        # put fake data into students.csv with trailing linebreak
        students_csv = os.path.join(del_dir, 'students.csv')
        open(students_csv, 'wb').write('line1\r\nline2\r\n')
        handle_student_removed(self.student, None)
        contents = open(students_csv, 'rb').read().split('\r\n')
        # there should be 4 lines in result csv (including trailing linebreak)
        self.assertEqual(len(contents), 4)
        return

    def test_old_files_removed(self):
        # make sure old files are not accessible any more
        self.setup_student(self.student)
        # Add a fake image
        self.create_passport_img(self.student)
        # make sure we can access the image before removal
        file_store = getUtility(IExtFileStore)
        image = file_store.getFileByContext(self.student, attr='passport.jpg')
        self.assertTrue(image is not None)

        # remove image (hopefully)
        handle_student_removed(self.student, None)

        # the is not accessible anymore
        image = file_store.getFileByContext(self.student, attr='passport.jpg')
        self.assertEqual(image, None)
        return

    def test_csv_file_entries_have_timestamp(self):
        # each row in written csv files has a ``del_date`` column to
        # tell when the associated student was deleted
        self.setup_student(self.student)
        del_dir = self.app['datacenter'].deleted_path
        students_csv = os.path.join(del_dir, 'students.csv')
        handle_student_removed(self.student, None)
        contents = open(students_csv, 'rb').read().split('\r\n')
        # the CSV header ends with a ``del_date`` column
        self.assertTrue(contents[0].endswith(',del_date'))
        # each line ends with an UTC timestamp
        timestamp = contents[1][-23:]
        self.assertTrue(re.match(
            '^\d\d-\d\d-\d\d \d\d:\d\d:\d\d\+00:00$', timestamp))
        return

class StudentTransferTests(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentTransferTests, self).setUp()

        # Add additional certificate
        self.certificate2 = createObject('waeup.Certificate')
        self.certificate2.code = 'CERT2'
        self.certificate2.application_category = 'basic'
        self.certificate2.start_level = 200
        self.certificate2.end_level = 500
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate2)

        # Add student with subobjects
        student = Student()
        self.app['students'].addStudent(student)
        student = self.setup_student(student)
        notify(grok.ObjectModifiedEvent(student))
        self.student = self.app['students'][student.student_id]
        return

    def test_transfer_student(self):
        self.assertRaises(
            RequiredMissing, self.student.transfer, self.certificate2)
        error = self.student.transfer(self.certificate2, current_session=1000)
        self.assertTrue(error == -1)
        error = self.student.transfer(self.certificate2, current_session=2013)
        self.assertTrue(error == None)
        self.assertEqual(self.student['studycourse_1'].certificate.code, 'CERT1')
        self.assertEqual(self.student['studycourse'].certificate.code, 'CERT2')
        self.assertEqual(self.student['studycourse_1'].current_session, 2012)
        self.assertEqual(self.student['studycourse'].current_session, 2013)
        self.assertEqual(self.student['studycourse'].entry_session,
            self.student['studycourse_1'].entry_session)
        self.assertEqual(self.student['studycourse_1'].__name__, 'studycourse_1')
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue('system - K1000000 - transferred from CERT1 to CERT2'
            in logcontent)
        messages = ' '.join(self.student.history.messages)
        self.assertMatches(
            '...<YYYY-MM-DD hh:mm:ss> UTC - '
            'Transferred from CERT1 to CERT2 by system', messages)

        # The students_catalog has been updated.
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(certcode=('CERT1', 'CERT1'))
        results = [x for x in results]
        self.assertEqual(len(results), 0)
        results = cat.searchResults(certcode=('CERT2', 'CERT2'))
        results = [x for x in results]
        self.assertEqual(len(results), 1)
        assert results[0] is self.app['students'][self.student.student_id]
        results = cat.searchResults(current_session=(2013,2013))
        results = [x for x in results]
        self.assertEqual(len(results), 1)
        assert results[0] is self.app['students'][self.student.student_id]

        # studycourse_1 is the previous course.
        self.assertFalse(self.student['studycourse'].is_previous)
        self.assertTrue(self.student['studycourse_1'].is_previous)

        # Students can be transferred (only) two times.
        error = self.student.transfer(self.certificate,
            current_session=2013)
        self.assertTrue(error == None)
        error = self.student.transfer(self.certificate2,
            current_session=2013)
        self.assertTrue(error == -3)
        self.assertEqual([i for i in self.student.keys()],
            [u'accommodation', u'payments', u'studycourse',
             u'studycourse_1', u'studycourse_2'])

        # The studycourse with highest order number is the previous
        # course.
        self.assertFalse(self.student['studycourse'].is_previous)
        self.assertFalse(self.student['studycourse_1'].is_previous)
        self.assertTrue(self.student['studycourse_2'].is_previous)

        # The students_catalog has been updated again.
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(certcode=('CERT1', 'CERT1'))
        results = [x for x in results]
        self.assertEqual(len(results), 1)
        assert results[0] is self.app['students'][self.student.student_id]

        # Previous transfer can be successively reverted.
        self.assertEqual(self.student['studycourse_2'].certificate.code, 'CERT2')
        self.assertEqual(self.student['studycourse_1'].certificate.code, 'CERT1')
        self.assertEqual(self.student['studycourse'].certificate.code, 'CERT1')
        error = self.student.revert_transfer()
        self.assertTrue(error == None)
        self.assertEqual([i for i in self.student.keys()],
            [u'accommodation', u'payments', u'studycourse',
             u'studycourse_1'])
        self.assertEqual(self.student['studycourse_1'].certificate.code, 'CERT1')
        self.assertEqual(self.student['studycourse'].certificate.code, 'CERT2')
        # The students_catalog has been updated again.
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(certcode=('CERT2', 'CERT2'))
        results = [x for x in results]
        self.assertEqual(len(results), 1)
        assert results[0] is self.app['students'][self.student.student_id]
        error = self.student.revert_transfer()
        self.assertTrue(error == None)
        self.assertEqual([i for i in self.student.keys()],
            [u'accommodation', u'payments', u'studycourse'])
        self.assertEqual(self.student['studycourse'].certificate.code, 'CERT1')
        error = self.student.revert_transfer()
        self.assertTrue(error == -1)
        # The students_catalog has been updated again.
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(certcode=('CERT1', 'CERT1'))
        results = [x for x in results]
        self.assertEqual(len(results), 1)
        assert results[0] is self.app['students'][self.student.student_id]
        results = cat.searchResults(certcode=('CERT2', 'CERT2'))
        results = [x for x in results]
        self.assertEqual(len(results), 0)
        logcontent = open(logfile).read()
        self.assertTrue('system - K1000000 - transfer reverted'
            in logcontent)
        messages = ' '.join(self.student.history.messages)
        self.assertTrue('Transfer reverted by system' in messages)
        return

class StudentFactoryTest(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentFactoryTest, self).setUp()
        self.factory = StudentFactory()

    def tearDown(self):
        super(StudentFactoryTest, self).tearDown()

    def test_interfaces(self):
        verify.verifyClass(IFactory, StudentFactory)
        verify.verifyObject(IFactory, self.factory)

    def test_factory(self):
        obj = self.factory()
        assert isinstance(obj, Student)

    def test_getInterfaces(self):
        implemented_by = self.factory.getInterfaces()
        assert implemented_by.isOrExtends(IStudent)
