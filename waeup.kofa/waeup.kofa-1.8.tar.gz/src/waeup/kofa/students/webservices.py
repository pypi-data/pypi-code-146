## $Id: webservices.py 16393 2021-02-04 09:14:47Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
import grok
import os
import xmlrpclib
from time import time
from cStringIO import StringIO
from zope.component import getUtility, queryUtility
from zope.catalog.interfaces import ICatalog
from waeup.kofa.interfaces import (
    IUniversity, IExtFileStore, IFileStoreNameChooser, IKofaUtils,
    GRADUATED, TRANSREL)
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.utils.helpers import get_fileformat, to_timezone
from waeup.kofa.students.catalog import StudentsQuery
from waeup.kofa.students.export import get_payments


def get_student(students, identifier):
    if identifier is None:
        return None
    student = students.get(identifier, None)
    if student is None:
        cat = queryUtility(ICatalog, name='students_catalog')
        results = list(
            cat.searchResults(matric_number=(identifier, identifier)))
        if len(results) == 1:
            student = results[0]
        else:
            results = list(
                cat.searchResults(reg_number=(identifier, identifier)))
            if len(results) == 1:
                student = results[0]
    return student

#class XMLRPCPermission(grok.Permission):
#    """Permission for using XMLRPC functions.
#    """
#    grok.name('waeup.xmlrpc')

#class XMLRPCUsers2(grok.Role):
#    """Usergroup 2
#    """
#    grok.name('waeup.xmlrpcusers2')
#    grok.title('XMLRPC Users Group 2')
#    grok.permissions('waeup.xmlrpc',)


class StudentsXMLRPC(grok.XMLRPC):
    """Student related XMLRPC webservices.

    Please note, that XMLRPC does not support real keyword arguments
    but positional arguments only.
    """

    grok.context(IUniversity)

    @grok.require('waeup.xmlrpc')
    def get_student_id(self, reg_number=None):
        """Get the id of a student with registration number `reg_number`.

        Returns the student id as string if successful, ``None`` else.
        """
        if reg_number is not None:
            cat = getUtility(ICatalog, name='students_catalog')
            result = list(
                cat.searchResults(reg_number=(reg_number, reg_number),
                                  _limit=1))
            if not len(result):
                return None
            return result[0].student_id
        return None

    @grok.require('waeup.xmlrpc')
    def get_courses_by_session(self, identifier=None, session=None):
        """1. What COURSES are registered by student X in session Y?

        """
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            return None
        try:
            session = int(session)
        except (TypeError, ValueError):
            pass
        sessionsearch = True
        if session in (None, ''):
            sessionsearch = False
        studycourse = student['studycourse']
        coursetickets = {}
        for level in studycourse.values():
            if sessionsearch and level.level_session != session:
                continue
            for ct in level.values():
                coursetickets.update(
                    {"%s|%s" % (level.level, ct.code): ct.title})
        if not coursetickets:
            return None
        return coursetickets

    @grok.require('waeup.xmlrpc')
    def get_students_by_course(self, course=None, session=None):
        """2. What STUDENTS registered (student id / matric no)
        for course Z in session Y and did they pay school fee?

        """
        try:
            session = int(session)
        except (TypeError, ValueError):
            pass
        sessionsearch = True
        if session in (None, ''):
            sessionsearch = False
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        if sessionsearch:
            coursetickets = cat.searchResults(
                session=(session, session),
                code=(course, course))
        else:
            coursetickets = cat.searchResults(
                code=(course, course))
        if not coursetickets:
            return None
        hitlist = []
        for c_ticket in coursetickets:
            amount = 0
            for p_ticket in c_ticket.student['payments'].values():
                if p_ticket.p_state == 'paid' and \
                    p_ticket.p_category == 'schoolfee' and \
                    p_ticket.p_session == c_ticket.__parent__.level_session:
                    amount = p_ticket.amount_auth
            hitlist.append((
                c_ticket.student.student_id,
                c_ticket.student.matric_number,
                c_ticket.__parent__.validated_by,
                amount
                ))
        return list(set(hitlist))

    @grok.require('waeup.xmlrpc')
    def get_students_by_department(self, faccode=None, depcode=None,
                                   session=None, level=None):
        """A webservice to pull student's registered courses in a
        department
        """
        try:
            session = int(session)
            level = int(level)
        except (TypeError, ValueError):
            pass
        if session in (None, '',0):
            session= None
        if level in (None, '',0):
            level= None
        try:
            department =self.context['faculties'][faccode][depcode]
        except KeyError:
            return None
        courses = department.courses.keys()
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        hitdict = {}
        for course in courses:
            coursetickets = cat.searchResults(
                session=(session, session),
                level=(level, level),
                code=(course, course))
            for c_ticket in coursetickets:
                if not c_ticket.student.student_id in hitdict.keys():
                    hitdict[c_ticket.student.student_id] = (
                        c_ticket.student.matric_number,
                        c_ticket.student.display_fullname,
                        c_ticket.student.current_session,
                        c_ticket.student.current_level,
                        [c_ticket.code,])
                else:
                    hitdict[c_ticket.student.student_id][4].append(
                        c_ticket.code,)
        return hitdict

    @grok.require('waeup.xmlrpc')
    def get_student_info(self, identifier=None):
        """3a. Who is the student with matriculation number / student id

        """
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            return None
        return [student.display_fullname, student.certcode,
            student.phone, student.email]

    @grok.require('waeup.Public')
    def get_grad_student(self, identifier=None, email=None):
        """Check if student record exist, check email address and
        retrieve registration state.
        """
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            return None
        correct_email = False
        has_graduated = False
        transcript_released = False
        if student.email == email:
            correct_email = True
        if student.state == GRADUATED:
            has_graduated = True
        if student.state == TRANSREL:
            transcript_released = True
        return [correct_email, has_graduated, transcript_released]

    @grok.require('waeup.xmlrpc')
    def get_student_passport(self, identifier=None):
        """3b. Get passport picture of student with
        matriculation number / student id.

        """
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            return None
        img = getUtility(IExtFileStore).getFileByContext(
            student, attr='passport.jpg')
        return xmlrpclib.Binary(img.read())

    @grok.require('waeup.xmlrpc')
    def get_paid_sessions(self, identifier=None):
        """6. Get list of SESSIONS school fees paid by student X.

        """
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            return None
        payments_dict = {}
        for ticket in student['payments'].values():
            if ticket.p_state == 'paid' and \
                ticket.p_category == 'schoolfee':
                payments_dict[str(ticket.p_session)] = ticket.amount_auth
        if not payments_dict:
            return None
        return payments_dict

    @grok.require('waeup.xmlrpc')
    def check_student_credentials(self, username, password):
        """Returns student data if username and password are valid,
        None else.

        We only query the students authenticator plugin in order not
        to mix up with other credentials (admins, staff, etc.).

        All additional checks performed by usual student
        authentication apply. For instance for suspended students we
        won't get a successful response but `None`.

        This method can be used by CAS to authentify students for
        external systems like moodle.
        """
        from zope.pluggableauth.interfaces import IAuthenticatorPlugin
        auth = getUtility(IAuthenticatorPlugin, name='students')
        creds = dict(login=username, password=password)
        principal = auth.authenticateCredentials(creds)
        if principal is None:
            return None
        return dict(email=principal.email, id=principal.id,
                    type=principal.user_type,
                    description=principal.description)

    @grok.require('waeup.xmlrpc')
    def get_student_moodle_data(self, identifier=None):
        """Returns student data to update user data and enroll user
        in Moodle courses.

        """
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            return None
        return dict(email=student.email,
                    firstname=student.firstname,
                    lastname=student.lastname,
                    )

    @grok.require('waeup.putBiometricData')
    def put_student_fingerprints(self, identifier=None, fingerprints={}):
        """Store fingerprint files for student identified by `identifier`.

        `fingerprints` is expected to be a dict with strings
        ``1``..``10`` as keys and binary data as values.

        The keys ``1``..``10`` represent respective fingers: ``1`` is
        the left thumb, ``10`` the little finger of right hand.

        The binary data values are expected to be fingerprint minutiae
        files as created by the libfprint library. With the std python
        `xmlrpclib` client you can create such values with
        `xmlrpclib.Binary(<BINARY_DATA_HERE>)`.

        The following problems will raise errors:

        - Invalid student identifiers (student does not exist or
          unknown format of identifier)

        - Fingerprint files that are not put into a dict.

        - Fingerprint dicts that contain non-FPM files (or otherwise
          invalid .fpm data).

        Returns `True` in case of successful operation (at least one
        fingerprint was stored), `False` otherwise.
        """
        result = False
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            raise xmlrpclib.Fault(
                xmlrpclib.INVALID_METHOD_PARAMS,
                "No such student: '%s'" % identifier)
        if not isinstance(fingerprints, dict):
            raise xmlrpclib.Fault(
                xmlrpclib.INVALID_METHOD_PARAMS,
                "Invalid fingerprint data: must be in dict")
        for str_key, val in fingerprints.items():
            num = 0
            try:
                num = int(str_key)
            except ValueError:
                pass
            if num < 1 or num > 10:
                continue
            if not isinstance(val, xmlrpclib.Binary):
                raise xmlrpclib.Fault(
                    xmlrpclib.INVALID_METHOD_PARAMS,
                    "Invalid data for finger %s" % num)
            fmt = get_fileformat(None, val.data)
            if fmt != 'fpm':
                raise xmlrpclib.Fault(
                    xmlrpclib.INVALID_METHOD_PARAMS,
                    "Invalid file format for finger %s" % num)
            file_store = getUtility(IExtFileStore)
            file_id = IFileStoreNameChooser(student).chooseName(
                attr='finger%s.fpm' % num)
            file_store.createFile(file_id, StringIO(val.data))
            student.writeLogMessage(self, 'fingerprint stored')
            result = True
        return result

    @grok.require('waeup.getBiometricData')
    def get_student_fingerprints(self, identifier=None):
        """Returns student fingerprint data if available.

        Result set is a dictionary with entries for ``email``,
        ``firstname``, ``lastname``, ``img``, ``img_name``, and
        ``fingerprints``.

        Here ``img`` and ``img_name`` represent a photograph of the
        student (binary image data and filename
        respectively).

        ``fingerprints`` is a dictionary itself with possible entries
        ``1`` to ``10``, containing binary minutiae data
        (i.e. fingerprint scans).
        """
        students = self.context['students']
        student = get_student(students, identifier)
        if student is None:
            return dict()
        result = dict(
            email=student.email,
            firstname=student.firstname,
            lastname=student.lastname,
            fingerprints={},
            img_name=None,
            img=None,
            )
        file_store = getUtility(IExtFileStore)
        img = file_store.getFileByContext(student, attr='passport.jpg')
        if img is not None:
            result.update(
                img=xmlrpclib.Binary(img.read()),
                img_name=os.path.basename(img.name))

        for num in [str(x + 1) for x in range(10)]:
            fp_file = file_store.getFileByContext(
                student, attr='finger%s.fpm' % num)
            if fp_file is not None:
                result['fingerprints'][num] = xmlrpclib.Binary(fp_file.read())
        return result

    @grok.require('waeup.xmlrpc')
    def get_bursary_data(self,
            current_session=None, current_level=None, certcode=None,
            current_mode=None, depcode=None, p_session=None):
        """Returns bursary data of a subset of students.
        """
        if not current_session:
            current_session = None
        if not current_level:
            current_level = None
        if not depcode:
            depcode = None
        if not certcode:
            certcode = None
        if not current_mode:
            current_mode = None
        hitlist = []
        cat = queryUtility(ICatalog, name='students_catalog')
        results = list(
            cat.searchResults(
                current_session=(current_session, current_session),
                current_level=(current_level, current_level),
                certcode=(certcode, certcode),
                current_mode=(current_mode, current_mode),
                depcode=(depcode, depcode),
                ))
        payments = get_payments(results, paysession=p_session)
        tz = getUtility(IKofaUtils).tzinfo
        for payment in payments:
            hitlist.append(dict(
                student_id=payment.student.student_id,
                matric_number=payment.student.matric_number,
                reg_number=payment.student.reg_number,
                firstname=payment.student.firstname,
                middlename=payment.student.middlename,
                lastname=payment.student.lastname,
                state=payment.student.state,
                current_session=payment.student.current_session,
                entry_session=payment.student.entry_session,
                entry_mode=payment.student.entry_mode,
                faccode=payment.student.faccode,
                depcode=payment.student.depcode,
                certcode=payment.student.certcode,
                p_id=payment.p_id,
                amount_auth=payment.amount_auth,
                p_category=payment.p_category,
                display_item=payment.display_item,
                p_session=payment.p_session,
                p_state=payment.p_state,
                creation_date=str('%s#' % to_timezone(
                    payment.creation_date, tz)),
                payment_date=str('%s#' % to_timezone(
                    payment.payment_date, tz)),
                )
              )
        return hitlist

    @grok.require('waeup.xmlrpc')
    def get_payment(self, p_id='non_existent'):
        """Returns payment and payer data of payment tickets with specific p_id.
        """
        cat = getUtility(ICatalog, name='payments_catalog')
        result = list(cat.searchResults(p_id=(p_id, p_id)))
        if not len(result):
            return None
        payment =  result[0]
        return dict(
                p_id=payment.p_id,
                amount_auth=payment.amount_auth,
                p_category=payment.p_category,
                display_item=payment.display_item,
                p_session=payment.p_session,
                p_state=payment.p_state,
                r_company=getattr(payment, 'r_company', None),
                id = IPayer(payment).id,
                matric_number = IPayer(payment).matric_number,
                fullname = IPayer(payment).display_fullname,
                )

    @grok.require('waeup.xmlrpc')
    def get_unpaid_payments(self, days=3, company=None):
        """Returns the payment and payer data of unpaid payment
        tickets which have been created during the past days.
        """
        days_in_seconds = 86400 * int(days)
        timestamp_now = ("%d" % int(time()*10000))[1:]
        timestamp_now_minus_days = ("%d" % int((time()-days_in_seconds)*10000))[1:]
        p_id_now = ("p%s" % timestamp_now)
        p_id_minus_days = ("p%s" % timestamp_now_minus_days)
        cat = getUtility(ICatalog, name='payments_catalog')
        payments = list(
            cat.searchResults(p_id=(p_id_minus_days, p_id_now),
                              p_state=('unpaid', 'unpaid')))
        payments += list(
            cat.searchResults(p_id=(p_id_minus_days, p_id_now),
                              p_state=('failed', 'failed')))
        hitlist = []
        if company:
            for payment in payments:
                if company == getattr(payment, 'r_company', None):
                    hitlist.append(dict(
                        p_id=payment.p_id,
                        amount_auth=payment.amount_auth,
                        p_category=payment.p_category,
                        display_item=payment.display_item,
                        p_session=payment.p_session,
                        p_state=payment.p_state,
                        r_company=getattr(payment, 'r_company', None),
                        id = IPayer(payment).id,
                        matric_number = IPayer(payment).matric_number,
                        fullname = IPayer(payment).display_fullname,
                        )
                      )
            return hitlist
        for payment in payments:
            hitlist.append(dict(
                p_id=payment.p_id,
                amount_auth=payment.amount_auth,
                p_category=payment.p_category,
                display_item=payment.display_item,
                p_session=payment.p_session,
                p_state=payment.p_state,
                r_company=getattr(payment, 'r_company', None),
                id = IPayer(payment).id,
                matric_number = IPayer(payment).matric_number,
                fullname = IPayer(payment).display_fullname,
                )
              )
        return hitlist
