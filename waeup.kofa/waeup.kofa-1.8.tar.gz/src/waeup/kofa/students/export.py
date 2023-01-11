## $Id: export.py 16831 2022-02-24 10:23:10Z henrik $
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
"""Exporters for student related stuff.
"""
import os
import grok
from copy import deepcopy
from datetime import datetime, timedelta
from zope.component import getUtility
from waeup.kofa.interfaces import (
    IExtFileStore, IFileStoreNameChooser, IKofaUtils)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.university.interfaces import ICertificateCourse, ICourse
from waeup.kofa.students.catalog import StudentsQuery, CourseTicketsQuery
from waeup.kofa.students.interfaces import (
    IStudent, IStudentStudyCourse, IStudentStudyLevel, ICourseTicket,
    IStudentOnlinePayment, ICSVStudentExporter, IBedTicket)
from waeup.kofa.students.vocabularies import study_levels
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.utils.helpers import iface_names, to_timezone


def get_students(site, stud_filter=StudentsQuery()):
    """Get all students registered in catalog in `site`.
    """
    return stud_filter.query()

def get_studycourses(students, previous=0):
    """Get studycourses of `students`.
    """
    studycourse = 'studycourse'
    if previous == 1:
        studycourse = 'studycourse_1'
    elif previous == 2:
        studycourse = 'studycourse_2'
    for x in students:
        if x.get(studycourse, None) is None:
            continue
        yield x.get(studycourse, None)

def get_levels(students, previous=0, **kw):
    """Get all studylevels of `students`.
    """
    levels = []
    level_session = kw.get('level_session', None)
    for course in get_studycourses(students, previous):
        for level in course.values():
            if level_session not in ('all', None) and \
                int(level_session) != level.level_session:
                continue
            levels.append(level)
    return levels

def get_tickets(students, previous=0, **kw):
    """Get course tickets of `students`.
    If code is passed through, filter course tickets
    which belong to this course code and meet level=level
    and level_session=level_session.
    If not, but ct_level, ct_session and ct_semester
    are passed through, filter course tickets
    which meet level==ct_level, level_session==ct_session
    and semester==ct_semester.
    """
    tickets = []
    code = kw.get('code', None)
    level = kw.get('level', None)
    session = kw.get('session', None)
    ct_level = kw.get('ct_level', None)
    ct_session = kw.get('ct_session', None)
    ct_semester = kw.get('ct_semester', None)
    if code is None:
        for level_obj in get_levels(students, previous, **kw):
            for ticket in level_obj.values():
                if ct_level not in ('all', None):
                    if level_obj.level in (10, 999, 1000, None)  \
                        and int(ct_level) != level_obj.level:
                        continue
                    if level_obj.level not in range(
                        int(ct_level), int(ct_level)+100, 10):
                        continue
                if ct_session not in ('all', None) and \
                    int(ct_session) != level_obj.level_session:
                    continue
                if ct_semester not in ('all', None) and \
                    int(ct_semester) != ticket.semester:
                    continue
                tickets.append(ticket)
    else:
        for level_obj in get_levels(students, previous, **kw):
            for ticket in level_obj.values():
                if ticket.code != code:
                    continue
                if level not in ('all', None):
                    if level_obj.level in (10, 999, 1000, None)  \
                        and int(level) != level_obj.level:
                        continue
                    if level_obj.level not in range(
                        int(level), int(level)+100, 10):
                        continue
                if session not in ('all', None) and \
                    int(session) != level_obj.level_session:
                    continue
                tickets.append(ticket)
    return tickets

def get_tickets_for_lecturer(students, previous=0, **kw):
    """Get course tickets of `students`.
    Filter course tickets which belong to this course code and
    which are editable by lecturers. The latter requirement was disabled
    on 10/03/21.
    """
    tickets = []
    code = kw.get('code', None)
    level_session = kw.get('session', None)
    level = kw.get('level', None)
    for level_obj in get_levels(students, previous, **kw):
        for ticket in level_obj.values():
            if ticket.code != code:
                continue
            # Disabled on 10/03/21
            #if not ticket.editable_by_lecturer:
            #    continue
            if level not in ('all', None):
                if level_obj.level in (10, 999, 1000, None)  \
                    and int(level) != level_obj.level:
                    continue
                if level_obj.level not in range(int(level), int(level)+100, 10):
                    continue
            if level_session not in ('all', None) and \
                int(level_session) != level_obj.level_session:
                continue
            tickets.append(ticket)
    return tickets

def get_outstanding(students, **kw):
    """Get students with outstanding certificate courses.
    """
    students_wo = []
    for student in students:
        certificate = getattr(
            student.get('studycourse', None), 'certificate', None)
        if certificate:
            allticketcodes = list()
            failedticketcodes = list() # taken but failed
            nottakenticketcodes = list() # registered but not taken
            missedticketcodes = list() # not registered
            # collect failed, not taken and all courses
            for level in student['studycourse'].values():
                # check if already failed or not taken courses have been passed later
                failedticketcodes_copy = deepcopy(failedticketcodes)
                nottakenticketcodes_copy = deepcopy(nottakenticketcodes)
                for code in failedticketcodes_copy:
                    if code.strip('m_').strip('_m') in level.passed_params[6]:
                        failedticketcodes.remove(code)
                for code in nottakenticketcodes_copy:
                    if code in level.passed_params[6]:
                        nottakenticketcodes.remove(code)
                failedticketcodes += level.passed_params[4].split()
                nottakenticketcodes += level.passed_params[5].split()
                for ticket in level.values():
                    allticketcodes.append(ticket.code)
            # collect missed tickets
            for certcourse in certificate.values():
                if certcourse.getCourseCode() not in allticketcodes:
                    missedticketcodes.append(certcourse.__name__)
            student_wo = (student, missedticketcodes,
                          failedticketcodes, nottakenticketcodes)
            students_wo.append(student_wo)
    return students_wo

def get_payments(students, p_states=None, **kw):
    """Get all payment tickets of `students` within given payment_date period.
    """
    date_format = '%d/%m/%Y'
    payments = []
    p_start = kw.get('payments_start')
    p_end = kw.get('payments_end')
    paycat = kw.get('paycat')
    paysession = kw.get('paysession')
    for student in students:
        for payment in student.get('payments', {}).values():
            if p_start and p_end:
                if not payment.payment_date:
                    continue
                payments_start = datetime.strptime(p_start, date_format)
                payments_end = datetime.strptime(p_end, date_format)
                tz = getUtility(IKofaUtils).tzinfo
                payments_start = tz.localize(payments_start)
                payments_end = tz.localize(payments_end) + timedelta(days=1)
                payment_date = to_timezone(payment.payment_date, tz)
                if payment_date < payments_start or payment_date > payments_end:
                    continue
            if p_states and not payment.p_state in p_states:
                continue
            if paycat not in ('all', None) and payment.p_category != paycat:
                continue
            if paysession not in ('all', None) \
                and payment.p_session != int(paysession):
                continue
            payments.append(payment)
    return payments

def get_bedtickets(students):
    """Get all bed tickets of `students`.
    """
    tickets = []
    for student in students:
        for ticket in student.get('accommodation', {}).values():
            tickets.append(ticket)
    return tickets

class StudentExporterBase(ExporterBase):
    """Exporter for students or related objects.
    This is a baseclass.
    """
    grok.baseclass()
    grok.implements(ICSVStudentExporter)
    grok.provides(ICSVStudentExporter)

    def filter_func(self, x, **kw):
        return x

    def get_filtered(self, site, **kw):
        """Get students from a catalog filtered by keywords.
        students_catalog is the default catalog. The keys must be valid
        catalog index names.
        Returns a simple empty list, a list with `Student`
        objects or a catalog result set with `Student`
        objects.

        .. seealso:: `waeup.kofa.students.catalog.StudentsCatalog`

        """
        # Pass only given keywords to create FilteredCatalogQuery objects.
        # This way we avoid
        # trouble with `None` value ambivalences and queries are also
        # faster (normally less indexes to ask). Drawback is, that
        # developers must look into catalog to see what keywords are
        # valid.
        if kw.get('catalog', None) == 'coursetickets':
            coursetickets = CourseTicketsQuery(**kw).query()
            students = []
            for ticket in coursetickets:
                students.append(ticket.student)
            return list(set(students))
        # Payments can be filtered by payment date and payment category.
        # These parameters are not keys of the catalog and must thus be
        # removed from kw.
        try:
            del kw['payments_start']
            del kw['payments_end']
            del kw['paycat']
            del kw['paysession']
        except KeyError:
            pass
        # Coursetickets can be filtered by level and session.
        # These parameters are not keys of the catalog and must thus be
        # removed from kw.
        try:
            del kw['ct_level']
            del kw['ct_session']
            del kw['ct_semester']
        except KeyError:
            pass
        # Studylevels can be filtered by level_session.
        # This parameter is not a key of the catalog and must thus be
        # removed from kw.
        try:
            del kw['level_session']
        except KeyError:
            pass
        query = StudentsQuery(**kw)
        return query.query()

    def get_selected(self, site, selected):
        """Get set of selected students.
        Returns a simple empty list or a list with `Student`
        objects.
        """
        students = []
        students_container = site.get('students', {})
        for id in selected:
            student = students_container.get(id, None)
            if student is None:
                # try matric number
                result = list(StudentsQuery(matric_number=id).query())
                if result:
                    student = result[0]
                else:
                    continue
            students.append(student)
        return students

    def export(self, values, filepath=None):
        """Export `values`, an iterable, as CSV file.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for value in values:
            self.write_item(value, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export students into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        return self.export(self.filter_func(get_students(site)), filepath)

    def export_student(self, student, filepath=None):
        return self.export(self.filter_func([student]), filepath=filepath)

    def export_filtered(self, site, filepath=None, **kw):
        """Export items denoted by `kw`.
        If `filepath` is ``None``, a raw string with CSV data should
        be returned.
        """
        data = self.get_filtered(site, **kw)
        return self.export(self.filter_func(data, **kw), filepath=filepath)

    def export_selected(self,site, filepath=None, **kw):
        """Export data for selected set of students.
        """
        selected = kw.get('selected', [])
        data = self.get_selected(site, selected)
        return self.export(self.filter_func(data, **kw), filepath=filepath)


class StudentExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Exporter first filters the set of students by searching the
    students catalog. Then it exports student base data of this set of students.
    """
    grok.name('students')

    fields = tuple(sorted(iface_names(IStudent))) + (
        'password', 'state', 'history', 'certcode', 'is_postgrad',
        'current_level', 'current_session', 'entry_session')
    title = _(u'Students (Data Backup)')

    def mangle_value(self, value, name, context=None):
        """The mangler prepares the history messages and adds a hash symbol at
        the end of the phone number to avoid annoying automatic number
        transformation by Excel or Calc."""
        if name == 'history':
            value = value.messages
        if 'phone' in name and value is not None:
            # Append hash '#' to phone numbers to circumvent
            # unwanted excel automatic
            value = str('%s#' % value)
        return super(
            StudentExporter, self).mangle_value(
            value, name, context=context)

class TrimmedDataExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Trimmed Data Exporter first filters the set of students 
    by searching the students catalog. Then it exports a trimmed data set
    of this set of students. 
    """
    grok.name('trimmed')

    fields = (
        'student_id',
        'matric_number',
        'reg_number',
        'firstname',
        'middlename',
        'lastname',
        'sex',
        'email',
        'phone',
        'nationality',
        'date_of_birth',
        'state',
        'current_mode',
        'certcode',
        'faccode',
        'depcode',
        'current_level',
        'current_session',
        'current_verdict',
        'entry_session')
    title = _(u'Students (Trimmed Data)')

    def mangle_value(self, value, name, context=None):
        """The mangler prepares the history messages and adds a hash symbol at
        the end of the phone number to avoid annoying automatic number
        transformation by Excel or Calc."""
        if 'phone' in name and value is not None:
            # Append hash '#' to phone numbers to circumvent
            # unwanted excel automatic
            value = str('%s#' % value)
        return super(
            TrimmedDataExporter, self).mangle_value(
            value, name, context=context)

class StudentStudyCourseExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Study Course Exporter first filters the set of students
    by searching the students catalog. Then it exports the data of the current
    study course container of each student from this set. It does
    not export their content.
    """
    grok.name('studentstudycourses')
    previous = 0

    fields = tuple(sorted(iface_names(IStudentStudyCourse))) + (
        'student_id', 'previous')
    title = _(u'Student Study Courses (Data Backup)')

    def filter_func(self, x, **kw):
        return get_studycourses(x)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the certificate code and the student id.
        """
        if name == 'certificate' and value is not None:
            # XXX: hopefully cert codes are unique site-wide
            value = value.code
        if name == 'student_id' and context is not None:
            student = context.student
            value = getattr(student, name, None)
        if name == 'previous':
            return self.previous
        return super(
            StudentStudyCourseExporter, self).mangle_value(
            value, name, context=context)

class FirstStudentStudyCourseExporter(StudentStudyCourseExporter):
    """The First Student Study Course Exporter exports the first
    study course if student was transferred.
    """
    grok.name('studentstudycourses_1')
    previous = 1
    title = _(u'First Student Study Courses (Data Backup)')

    def filter_func(self, x, **kw):
        return get_studycourses(x, 1)

class SecondStudentStudyCourseExporter(StudentStudyCourseExporter):
    """The Second Student Study Course Exporter exports the second
    study course if student was transferred twice.
    """
    grok.name('studentstudycourses_2')
    previous = 2
    title = _(u'Second Student Study Courses (Data Backup)')

    def filter_func(self, x, **kw):
        return get_studycourses(x, 2)

class StudentStudyLevelExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Study Level Exporter first filters the set of students
    by searching the students catalog. Then it exports the data of the student's
    study level container data but not their content (course tickets).
    The exporter iterates over all objects in the students' ``studycourse``
    containers.
    """
    grok.name('studentstudylevels')
    previous = 0

    fields = tuple(sorted(iface_names(
        IStudentStudyLevel))) + (
        'student_id', 'number_of_tickets','certcode', 'previous')
    title = _(u'Student Study Levels (Data Backup)')

    def filter_func(self, x, **kw):
        return get_levels(x, **kw)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student id, nothing else.
        """
        if name == 'student_id' and context is not None:
            student = context.student
            value = getattr(student, name, None)
        if name == 'previous':
            return self.previous
        return super(
            StudentStudyLevelExporter, self).mangle_value(
            value, name, context=context)

class FirstStudentStudyLevelExporter(StudentStudyLevelExporter):
    """The First Student Study Level Exporter exports study levels of the
    first study course if the student was transferred.
    """
    grok.name('studentstudylevels_1')
    previous = 1
    title = _(u'First Course Student Study Levels (Data Backup)')

    def filter_func(self, x, **kw):
        return get_levels(x, 1, **kw)

class SecondStudentStudyLevelExporter(StudentStudyLevelExporter):
    """The Second Student Study Level Exporter exports study levels of the
    second tudy course if the student was transferred twice.
    """
    grok.name('studentstudylevels_2')
    previous = 2
    title = _(u'Second Course Student Study Levels (Data Backup)')

    def filter_func(self, x, **kw):
        return get_levels(x, 2, **kw)

class CourseTicketExporter(grok.GlobalUtility, StudentExporterBase):
    """The Course Ticket Exporter exports course tickets. Usually,
    the exporter first filters the set of students by searching the
    students catalog. Then it collects and iterates over all ``studylevel``
    containers of the filtered student set and finally
    iterates over all items inside these containers.

    If the course code is passed through, the exporter uses a different
    catalog. It searches for students in the course tickets catalog and
    exports those course tickets which belong to the given course code and
    also meet level and session passed through at the same time.
    This happens if the exporter is called at course level in the academic
    section.
    """
    grok.name('coursetickets')

    fields = tuple(sorted(iface_names(ICourseTicket) +
        ['level', 'code', 'level_session'])) + ('student_id',
        'certcode', 'display_fullname', 'previous')
    title = _(u'Course Tickets (Data Backup)')
    previous = 0

    def filter_func(self, x, **kw):
        return get_tickets(x, **kw)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student's id and fullname.
        """
        if context is not None:
            student = context.student
            if name in ('student_id', 'display_fullname') and student is not None:
                value = getattr(student, name, None)
        if name == 'previous':
            return self.previous
        return super(
            CourseTicketExporter, self).mangle_value(
            value, name, context=context)

class FirstCourseTicketExporter(CourseTicketExporter):
    """The First Course Ticket Exporter exports course tickets of
    first study courses if the student was transferred.
    """
    grok.name('coursetickets_1')
    previous = 1
    title = _(u'First Course Course Tickets (Data Backup)')

    def filter_func(self, x, **kw):
        return get_tickets(x, 1, **kw)

class SecondCourseTicketExporter(CourseTicketExporter):
    """The Second Course Ticket Exporter exports course tickets of
    second study courses if the student was transferred twice.
    """
    grok.name('coursetickets_2')
    previous = 2
    title = _(u'Second Course Course Tickets (Data Backup)')

    def filter_func(self, x, **kw):
        return get_tickets(x, 2, **kw)

class StudentPaymentExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Payment Exporter first filters the set of students
    by searching the students catalog. Then it exports student payment
    tickets by iterating over the items of the student's ``payments``
    container. If the payment period is given, only tickets, which were
    paid in payment period, are considered for export.
    """
    grok.name('studentpayments')

    fields = tuple(
        sorted(iface_names(
            IStudentOnlinePayment, exclude_attribs=False,
            omit=['display_item', 'certificate', 'student', 'p_option']))) + (
            'student_id','state','current_session')
    title = _(u'Student Payments (Data Backup)')

    def filter_func(self, x, **kw):
        return get_payments(x, **kw)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student's id, registration
        state and current session.
        """
        if context is not None:
            student = context.student
            if name in ['student_id','state','entry_session',
                        'current_session'] and student is not None:
                value = getattr(student, name, None)
        return super(
            StudentPaymentExporter, self).mangle_value(
            value, name, context=context)

class StudentTrimmedPaymentExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Trimmed Payment Exporter is a slightly customized version
    of the StudentPaymentExporter requested by Uniben.
    """
    grok.name('trimmedpayments')

    fields = tuple(
        sorted(iface_names(
            IStudentOnlinePayment, exclude_attribs=False,
            omit=['display_item', 'certificate', 'student', 'ac', 'p_option']))) + (
            'student_id','faccode', 'depcode', 'state','current_session')
    title = _(u'Student Payments (Sorted Data)')

    def filter_func(self, x, **kw):
        payments = get_payments(x, **kw)
        return sorted([payment for payment in payments],
            key=lambda payment: str(payment.p_category) + str(payment.student.faccode)
                + str(payment.student.depcode) + str(payment.p_item))

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student's id, registration
        state and current session.
        """
        if context is not None:
            student = context.student
            if name in ['student_id','state', 'faccode', 'depcode',
                        'current_session'] and student is not None:
                value = getattr(student, name, None)
        return super(
            StudentTrimmedPaymentExporter, self).mangle_value(
            value, name, context=context)

class DataForLecturerExporter(grok.GlobalUtility, StudentExporterBase):
    """The Data for Lecturer Exporter searches for students in the course
    tickets catalog and exports those course tickets which belong to the
    given course code, meet level and session passed through at the
    same time, and which are editable by lecturers (disabled on 10/03/21).
    This exporter can only be called at course level in the academic section.
    """
    grok.name('lecturer')

    fields = ('matric_number', 'student_id', 'display_fullname',
              'level', 'code', 'level_session', 'score')

    title = _(u'Data for Lecturer')

    def filter_func(self, x, **kw):
        tickets = get_tickets_for_lecturer(x, **kw)
        return sorted([ticket for ticket in tickets],
            key=lambda ticket: str(ticket.fcode) + str(ticket.dcode)
                + str(ticket.student.matric_number))

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student's id and fullname.
        """
        if context is not None:
            student = context.student
            if name in ('matric_number',
                        'reg_number',
                        'student_id',
                        'display_fullname',) and student is not None:
                value = getattr(student, name, None)
        return super(
            DataForLecturerExporter, self).mangle_value(
            value, name, context=context)

class OutstandingCoursesExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Outstanding Courses Exporter first filters the set of 
    students by searching the students catalog. Then it exports students with 
    lists of outstanding courses, i.e. courses which the student has
    missed (not registered at all), failed (registered but not passed)
    or nottaken (registered but not taken).
    """
    grok.name('outstandingcourses')

    fields = ('student_id', 'matric_number', 'certcode', 'display_fullname',
              'missed', 'failed', 'nottaken')
    title = _(u'Outstanding Courses')

    def filter_func(self, x, **kw):
        return get_outstanding(x, **kw)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student's id, fullname and certcode,
        and it collects the lists of outstanding courses.
        """
        if context is not None:
            if name in ('student_id', 'matric_number',
                        'display_fullname', 'certcode'):
                value = getattr(context[0], name, None)
            elif name == 'missed':
                value = ' '.join(context[1])
            elif name == 'failed':
                value = ' '.join(context[2])
            elif name == 'nottaken':
                value = ' '.join(context[3])
        return super(
            OutstandingCoursesExporter, self).mangle_value(
            value, name, context=context)

class UnpaidPaymentsExporter(StudentPaymentExporter):
    """The Unpaid Payments Exporter works just like the
    Student Payment (singular intended) Exporter  but it exports only 
    unpaid tickets. This exporter is designed for finding and finally 
    purging outdated payment tickets.
    """
    grok.name('unpaidpayments')

    title = _(u'Unpaid Payment Tickets')

    def filter_func(self, x, **kw):
        return get_payments(x, p_states=('unpaid',) , **kw)

class DataForBursaryExporter(StudentPaymentExporter):
    """The Data for Bursary Exporter works just like the Student Payment
    Exporter but it exports much more information about the student. It combines
    payment and student data in one table in order to spare postprocessing of 
    two seperate export files. The exporter is primarily used by bursary
    officers who have exclusively access to this exporter. The exporter
    exports ``paid``, ``waived`` and ``scholarship`` payment tickets.
    """
    grok.name('bursary')

    def filter_func(self, x, **kw):
        return get_payments(x, p_states=('paid', 'waived', 'scholarship'), **kw)

    fields = tuple(
        sorted(iface_names(
            IStudentOnlinePayment, exclude_attribs=False,
            omit=['display_item', 'certificate', 'student', 'p_option']))) + (
            'student_id','matric_number','reg_number',
            'firstname', 'middlename', 'lastname','sex',
            'state','current_session',
            'entry_session', 'entry_mode',
            'faccode', 'depcode','certcode')
    title = _(u'Payment Data for Bursary')

    def mangle_value(self, value, name, context=None):
        """The mangler fetches the student data.
        """
        if context is not None:
            student = context.student
            if name in [
                'student_id','matric_number', 'reg_number',
                'firstname', 'middlename', 'lastname','sex',
                'state', 'current_session',
                'entry_session', 'entry_mode',
                'faccode', 'depcode', 'certcode'] and student is not None:
                value = getattr(student, name, None)
        return super(
            StudentPaymentExporter, self).mangle_value(
            value, name, context=context)

class AccommodationPaymentsExporter(DataForBursaryExporter):
    """The Accommodation Payments Exporter works like the Data for Bursary
    Exporter above. The exporter exports ``paid``, ``waived`` and ``scholarship``
    payment tickets with category ``bed_allocation`` or ``hostel_maintenance``.
    The exporter is primarily used by accommodation officers who have
    exclusively access to this exporter.
    """
    grok.name('accommodationpayments')

    def filter_func(self, x, **kw):
        kw['paycat'] = 'bed_allocation'
        payments = get_payments(x, p_states=(
          'paid', 'waived', 'scholarship'), **kw)
        kw['paycat'] = 'hostel_maintenance'
        payments += get_payments(x, p_states=(
          'paid', 'waived', 'scholarship'), **kw)
        return payments

    title = _(u'Accommodation Payments')

class BedTicketExporter(grok.GlobalUtility, StudentExporterBase):
    """The Bed Ticket Exporter first filters the set of students
    by searching the students catalog. Then it exports bed
    tickets by iterating over the items of the student's ``accommodation``
    container.
    """
    grok.name('bedtickets')

    fields = tuple(
        sorted(iface_names(
            IBedTicket, exclude_attribs=False,
            omit=['display_coordinates', 'maint_payment_made']))) + (
            'student_id', 'actual_bed_type')
    title = _(u'Bed Tickets (Data Backup)')

    def filter_func(self, x, **kw):
        return get_bedtickets(x)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student id and the type of the bed
        which has been booked in the ticket.
        """
        if context is not None:
            student = context.student
            if name in ['student_id'] and student is not None:
                value = getattr(student, name, None)
        if name == 'bed' and value is not None:
            value = getattr(value, 'bed_id', None)
        if name == 'actual_bed_type':
            value = getattr(getattr(context, 'bed', None), 'bed_type', None)
        return super(
            BedTicketExporter, self).mangle_value(
            value, name, context=context)

class SchoolFeePaymentsOverviewExporter(StudentExporter):
    """The School Fee Payments Overview Exporter first filters the set of students
    by searching the students catalog. Then it exports some student base data
    together with the total school fee amount paid in each year over a
    predefined year range (current year - 9, ... , current year + 1).
    """
    grok.name('sfpaymentsoverview')

    curr_year = datetime.now().year
    year_range = range(curr_year - 11, curr_year + 1)
    year_range_tuple = tuple([str(year) for year in year_range])
    fields = ('student_id', 'matric_number', 'display_fullname',
        'state', 'certcode', 'faccode', 'depcode', 'is_postgrad',
        'current_level', 'current_session', 'current_mode',
        'entry_session', 'reg_number'
        ) + year_range_tuple
    title = _(u'School Fee Payments Overview')

    def mangle_value(self, value, name, context=None):
        """The mangler summarizes the school fee amounts made per year. It
        iterates over all paid school fee payment tickets and
        adds together the amounts paid in a year. Waived payments
        are marked ``waived`` and scholarship payments marked `scholarship`.
        """
        if name in self.year_range_tuple and context is not None:
            value = 0
            for ticket in context['payments'].values():
                if ticket.p_category == 'schoolfee' and \
                    ticket.p_session == int(name):
                    if ticket.p_state == 'waived':
                        value = 'waived'
                        break
                    if ticket.p_state == 'scholarship':
                        value = 'scholarship'
                        break
                    if ticket.p_state == 'paid':
                        try:
                            value += ticket.amount_auth
                        except TypeError:
                            pass
            if value == 0:
                value = ''
            elif isinstance(value, float):
                value = round(value, 2)
        return super(
            StudentExporter, self).mangle_value(
            value, name, context=context)

class SessionPaymentsOverviewExporter(StudentExporter):
    """The Session Payments Overview Exporter first filters the set of students
    by searching the students catalog. Then it exports some student base data
    together with the total amount paid in predefined payment categories
    over the previous three session (referring to current academic session).
    Sample output:

    header: ``...schoolfee13,schoolfee14,schoolfee15,gown13,gown14,gown15...``

    data: ``...2000.0,,3000.0,,,1000.0,...``

    This csv data string means that the student paid 2000.0 school fee in 2013
    and 3000.0 in 2015. S/He furthermore paid 1000.0 for gown rental in 2015.
    """
    grok.name('sessionpaymentsoverview')

    paycats = ('schoolfee', 'clearance', 'gown', 'transcript')
    regular_fields = ('student_id', 'matric_number', 'display_fullname',
        'state', 'certcode', 'faccode', 'depcode', 'is_postgrad',
        'current_level', 'current_session', 'current_mode',
        'entry_session', 'reg_number'
        )
    title = _(u'Session Payments Overview')

    @property
    def paycatyears(self):
        cas = grok.getSite()['configuration'].current_academic_session
        paycatyears = []
        if cas:
            year_range = range(cas-2, cas+1)
            year_range_tuple = tuple([str(year)[2:] for year in year_range])
            paycatyears = [
                cat+year for cat in self.paycats for year in year_range_tuple]
        return paycatyears

    @property
    def fields(self):
        return self.regular_fields + tuple(self.paycatyears)

    def mangle_value(self, value, name, context=None):
        """
        """
        amounts = dict()
        for catyear in self.paycatyears:
            amounts[catyear] = 0.0
        if name[:-2] in self.paycats and context is not None:
            for ticket in context['payments'].values():
                if ticket.p_category == name[:-2]:
                    if ticket.p_state in ('waived', 'paid'):
                        if str(ticket.p_session)[2:] == name[-2:]:
                            amounts[name] += ticket.amount_auth
            if amounts[name] == 0.0:
                value = ''
            elif isinstance(amounts[name], float):
                value = round(amounts[name], 2)
        return super(
            StudentExporter, self).mangle_value(
            value, name, context=context)

class StudyLevelsOverviewExporter(StudentExporter):
    """The Student Study Levels Overview Exporter first filters the set of
    students by searching the students catalog. Then it exports some student
    base data together with the session key of registered levels.
    Sample output:

    header: ``...100,110,120,200,210,220,300...``

    data: ``...2010,,,2011,2012,,2013...``

    This csv data string means that level 100 was registered in session 
    2010/2011, level 200 in session 2011/2012, level 210 (200 on 1st probation)
    in session 2012/2013 and level 300 in session 2013/2014.
    """
    grok.name('studylevelsoverview')

    avail_levels = tuple([str(x) for x in study_levels(None)])

    fields = ('student_id', ) + (
        'state', 'certcode', 'faccode', 'depcode', 'is_postgrad',
        'entry_session', 'current_level', 'current_session',
        ) + avail_levels
    title = _(u'Study Levels Overview')

    def mangle_value(self, value, name, context=None):
        """The mangler checks if a given level has been registered. It returns
        the ``level_session`` attribute of the student study level object
        if the named level exists.
        """
        if name in self.avail_levels and context is not None:
            value = ''
            for level in context['studycourse'].values():
                if level.level == int(name):
                    value = '%s' % level.level_session
                    break
        return super(
            StudentExporter, self).mangle_value(
            value, name, context=context)

class ComboCardDataExporter(grok.GlobalUtility, StudentExporterBase):
    """Like all other exporters the Combo Card Data Exporter first filters the
    set of students by searching the students catalog. Then it exports some
    student base data which are neccessary to print for the Interswitch combo 
    card (identity card for students). The output contains a ``passport_path``
    column which contains the filesystem path of the passport image file.
    If no path is given, no passport image file exists.
    """
    grok.name('combocard')

    fields = ('display_fullname',
              'student_id','matric_number',
              'certificate', 'faculty', 'department', 'passport_path')
    title = _(u'Combo Card Data')

    def mangle_value(self, value, name, context=None):
        """The mangler determines the titles of faculty, department
        and certificate. It also computes the path of passport image file
        stored in the filesystem.
        """
        certificate = context['studycourse'].certificate
        if name == 'certificate' and certificate is not None:
            value = certificate.title
        if name == 'department' and certificate is not None:
            value = certificate.__parent__.__parent__.longtitle
        if name == 'faculty' and certificate is not None:
            value = certificate.__parent__.__parent__.__parent__.longtitle
        if name == 'passport_path' and certificate is not None:
            file_id = IFileStoreNameChooser(context).chooseName(
                attr='passport.jpg')
            os_path = getUtility(IExtFileStore)._pathFromFileID(file_id)
            if not os.path.exists(os_path):
                value = None
            else:
                value = '/'.join(os_path.split('/')[-4:])
        return super(
            ComboCardDataExporter, self).mangle_value(
            value, name, context=context)

class TranscriptDataExporter(StudentExporter):
    """The Transcript Data Exporter first filters the set of
    students by searching the students catalog. Then it exports student data
    along with their transcript data.
    """
    grok.name('transcriptdata')

    fields = ('student_id', ) + (
        'state', 'certcode', 'faccode', 'depcode',
        'entry_session', 'current_level', 'current_session',
        'transcript_data')
    title = _(u'Transcript Data')

    def mangle_value(self, value, name, context=None):
        """The mangler determines and formats the transcript data.
        """
        if name == 'transcript_data':
            value = {}
            td = context['studycourse'].getTranscriptData()[0]
            for level in td:
                tickets_1 = ','.join(i.code for i in level['tickets_1'])
                tickets_2 = ','.join(i.code for i in level['tickets_2'])
                tickets_3 = ','.join(i.code for i in level['tickets_3'])
                value = "Level %s; 1st: %s; 2nd: %s; 3rd: %s; sgpa: %s" % (
                    level['level_key'], tickets_1, tickets_2,
                    tickets_3, level['sgpa'],
                    )
        return super(
            TranscriptDataExporter, self).mangle_value(
            value, name, context=context)