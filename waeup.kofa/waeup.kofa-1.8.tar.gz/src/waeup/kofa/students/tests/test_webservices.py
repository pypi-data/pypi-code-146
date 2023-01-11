# Tests for webservices
import xmlrpclib
import os
from time import time
from cStringIO import StringIO
from zope.app.testing.xmlrpc import ServerProxy
from zope.component import getUtility, createObject
from waeup.kofa.interfaces import (
    IExtFileStore, IFileStoreNameChooser, IKofaUtils)
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.utils.helpers import to_timezone
from waeup.kofa.students.payments import StudentOnlinePayment
from waeup.kofa.students.tests.test_browser import StudentsFullSetup
from waeup.kofa.students.studylevel import StudentStudyLevel, CourseTicket


class XMLRPCTests(StudentsFullSetup):

    layer = FunctionalLayer

    def setup_student(self, student):
        study_level = StudentStudyLevel()
        study_level.level_session = 2012
        study_level.level_verdict = "A"
        study_level.level = 100
        study_level.validated_by = u"my adviser"
        student['studycourse'].addStudentStudyLevel(
            self.certificate, study_level)

        ticket = CourseTicket()
        ticket.automatic = True
        ticket.carry_over = True
        ticket.code = u'CRS1'
        ticket.title = u'Course 1'
        ticket.fcode = u'fac1'
        ticket.dcode = u'dep1'
        ticket.credits = 100
        ticket.passmark = 100
        ticket.semester = 2
        study_level[ticket.code] = ticket

    def create_passport_img(self, student):
        # create some passport file for `student`
        storage = getUtility(IExtFileStore)
        image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        self.image_contents = open(image_path, 'rb').read()
        file_id = IFileStoreNameChooser(student).chooseName(
            attr='passport.jpg')
        storage.createFile(file_id, StringIO(self.image_contents))

    def create_fpm_file(self, student, finger_num):
        # create some .fpm file for `student` finger `finger_num`
        storage = getUtility(IExtFileStore)
        file_id = IFileStoreNameChooser(student).chooseName(
            attr='%s.fpm' % finger_num)
        storage.createFile(file_id, StringIO('FP1FakedMintiaeFile1'))

    def XMLRPC_post(self, body):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.addHeader('Content-Length', len(body))
        self.browser.post('http://localhost/app', body,
            'text/xml; charset=utf-8')
        return self.browser.contents

    def test_get_student_id_no_match(self):
        # w/o any students we get none
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        result = server.get_student_id('Nonsense')
        self.assertTrue(result is None)
        return

    def test_get_student_id_regno_exists(self):
        # we can get the id of an existing student with matching reg_no
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        result = server.get_student_id('123')
        self.assertEqual(result, 'K1000000')
        self.assertEqual(self.student_id, result)
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_student_id</methodName>
<params>
<param>
<value><string>123</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><string>K1000000</string></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_get_student_id_block_unauthorized(self):
        # requests from unauthorized users are blocked
        # no username nor password
        server = ServerProxy('http://localhost/app')
        self.assertRaises(
            xmlrpclib.ProtocolError, server.get_student_id, '123')
        # wrong password
        server = ServerProxy('http://mgr:WRONGPW@localhost/app')
        self.assertRaises(
            xmlrpclib.ProtocolError, server.get_student_id, '123')
        # wrong username
        server = ServerProxy('http://WRONGUSER:mgrpw@localhost/app')
        self.assertRaises(
            xmlrpclib.ProtocolError, server.get_student_id, '123')
        return

    def test_get_courses_by_session(self):
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        result = server.get_courses_by_session('K1000000')
        self.assertEqual(result, None)
        self.setup_student(self.student)
        result = server.get_courses_by_session('K1000000', '2010')
        self.assertEqual(result, None)
        result = server.get_courses_by_session('K1000000', '2012')
        self.assertEqual(result,
            {'100|CRS1': 'Course 1', '100|COURSE1': 'Unnamed Course'})
        result = server.get_courses_by_session('K1000000')
        self.assertEqual(result,
            {'100|CRS1': 'Course 1', '100|COURSE1': 'Unnamed Course'})
        # Also matric_number ...
        result = server.get_courses_by_session('234')
        self.assertEqual(result,
            {'100|CRS1': 'Course 1', '100|COURSE1': 'Unnamed Course'})
        # ... or reg_number can be used.
        result = server.get_courses_by_session('123')
        self.assertEqual(result,
            {'100|CRS1': 'Course 1', '100|COURSE1': 'Unnamed Course'})
        result = server.get_courses_by_session('Nonsense')
        self.assertEqual(result, None)
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_courses_by_session</methodName>
<params>
<param>
<value><string>K1000000</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><struct>
<member>
<name>100|CRS1</name>
<value><string>Course 1</string></value>
</member>
<member>
<name>100|COURSE1</name>
<value><string>Unnamed Course</string></value>
</member>
</struct></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_get_students_by_course(self):
        self.setup_student(self.student)
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        result = server.get_students_by_course('CRS1', '2010')
        self.assertEqual(result, None)
        result = server.get_students_by_course('CRS1', '2012')
        self.assertEqual(result, [['K1000000', '234', 'my adviser', 0], ])
        result = server.get_students_by_course('CRS1')
        self.assertEqual(result, [['K1000000', '234', 'my adviser', 0], ])
        payment = StudentOnlinePayment()
        payment.p_id = 'my-id'
        payment.p_session = 2012
        payment.amount_auth = 12.12
        payment.p_state = u'paid'
        payment.p_category = u'schoolfee'
        self.student['payments']['my-payment'] = payment
        result = server.get_students_by_course('CRS1')
        self.assertEqual(result, [['K1000000', '234', 'my adviser', 12.12], ])
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_students_by_course</methodName>
<params>
<param>
<value><string>CRS1</string></value>
<value><string>2012</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><array><data>
<value><array><data>
<value><string>K1000000</string></value>
<value><string>234</string></value>
<value><string>my adviser</string></value>
<value><double>12.12</double></value>
</data></array></value>
</data></array></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_get_students_by_department(self):
        self.course2 = createObject('waeup.Course')
        self.course2.code = 'COURSE2'
        self.app['faculties']['fac1']['dep1'].courses.addCourse(
            self.course2)
        self.setup_student(self.student)
        ticket = CourseTicket()
        ticket.code = u'COURSE2'
        ticket.title = u'Course 2'
        ticket.fcode = u'fac1'
        ticket.dcode = u'fac1'
        self.student['studycourse']['100'][ticket.code] = ticket
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        result = server.get_students_by_department('fac1','dep1', '2011')
        self.assertEqual(result, {})
        result = server.get_students_by_department('fac1','dep1', '2012', '200')
        self.assertEqual(result, {})
        result = server.get_students_by_department('fac1','dep1', '2012', '100')
        self.assertEqual(
            result, {'K1000000': [
            '234', 'Anna Tester', 2004, 100, ['COURSE1', 'COURSE2']]})
        result = server.get_students_by_department('fac1','dep1', '0', '100')
        self.assertEqual(
            result, {'K1000000': [
            '234', 'Anna Tester', 2004, 100, ['COURSE1', 'COURSE2']]})
        result = server.get_students_by_department('fac1','dep1')
        self.assertEqual(
            result, {'K1000000': [
            '234', 'Anna Tester', 2004, 100, ['COURSE1', 'COURSE2']]})
        result = server.get_students_by_department('fac1','dep2')
        self.assertEqual(result, None)
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_students_by_department</methodName>
<params>
<param>
<value><string>fac1</string></value>
<value><string>dep1</string></value>
<value><int>0</int></value>
<value><int>100</int></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><struct>
<member>
<name>K1000000</name>
<value><array><data>
<value><string>234</string></value>
<value><string>Anna Tester</string></value>
<value><int>2004</int></value>
<value><int>100</int></value>
<value><array><data>
<value><string>COURSE1</string></value>
<value><string>COURSE2</string></value>
</data></array></value>
</data></array></value>
</member>
</struct></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_get_student_info(self):
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        result = server.get_student_info('123')
        self.assertEqual(result,
            ['Anna Tester', 'CERT1', '1234', 'aa@aa.ng'])
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_student_info</methodName>
<params>
<param>
<value><string>K1000000</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><array><data>
<value><string>Anna Tester</string></value>
<value><string>CERT1</string></value>
<value><string>1234</string></value>
<value><string>aa@aa.ng</string></value>
</data></array></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_get_grad_student(self):
        server = ServerProxy('http://localhost/app')
        self.setup_student(self.student)
        result = server.get_grad_student('123', 'aa@aa.ng')
        self.assertEqual(result,
            [True, False, False])
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_grad_student</methodName>
<params>
<param>
<value><string>K1000000</string></value>
</param>
<param>
<value><string>aa@aa.ng</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><array><data>
<value><boolean>1</boolean></value>
<value><boolean>0</boolean></value>
<value><boolean>0</boolean></value>
</data></array></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_get_student_passport(self):
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        self.create_passport_img(self.student)
        result = server.get_student_passport('123')
        img = getUtility(IExtFileStore).getFileByContext(
            self.student, attr='passport.jpg')
        binary = img.read()
        self.assertEqual(binary, result)
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_student_passport</methodName>
<params>
<param>
<value><string>K1000000</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><base64>
/9j/4AAQSkZJRgABAgAAZABkAAD/7AARRHVja3kAAQAEAAAAPAAA/+4ADkFkb2JlAGTAAAAAAf/b
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertTrue(xmlout.startswith(RESPONSE_XML))

    def test_get_paid_sessions(self):
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        payment = StudentOnlinePayment()
        payment.p_id = 'my-id'
        payment.p_session = 2009
        payment.amount_auth = 12.12
        payment.p_state = u'paid'
        payment.p_category = u'schoolfee'
        self.student['payments']['my-payment'] = payment
        result = server.get_paid_sessions('123')
        self.assertEqual(result, {'2009': 12.12})
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_paid_sessions</methodName>
<params>
<param>
<value><string>K1000000</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><struct>
<member>
<name>2009</name>
<value><double>12.12</double></value>
</member>
</struct></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_check_student_credentials(self):
        # make sure we can get student infos providing valid creds
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        stud_id = self.student.student_id
        result = server.check_student_credentials(stud_id, 'spwd')
        self.assertEqual(
            result, {
                'description': 'Anna Tester',
                'email': 'aa@aa.ng',
                'id': 'K1000000',
                'type': 'student'}
            )
        return

    def test_get_student_moodle_data(self):
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        result = server.get_student_moodle_data(self.student.student_id)
        self.assertEqual(result,
            {'lastname': 'Tester', 'email': 'aa@aa.ng', 'firstname': 'Anna'})
        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_student_moodle_data</methodName>
<params>
<param>
<value><string>K1000000</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><struct>
<member>
<name>lastname</name>
<value><string>Tester</string></value>
</member>
<member>
<name>email</name>
<value><string>aa@aa.ng</string></value>
</member>
<member>
<name>firstname</name>
<value><string>Anna</string></value>
</member>
</struct></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_put_student_fingerprints_no_stud(self):
        # invalid student ids will result in `False`
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.assertRaises(
            xmlrpclib.Fault, server.put_student_fingerprints,
            'invalid id', {})

    def test_put_student_fingerprints_non_dict(self):
        # fingerprints must be passed in in a dict
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        self.assertRaises(
            xmlrpclib.Fault, server.put_student_fingerprints,
            self.student.student_id, 'not-a-dict')

    def test_put_student_fingerprints_non_num_keys_ignored(self):
        # non-numeric keys in fingerprint dict are ignored
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        result = server.put_student_fingerprints(
            self.student.student_id, {'not-a-num': 'foo',
                                      '12.2': 'bar',
                                      '123': 'baz'})
        self.assertEqual(result, False)

    def test_put_student_fingerprints_non_fpm_data(self):
        # we cannot pass non-.fpm files as values
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        self.assertRaises(
            xmlrpclib.Fault, server.put_student_fingerprints,
            self.student.student_id, {'1': 'not-a-fingerprint'})

    def test_put_student_fingerprints_invalid_file_format(self):
        # invalid files will result in `False`
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        invalid_fpm = xmlrpclib.Binary('invalid file')
        self.assertRaises(
            xmlrpclib.Fault, server.put_student_fingerprints,
            self.student.student_id, {'1': invalid_fpm})

    def test_put_student_fingerprints(self):
        # we can store fingerprints
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        fpm = xmlrpclib.Binary('FP1faked_fpm')
        result = server.put_student_fingerprints(
            self.student.student_id, {'1': fpm})
        self.assertEqual(result, True)
        stored_file = getUtility(IExtFileStore).getFileByContext(
            self.student, attr="finger1.fpm")
        self.assertEqual(stored_file.read(), 'FP1faked_fpm')
        # storing is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - grok.meta.StudentsXMLRPC '
            '- K1000000 - fingerprint stored' in logcontent)

    def test_put_student_fingerprints_existing(self):
        # existing fingerprints are overwritten
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        self.create_fpm_file(self.student, '1')
        fpm1 = xmlrpclib.Binary('FP1faked_fpm1')
        fpm2 = xmlrpclib.Binary('FP1faked_fpm2')
        result = server.put_student_fingerprints(
            self.student.student_id, {'1': fpm1, '3': fpm2})
        self.assertEqual(result, True)
        stored_file1 = getUtility(IExtFileStore).getFileByContext(
            self.student, attr="finger1.fpm")
        stored_file2 = getUtility(IExtFileStore).getFileByContext(
            self.student, attr="finger3.fpm")
        self.assertEqual(stored_file1.read(), 'FP1faked_fpm1')
        self.assertEqual(stored_file2.read(), 'FP1faked_fpm2')

    def test_get_student_fingerprints_no_stud(self):
        # invalid student ids result in empty dict
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        result = server.get_student_fingerprints('invalid id')
        self.assertEqual(result, {})

    def test_get_student_fingerprints_no_files(self):
        # we get student data, but no fingerprints if not stored before
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        result = server.get_student_fingerprints(self.student.student_id)
        self.assertEqual(
            result,
            {'lastname': 'Tester',
             'email': 'aa@aa.ng',
             'firstname': 'Anna',
             'fingerprints': {},
             'img': None,
             'img_name': None,
             })

    def test_get_student_fingerprints_passport(self):
        # we get a photograph of the student if avail.
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        self.create_passport_img(self.student)
        result = server.get_student_fingerprints(self.student.student_id)
        self.assertTrue(
            isinstance(result['img'], xmlrpclib.Binary))
        self.assertEqual(result['img_name'], 'passport_K1000000.jpg')

    def test_get_student_fingerprints_fpm(self):
        # we get minutiae files if any are avail.
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_student(self.student)
        self.create_fpm_file(self.student, 'finger1')
        result = server.get_student_fingerprints(self.student.student_id)
        self.assertTrue('1' in result['fingerprints'].keys())
        self.assertTrue(
            isinstance(result['fingerprints']['1'], xmlrpclib.Binary))

    def test_get_student_fingerprints_block_unauthorized(self):
        # requests from unauthorized users are blocked
        # no username nor password
        server = ServerProxy('http://localhost/app')
        self.setup_student(self.student)
        stud_id = self.student.student_id
        self.assertRaises(
            xmlrpclib.ProtocolError, server.get_student_id, stud_id)
        # wrong password
        server = ServerProxy('http://mgr:WRONGPW@localhost/app')
        self.assertRaises(
            xmlrpclib.ProtocolError, server.get_student_id, stud_id)
        # wrong username
        server = ServerProxy('http://WRONGUSER:mgrpw@localhost/app')
        self.assertRaises(
            xmlrpclib.ProtocolError, server.get_student_id, stud_id)
        return

    def test_get_bursary_data(self):
        tz = getUtility(IKofaUtils).tzinfo
        payment1 = StudentOnlinePayment()
        payment1.p_id = 'my-id1'
        payment1.p_session = 2012
        payment1.amount_auth = 12.12
        payment1.p_state = u'paid'
        payment1.p_category = u'schoolfee'
        self.student['payments']['my-payment1'] = payment1
        payment2 = StudentOnlinePayment()
        payment2.p_id = 'my-id2'
        payment2.p_session = 2012
        payment2.amount_auth = 12.12
        payment2.p_state = u'paid'
        payment2.p_category = u'clearance'
        self.student['payments']['my-payment2'] = payment2
        server = ServerProxy('http://mgr:mgrpw@localhost/app', allow_none=True)
        result = server.get_bursary_data(None,None,None,None,'dep1',2012)
        self.assertEqual(
            result,[
            {'entry_mode': None, 'reg_number': '123', 'display_item': None,
                'firstname': 'Anna', 'payment_date': 'None#',
                'middlename': None, 'student_id': 'K1000000', 'p_id':
                'my-id1', 'certcode': 'CERT1', 'entry_session': 2004,
                'creation_date': str('%s#' % to_timezone(payment1.creation_date, tz)),
                'state': 'created', 'current_session': 2004,
                'faccode': 'fac1', 'lastname': 'Tester',
                'p_category': 'schoolfee', 'amount_auth': 12.12,
                'p_state': 'paid', 'p_session': 2012, 'matric_number': '234',
                'depcode': 'dep1'},
            {'entry_mode': None, 'reg_number': '123', 'display_item': None,
                'firstname': 'Anna', 'payment_date': 'None#',
                'middlename': None, 'student_id': 'K1000000',
                'p_id': 'my-id2', 'certcode': 'CERT1', 'entry_session': 2004,
                'creation_date': str('%s#' % to_timezone(payment2.creation_date, tz)),
                'state': 'created', 'current_session': 2004, 'faccode': 'fac1',
                'lastname': 'Tester', 'p_category': 'clearance',
                'amount_auth': 12.12, 'p_state': 'paid', 'p_session': 2012,
                'matric_number': '234', 'depcode': 'dep1'}
            ]
            )

        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_bursary_data</methodName>
<params>
<param>
<value><string></string></value>
<value><string></string></value>
<value><string></string></value>
<value><string></string></value>
<value><string>dep1</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><array><data>
<value><struct>
<member>
<name>entry_mode</name>
<value><nil/></value></member>
<member>
<name>reg_number</name>
<value><string>123</string></value>
</member>
<member>
<name>display_item</name>
<value><nil/></value></member>
<member>
<name>firstname</name>
<value><string>Anna</string></value>
</member>
<member>
<name>payment_date</name>
<value><string>None#</string></value>
</member>
<member>
<name>middlename</name>
<value><nil/></value></member>
<member>
<name>student_id</name>
<value><string>K1000000</string></value>
</member>
<member>
<name>p_id</name>
<value><string>my-id1</string></value>
</member>
<member>
<name>certcode</name>
<value><string>CERT1</string></value>
</member>
<member>
<name>creation_date</name>
<value><string>%s</string></value>
</member>
<member>
<name>matric_number</name>
<value><string>234</string></value>
</member>
<member>
<name>state</name>
<value><string>created</string></value>
</member>
<member>
<name>lastname</name>
<value><string>Tester</string></value>
</member>
<member>
<name>current_session</name>
<value><int>2004</int></value>
</member>
<member>
<name>faccode</name>
<value><string>fac1</string></value>
</member>
<member>
<name>entry_session</name>
<value><int>2004</int></value>
</member>
<member>
<name>p_category</name>
<value><string>schoolfee</string></value>
</member>
<member>
<name>amount_auth</name>
<value><double>12.12</double></value>
</member>
<member>
<name>p_session</name>
<value><int>2012</int></value>
</member>
<member>
<name>p_state</name>
<value><string>paid</string></value>
</member>
<member>
<name>depcode</name>
<value><string>dep1</string></value>
</member>
</struct></value>
<value><struct>
<member>
<name>entry_mode</name>
<value><nil/></value></member>
<member>
<name>reg_number</name>
<value><string>123</string></value>
</member>
<member>
<name>display_item</name>
<value><nil/></value></member>
<member>
<name>firstname</name>
<value><string>Anna</string></value>
</member>
<member>
<name>payment_date</name>
<value><string>None#</string></value>
</member>
<member>
<name>middlename</name>
<value><nil/></value></member>
<member>
<name>student_id</name>
<value><string>K1000000</string></value>
</member>
<member>
<name>p_id</name>
<value><string>my-id2</string></value>
</member>
<member>
<name>certcode</name>
<value><string>CERT1</string></value>
</member>
<member>
<name>creation_date</name>
<value><string>%s</string></value>
</member>
<member>
<name>matric_number</name>
<value><string>234</string></value>
</member>
<member>
<name>state</name>
<value><string>created</string></value>
</member>
<member>
<name>lastname</name>
<value><string>Tester</string></value>
</member>
<member>
<name>current_session</name>
<value><int>2004</int></value>
</member>
<member>
<name>faccode</name>
<value><string>fac1</string></value>
</member>
<member>
<name>entry_session</name>
<value><int>2004</int></value>
</member>
<member>
<name>p_category</name>
<value><string>clearance</string></value>
</member>
<member>
<name>amount_auth</name>
<value><double>12.12</double></value>
</member>
<member>
<name>p_session</name>
<value><int>2012</int></value>
</member>
<member>
<name>p_state</name>
<value><string>paid</string></value>
</member>
<member>
<name>depcode</name>
<value><string>dep1</string></value>
</member>
</struct></value>
</data></array></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        response = RESPONSE_XML % (str('%s#' % to_timezone(payment1.creation_date, tz)),
                                   str('%s#' % to_timezone(payment2.creation_date, tz))
                                   )
        self.assertEqual(xmlout, response)
        return

    def test_get_payment(self):
        payment1 = StudentOnlinePayment()
        payment1.p_id = 'my-id1'
        payment1.p_session = 2012
        payment1.amount_auth = 12.12
        payment1.p_state = u'failed'
        payment1.p_category = u'schoolfee'
        payment1.r_company = u'xyz'
        self.student['payments']['my-payment1'] = payment1
        server = ServerProxy('http://mgr:mgrpw@localhost/app', allow_none=True)
        results = server.get_payment()
        self.assertEqual(results, None)
        results = server.get_payment('nonsense')
        self.assertEqual(results, None)
        results = server.get_payment('my-id1')
        self.assertEqual(
            results,
                {'display_item': None,
                'p_id': 'my-id1',
                'p_category': 'schoolfee',
                'amount_auth': 12.12, 'p_session': 2012,
                'p_state': 'failed',
                'r_company': 'xyz',
                'fullname': 'Anna Tester',
                'id': 'K1000000',
                'matric_number': '234'}
                )

        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_payment</methodName>
<params>
<param>
<value><string>my-id1</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><struct>
<member>
<name>display_item</name>
<value><nil/></value></member>
<member>
<name>amount_auth</name>
<value><double>12.12</double></value>
</member>
<member>
<name>p_id</name>
<value><string>my-id1</string></value>
</member>
<member>
<name>r_company</name>
<value><string>xyz</string></value>
</member>
<member>
<name>matric_number</name>
<value><string>234</string></value>
</member>
<member>
<name>p_category</name>
<value><string>schoolfee</string></value>
</member>
<member>
<name>fullname</name>
<value><string>Anna Tester</string></value>
</member>
<member>
<name>p_state</name>
<value><string>failed</string></value>
</member>
<member>
<name>p_session</name>
<value><int>2012</int></value>
</member>
<member>
<name>id</name>
<value><string>K1000000</string></value>
</member>
</struct></value>
</param>
</params>
</methodResponse>
"""
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return

    def test_get_unpaid_payments(self):
        timestamp1 = ("%d" % int((time()-10)*10000))[1:]
        timestamp2 = ("%d" % int((time()-5)*10000))[1:]
        timestamp3 = ("%d" % int((time()-(3*86400))*10000))[1:]
        p_id_1 = ("p%s" % timestamp1)
        p_id_2 = ("p%s" % timestamp2)
        p_id_3 = ("p%s" % timestamp3)
        payment1 = StudentOnlinePayment()
        payment1.p_id = p_id_1
        payment1.p_session = 2012
        payment1.amount_auth = 12.12
        payment1.p_state = u'failed'
        payment1.p_category = u'schoolfee'
        payment1.r_company = u'xyz'
        self.student['payments']['my-payment1'] = payment1
        payment2 = StudentOnlinePayment()
        payment2.p_id = p_id_2
        payment2.p_session = 2012
        payment2.amount_auth = 12.12
        payment2.p_state = u'paid'
        payment2.p_category = u'clearance'
        self.student['payments']['my-payment2'] = payment2
        payment3 = StudentOnlinePayment()
        payment3.p_id = p_id_3
        payment3.p_session = 2012
        payment3.amount_auth = 12.12
        payment3.p_state = u'unpaid'
        payment3.p_category = u'schoolfee'
        self.student['payments']['my-payment3'] = payment3
        server = ServerProxy('http://mgr:mgrpw@localhost/app', allow_none=True)
        results = server.get_unpaid_payments(1)
        self.assertEqual(
            results,[
                {'display_item': None,
                'p_id': '%s' % p_id_1,
                'p_category': 'schoolfee',
                'amount_auth': 12.12, 'p_session': 2012,
                'p_state': 'failed',
                'r_company': 'xyz',
                'fullname': 'Anna Tester',
                'id': 'K1000000',
                'matric_number': '234'}
                ])
        results = server.get_unpaid_payments(4)
        self.assertEqual(
            results,[
                {'display_item': None,
                  'p_id': '%s' % p_id_3,
                  'p_category': 'schoolfee',
                  'amount_auth': 12.12,
                  'p_session': 2012,
                  'p_state': 'unpaid',
                  'r_company': None,
                  'fullname': 'Anna Tester',
                  'id': 'K1000000',
                  'matric_number': '234'},
                {'display_item': None,
                  'p_id': '%s' % p_id_1,
                  'p_category': 'schoolfee',
                  'amount_auth': 12.12,
                  'p_session': 2012,
                  'p_state': 'failed',
                  'r_company': 'xyz',
                  'fullname': 'Anna Tester',
                  'id': 'K1000000',
                  'matric_number': '234'},
                ])
        results = server.get_unpaid_payments(4,'xyz')
        self.assertEqual(
            results,[
                {'display_item': None,
                  'p_id': '%s' % p_id_1,
                  'p_category': 'schoolfee',
                  'amount_auth': 12.12,
                  'p_session': 2012,
                  'p_state': 'failed',
                  'r_company': 'xyz',
                  'fullname': 'Anna Tester',
                  'id': 'K1000000',
                  'matric_number': '234'},
                ])

        REQUEST_XML = """\
<?xml version="1.0"?>
<methodCall>
<methodName>get_unpaid_payments</methodName>
<params>
<param>
<value><string>1</string></value>
</param>
</params>
</methodCall>"""
        RESPONSE_XML = """\
<?xml version='1.0'?>
<methodResponse>
<params>
<param>
<value><array><data>
<value><struct>
<member>
<name>display_item</name>
<value><nil/></value></member>
<member>
<name>amount_auth</name>
<value><double>12.12</double></value>
</member>
<member>
<name>p_id</name>
<value><string>%s</string></value>
</member>
<member>
<name>r_company</name>
<value><string>xyz</string></value>
</member>
<member>
<name>matric_number</name>
<value><string>234</string></value>
</member>
<member>
<name>p_category</name>
<value><string>schoolfee</string></value>
</member>
<member>
<name>fullname</name>
<value><string>Anna Tester</string></value>
</member>
<member>
<name>p_state</name>
<value><string>failed</string></value>
</member>
<member>
<name>p_session</name>
<value><int>2012</int></value>
</member>
<member>
<name>id</name>
<value><string>K1000000</string></value>
</member>
</struct></value>
</data></array></value>
</param>
</params>
</methodResponse>
""" % p_id_1
        xmlout = self.XMLRPC_post(REQUEST_XML)
        self.assertEqual(xmlout, RESPONSE_XML)
        return