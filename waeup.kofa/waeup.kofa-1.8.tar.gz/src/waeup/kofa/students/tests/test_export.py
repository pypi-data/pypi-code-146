## $Id: test_export.py 16831 2022-02-24 10:23:10Z henrik $
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

import os
import grok
import datetime
from cStringIO import StringIO
from zope.component import queryUtility, getUtility, createObject
from zope.event import notify
from zope.interface.verify import verifyObject, verifyClass
from waeup.kofa.interfaces import (
    ICSVExporter, IExtFileStore, IFileStoreNameChooser)
from waeup.kofa.students.catalog import StudentsQuery
from waeup.kofa.university.course import Course
from waeup.kofa.university.certificate import CertificateCourse
from waeup.kofa.students.export import (
    StudentExporter,
    StudentStudyCourseExporter,
    FirstStudentStudyCourseExporter,
    SecondStudentStudyCourseExporter,
    StudentStudyLevelExporter,
    FirstStudentStudyLevelExporter,
    SecondStudentStudyLevelExporter,
    CourseTicketExporter,
    FirstCourseTicketExporter,
    SecondCourseTicketExporter,
    StudentPaymentExporter, BedTicketExporter,
    SchoolFeePaymentsOverviewExporter, StudyLevelsOverviewExporter,
    ComboCardDataExporter, DataForBursaryExporter,
    UnpaidPaymentsExporter, SessionPaymentsOverviewExporter,
    OutstandingCoursesExporter,
    AccommodationPaymentsExporter,
    TranscriptDataExporter,
    TrimmedDataExporter,
    StudentTrimmedPaymentExporter,
    get_students,)
from waeup.kofa.students.accommodation import BedTicket
from waeup.kofa.students.interfaces import ICSVStudentExporter
from waeup.kofa.students.payments import StudentOnlinePayment
from waeup.kofa.students.student import Student
from waeup.kofa.students.studycourse import StudentStudyCourse
from waeup.kofa.students.studylevel import StudentStudyLevel, CourseTicket
from waeup.kofa.students.tests.test_batching import StudentImportExportSetup
from waeup.kofa.testing import FunctionalLayer

curr_year = datetime.datetime.now().year
year_range = range(curr_year - 11, curr_year + 1)
year_range_str = ','.join([str(i) for i in year_range])

class ExportHelperTests(StudentImportExportSetup):
    layer = FunctionalLayer
    def setUp(self):
        super(ExportHelperTests, self).setUp()
        student = Student()
        self.app['students'].addStudent(student)
        student = self.setup_student(student)
        notify(grok.ObjectModifiedEvent(student))
        self.student = self.app['students'][student.student_id]
        return

    def test_get_students_plain(self):
        # without a filter we get all students
        result = get_students(self.app)
        self.assertEqual(len(list(result)), 1)
        return

    def test_get_students_by_session(self):
        # we can filter out students of a certain session
        my_filter1 = StudentsQuery(current_session=2012)
        result = get_students(self.app, stud_filter=my_filter1)
        self.assertEqual(len(list(result)), 1)

        my_filter2 = StudentsQuery(current_session=1964)
        result = get_students(self.app, stud_filter=my_filter2)
        self.assertEqual(len(list(result)), 0)
        return

    def test_get_students_by_level(self):
        # we can filter out students of a certain level
        my_filter1 = StudentsQuery(current_level=200)
        result = get_students(self.app, stud_filter=my_filter1)
        self.assertEqual(len(list(result)), 1)

        my_filter2 = StudentsQuery(current_level=300)
        result = get_students(self.app, stud_filter=my_filter2)
        self.assertEqual(len(list(result)), 0)
        return

    def test_get_students_by_deptcode(self):
        # we can filter out students of a certain dept.
        my_filter1 = StudentsQuery(depcode='NA')
        result = get_students(self.app, stud_filter=my_filter1)
        self.assertEqual(len(list(result)), 1)

        my_filter2 = StudentsQuery(depcode='NOTEXISTING')
        result = get_students(self.app, stud_filter=my_filter2)
        self.assertEqual(len(list(result)), 0)
        return

    def test_get_students_by_faccode(self):
        # we can filter out students of a certain faculty.
        my_filter1 = StudentsQuery(faccode='NA')
        result = get_students(self.app, stud_filter=my_filter1)
        self.assertEqual(len(list(result)), 1)

        my_filter2 = StudentsQuery(faccode='NOTEXISTING')
        result = get_students(self.app, stud_filter=my_filter2)
        self.assertEqual(len(list(result)), 0)
        return

    def test_get_students_by_current_mode(self):
        # we can filter out students in a certain mode.
        my_filter1 = StudentsQuery(current_mode='ug_ft')
        result = get_students(self.app, stud_filter=my_filter1)
        self.assertEqual(len(list(result)), 1)

        my_filter2 = StudentsQuery(current_mode='NOTEXISTING')
        result = get_students(self.app, stud_filter=my_filter2)
        self.assertEqual(len(list(result)), 0)
        return


class StudentExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    std_csv_entry = (
        'my adm code,my clr code,1981-02-04#,anna@sample.com,,'
        'Anna,,Tester,234,M.,NG,,,"Studentroad 21\nLagos 123456\n",,'
        '+234-123-12345#,123,f,A111111,0,,,created'
        )

    def setUp(self):
        super(StudentExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = StudentExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, StudentExporter)
        return

    def test_get_as_utility(self):
        # we can get an student exporter as utility
        result = queryUtility(ICSVExporter, name="students")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can really export students
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = StudentExporter()
        exporter.export([self.student], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'adm_code,clr_code,date_of_birth,email,'
            'employer,firstname,flash_notice,lastname,matric_number,middlename,'
            'nationality,officer_comment,parents_email,'
            'perm_address,personal_updated,'
            'phone,reg_number,sex,student_id,suspended,suspended_comment,'
            'password,state,history,certcode,is_postgrad,'
            'current_level,current_session,entry_session\r\n'
            'my adm code,my clr code,'
            '1981-02-04#,anna@sample.com,,Anna,,Tester,234,M.,NG,,,'
            '"Studentroad 21\nLagos 123456\n",,+234-123-12345#,123,f,'
            'A111111,0,,,created'
            in result
            )
        return

    def test_export_all(self):
        # we can really export students
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = StudentExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'adm_code,clr_code,date_of_birth,email,'
            'employer,firstname,flash_notice,lastname,matric_number,middlename,'
            'nationality,officer_comment,parents_email,'
            'perm_address,personal_updated,'
            'phone,reg_number,sex,student_id,suspended,suspended_comment,'
            'password,state,history,certcode,is_postgrad,'
            'current_level,current_session,entry_session\r\n'
            'my adm code,my clr code,1981-02-04#,anna@sample.com,,'
            'Anna,,Tester,234,M.,NG,,,"Studentroad 21\nLagos 123456\n"'
            ',,+234-123-12345#,123,f,A111111,0,,,created'
            in result
            )
        return

    def test_export_student(self):
        # we can export a single student
        self.setup_student(self.student)
        exporter = StudentExporter()
        exporter.export_student(self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'adm_code,clr_code,date_of_birth,email,'
            'employer,firstname,flash_notice,lastname,matric_number,middlename,'
            'nationality,officer_comment,parents_email,'
            'perm_address,personal_updated,'
            'phone,reg_number,sex,student_id,suspended,suspended_comment,'
            'password,state,history,certcode,is_postgrad,'
            'current_level,current_session,entry_session\r\n'
            'my adm code,my clr code,1981-02-04#,anna@sample.com,,'
            'Anna,,Tester,234,M.,NG,,,"Studentroad 21\nLagos 123456\n"'
            ',,+234-123-12345#,123,f,A111111,0,,,created'
            in result
            )
        return

    def test_export_filtered(self):
        # we can export a filtered set of students (filtered by session/level)
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))
        exporter = StudentExporter()

        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=None)
        result1 = open(self.outfile, 'rb').read()
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=2012, current_level=None)
        result2 = open(self.outfile, 'rb').read()
        # current_level and current_session can be both a string ...
        exporter.export_filtered(
            self.app, self.outfile,
            current_session='2012', current_level=u'200')
        result3 = open(self.outfile, 'rb').read()
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=2011, current_level=None)
        result4 = open(self.outfile, 'rb').read()
        # ... and an integer
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=100)
        result5 = open(self.outfile, 'rb').read()
        # Also students at probating levels are being exported ...
        self.student['studycourse'].current_level = 210
        notify(grok.ObjectModifiedEvent(self.student))
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=200)
        result6 = open(self.outfile, 'rb').read()
        # ... but not in the wrong level range.
        self.student['studycourse'].current_level = 310
        notify(grok.ObjectModifiedEvent(self.student))
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=200)
        result7 = open(self.outfile, 'rb').read()
        self.assertTrue(self.std_csv_entry in result1)
        self.assertTrue(self.std_csv_entry in result2)
        self.assertTrue(self.std_csv_entry in result3)
        self.assertFalse(self.std_csv_entry in result4)
        self.assertFalse(self.std_csv_entry in result5)
        self.assertTrue(self.std_csv_entry in result6)
        self.assertFalse(self.std_csv_entry in result7)
        return

    def test_export_selected(self):
        # we can export a filtered set of students (filtered by session/level)
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))
        exporter = StudentExporter()
        exporter.export_selected(
            self.app, self.outfile, selected=['A111111'])
        result1 = open(self.outfile, 'rb').read()
        exporter.export_selected(
            self.app, self.outfile, selected=[])
        result2 = open(self.outfile, 'rb').read()
        self.assertTrue(self.std_csv_entry in result1)
        self.assertFalse(self.std_csv_entry in result2)
        return

    def test_export_filtered_by_dept(self):
        # we can export a set of students filtered by department
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))
        exporter = StudentExporter()
        # current_session can be both a string ...
        exporter.export_filtered(
            self.app, self.outfile,
            current_session='2012', current_level=u'200', depcode='NA')
        result1 = open(self.outfile, 'rb').read()
        # ... and an integer
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=2012, current_level=200, depcode='NODEPT')
        result2 = open(self.outfile, 'rb').read()
        self.assertTrue(self.std_csv_entry in result1)
        self.assertTrue(self.std_csv_entry not in result2)
        return

    def test_export_filtered_by_faculty(self):
        # we can export a set of students filtered by faculty
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))
        exporter = StudentExporter()

        exporter.export_filtered(
            self.app, self.outfile,
            current_session=2012, current_level='200', faccode='NA')
        result1 = open(self.outfile, 'rb').read()
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=2012, current_level=200, faccode='NOFAC')
        result2 = open(self.outfile, 'rb').read()
        self.assertTrue(self.std_csv_entry in result1)
        self.assertTrue(self.std_csv_entry not in result2)
        return



class StudentTrimmedDataExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    std_csv_entry = (
        'my adm code,my clr code,1981-02-04#,anna@sample.com,,'
        'Anna,,Tester,234,M.,NG,,,"Studentroad 21\nLagos 123456\n",,'
        '+234-123-12345#,123,f,A111111,0,,,created'
        )

    def setUp(self):
        super(StudentTrimmedDataExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = TrimmedDataExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, TrimmedDataExporter)
        return

    def test_get_as_utility(self):
        # we can get an student exporter as utility
        result = queryUtility(ICSVExporter, name="trimmed")
        self.assertTrue(result is not None)
        return

    def test_export_all(self):
        # we can really export students
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = TrimmedDataExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'student_id,matric_number,reg_number,firstname,middlename,'
            'lastname,sex,email,phone,nationality,date_of_birth,state,'
            'current_mode,certcode,faccode,depcode,current_level,'
            'current_session,current_verdict,entry_session\r\n'
            'A111111,234,123,Anna,M.,Tester,f,anna@sample.com,+234-123-12345#,'
            'NG,1981-02-04#,created,ug_ft,CERT1,NA,NA,200,2012,0,2010'
            in result
            )
        return

class StudentStudyCourseExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentStudyCourseExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = StudentStudyCourseExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, StudentStudyCourseExporter)
        return

    def test_get_as_utility(self):
        # we can get an student exporter as utility
        result = queryUtility(ICSVExporter, name="studentstudycourses")
        self.assertTrue(result is not None)
        return

    def test_export_empty(self):
        # we can export a nearly empty study course
        study_course = StudentStudyCourse()
        exporter = StudentStudyCourseExporter()
        exporter.export([study_course], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'

            ',,,0,,,0,,0\r\n'
            )
        return

    def test_export(self):
        # we can really export study courses.
        # set values we can expect in export file
        self.setup_student(self.student)
        study_course = self.student.get('studycourse')
        exporter = StudentStudyCourseExporter()
        exporter.export([study_course], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'

            'CERT1,200,2012,0,ug_ft,2010,0,A111111,0\r\n'
            )
        return

    def test_export_all(self):
        # we can really export students
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = StudentStudyCourseExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'

            'CERT1,200,2012,0,ug_ft,2010,0,A111111,0\r\n'
            )
        return

    def test_export_student(self):
        # we can export studycourse of a certain student
        self.setup_student(self.student)
        exporter = StudentStudyCourseExporter()
        exporter.export_student(self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'

            'CERT1,200,2012,0,ug_ft,2010,0,A111111,0\r\n'
            )
        return

    def test_export_filtered(self):
        # we can export studycourses of a filtered set of students
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))

        exporter = StudentStudyCourseExporter()
        exporter.export_filtered(
            self.student, self.outfile, current_session=2012)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'

            'CERT1,200,2012,0,ug_ft,2010,0,A111111,0\r\n'
            )
        return

    def test_export_selected_student_id(self):
        # we can export a filtered set of students (filtered by session/level)
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))
        exporter = StudentStudyCourseExporter()
        exporter.export_selected(
            self.app, self.outfile, selected=['A111111'])
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'

            'CERT1,200,2012,0,ug_ft,2010,0,A111111,0\r\n'
            )
        return

    def test_export_selected_matric_number(self):
        # we can export a filtered set of students (filtered by session/level)
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))
        exporter = StudentStudyCourseExporter()
        exporter.export_selected(
            self.app, self.outfile, selected=['234'])
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'

            'CERT1,200,2012,0,ug_ft,2010,0,A111111,0\r\n'
            )
        return

class PreviousStudyCourseExporterTests(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(PreviousStudyCourseExporterTests, self).setUp()
        self.setup_for_export()
        self.certificate2 = createObject('waeup.Certificate')
        self.certificate2.code = 'CERT2'
        self.certificate2.application_category = 'basic'
        self.certificate2.start_level = 200
        self.certificate2.end_level = 500
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate2)
        return

    def test_export_studycourses(self):
        self.setup_student(self.student)
        exporter = FirstStudentStudyCourseExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'
            )
        error = self.student.transfer(self.certificate2, current_session=2013)
        self.assertTrue(error == None)
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'
            'CERT1,200,2012,0,ug_ft,2010,0,A111111,1\r\n')
        error = self.student.transfer(self.certificate,
                                      current_session=2014,
                                      current_level=300)
        self.assertTrue(error == None)
        exporter = SecondStudentStudyCourseExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'
            'CERT2,,2013,,transfer,2010,,A111111,2\r\n')
        exporter = StudentStudyCourseExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'certificate,current_level,current_session,current_verdict,'
            'entry_mode,entry_session,previous_verdict,student_id,previous\r\n'
            'CERT1,300,2014,,transfer,2010,,A111111,0\r\n')
        return

    def test_export_studylevels(self):
        self.setup_student(self.student)
        exporter = FirstStudentStudyLevelExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,student_id,'
            'number_of_tickets,certcode,previous\r\n'
            )
        error = self.student.transfer(self.certificate2, current_session=2013)
        self.assertTrue(error == None)
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,student_id,'
            'number_of_tickets,certcode,previous\r\n'
            '0.00,100,2012,A,100,,,,A111111,1,CERT1,1\r\n' )
        study_level = StudentStudyLevel()
        study_level.level_session = 2015
        study_level.level_verdict = "C"
        study_level.level = 400
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate2, study_level)
        error = self.student.transfer(self.certificate,
                                      current_session=2014,
                                      current_level=300)
        self.assertTrue(error == None)
        exporter = SecondStudentStudyLevelExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,student_id,'
            'number_of_tickets,certcode,previous\r\n'
            '0.00,400,2015,C,0,,,,A111111,0,CERT2,2\r\n')
        exporter = StudentStudyLevelExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,student_id,'
            'number_of_tickets,certcode,previous\r\n')
        return

    def test_export_coursetickets(self):
        self.setup_student(self.student)
        exporter = FirstCourseTicketExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,'
            'fcode,level,level_session,mandatory,outstanding,passmark,'
            'score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            )
        error = self.student.transfer(self.certificate2, current_session=2013)
        self.assertTrue(error == None)
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,'
            'fcode,level,level_session,mandatory,outstanding,passmark,'
            'score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,'
            'A111111,CERT1,Anna M. Tester,1\r\n')
        study_level = StudentStudyLevel()
        study_level.level_session = 2015
        study_level.level_verdict = "C"
        study_level.level = 400
        self.student['studycourse'].addStudentStudyLevel(
            self.certificate2, study_level)
        ticket = CourseTicket()
        ticket.automatic = True
        ticket.carry_over = True
        ticket.code = u'CRS9'
        ticket.title = u'Course 9'
        ticket.fcode = u'FAC9'
        ticket.dcode = u'DEP9'
        ticket.credits = 150
        ticket.passmark = 100
        ticket.semester = 2
        study_level[ticket.code] = ticket
        error = self.student.transfer(self.certificate,
                                      current_session=2014,
                                      current_level=300)
        self.assertTrue(error == None)
        exporter = SecondCourseTicketExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,'
            'fcode,level,level_session,mandatory,outstanding,passmark,'
            'score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n1,1,CRS9,,150,DEP9,FAC9,400,2015,0,0,'
            '100,,2,,Course 9,A111111,CERT2,Anna M. Tester,2\r\n')
        exporter = CourseTicketExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,'
            'fcode,level,level_session,mandatory,outstanding,passmark,'
            'score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            )
        return

class StudentStudyLevelExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentStudyLevelExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = StudentStudyLevelExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, StudentStudyLevelExporter)
        return

    def test_get_as_utility(self):
        # we can get an student exporter as utility
        result = queryUtility(ICSVExporter, name="studentstudylevels")
        self.assertTrue(result is not None)
        return

    def test_export_empty(self):
        # we can export a nearly empty study level
        study_level = StudentStudyLevel()
        exporter = StudentStudyLevelExporter()
        exporter.export([study_level], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,'
            'student_id,number_of_tickets,certcode,previous\r\n'
            '0.00,,,0,0,,,,,0,,0\r\n'
            )
        return

    def test_export(self):
        # we can really export study levels.
        # set values we can expect in export file
        self.setup_student(self.student)
        study_course = self.student.get('studycourse')
        study_level = study_course[study_course.keys()[0]]
        exporter = StudentStudyLevelExporter()
        exporter.export([study_level], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,'
            'student_id,number_of_tickets,certcode,previous\r\n'
            '0.00,100,2012,A,100,,,,A111111,1,CERT1,0\r\n'
            )
        return

    def test_export_all(self):
        # we can really export study levels
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = StudentStudyLevelExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,'
            'student_id,number_of_tickets,certcode,previous\r\n'
            '0.00,100,2012,A,100,,,,A111111,1,CERT1,0\r\n'
            )
        return

    def test_export_student(self):
        # we can really export study levels of a certain student
        self.setup_student(self.student)
        exporter = StudentStudyLevelExporter()
        exporter.export_student(self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,'
            'student_id,number_of_tickets,certcode,previous\r\n'
            '0.00,100,2012,A,100,,,,A111111,1,CERT1,0\r\n'
            )
        return

    def test_export_filtered(self):
        # we can export studylevels of a filtered set of students
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))

        exporter = StudentStudyLevelExporter()
        exporter.export_filtered(
            self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,'
            'student_id,number_of_tickets,certcode,previous\r\n'
            '0.00,100,2012,A,100,,,,A111111,1,CERT1,0\r\n'
            )
        return

    def test_export_selected(self):
        # we can export studylevels of a filtered set of students
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))

        exporter = StudentStudyLevelExporter()
        exporter.export_selected(
            self.app, self.outfile, selected=['A111111'])
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'gpa,level,level_session,level_verdict,total_credits,'
            'transcript_remark,validated_by,validation_date,'
            'student_id,number_of_tickets,certcode,previous\r\n'
            '0.00,100,2012,A,100,,,,A111111,1,CERT1,0\r\n'
            )
        return

class CourseTicketExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(CourseTicketExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = CourseTicketExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, CourseTicketExporter)
        return

    def test_get_as_utility(self):
        # we can get an student exporter as utility
        result = queryUtility(ICSVExporter, name="coursetickets")
        self.assertTrue(result is not None)
        return

    def test_export_empty(self):
        # we can export a nearly empty course ticket
        ticket = CourseTicket()
        exporter = CourseTicketExporter()
        exporter.export([ticket], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '0,0,,,,,,,,0,0,,,,,,,,,0\r\n'
            )
        return

    def test_export(self):
        # we can really export course tickets.
        # set values we can expect in export file
        self.setup_student(self.student)
        study_course = self.student.get('studycourse')
        study_level = study_course[study_course.keys()[0]]
        ticket = study_level['CRS1']
        exporter = CourseTicketExporter()
        exporter.export([ticket], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        return

    def test_export_all(self):
        # we can really export all course tickets
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = CourseTicketExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        return

    def test_export_student(self):
        # we can really export all course tickets of a certain student
        self.setup_student(self.student)
        exporter = CourseTicketExporter()
        exporter.export_student(self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        return

    def test_export_filtered(self):
        # we can export course tickets of a filtered set of students
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))

        exporter = CourseTicketExporter()
        exporter.export_filtered(self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        # We can set the course tickets level, semester and level_session 
        # without code (used in the datacenter)
        notify(grok.ObjectModifiedEvent(self.student['studycourse']['100']['CRS1']))
        exporter.export_filtered(self.student, self.outfile, ct_level='100',
            ct_session='2012', ct_semester='2')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        # 'all' does select all
        notify(grok.ObjectModifiedEvent(self.student['studycourse']['100']['CRS1']))
        exporter.export_filtered(self.student, self.outfile, ct_level='all',
            ct_session='2012', ct_semester='all')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        # Level 200 tickets do not exist.
        notify(grok.ObjectModifiedEvent(self.student['studycourse']['100']['CRS1']))
        exporter.export_filtered(self.student, self.outfile, ct_level='200')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
                        )
        # Session 2013 tickets do not exist.
        notify(grok.ObjectModifiedEvent(self.student['studycourse']['100']['CRS1']))
        exporter.export_filtered(self.student, self.outfile,
            ct_level='all', ct_session='2013')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            )
        # 1st semester tickets do not exist.
        notify(grok.ObjectModifiedEvent(self.student['studycourse']['100']['CRS1']))
        exporter.export_filtered(self.student, self.outfile,
            ct_level='all', ct_session='all', ct_semester='1')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            )
        # If the coursetickets catalog is used to filter students
        # and (course) code is not None
        # only course tickets which belong to this course are exported
        exporter.export_filtered(
            self.student, self.outfile, catalog='coursetickets', code='CRS1')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,100,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        exporter.export_filtered(
            self.student, self.outfile, catalog='coursetickets', code='any code')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            )
        # Also tickets in probating levels are exported. Therefore
        # we change the level attribute to fake a 110 level.
        self.student['studycourse']['100'].level = 110
        notify(grok.ObjectModifiedEvent(self.student['studycourse']['100']['CRS1']))
        exporter.export_filtered(
            self.student, self.outfile, catalog='coursetickets', code='CRS1', level='100')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'automatic,carry_over,code,course_category,credits,dcode,fcode,level,level_session,'
            'mandatory,outstanding,passmark,score,semester,ticket_session,title,student_id,certcode,'
            'display_fullname,previous\r\n'
            '1,1,CRS1,,100,DEP1,FAC1,110,2012,0,0,100,,2,,Course 1,A111111,CERT1,'
            'Anna M. Tester,0\r\n'
            )
        return

class OutstandingCoursesExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(OutstandingCoursesExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = OutstandingCoursesExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, OutstandingCoursesExporter)
        return

    def test_get_as_utility(self):
        # we can get an student exporter as utility
        result = queryUtility(ICSVExporter, name="outstandingcourses")
        self.assertTrue(result is not None)
        return

    def test_export_all(self):
        course1 = Course(u'Cheese Basics', 'C1')
        course2 = Course(u'Advanced Cheese Making', 'C2')
        course3 = Course(u'Selling Cheese', 'C3')
        self.app['faculties']['fac1']['dep1'].courses.addCourse(course1)
        self.app['faculties']['fac1']['dep1'].courses.addCourse(course2)
        self.app['faculties']['fac1']['dep1'].courses.addCourse(course3)
        self.certificate.addCertCourse(course1, 100, True)
        self.certificate.addCertCourse(course2, 400, False)
        self.certificate.addCertCourse(course3, 100, False)
        self.setup_student(self.student)
        self.student['studycourse']['100']['C3'].score = 25
        exporter = OutstandingCoursesExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        # The only student has registered C1, C3 and CRS1
        # She missed C2, has failed C3 and  did not
        # take C1 and CRS1
        self.assertEqual(
            result,
            'student_id,matric_number,certcode,display_fullname,missed,failed,nottaken\r\n'
            'A111111,234,CERT1,Anna M. Tester,C2_400,C3,C1 CRS1\r\n'
            )
        return

class StudentPaymentExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentPaymentExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = StudentPaymentExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, StudentPaymentExporter)
        return

    def test_get_as_utility(self):
        # we can get a payments exporter as utility
        result = queryUtility(ICSVExporter, name="studentpayments")
        self.assertTrue(result is not None)
        return

    def test_export_empty(self):
        # we can export a nearly empty payment
        payment = StudentOnlinePayment()
        payment.creation_date = datetime.datetime(2012, 4, 1, 13, 12, 1)
        exporter = StudentPaymentExporter()
        exporter.export([payment], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'

            ',0.0,2012-04-01 13:12:01#,,[],1,,,,,unpaid,,0.0,,,,,\r\n'
            )
        return

    def test_export(self):
        # we can really export student payments.
        # set values we can expect in export file
        self.setup_student(self.student)
        payment = self.student['payments']['my-payment']
        exporter = StudentPaymentExporter()
        exporter.export([payment], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'

            '666,12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,'
            'p-item,100,%s,paid,%s-04-01 14:12:01#,12.12,'
            'r-code,,A111111,created,2012\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        return

    def test_export_all(self):
        # we can really export all payments
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = StudentPaymentExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'

            '666,12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,'
            'p-item,100,%s,paid,%s-04-01 14:12:01#,12.12,'
            'r-code,,A111111,created,2012\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        return

    def test_export_student(self):
        # we can really export all payments of a certain student
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = StudentPaymentExporter()
        exporter.export_student(self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'

            '666,12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,'
            'p-item,100,%s,paid,%s-04-01 14:12:01#,12.12,'
            'r-code,,A111111,created,2012\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        return

    def test_export_filtered(self):
        # we can export payments of a filtered set of students
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))

        exporter = StudentPaymentExporter()
        exporter.export_filtered(
            self.student, self.outfile, current_level=200)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'

            '666,12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,'
            'p-item,100,%s,paid,%s-04-01 14:12:01#,12.12,'
            'r-code,,A111111,created,2012\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        return

    def test_export_filtered_by_date(self):
        # payments_start and payments_end are being ignored
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))
        exporter = StudentPaymentExporter()
        # A key xxx does not exist
        self.assertRaises(
            KeyError, exporter.export_filtered, self.app, self.outfile,
            current_session=None,
            current_level=None, xxx='nonsense')
        # payments_start and payments_end do exist but must match format '%Y-%m-%d'
        self.assertRaises(
            ValueError, exporter.export_filtered, self.app, self.outfile,
            current_session=None, current_level=None,
            payments_start='nonsense', payments_end='nonsense')
        # If they match the format they are ignored by get_filtered and the
        # exporter works properly.
        # Attention: End day is included!
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=None,
            payments_start='01/04/%s' % (curr_year-6),
            payments_end='01/04/%s' % (curr_year-6))
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'

            '666,12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,'
            'p-item,100,%s,paid,%s-04-01 14:12:01#,12.12,'
            'r-code,,A111111,created,2012\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        # Payment date is 2012-04-01, 14:12:01.
        # No results if payment_date is outside the given period.
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=None,
            payments_start='30/03/2012', payments_end='31/03/2012')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'
            )
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=None,
            payments_start='02/04/2012', payments_end='03/04/2012')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'
            )
        # No results if payment_date is not set
        self.payment.payment_date = None
        exporter.export_filtered(
            self.app, self.outfile,
            current_session=None, current_level=None,
            payments_start='31/03/2012', payments_end='02/04/2012')
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'
            )
        return

class StudentTrimmedPaymentExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentTrimmedPaymentExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = StudentTrimmedPaymentExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, StudentTrimmedPaymentExporter)
        return

    def test_get_as_utility(self):
        # we can get a payments exporter as utility
        result = queryUtility(ICSVExporter, name="trimmedpayments")
        self.assertTrue(result is not None)
        return

    def test_export_all(self):
        # we can really export all payments
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = StudentTrimmedPaymentExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'amount_auth,creation_date,p_category,p_combi,p_current,'
            'p_id,p_item,p_level,p_session,p_state,payment_date,'
            'r_amount_approved,r_code,r_desc,student_id,faccode,'
            'depcode,state,current_session\r\n'

            '12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,p-item,'
            '100,%s,paid,%s-04-01 14:12:01#,12.12,r-code,,'
            'A111111,NA,NA,created,2012\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        return


class UnpaidPaymentsExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(UnpaidPaymentsExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_export_all(self):
        # we can really export all payments
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = UnpaidPaymentsExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        # No unpaid ticket exists
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'
            )
        # Make ticket unpaid
        self.payment.p_state = 'unpaid'
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,'
            'p_item,p_level,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,student_id,state,current_session\r\n'

            '666,12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,'
            'p-item,100,%s,unpaid,%s-04-01 14:12:01#,12.12,'
            'r-code,,A111111,created,2012\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        return

class BursaryDataExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(BursaryDataExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_export_all(self):
        # we can really export all payments
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = DataForBursaryExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,p_item,'
            'p_level,p_session,p_state,payment_date,r_amount_approved,r_code,'
            'r_desc,student_id,matric_number,reg_number,firstname,middlename,lastname,'
            'sex,state,current_session,entry_session,entry_mode,faccode,depcode,certcode\r\n'

            '666,12.12,%s-04-01 13:12:01#,schoolfee,[],1,my-id,p-item,100,%s,'
            'paid,%s-04-01 14:12:01#,12.12,r-code,,A111111,234,123,'
            'Anna,M.,Tester,f,created,2012,2010,ug_ft,NA,NA,CERT1\r\n'
            % (curr_year-6, curr_year-6, curr_year-6)
            )
        return

class AccommodationPaymentsExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(AccommodationPaymentsExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_export_all(self):
        self.setup_student(self.student)
        # add accommodation payments
        payment = StudentOnlinePayment()
        payment.creation_date = datetime.datetime(curr_year-6, 4, 1, 13, 12, 1)
        payment.p_id = 'id1'
        payment.p_category = u'bed_allocation'
        payment.p_state = 'paid'
        payment.ac = u'abc'
        payment.p_item = u'xyz'
        payment.p_level = 100
        payment.p_session = curr_year - 6
        payment.payment_date = datetime.datetime(curr_year-6, 4, 1, 14, 12, 1)
        payment.amount_auth = 12.12
        payment.r_amount_approved = 12.12
        payment.r_code = u'cde'
        payment2 = StudentOnlinePayment()
        payment2.creation_date = datetime.datetime(curr_year-6, 4, 1, 13, 12, 1)
        payment2.p_id = 'id2'
        payment2.p_category = u'hostel_maintenance'
        payment2.p_state = 'paid'
        payment2.ac = u'abc'
        payment2.p_item = u'xyz'
        payment2.p_level = 100
        payment2.p_session = curr_year - 6
        payment2.payment_date = datetime.datetime(curr_year-6, 4, 1, 14, 12, 1)
        payment2.amount_auth = 12.12
        payment2.r_amount_approved = 12.12
        payment2.r_code = u'cde'
        # XXX: there is no addPayment method to give predictable names
        self.payment = self.student['payments']['id1'] = payment
        self.payment = self.student['payments']['id2'] = payment2
        exporter = AccommodationPaymentsExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        # only accommodation payments are exported
        self.assertEqual(
            result,
            'ac,amount_auth,creation_date,p_category,p_combi,p_current,p_id,p_item,'
            'p_level,p_session,p_state,payment_date,r_amount_approved,r_code,'
            'r_desc,student_id,matric_number,reg_number,firstname,middlename,lastname,sex,'
            'state,current_session,entry_session,entry_mode,faccode,depcode,certcode\r\n'
            'abc,12.12,%s-04-01 13:12:01#,bed_allocation,[],1,id1,xyz,100,%s,'
            'paid,%s-04-01 14:12:01#,12.12,cde,,A111111,234,123,'
            'Anna,M.,Tester,f,created,2012,2010,ug_ft,NA,NA,CERT1\r\n'
            'abc,12.12,%s-04-01 13:12:01#,hostel_maintenance,[],1,id2,xyz,100,%s,'
            'paid,%s-04-01 14:12:01#,12.12,cde,,A111111,234,123,'
            'Anna,M.,Tester,f,created,2012,2010,ug_ft,NA,NA,CERT1\r\n'
            % (curr_year-6, curr_year-6, curr_year-6,
               curr_year-6, curr_year-6, curr_year-6)
            )
        return

class BedTicketExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(BedTicketExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = BedTicketExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, BedTicketExporter)
        return

    def test_get_as_utility(self):
        # we can get a bedtickets exporter as utility
        result = queryUtility(ICSVExporter, name="bedtickets")
        self.assertTrue(result is not None)
        return

    def test_export_empty(self):
        # we can export a nearly empty bedticket
        bedticket = BedTicket()
        bed = self.app['hostels']['hall-1']['hall-1_A_101_A']
        bedticket.bed = bed
        exporter = BedTicketExporter()
        exporter.export([bedticket], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            result,
            'bed,bed_coordinates,bed_type,booking_code,booking_date,'
            'booking_session,student_id,actual_bed_type\r\n'
            'hall-1_A_101_A,,,,<YYYY-MM-DD hh:mm:ss>.<6-DIGITS>#,,,regular_male_fr\r\n'
            )
        return

    def test_export(self):
        # we can really export student bedtickets.
        # set values we can expect in export file
        self.setup_student(self.student)
        bedticket = self.student['accommodation']['2004']
        exporter = BedTicketExporter()
        exporter.export([bedticket], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            result,
            'bed,bed_coordinates,bed_type,booking_code,booking_date,'
            'booking_session,student_id,actual_bed_type\r\n'
            'hall-1_A_101_A,,any bed type,,<YYYY-MM-DD hh:mm:ss>.<6-DIGITS>#,2004,'
            'A111111,regular_male_fr\r\n'
            )
        return

    def test_export_all(self):
        # we can really export all bedtickets
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = BedTicketExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            result,
            'bed,bed_coordinates,bed_type,booking_code,booking_date,'
            'booking_session,student_id,actual_bed_type\r\n'
            'hall-1_A_101_A,,any bed type,,<YYYY-MM-DD hh:mm:ss>.<6-DIGITS>#,2004,'
            'A111111,regular_male_fr\r\n'
            )
        return

    def test_export_student(self):
        # we can really export all bedtickets of a certain student
        # set values we can expect in export file
        self.setup_student(self.student)
        exporter = BedTicketExporter()
        exporter.export_student(self.student, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            result,
            'bed,bed_coordinates,bed_type,booking_code,booking_date,'
            'booking_session,student_id,actual_bed_type\r\n'
            'hall-1_A_101_A,,any bed type,,<YYYY-MM-DD hh:mm:ss>.<6-DIGITS>#,2004,'
            'A111111,regular_male_fr\r\n'
            )
        return

    def test_export_filtered(self):
        # we can export payments of a filtered set of students
        self.setup_student(self.student)
        self.app['students'].addStudent(self.student)
        notify(grok.ObjectModifiedEvent(self.student))

        exporter = BedTicketExporter()
        exporter.export_filtered(
            self.student, self.outfile, current_level=200)
        result = open(self.outfile, 'rb').read()
        self.assertMatches(
            result,
            'bed,bed_coordinates,bed_type,booking_code,booking_date,'
            'booking_session,student_id,actual_bed_type\r\n'
            'hall-1_A_101_A,,any bed type,,<YYYY-MM-DD hh:mm:ss>.<6-DIGITS>#,'
            '2004,A111111,regular_male_fr\r\n')
        return


class SchoolFeePaymentsOverviewExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(SchoolFeePaymentsOverviewExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = SchoolFeePaymentsOverviewExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, SchoolFeePaymentsOverviewExporter)
        return

    def test_get_as_utility(self):
        # we can get a payments exporter as utility
        result = queryUtility(ICSVExporter, name="sfpaymentsoverview")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        self.setup_student(self.student)
        exporter = SchoolFeePaymentsOverviewExporter()
        exporter.export([self.student], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'student_id,matric_number,display_fullname,state,certcode,'
            'faccode,depcode,is_postgrad,'
            'current_level,current_session,current_mode,entry_session,'
            'reg_number,%s\r\n'
            'A111111,234,Anna M. Tester,created,CERT1,NA,NA,0,'
            '200,2012,ug_ft,2010,'
            % year_range_str in result
            )
        return

    def test_export_all(self):
        # we can really export students
        # set values we can expect in export file
        self.setup_student(self.student)
        # We add successful payments. 
        payment_2 = StudentOnlinePayment()
        payment_2.p_id = 'my-id'
        payment_2.p_session = curr_year - 5
        payment_2.amount_auth = 13.13
        payment_2.p_state = 'paid'
        payment_2.p_category = u'schoolfee'
        self.student['payments']['my-2ndpayment'] = payment_2
        # This one could be a balance payment.
        # The amount is being added.
        payment_3 = StudentOnlinePayment()
        payment_3.p_id = 'my-id_2'
        payment_3.p_session = curr_year - 5
        payment_3.amount_auth = 1.01
        payment_3.p_state = 'paid'
        payment_3.p_category = u'schoolfee'
        self.student['payments']['my-3rdpayment'] = payment_3
        # One session school fee has been waived
        payment_4 = StudentOnlinePayment()
        payment_4.p_id = 'my-id_2'
        payment_4.p_session = curr_year - 4
        payment_4.amount_auth = 1.01
        payment_4.p_state = 'waived'
        payment_4.p_category = u'schoolfee'
        self.student['payments']['my-4thpayment'] = payment_4
        exporter = SchoolFeePaymentsOverviewExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'student_id,matric_number,display_fullname,state,'
            'certcode,faccode,depcode,is_postgrad,'
            'current_level,current_session,current_mode,entry_session,'
            'reg_number,%s\r\nA111111,234,Anna M. Tester,created,CERT1,NA,NA,0,'
            '200,2012,ug_ft,2010,123,,,,,,12.12,14.14,waived,,,,\r\n'
            % year_range_str in result
            )
        return

class SessionPaymentsOverviewExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(SessionPaymentsOverviewExporterTest, self).setUp()
        self.setup_for_export()
        paycats = ('schoolfee', 'clearance', 'gown', 'transcript')
        paycatyears = ''
        grok.getSite()['configuration'].current_academic_session = curr_year - 4
        year_range = range(curr_year-6, curr_year-3)
        year_range_tuple = tuple([str(year)[2:] for year in year_range])
        for cat in paycats:
            for year in year_range_tuple:
                paycatyears += '%s,'%(cat+str(year))
        self.paycatyears = paycatyears.strip(',')
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = SessionPaymentsOverviewExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, SessionPaymentsOverviewExporter)
        return

    def test_get_as_utility(self):
        # we can get a payments exporter as utility
        result = queryUtility(ICSVExporter, name="sessionpaymentsoverview")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        self.setup_student(self.student)
        exporter = SessionPaymentsOverviewExporter()
        exporter.export([self.student], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'student_id,matric_number,display_fullname,state,certcode,'
            'faccode,depcode,is_postgrad,current_level,current_session,'
            'current_mode,entry_session,reg_number,%s\r\n'
            'A111111,234,Anna M. Tester,created,CERT1,NA,NA,0,200,'
            '2012,ug_ft,2010,123,'
            '12.12,,,,,,,,,,,\r\n' %self.paycatyears in result
            )
        return

    def test_export_all(self):
        self.setup_student(self.student)
        # We add successful payments.
        payment_2 = StudentOnlinePayment()
        payment_2.p_id = 'my-id'
        payment_2.p_session = curr_year - 5
        payment_2.amount_auth = 13.13
        payment_2.p_state = 'paid'
        payment_2.p_category = u'schoolfee'
        self.student['payments']['my-2ndpayment'] = payment_2
        # This one could be a balance payment.
        # The amount is being added.
        payment_3 = StudentOnlinePayment()
        payment_3.p_id = 'my-id_2'
        payment_3.p_session = curr_year - 5
        payment_3.amount_auth = 1.01
        payment_3.p_state = 'paid'
        payment_3.p_category = u'schoolfee'
        self.student['payments']['my-3rdpayment'] = payment_3
        # One session school fee has been waived
        payment_4 = StudentOnlinePayment()
        payment_4.p_id = 'my-id_2'
        payment_4.p_session = curr_year - 4
        payment_4.amount_auth = 1.01
        payment_4.p_state = 'waived'
        payment_4.p_category = u'schoolfee'
        self.student['payments']['my-4thpayment'] = payment_4
        exporter = SessionPaymentsOverviewExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'student_id,matric_number,display_fullname,state,certcode,faccode,'
            'depcode,is_postgrad,current_level,current_session,'
            'current_mode,entry_session,reg_number,%s\r\n'
            'A111111,234,Anna M. Tester,created,CERT1,NA,NA,0,200,2012,ug_ft,'
            '2010,123,'
            '12.12,14.14,1.01,,,,,,,,,\r\n'
            %self.paycatyears in result
            )
        return

class StudyLevelsOverviewExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudyLevelsOverviewExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_ifaces(self):
        obj = StudyLevelsOverviewExporter()
        verifyObject(ICSVStudentExporter, obj)
        verifyClass(ICSVStudentExporter, StudyLevelsOverviewExporter)
        return

    def test_get_as_utility(self):
        result = queryUtility(ICSVExporter, name="studylevelsoverview")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        self.setup_student(self.student)
        exporter = StudyLevelsOverviewExporter()
        exporter.export([self.student], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
             'student_id,state,certcode,faccode,depcode,is_postgrad,'
             'entry_session,current_level,current_session,'
             '0,10,100,110,120,200,210,220,300,310,320,400,410,420,500,'
             '510,520,600,610,620,700,710,720,800,810,820,900,910,920,999,1000\r\n'
             'A111111,created,CERT1,NA,NA,0,2010,200,2012,,,2012'
             ',,,,,,,,,,,,,,,,,,,,,,,,,,,,\r\n',
            result
            )
        return

    def test_export_all(self):
        self.setup_student(self.student)
        exporter = StudyLevelsOverviewExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            'student_id,state,certcode,faccode,depcode,is_postgrad,'
            'entry_session,current_level,current_session,'
            '0,10,100,110,120,200,210,220,300,310,320,400,410,420,500,'
            '510,520,600,610,620,700,710,720,800,810,820,900,910,920,999,1000\r\n'
            'A111111,created,CERT1,NA,NA,0,2010,200,2012,,,2012'
            ',,,,,,,,,,,,,,,,,,,,,,,,,,,,\r\n',
            result
            )
        return

class ComboCardExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(ComboCardExporterTest, self).setUp()
        self.setup_for_export()
        return

    def create_passport_img(self, student):
        # create some passport file for `student`
        storage = getUtility(IExtFileStore)
        image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        self.image_contents = open(image_path, 'rb').read()
        file_id = IFileStoreNameChooser(student).chooseName(
            attr='passport.jpg')
        storage.createFile(file_id, StringIO(self.image_contents))

    def test_export_all(self):
        self.setup_student(self.student)
        self.create_passport_img(self.student)
        exporter = ComboCardDataExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'display_fullname,student_id,matric_number,certificate,faculty,'
            'department,passport_path\r\nAnna M. Tester,A111111,234,'
            'Unnamed Certificate,Faculty of Unnamed Faculty (NA),'
            'Department of Unnamed Department (NA),'
            'students/00110/A111111/passport_A111111.jpg\r\n'
            in result
            )
        return

class TranscriptDataExporterTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(TranscriptDataExporterTest, self).setUp()
        self.setup_for_export()
        return

    def test_export_all(self):
        self.setup_student(self.student)
        study_course = self.student.get('studycourse')
        study_level = study_course[study_course.keys()[0]]
        ticket = study_level['CRS1']
        ticket.score = 20
        exporter = TranscriptDataExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'student_id,state,certcode,faccode,depcode,entry_session,'
            'current_level,current_session,transcript_data\r\n'
            'A111111,created,CERT1,NA,NA,2010,200,2012,'
            'Level 100; 1st: ; 2nd: CRS1; 3rd: ; sgpa: 0.0\r\n'
            in result
            )
        return
