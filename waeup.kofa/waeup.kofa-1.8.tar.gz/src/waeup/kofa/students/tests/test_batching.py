# -*- coding: utf-8 -*-
## $Id: test_batching.py 16834 2022-02-24 12:48:18Z henrik $
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
"""Unit tests for students-related data processors.
"""
import os
import shutil
import tempfile
import unittest
import datetime
import grok
from time import time
from zope.event import notify
from zope.component import createObject, queryUtility
from zope.component.hooks import setSite, clearSite
from zope.catalog.interfaces import ICatalog
from zope.interface.verify import verifyClass, verifyObject
from hurry.workflow.interfaces import IWorkflowState

from waeup.kofa.app import University
from waeup.kofa.interfaces import (
    IBatchProcessor, FatalCSVError, IUserAccount, DuplicationError)
from waeup.kofa.students.batching import (
    StudentProcessor, StudentStudyCourseProcessor,
    StudentStudyLevelProcessor, CourseTicketProcessor,
    StudentOnlinePaymentProcessor, StudentVerdictProcessor,
    )
from waeup.kofa.students.payments import StudentOnlinePayment
from waeup.kofa.students.student import Student
from waeup.kofa.students.studylevel import StudentStudyLevel, CourseTicket
from waeup.kofa.students.accommodation import BedTicket
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.university.faculty import Faculty
from waeup.kofa.university.department import Department
from waeup.kofa.hostels.hostel import Hostel, Bed, NOT_OCCUPIED


STUDENT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_student_data.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS = STUDENT_SAMPLE_DATA.split(
    '\n')[0].split(',')

STUDENT_SAMPLE_DATA_UPDATE = open(
    os.path.join(os.path.dirname(__file__), 'sample_student_data_update.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS_UPDATE = STUDENT_SAMPLE_DATA_UPDATE.split(
    '\n')[0].split(',')

STUDENT_SAMPLE_DATA_UPDATE2 = open(
    os.path.join(os.path.dirname(__file__), 'sample_student_data_update2.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS_UPDATE2 = STUDENT_SAMPLE_DATA_UPDATE2.split(
    '\n')[0].split(',')

STUDENT_SAMPLE_DATA_UPDATE3 = open(
    os.path.join(os.path.dirname(__file__), 'sample_student_data_update3.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS_UPDATE3 = STUDENT_SAMPLE_DATA_UPDATE3.split(
    '\n')[0].split(',')

STUDENT_SAMPLE_DATA_UPDATE4 = open(
    os.path.join(os.path.dirname(__file__), 'sample_student_data_update4.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS_UPDATE4 = STUDENT_SAMPLE_DATA_UPDATE4.split(
    '\n')[0].split(',')

STUDYCOURSE_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_studycourse_data.csv'),
    'rb').read()

STUDYCOURSE_HEADER_FIELDS = STUDYCOURSE_SAMPLE_DATA.split(
    '\n')[0].split(',')

FIRST_STUDYCOURSE_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_first_studycourse_data.csv'),
    'rb').read()

FIRST_STUDYCOURSE_HEADER_FIELDS = FIRST_STUDYCOURSE_SAMPLE_DATA.split(
    '\n')[0].split(',')

TRANSFER_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_transfer_data.csv'),
    'rb').read()

TRANSFER_HEADER_FIELDS = TRANSFER_SAMPLE_DATA.split(
    '\n')[0].split(',')

VERDICT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_verdict_data.csv'),
    'rb').read()

VERDICT_HEADER_FIELDS = VERDICT_SAMPLE_DATA.split(
    '\n')[0].split(',')

STUDENT_SAMPLE_DATA_MIGRATION = open(
    os.path.join(os.path.dirname(__file__),
                 'sample_student_data_migration.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS_MIGRATION = STUDENT_SAMPLE_DATA_MIGRATION.split(
    '\n')[0].split(',')

STUDENT_SAMPLE_DATA_DUPLICATES = open(
    os.path.join(os.path.dirname(__file__),
                 'sample_student_data_duplicates.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS_DUPLICATES = STUDENT_SAMPLE_DATA_DUPLICATES.split(
    '\n')[0].split(',')

STUDENT_SAMPLE_DATA_EXTASCII = open(
    os.path.join(os.path.dirname(__file__),
                 'sample_student_data_extascii.csv'),
    'rb').read()

STUDENT_HEADER_FIELDS_EXTASCII = STUDENT_SAMPLE_DATA_EXTASCII.split(
    '\n')[0].split(',')

STUDYLEVEL_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_studylevel_data.csv'),
    'rb').read()

STUDYLEVEL_HEADER_FIELDS = STUDYLEVEL_SAMPLE_DATA.split(
    '\n')[0].split(',')

FIRST_STUDYLEVEL_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_first_studylevel_data.csv'),
    'rb').read()

FIRST_STUDYLEVEL_HEADER_FIELDS = FIRST_STUDYLEVEL_SAMPLE_DATA.split(
    '\n')[0].split(',')

COURSETICKET_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_courseticket_data.csv'),
    'rb').read()

COURSETICKET_HEADER_FIELDS = COURSETICKET_SAMPLE_DATA.split(
    '\n')[0].split(',')

FIRST_COURSETICKET_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_first_courseticket_data.csv'),
    'rb').read()

FIRST_COURSETICKET_HEADER_FIELDS = FIRST_COURSETICKET_SAMPLE_DATA.split(
    '\n')[0].split(',')

PAYMENT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_payment_data.csv'),
    'rb').read()

PAYMENT_HEADER_FIELDS = PAYMENT_SAMPLE_DATA.split(
    '\n')[0].split(',')

PAYMENT_CREATE_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_create_payment_data.csv'),
    'rb').read()

PAYMENT_CREATE_HEADER_FIELDS = PAYMENT_CREATE_SAMPLE_DATA.split(
    '\n')[0].split(',')

curr_year = datetime.datetime.now().year

class StudentImportExportSetup(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentImportExportSetup, self).setUp()
        self.dc_root = tempfile.mkdtemp()
        self.workdir = tempfile.mkdtemp()
        app = University()
        app['datacenter'].setStoragePath(self.dc_root)
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(app)

        # Populate university
        self.certificate = createObject('waeup.Certificate')
        self.certificate.code = 'CERT1'
        self.certificate.application_category = 'basic'
        self.certificate.start_level = 200
        self.certificate.end_level = 500
        self.certificate.study_mode = u'ug_ft'
        self.app['faculties']['fac1'] = Faculty()
        self.app['faculties']['fac1']['dep1'] = Department()
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate)

        # Create a hostel with two beds
        hostel = Hostel()
        hostel.hostel_id = u'hall-1'
        hostel.hostel_name = u'Hall 1'
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

        self.logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        return

    def tearDown(self):
        super(StudentImportExportSetup, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def setup_for_export(self):
        student = Student()
        student.student_id = u'A111111'
        self.app['students'][student.student_id] = self.student = student
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        return

    def setup_student(self, student):
        # set predictable values for `student`
        student.matric_number = u'234'
        student.adm_code = u'my adm code'
        student.clr_code = u'my clr code'
        student.perm_address = u'Studentroad 21\nLagos 123456\n'
        student.reg_number = u'123'
        student.firstname = u'Anna'
        student.lastname = u'Tester'
        student.middlename = u'M.'
        student.date_of_birth = datetime.date(1981, 2, 4)
        student.sex = 'f'
        student.email = 'anna@sample.com'
        student.phone = u'+234-123-12345'
        student.notice = u'Some notice\nin lines.'
        student.nationality = u'NG'

        student['studycourse'].certificate = self.certificate
        student['studycourse'].entry_mode = 'ug_ft'
        student['studycourse'].entry_session = 2010
        student['studycourse'].current_session = 2012
        student['studycourse'].current_level = int(self.certificate.start_level)

        study_level = StudentStudyLevel()
        study_level.level_session = 2012
        study_level.level_verdict = "A"
        study_level.level = 100
        student['studycourse'].addStudentStudyLevel(
            self.certificate, study_level)

        ticket = CourseTicket()
        ticket.automatic = True
        ticket.carry_over = True
        ticket.code = u'CRS1'
        ticket.title = u'Course 1'
        ticket.fcode = u'FAC1'
        ticket.dcode = u'DEP1'
        ticket.credits = 100
        ticket.passmark = 100
        ticket.semester = 2
        study_level[ticket.code] = ticket

        bedticket = BedTicket()
        bedticket.booking_session = 2004
        bedticket.bed_type = u'any bed type'
        bedticket.bed = self.app['hostels']['hall-1']['hall-1_A_101_A']
        student['accommodation'].addBedTicket(bedticket)

        self.add_payment(student)
        return student

    def add_payment(self, student):
        # get a payment with all fields set
        payment = StudentOnlinePayment()
        payment.creation_date = datetime.datetime(curr_year-6, 4, 1, 13, 12, 1)
        payment.p_id = 'my-id'
        payment.p_category = u'schoolfee'
        payment.p_state = 'paid'
        payment.ac = u'666'
        payment.p_item = u'p-item'
        payment.p_level = 100
        payment.p_session = curr_year - 6
        payment.payment_date = datetime.datetime(curr_year-6, 4, 1, 14, 12, 1)
        payment.amount_auth = 12.12
        payment.r_amount_approved = 12.12
        payment.r_code = u'r-code'
        # XXX: there is no addPayment method to give predictable names
        self.payment = student['payments']['my-payment'] = payment
        return payment


class StudentProcessorTest(StudentImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentProcessorTest, self).setUp()

        # Add student with subobjects
        student = Student()
        self.app['students'].addStudent(student)
        student = self.setup_student(student)
        notify(grok.ObjectModifiedEvent(student))
        self.student = self.app['students'][student.student_id]

        self.processor = StudentProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_student_data.csv')
        self.csv_file_update = os.path.join(
            self.workdir, 'sample_student_data_update.csv')
        self.csv_file_update2 = os.path.join(
            self.workdir, 'sample_student_data_update2.csv')
        self.csv_file_update3 = os.path.join(
            self.workdir, 'sample_student_data_update3.csv')
        self.csv_file_update4 = os.path.join(
            self.workdir, 'sample_student_data_update4.csv')
        self.csv_file_migration = os.path.join(
            self.workdir, 'sample_student_data_migration.csv')
        self.csv_file_duplicates = os.path.join(
            self.workdir, 'sample_student_data_duplicates.csv')
        self.csv_file_extascii = os.path.join(
            self.workdir, 'sample_student_data_extascii.csv')
        open(self.csv_file, 'wb').write(STUDENT_SAMPLE_DATA)
        open(self.csv_file_update, 'wb').write(STUDENT_SAMPLE_DATA_UPDATE)
        open(self.csv_file_update2, 'wb').write(STUDENT_SAMPLE_DATA_UPDATE2)
        open(self.csv_file_update3, 'wb').write(STUDENT_SAMPLE_DATA_UPDATE3)
        open(self.csv_file_update4, 'wb').write(STUDENT_SAMPLE_DATA_UPDATE4)
        open(self.csv_file_migration, 'wb').write(STUDENT_SAMPLE_DATA_MIGRATION)
        open(self.csv_file_duplicates, 'wb').write(STUDENT_SAMPLE_DATA_DUPLICATES)
        open(self.csv_file_extascii, 'wb').write(STUDENT_SAMPLE_DATA_EXTASCII)

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, StudentProcessor) is True

    def test_parentsExist(self):
        self.assertFalse(self.processor.parentsExist(None, dict()))
        self.assertTrue(self.processor.parentsExist(None, self.app))

    def test_entryExists(self):
        assert self.processor.entryExists(
            dict(student_id='ID_NONE'), self.app) is False
        assert self.processor.entryExists(
            dict(reg_number='123'), self.app) is True

    def test_getParent(self):
        parent = self.processor.getParent(None, self.app)
        assert parent is self.app['students']

    def test_getEntry(self):
        assert self.processor.getEntry(
            dict(student_id='ID_NONE'), self.app) is None
        assert self.processor.getEntry(
            dict(student_id=self.student.student_id), self.app) is self.student

    def test_addEntry(self):
        new_student = Student()
        self.processor.addEntry(
            new_student, dict(), self.app)
        assert len(self.app['students'].keys()) == 2

    def test_checkConversion(self):
        # Make sure we can check conversions and that the stud_id
        # counter is not raised during such checks.
        initial_stud_id = self.app['students']._curr_stud_id
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', state='admitted'))
        self.assertEqual(len(errs),0)
        # Empty state is allowed
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', state=''))
        self.assertEqual(len(errs),0)
        #self.assertTrue(('state', 'no value provided') in errs)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', state='nonsense'))
        self.assertEqual(len(errs),1)
        self.assertTrue(('state', 'not allowed') in errs)
        new_stud_id = self.app['students']._curr_stud_id
        self.assertEqual(initial_stud_id, new_stud_id)
        return

    def test_checkUpdateRequirements(self):
        # Make sure that pg students can't be updated with wrong transition.
        err = self.processor.checkUpdateRequirements(self.student,
            dict(reg_number='1', state='returning'), self.app)
        self.assertTrue(err is None)
        self.certificate.study_mode = 'pg_ft'
        err = self.processor.checkUpdateRequirements(self.student,
            dict(reg_number='1', state='returning'), self.app)
        self.assertEqual(err, 'State not allowed (pg student).')
        IWorkflowState(self.student).setState('school fee paid')
        err = self.processor.checkUpdateRequirements(self.student,
            dict(reg_number='1', transition='reset6'), self.app)
        self.assertEqual(err, 'Transition not allowed (pg student).')
        err = self.processor.checkUpdateRequirements(self.student,
            dict(reg_number='1', transition='register_courses'), self.app)
        self.assertEqual(err, 'Transition not allowed (pg student).')


    def test_delEntry(self):
        assert self.student.student_id in self.app['students'].keys()
        self.processor.delEntry(
            dict(reg_number=self.student.reg_number), self.app)
        assert self.student.student_id not in self.app['students'].keys()

    def test_import(self):
        self.assertEqual(self.app['students']._curr_stud_id, 1000001)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDENT_HEADER_FIELDS)
        self.assertEqual(num_warns, 0)
        # Nine students have been added.
        self.assertEqual(len(self.app['students']), 10)
        # Three empty rows have been skipped.
        self.assertEqual(num, 12)
        self.assertEqual(self.app['students']['X666666'].reg_number,'1')
        self.assertEqual(
            self.app['students']['X666666'].state, 'courses validated')
        # history was successfully impotrted
        history = self.app['students']['X666666'].history.messages
        self.assertEqual(history[0],
            '2012-10-23 00:05:39 WAT - Record created by System Admin')
        self.assertTrue(
            "State 'courses validated' imported by system" in history[3])
        # history import has been logged
        logcontent = open(self.logfile).read()
        self.assertTrue(
            "history=[u'2012-10-23 00:05:39 WAT - Record created by System Admin'"
            in logcontent)
        # Two new student_ids have been created.
        self.assertEqual(self.app['students']._curr_stud_id, 1000003)
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_extascii(self):
        self.assertEqual(self.app['students']._curr_stud_id, 1000001)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_extascii, STUDENT_HEADER_FIELDS_EXTASCII)
        self.assertEqual(num_warns,0)
        self.assertEqual(len(self.app['students']), 3)
        self.assertEqual(self.app['students']['X111111'].reg_number,'1')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_update(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update, STUDENT_HEADER_FIELDS_UPDATE, 'update')
        self.assertEqual(num_warns,0)
        # state has changed
        self.assertEqual(self.app['students']['X666666'].state,'admitted')
        # state has not changed
        self.assertEqual(self.app['students']['Y777777'].state,
                         'courses validated')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_update2(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        container = self.app['students']
        self.assertEqual(
            IUserAccount(container['X666666']).checkPassword('test1234'), True)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update2, STUDENT_HEADER_FIELDS_UPDATE2, 'update')
        self.assertEqual(num_warns,0)
        # The phone import value of Pieri was None.
        # Confirm that phone has not been cleared.
        for key in container.keys():
            if container[key].firstname == 'Aaren':
                aaren = container[key]
                break
        self.assertEqual(aaren.phone, '--1234')
        # The phone import value of Claus was a deletion marker.
        # Confirm that phone has been cleared.
        for key in container.keys():
            if container[key].firstname == 'Claus':
                claus = container[key]
                break
        assert claus.phone is None
        # The password of X666666 has been removed
        self.assertEqual(
            IUserAccount(container['X666666']).password, None)
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_update3(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update3, STUDENT_HEADER_FIELDS_UPDATE3, 'update')
        content = open(fail_file).read()
        self.assertEqual(
            content,
            'reg_number,student_id,transition,firstname,--ERRORS--\r\n'
            '<IGNORE>,X666666,request_clearance,<IGNORE>,Transition not allowed.\r\n'
            '<IGNORE>,X666666,<IGNORE>,XXX,RequiredMissing: firstname\r\n'
            )
        self.assertEqual(num_warns,2)
        self.assertEqual(self.app['students']['Y777777'].state,'returning')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_update4(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDENT_HEADER_FIELDS)
        self.assertRaises(
            FatalCSVError, self.processor.doImport, self.csv_file_update4,
            STUDENT_HEADER_FIELDS_UPDATE4, 'update')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_remove(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update, STUDENT_HEADER_FIELDS_UPDATE, 'remove')
        self.assertEqual(num_warns,0)
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_migration_data(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_migration, STUDENT_HEADER_FIELDS_MIGRATION)
        content = open(fail_file).read()
        self.assertEqual(num_warns,3)
        assert len(self.app['students'].keys()) == 5
        self.assertEqual(
            content,
            'reg_number,firstname,student_id,sex,email,phone,state,date_of_birth,lastname,password,matric_number,history,--ERRORS--\r\n'
            '4,John,D123456,m,aa@aa.ng,1234,nonsense,1990-01-05,Wolter,mypw1,100003,<IGNORE>,state: not allowed\r\n'
            '5,John,E123456,x,aa@aa.ng,1234,<IGNORE>,1990-01-06,Kennedy,<IGNORE>,100004,<IGNORE>,sex: Invalid value\r\n'
            '7,Ulli,G123456,m,aa@aa.ng,1234,<IGNORE>,1990-01-06,Meyer,<IGNORE>,100007,nonsense,history: malformed string\r\n'
            )
        students = self.app['students']
        self.assertTrue('A123456' in students.keys())
        self.assertEqual(students['A123456'].state, 'clearance started')
        self.assertEqual(students['A123456'].date_of_birth,
                         datetime.date(1990, 1, 2))
        self.assertFalse(students['A123456'].clearance_locked)
        self.assertEqual(students['B123456'].state, 'cleared')
        self.assertEqual(students['B123456'].date_of_birth,
                         datetime.date(1990, 1, 3))
        self.assertTrue(students['B123456'].clearance_locked)
        history = students['A123456'].history.messages
        self.assertEqual(history[0],
            '2012-10-23 00:05:39 WAT - Record created by System Admin')
        self.assertTrue(
            "State 'clearance started' imported by system" in history[3])
        # state was empty and student is thus in state created
        self.assertEqual(students['F123456'].state,'created')
        # passwords were set correctly
        self.assertEqual(
            IUserAccount(students['A123456']).checkPassword('mypw1'), True)
        self.assertEqual(
            IUserAccount(students['C123456']).checkPassword('mypw1'), True)
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_duplicate_data(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_duplicates, STUDENT_HEADER_FIELDS_DUPLICATES)
        content = open(fail_file).read()
        self.assertEqual(num_warns,4)
        self.assertEqual(
            content,
            'reg_number,firstname,student_id,sex,email,phone,state,date_of_birth,lastname,password,matric_number,--ERRORS--\r\n'
            '1,Aaren,B123456,m,aa@aa.ng,1234,cleared,1990-01-03,Finau,mypw1,100001,reg_number: Invalid input\r\n'
            '2,Aaren,C123456,m,aa@aa.ng,1234,admitted,1990-01-04,Berson,mypw1,100000,matric_number: Invalid input\r\n'
            '1,Frank,F123456,m,aa@aa.ng,1234,<IGNORE>,1990-01-06,Meyer,<IGNORE>,100000,reg_number: Invalid input; matric_number: Invalid input\r\n'
            '3,Uli,A123456,m,aa@aa.ng,1234,<IGNORE>,1990-01-07,Schulz,<IGNORE>,100002,This object already exists.\r\n'
            )
        shutil.rmtree(os.path.dirname(fin_file))

class StudentStudyCourseProcessorTest(StudentImportExportSetup):

    def setUp(self):
        super(StudentStudyCourseProcessorTest, self).setUp()

        # Add student with subobjects
        student = Student()
        self.app['students'].addStudent(student)
        student = self.setup_student(student)
        notify(grok.ObjectModifiedEvent(student))
        self.student = self.app['students'][student.student_id]

        # Import students with subobjects
        student_file = os.path.join(self.workdir, 'sample_student_data.csv')
        open(student_file, 'wb').write(STUDENT_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = StudentProcessor().doImport(
            student_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        self.processor = StudentStudyCourseProcessor()
        self.csv_file = os.path.join(
            self.workdir, 'sample_studycourse_data.csv')
        open(self.csv_file, 'wb').write(STUDYCOURSE_SAMPLE_DATA)
        self.csv_file_transfer = os.path.join(
            self.workdir, 'sample_transfer_data.csv')
        open(self.csv_file_transfer, 'wb').write(TRANSFER_SAMPLE_DATA)
        return

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, StudentStudyCourseProcessor) is True

    def test_entryExists(self):
        assert self.processor.entryExists(
            dict(reg_number='REG_NONE'), self.app) is False
        assert self.processor.entryExists(
            dict(reg_number='1'), self.app) is True

    def test_getEntry(self):
        student = self.processor.getEntry(
            dict(reg_number='1'), self.app).__parent__
        self.assertEqual(student.reg_number,'1')

    def test_checkConversion(self):
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', certificate='CERT1', current_level='200'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', certificate='CERT999'))
        self.assertEqual(len(errs),1)
        self.assertTrue(('certificate', u'Invalid value') in errs)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', certificate='CERT1', current_level='100'))
        self.assertEqual(len(errs),1)
        self.assertTrue(('current_level','not in range') in errs)
        # If we import only current_level, no conversion checking is done.
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', current_level='100'))
        self.assertEqual(len(errs),0)

    def test_checkUpdateRequirements(self):
        # Current level must be in range of certificate.
        # Since row has passed the converter, current_level is an integer.
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=100), self.app)
        self.assertEqual(err, 'current_level not in range.')
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=200), self.app)
        self.assertTrue(err is None)
        # We can update pg students.
        self.student['studycourse'].certificate.start_level=999
        self.student['studycourse'].certificate.end_level=999
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=999), self.app)
        self.assertTrue(err is None)
        # Make sure that pg students can't be updated with wrong transition.
        IWorkflowState(self.student).setState('returning')
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=999), self.app)
        self.assertEqual(err, 'Not a pg student.')
        # If certificate is not given in row (and has thus
        # successfully passed checkConversion) the certificate
        # attribute must be set.
        self.student['studycourse'].certificate = None
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=100), self.app)
        self.assertEqual(err, 'No certificate to check level.')
        # When transferring students the method also checks
        # if the former studycourse is complete.
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', certificate='CERT1', current_level=200,
            entry_mode='transfer'), self.app)
        self.assertEqual(err, 'Former study course record incomplete.')
        self.student['studycourse'].certificate = self.certificate
        self.student['studycourse'].entry_session = 2005
        # The method doesn't care if current_level
        # is not in range of CERT1. This is done by checkConversion
        # if certificate is in row.
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', certificate='CERT1', current_level=200,
            entry_mode='transfer'), self.app)
        self.assertTrue(err is None)
        # In state 'transcript validated' studycourses are locked.
        IWorkflowState(self.student).setState('transcript validated')
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=999), self.app)
        self.assertEqual(err, 'Studycourse is locked.')
        # In state 'graduated' studycourses are also locked.
        IWorkflowState(self.student).setState('graduated')
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=999), self.app)
        self.assertEqual(err, 'Studycourse is locked.')
        # In state 'transcript released' studycourses are also locked ...
        IWorkflowState(self.student).setState('transcript released')
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=999), self.app)
        self.assertEqual(err, 'Studycourse is locked.')
        # ... but not in state 'transcript requested'.
        IWorkflowState(self.student).setState('transcript requested')
        err = self.processor.checkUpdateRequirements(
            self.student['studycourse'],
            dict(reg_number='1', current_level=999), self.app)
        self.assertTrue(err is None)

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYCOURSE_HEADER_FIELDS,'update')
        self.assertEqual(num_warns,1)
        content = open(fail_file).read()
        self.assertTrue('current_level: not in range' in content)
        studycourse = self.processor.getEntry(dict(reg_number='1'), self.app)
        self.assertEqual(studycourse.certificate.code, u'CERT1')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_transfer(self):
        self.certificate2 = createObject('waeup.Certificate')
        self.certificate2.code = 'CERT2'
        self.certificate2.application_category = 'basic'
        self.certificate2.start_level = 200
        self.certificate2.end_level = 500
        self.certificate2.study_mode = u'ug_pt'
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate2)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_transfer, TRANSFER_HEADER_FIELDS,'update')
        self.assertEqual(num_warns,0)
        self.assertEqual(self.student['studycourse'].certificate.code, 'CERT2')
        self.assertEqual(self.student['studycourse_1'].certificate.code, 'CERT1')
        self.assertEqual(self.student['studycourse'].entry_mode, 'transferred')
        self.assertEqual(self.student['studycourse_1'].entry_mode, 'ug_ft')
        self.assertEqual(self.student.current_mode, 'ug_pt')
        shutil.rmtree(os.path.dirname(fin_file))
        # Transfer has bee logged.
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'INFO - system - K1000000 - transferred from CERT1 to CERT2\n'
            in logcontent)
        self.assertTrue(
            'INFO - system - '
            'StudentStudyCourse Processor - '
            'sample_transfer_data - K1000000 - updated: entry_mode=transferred, '
            'certificate=CERT2, current_session=2009, current_level=300'
            in logcontent)
        # A history message has been added.
        history = ' '.join(self.student.history.messages)
        self.assertTrue(
            "Transferred from CERT1 to CERT2 by system" in history)
        # The catalog has been updated
        cat = queryUtility(ICatalog, name='students_catalog')
        results = list(
            cat.searchResults(
            certcode=('CERT2', 'CERT2')))
        self.assertTrue(results[0] is self.student)
        results = list(
            cat.searchResults(
            current_session=(2009, 2009)))
        self.assertTrue(results[0] is self.student)
        results = list(
            cat.searchResults(
            certcode=('CERT1', 'CERT1')))
        self.assertEqual(len(results), 0)

class StudentStudyLevelProcessorTest(StudentImportExportSetup):

    def setUp(self):
        super(StudentStudyLevelProcessorTest, self).setUp()

        # Import students with subobjects
        student_file = os.path.join(self.workdir, 'sample_student_data.csv')
        open(student_file, 'wb').write(STUDENT_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = StudentProcessor().doImport(
            student_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        # Update study courses
        studycourse_file = os.path.join(
            self.workdir, 'sample_studycourse_data.csv')
        open(studycourse_file, 'wb').write(STUDYCOURSE_SAMPLE_DATA)
        processor = StudentStudyCourseProcessor()
        num, num_warns, fin_file, fail_file = processor.doImport(
            studycourse_file, STUDYCOURSE_HEADER_FIELDS,'update')
        shutil.rmtree(os.path.dirname(fin_file))

        self.processor = StudentStudyLevelProcessor()
        self.csv_file = os.path.join(
            self.workdir, 'sample_studylevel_data.csv')
        open(self.csv_file, 'wb').write(STUDYLEVEL_SAMPLE_DATA)

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, StudentStudyLevelProcessor) is True

    def test_checkConversion(self):
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', level='220'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', level='999'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', level='1000'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', level='1100'))
        self.assertEqual(len(errs),1)
        self.assertTrue(('level', u'Invalid value') in errs)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', level='xyz'))
        self.assertEqual(len(errs),1)
        self.assertTrue(('level', u'Invalid value') in errs)

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'create')
        self.assertEqual(num_warns,3)
        assert self.processor.entryExists(
            dict(reg_number='1', level='100'), self.app) is True
        studylevel = self.processor.getEntry(
            dict(reg_number='1', level='100'), self.app)
        self.assertEqual(studylevel.__parent__.certificate.code, u'CERT1')
        self.assertEqual(studylevel.level_session, 2008)
        self.assertEqual(studylevel.level_verdict, '0')
        self.assertEqual(studylevel.level, 100)
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry,
        self.assertTrue(
            'INFO - system - StudentStudyLevel Processor - '
            'sample_studylevel_data - K1000000 - updated: '
            'level=100, level_verdict=C, level_session=2009'
            in logcontent)
        content = open(fail_file).read()
        self.assertEqual(
            content,
            'reg_number,level_verdict,level_session,matric_number,level,'
            '--ERRORS--\r\n'
            '1,A,2008,<IGNORE>,111,level: Invalid value\r\n'
            '1,A,2008,<IGNORE>,nonsense,level: Invalid value\r\n'
            '1,A,2008,<IGNORE>,<IGNORE>,level: Invalid value\r\n'
            )
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_update(self):
        # We perform the same import twice,
        # the second time in update mode. The number
        # of warnings must be the same.
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'update')
        self.assertEqual(num_warns,3)
        studylevel = self.processor.getEntry(
            dict(reg_number='1', level='100'), self.app)
        self.assertEqual(studylevel.level, 100)
        content = open(fail_file).read()
        self.assertEqual(
            content,
            'reg_number,level_verdict,level_session,matric_number,level,'
            '--ERRORS--\r\n'
            '1,A,2008,<IGNORE>,111,level: Invalid value\r\n'
            '1,A,2008,<IGNORE>,nonsense,level: Invalid value\r\n'
            '1,A,2008,<IGNORE>,<IGNORE>,Cannot update: no such entry\r\n'
            )
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_update_locked(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        # In state 'transcript validated' studylevels can't be edited
        student = self.app['students']['X666666']
        IWorkflowState(student).setState('transcript validated')
        # Two more records could't be imported because course tickets
        # of X666666 are locked
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'update')
        self.assertEqual(num_warns,5)
        content = open(fail_file).read()
        self.assertEqual(
            content,
            'reg_number,level_verdict,level_session,matric_number,level,--ERRORS--\r\n'
            '1,<IGNORE>,2008,<IGNORE>,100,Studylevel is locked.\r\n'
            '1,<IGNORE>,2008,<IGNORE>,200,Studylevel is locked.\r\n'
            '1,A,2008,<IGNORE>,111,level: Invalid value\r\n'
            '1,A,2008,<IGNORE>,nonsense,level: Invalid value\r\n'
            '1,A,2008,<IGNORE>,<IGNORE>,Cannot update: no such entry\r\n'
            )
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_remove(self):
        # We perform the same import twice,
        # the second time in remove mode. The number
        # of warnings must be the same.
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'remove')
        assert self.processor.entryExists(
            dict(reg_number='1', level='100'), self.app) is False
        self.assertEqual(num_warns,3)
        shutil.rmtree(os.path.dirname(fin_file))

class CourseTicketProcessorTest(StudentImportExportSetup):

    def setUp(self):
        super(CourseTicketProcessorTest, self).setUp()

        # Import students with subobjects
        student_file = os.path.join(self.workdir, 'sample_student_data.csv')
        open(student_file, 'wb').write(STUDENT_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = StudentProcessor().doImport(
            student_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        # Add course and certificate course
        self.course = createObject('waeup.Course')
        self.course.code = 'COURSE1'
        self.course.semester = 1
        self.course.credits = 10
        self.course.passmark = 40
        self.app['faculties']['fac1']['dep1'].courses.addCourse(
            self.course)
        self.app['faculties']['fac1']['dep1'].certificates[
            'CERT1'].addCertCourse(
            self.course, level=100)

        # Update study courses
        studycourse_file = os.path.join(
            self.workdir, 'sample_studycourse_data.csv')
        open(studycourse_file, 'wb').write(STUDYCOURSE_SAMPLE_DATA)
        processor = StudentStudyCourseProcessor()
        num, num_warns, fin_file, fail_file = processor.doImport(
            studycourse_file, STUDYCOURSE_HEADER_FIELDS,'update')
        shutil.rmtree(os.path.dirname(fin_file))

        # Import study levels
        processor = StudentStudyLevelProcessor()
        studylevel_file = os.path.join(
            self.workdir, 'sample_studylevel_data.csv')
        open(studylevel_file, 'wb').write(STUDYLEVEL_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = processor.doImport(
            studylevel_file, STUDYLEVEL_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))

        self.processor = CourseTicketProcessor()
        self.csv_file = os.path.join(
            self.workdir, 'sample_courseticket_data.csv')
        open(self.csv_file, 'wb').write(COURSETICKET_SAMPLE_DATA)

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, CourseTicketProcessor) is True

    def test_checkConversion(self):
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', code='COURSE1', level='220'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(reg_number='1', code='COURSE2', level='220'))
        self.assertEqual(len(errs),1)
        self.assertTrue(('code','non-existent') in errs)

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'create')
        fail_file = open(fail_file).read()
        self.assertEqual(num_warns,5)
        self.assertEqual(fail_file,
            'reg_number,code,mandatory,level,level_session,ticket_session,score,unlock_score,matric_number,--ERRORS--\r\n'
            '1,COURSE1,<IGNORE>,nonsense,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,Not all parents do exist yet.\r\n'
            '1,NONSENSE,<IGNORE>,100,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,code: non-existent\r\n'
            '1,COURSE1,<IGNORE>,200,2004,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: does not match 2008\r\n'
            '1,COURSE1,<IGNORE>,300,2008,<IGNORE>,6,<IGNORE>,<IGNORE>,level object: does not exist\r\n'
            '1,COURSE1,<IGNORE>,300,2008X,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: Invalid value\r\n')
        assert self.processor.entryExists(
            dict(reg_number='1', level='100', code='COURSE1'),
            self.app) is True
        courseticket = self.processor.getEntry(
            dict(reg_number='1', level='100', code='COURSE1'), self.app)
        self.assertEqual(courseticket.__parent__.__parent__.certificate.code,
                         u'CERT1')
        self.assertEqual(courseticket.score, 1)
        self.assertEqual(courseticket.mandatory, True)
        self.assertEqual(courseticket.fcode, 'NA')
        self.assertEqual(courseticket.dcode, 'NA')
        self.assertEqual(courseticket.code, 'COURSE1')
        self.assertEqual(courseticket.title, 'Unnamed Course')
        self.assertEqual(courseticket.credits, 10)
        self.assertEqual(courseticket.passmark, 40)
        self.assertEqual(courseticket.semester, 1)
        self.assertEqual(courseticket.level, 100)
        self.assertEqual(courseticket.level_session, 2008)
        shutil.rmtree(os.path.dirname(fin_file))
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry,
        self.assertTrue(
            'INFO - system - CourseTicket Processor - '
            'sample_courseticket_data - K1000000 - 100 - '
            'updated: code=COURSE1, '
            'mandatory=False, score=3'
            in logcontent)

        # The catalog has been updated
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        results = list(
            cat.searchResults(
            level=(100, 100)))
        self.assertEqual(len(results),3)

    def test_import_update(self):
        # We perform the same import twice,
        # the second time in update mode. The number
        # of warnings must be the same.
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'create')
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'update')
        fail_file = open(fail_file).read()
        self.assertEqual(num_warns,5)
        self.assertEqual(fail_file,
            'reg_number,code,mandatory,level,level_session,ticket_session,score,unlock_score,matric_number,--ERRORS--\r\n'
            '1,COURSE1,<IGNORE>,nonsense,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,Cannot update: no such entry\r\n'
            '1,NONSENSE,<IGNORE>,100,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,code: non-existent\r\n'
            '1,COURSE1,<IGNORE>,200,2004,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: does not match 2008\r\n'
            '1,COURSE1,<IGNORE>,300,2008,<IGNORE>,6,<IGNORE>,<IGNORE>,level object: does not exist\r\n'
            '1,COURSE1,<IGNORE>,300,2008X,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: Invalid value\r\n')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_remove(self):
        # We perform the same import twice,
        # the second time in remove mode. The number
        # of warnings must be the same.
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        assert self.processor.entryExists(
            dict(reg_number='1', level='100', code='COURSE1'), self.app) is True
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'remove')
        self.assertEqual(num_warns,5)
        assert self.processor.entryExists(
            dict(reg_number='1', level='100', code='COURSE1'), self.app) is False
        shutil.rmtree(os.path.dirname(fin_file))
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'INFO - system - K1000000 - Course ticket in 100 removed: COURSE1'
            in logcontent)

    def test_import_update_locked(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        # In state 'transcript validated' course tickets can't edited
        student = self.app['students']['X666666']
        IWorkflowState(student).setState('transcript validated')
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'update')
        fail_file = open(fail_file).read()
        # Two more records could't be imported because course tickets
        # of X666666 are locked
        self.assertEqual(num_warns,7)
        self.assertEqual(fail_file,
            'reg_number,code,mandatory,level,level_session,ticket_session,score,unlock_score,matric_number,--ERRORS--\r\n'
            '1,COURSE1,True,100,<IGNORE>,<IGNORE>,1,<IGNORE>,<IGNORE>,Studycourse is locked.\r\n'
            '1,COURSE1,True,200,2008,<IGNORE>,1,<IGNORE>,<IGNORE>,Studycourse is locked.\r\n'
            '1,COURSE1,<IGNORE>,nonsense,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,Cannot update: no such entry\r\n'
            '1,NONSENSE,<IGNORE>,100,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,code: non-existent\r\n'
            '1,COURSE1,<IGNORE>,200,2004,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: does not match 2008\r\n'
            '1,COURSE1,<IGNORE>,300,2008,<IGNORE>,6,<IGNORE>,<IGNORE>,level object: does not exist\r\n'
            '1,COURSE1,<IGNORE>,300,2008X,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: Invalid value\r\n')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_create_locked(self):
        # In state 'transcript validated' course tickets can't be created
        student = self.app['students']['X666666']
        IWorkflowState(student).setState('transcript validated')
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'create')
        fail_file = open(fail_file).read()
        self.assertEqual(num_warns,7)
        self.assertEqual(fail_file,
            'reg_number,code,mandatory,level,level_session,ticket_session,score,unlock_score,matric_number,--ERRORS--\r\n'
            '1,COURSE1,True,100,<IGNORE>,<IGNORE>,1,<IGNORE>,<IGNORE>,Studycourse is locked.\r\n'
            '1,COURSE1,True,200,2008,<IGNORE>,1,<IGNORE>,<IGNORE>,Studycourse is locked.\r\n'
            '1,COURSE1,<IGNORE>,nonsense,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,Not all parents do exist yet.\r\n'
            '1,NONSENSE,<IGNORE>,100,<IGNORE>,<IGNORE>,5,<IGNORE>,<IGNORE>,code: non-existent\r\n'
            '1,COURSE1,<IGNORE>,200,2004,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: does not match 2008\r\n'
            '1,COURSE1,<IGNORE>,300,2008,<IGNORE>,6,<IGNORE>,<IGNORE>,level object: does not exist\r\n'
            '1,COURSE1,<IGNORE>,300,2008X,<IGNORE>,6,<IGNORE>,<IGNORE>,level_session: Invalid value\r\n')
        self.assertFalse(self.processor.entryExists(
            dict(reg_number='1', level='100', code='COURSE1'),
            self.app))
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_remove_locked(self):
        # We perform the same import twice,
        # the second time in remove mode. 
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        assert self.processor.entryExists(
            dict(reg_number='1', level='100', code='COURSE1'), self.app) is True
        # In state 'transcript validated' course tickets can't be removed
        student = self.app['students']['X666666']
        IWorkflowState(student).setState('transcript validated')
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, COURSETICKET_HEADER_FIELDS,'remove')
        self.assertEqual(num_warns,7)
        assert self.processor.entryExists(
            dict(reg_number='1', level='100', code='COURSE1'), self.app) is True
        logcontent = open(self.logfile).read()
        self.assertFalse(
            'INFO - system - X666666 - Course ticket in 100 removed: COURSE1'
            in logcontent)
        fail_file = open(fail_file).read()
        self.assertEqual(fail_file,
            'reg_number,code,matric_number,level,--ERRORS--\r\n'
            '1,COURSE1,<IGNORE>,100,Studycourse is locked.\r\n'
            '1,COURSE1,<IGNORE>,200,Studycourse is locked.\r\n'
            '1,COURSE1,<IGNORE>,nonsense,Cannot remove: no such entry\r\n'
            '1,NONSENSE,<IGNORE>,100,Cannot remove: no such entry\r\n'
            '1,COURSE1,<IGNORE>,200,Studycourse is locked.\r\n'
            '1,COURSE1,<IGNORE>,300,Cannot remove: no such entry\r\n'
            '1,COURSE1,<IGNORE>,300,Cannot remove: no such entry\r\n'
            )
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_firstcourse_with_content(self):
        processor = StudentStudyCourseProcessor()
        csv_file = os.path.join(
            self.workdir, 'sample_first_studycourse_data.csv')
        open(csv_file, 'wb').write(FIRST_STUDYCOURSE_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = processor.doImport(
            csv_file, FIRST_STUDYCOURSE_HEADER_FIELDS,'create')
        self.assertEqual(num_warns,1)
        content = open(fail_file).read()
        self.assertTrue('current_level: not in range' in content)
        studycourse = processor.getEntry(
            dict(reg_number='1', previous='1'), self.app)
        self.assertEqual(studycourse.certificate.code, u'CERT1')
        self.assertEqual(studycourse.__name__, u'studycourse_1')
        cat = queryUtility(ICatalog, name='students_catalog')
        results = list(cat.searchResults(reg_number=('1', '1')))
        self.assertEqual([i for i in results[0].keys()],
            [u'accommodation', u'payments', u'studycourse', u'studycourse_1'])

        processor = StudentStudyLevelProcessor()
        csv_file = os.path.join(
            self.workdir, 'sample_first_studylevel_data.csv')
        open(csv_file, 'wb').write(FIRST_STUDYLEVEL_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = processor.doImport(
            csv_file, FIRST_STUDYLEVEL_HEADER_FIELDS,'create')
        self.assertEqual(num_warns,3)
        assert processor.entryExists(
            dict(reg_number='1', level='100'), self.app) is True
        studylevel = processor.getEntry(
            dict(reg_number='1', level='100'), self.app)
        self.assertEqual(studylevel.__parent__.certificate.code, u'CERT1')
        self.assertEqual(studylevel.level_session, 2008)
        self.assertEqual(studylevel.level_verdict, '0')
        self.assertEqual(studylevel.level, 100)
        self.assertEqual([i for i in results[0]['studycourse_1'].keys()],
            [u'100', u'200'])

        processor = CourseTicketProcessor()
        csv_file = os.path.join(
            self.workdir, 'sample_first_courseticket_data.csv')
        open(csv_file, 'wb').write(FIRST_COURSETICKET_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = processor.doImport(
            csv_file, FIRST_COURSETICKET_HEADER_FIELDS,'create')
        assert processor.entryExists(
            dict(reg_number='1', level='100',
                 code='COURSE1', previous='1'), self.app) is True
        self.assertEqual([i for i in results[0]['studycourse_1']['100'].keys()],
            [u'COURSE1'])
        shutil.rmtree(os.path.dirname(fin_file))

class PaymentProcessorTest(StudentImportExportSetup):

    def setUp(self):
        super(PaymentProcessorTest, self).setUp()

        # Add student with payment
        student = Student()
        student.firstname = u'Anna'
        student.lastname = u'Tester'
        student.reg_number = u'123'
        student.matric_number = u'234'
        self.app['students'].addStudent(student)
        self.student = self.app['students'][student.student_id]
        payment = createObject(u'waeup.StudentOnlinePayment')
        payment.p_id = 'p120'
        payment.p_session = 2012
        payment.p_category = 'schoolfee'
        payment.p_state = 'paid'
        self.student['payments'][payment.p_id] = payment

        # Import students with subobjects
        student_file = os.path.join(self.workdir, 'sample_student_data.csv')
        open(student_file, 'wb').write(STUDENT_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = StudentProcessor().doImport(
            student_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        self.processor = StudentOnlinePaymentProcessor()
        self.csv_file = os.path.join(
            self.workdir, 'sample_payment_data.csv')
        open(self.csv_file, 'wb').write(PAYMENT_SAMPLE_DATA)
        self.csv_file2 = os.path.join(
            self.workdir, 'sample_create_payment_data.csv')
        open(self.csv_file2, 'wb').write(PAYMENT_CREATE_SAMPLE_DATA)

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, StudentOnlinePaymentProcessor) is True

    def test_getEntry(self):
        assert self.processor.getEntry(
            dict(student_id='ID_NONE', p_id='nonsense'), self.app) is None
        assert self.processor.getEntry(
            dict(student_id=self.student.student_id, p_id='p120'),
            self.app) is self.student['payments']['p120']
        assert self.processor.getEntry(
            dict(student_id=self.student.student_id, p_id='XXXXXX112'),
            self.app) is self.student['payments']['p120']

    def test_delEntry(self):
        assert self.processor.getEntry(
            dict(student_id=self.student.student_id, p_id='p120'),
            self.app) is self.student['payments']['p120']
        self.assertEqual(len(self.student['payments'].keys()),1)
        self.processor.delEntry(
            dict(student_id=self.student.student_id, p_id='p120'),
            self.app)
        assert self.processor.getEntry(
            dict(student_id=self.student.student_id, p_id='p120'),
            self.app) is None
        self.assertEqual(len(self.student['payments'].keys()),0)

    def test_addEntry(self):
        self.assertEqual(len(self.student['payments'].keys()),1)
        payment1 = createObject(u'waeup.StudentOnlinePayment')
        payment1.p_id = 'p234'
        self.processor.addEntry(
            payment1, dict(student_id=self.student.student_id, p_id='p234'),
            self.app)
        self.assertEqual(len(self.student['payments'].keys()),2)
        self.assertEqual(self.student['payments']['p234'].p_id, 'p234')
        payment2 = createObject(u'waeup.StudentOnlinePayment')
        payment1.p_id = 'nonsense'
        # payment1.p_id will be replaced if p_id doesn't start with 'p'
        # and is not an old PIN
        self.processor.addEntry(
            payment2, dict(student_id=self.student.student_id, p_id='XXXXXX456'),
            self.app)
        self.assertEqual(len(self.student['payments'].keys()),3)
        self.assertEqual(self.student['payments']['p560'].p_id, 'p560')
        # Requirement added on 19/02/2015: same payment must not exist.
        payment3 = createObject(u'waeup.StudentOnlinePayment')
        payment3.p_id = 'p456'
        payment3.p_session = 2012
        payment3.p_category = 'schoolfee'
        self.assertRaises(
            DuplicationError, self.processor.addEntry, payment3,
            dict(student_id=self.student.student_id, p_id='p456'), self.app)
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'INFO - system - StudentOnlinePayment Processor - K1000000 - '
            'previous update cancelled'
            in logcontent)

    def test_checkConversion(self):
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='<IGNORE>'), mode='create')
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='<IGNORE>'), mode='update')
        self.assertEqual(len(errs),1)
        self.assertEqual(errs[0], ('p_id', u'missing'))
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='3816951266236341955'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='p1266236341955'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='ABC-11-1234567890'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='nonsense'))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs[0], ('p_id', u'invalid format'))
        timestamp = ("%d" % int(time()*10000))[1:]
        p_id = "p%s" % timestamp
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id=p_id))
        self.assertEqual(len(errs),0)
        dup_payment = createObject(u'waeup.StudentOnlinePayment')
        dup_payment.p_id = 'XYZ-99-1234567890'
        self.student['payments'][dup_payment.p_id] = dup_payment
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='XYZ-99-1234567890'), mode='create')
        self.assertEqual(len(errs),1)
        self.assertEqual(errs[0], ('p_id', u'p_id exists in K1000000 '))

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, PAYMENT_HEADER_FIELDS,'create')
        self.assertEqual(num_warns,0)

        payment = self.processor.getEntry(dict(reg_number='1',
            p_id='p2907979737440'), self.app)
        self.assertEqual(payment.p_id, 'p2907979737440')
        self.assertTrue(payment.p_current)
        cdate = payment.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(cdate, "2010-11-26 18:59:33")
        self.assertEqual(str(payment.creation_date.tzinfo),'UTC')

        payment = self.processor.getEntry(dict(matric_number='100001',
            p_id='p2907125937570'), self.app)
        self.assertEqual(payment.p_id, 'p2907125937570')
        self.assertEqual(payment.amount_auth, 19500.1)
        self.assertFalse(payment.p_current)
        cdate = payment.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        # Ooooh, still the old problem, see
        # http://mail.dzug.org/mailman/archives/zope/2006-August/001153.html.
        # WAT is interpreted as GMT-1 and not GMT+1
        self.assertEqual(cdate, "2010-11-25 21:16:33")
        self.assertEqual(str(payment.creation_date.tzinfo),'UTC')

        payment = self.processor.getEntry(dict(reg_number='3',
            p_id='ABC-11-1234567890'), self.app)
        self.assertEqual(payment.amount_auth, 19500.6)

        shutil.rmtree(os.path.dirname(fin_file))
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry
        self.assertTrue(
            'INFO - system - StudentOnlinePayment Processor - '
            'sample_payment_data - K1000001 - updated: '
            'p_item=BTECHBDT, creation_date=2010-02-15 13:19:01+00:00, '
            'p_category=schoolfee, amount_auth=19500.0, p_current=True, '
            'p_session=2009, '
            'p_id=p1266236341955, r_code=00, r_amount_approved=19500.0, '
            'p_state=paid'
            in logcontent)
        self.assertTrue(
            'INFO - system - StudentOnlinePayment Processor - '
            'sample_payment_data - K1000001 - updated: '
            'p_item=BTECHBDT, creation_date=2010-02-15 13:19:01+00:00, '
            'p_category=schoolfee, amount_auth=19500.6, p_current=True, '
            'p_session=2011, '
            'p_id=ABC-11-1234567890, r_code=SC, r_amount_approved=19500.0, '
            'p_state=paid'
            in logcontent)

    def test_import_update(self):
        # We perform the same import twice,
        # the second time in update mode. The number
        # of warnings increases becaus one p_id is missing.
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, PAYMENT_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, PAYMENT_HEADER_FIELDS,'update')
        self.assertEqual(num_warns,1)
        content = open(fail_file).read()
        shutil.rmtree(os.path.dirname(fin_file))
        self.assertTrue('p_id: missing' in content)

    def test_import_remove(self):
        # We perform the same import twice,
        # the second time in remove mode. The number
        # of warnings increases becaus one p_id is missing.
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, PAYMENT_HEADER_FIELDS,'create')
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, PAYMENT_HEADER_FIELDS,'remove')
        self.assertEqual(num_warns,1)
        content = open(fail_file).read()
        self.assertTrue('p_id: missing' in content)
        shutil.rmtree(os.path.dirname(fin_file))
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'INFO - system - K1000001 - Payment ticket removed: p1266236341955'
            in logcontent)

    def test_import_same_payment_exists(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file2, PAYMENT_CREATE_HEADER_FIELDS,'create')
        # One payment with same session and category exists
        self.assertEqual(num_warns,1)
        content = open(fail_file).read()
        self.assertTrue(
            '1,942,online,BTECHBDT,2010/11/26 19:59:33.744 GMT+1,0,'
            '19500,schoolfee,19500,2015,unpaid,'
            'Same payment has already been made.'
            in content)
        shutil.rmtree(os.path.dirname(fin_file))
        self.assertEqual(len(self.app['students']['X666666']['payments']), 13)

class StudentVerdictProcessorTest(StudentImportExportSetup):

    def setUp(self):
        super(StudentVerdictProcessorTest, self).setUp()

        # Import students with subobjects
        student_file = os.path.join(self.workdir, 'sample_student_data.csv')
        open(student_file, 'wb').write(STUDENT_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = StudentProcessor().doImport(
            student_file, STUDENT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        # Update study courses
        studycourse_file = os.path.join(
            self.workdir, 'sample_studycourse_data.csv')
        open(studycourse_file, 'wb').write(STUDYCOURSE_SAMPLE_DATA)
        processor = StudentStudyCourseProcessor()
        num, num_warns, fin_file, fail_file = processor.doImport(
            studycourse_file, STUDYCOURSE_HEADER_FIELDS,'update')
        shutil.rmtree(os.path.dirname(fin_file))
        # Import study levels
        self.csv_file = os.path.join(
            self.workdir, 'sample_studylevel_data.csv')
        open(self.csv_file, 'wb').write(STUDYLEVEL_SAMPLE_DATA)
        processor = StudentStudyLevelProcessor()
        num, num_warns, fin_file, fail_file = processor.doImport(
            self.csv_file, STUDYLEVEL_HEADER_FIELDS,'create')
        content = open(fail_file).read()
        shutil.rmtree(os.path.dirname(fin_file))

        self.processor = StudentVerdictProcessor()
        self.csv_file = os.path.join(
            self.workdir, 'sample_verdict_data.csv')
        open(self.csv_file, 'wb').write(VERDICT_SAMPLE_DATA)
        return

    def test_import(self):
        studycourse = self.processor.getEntry(dict(matric_number='100000'),
                                              self.app)
        self.assertEqual(studycourse['200'].level_verdict, '0')
        student = self.processor.getParent(
            dict(matric_number='100000'), self.app)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, VERDICT_HEADER_FIELDS,'update')
        self.assertEqual(num_warns,5)
        self.assertEqual(studycourse.current_verdict, '0')
        self.assertEqual(student.state, 'returning')
        self.assertEqual(studycourse.current_level, 200)
        self.assertEqual(studycourse['200'].level_verdict, '0')
        student = self.processor.getParent(
            dict(matric_number='100005'), self.app)
        self.assertEqual(student.state, 'returning')
        self.assertEqual(student['studycourse'].current_verdict, 'A')
        self.assertEqual(studycourse.current_level, 200)
        self.assertEqual(student['studycourse']['200'].validated_by, 'System')
        self.assertTrue(isinstance(
            student['studycourse']['200'].validation_date, datetime.datetime))
        student = self.processor.getParent(
            dict(matric_number='100008'), self.app)
        self.assertEqual(student['studycourse']['200'].validated_by, 'Juliana')
        content = open(fail_file).read()
        self.assertEqual(
            content,
            'current_session,current_level,bypass_validation,current_verdict,'
            'matric_number,validated_by,--ERRORS--\r\n'
            '2008,100,False,B,100001,<IGNORE>,Current level does not correspond.\r\n'
            '2007,200,<IGNORE>,C,100002,<IGNORE>,Current session does not correspond.\r\n'
            '2008,200,<IGNORE>,A,100003,<IGNORE>,Student in wrong state.\r\n'
            '2008,200,<IGNORE>,<IGNORE>,100004,<IGNORE>,No verdict in import file.\r\n'
            '2008,200,True,A,100007,<IGNORE>,Study level object is missing.\r\n'
            )
        logcontent = open(self.logfile).read()
        self.assertMatches(
            '... INFO - system - Verdict Processor (special processor, '
            'update only) - sample_verdict_data - X666666 - '
            'updated: current_verdict=0...',
            logcontent)
        self.assertMatches(
            '... INFO - system - X666666 - Returned...',
            logcontent)
        shutil.rmtree(os.path.dirname(fin_file))

def test_suite():
    suite = unittest.TestSuite()
    for testcase in [
        StudentProcessorTest,StudentStudyCourseProcessorTest,
        StudentStudyLevelProcessorTest,CourseTicketProcessorTest,
        PaymentProcessorTest,StudentVerdictProcessorTest]:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
                testcase
                )
        )
    return suite


