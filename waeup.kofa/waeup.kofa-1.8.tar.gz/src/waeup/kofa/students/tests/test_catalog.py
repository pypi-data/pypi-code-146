## $Id: test_catalog.py 14115 2016-08-23 08:54:40Z henrik $
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
import grok
import shutil
import tempfile
from zope.event import notify
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, createObject
from zope.component.hooks import setSite
from waeup.kofa.app import University
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.students.student import Student
from waeup.kofa.students.studylevel import StudentStudyLevel, CourseTicket
from waeup.kofa.university.faculty import Faculty
from waeup.kofa.university.department import Department

class CatalogTestSetup(FunctionalTestCase):
    # A setup for testing catalog related stuff.
    #
    # sets up a site with some student already created.
    layer = FunctionalLayer

    def create_cert(self, facname, deptname, certname):
        # helper: create faculty, dept, and cert
        self.app['faculties'][facname] = Faculty(code=facname)
        self.app['faculties'][facname][deptname] = Department(code=deptname)
        cert = createObject('waeup.Certificate')
        cert.start_level = 100
        cert.end_level = 500
        cert.code = certname
        self.app['faculties'][facname][deptname].certificates.addCertificate(
            cert)
        return cert

    def setUp(self):
        super(CatalogTestSetup, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(self.app)
        self.certificate = self.create_cert(u'fac1', u'dep1', u'CERT1')
        self.certificate.study_mode = u'ug_ft'

        # Create student with subobjects
        student = Student()
        student.firstname = u'Bob'
        student.lastname = u'Tester'
        student.matric_number = u'1234'
        self.app['students'].addStudent(student)
        self.student_id = student.student_id
        self.student = self.app['students'][self.student_id]
        self.student['studycourse'].certificate = self.certificate
        self.student['studycourse'].current_session = 2010
        self.student['studycourse'].current_level = 100
        # Update the students_catalog
        notify(grok.ObjectModifiedEvent(self.student))
        studylevel = createObject('waeup.StudentStudyLevel')
        studylevel.level = 100
        studylevel.level_session = 2010
        self.student['studycourse']['100'] = studylevel
        ticket = createObject('waeup.CourseTicket')
        ticket.code = 'Course1'
        ticket.credits = 30
        ticket.score = 70
        self.student['studycourse']['100']['Course1'] = ticket
        payment = createObject(u'waeup.StudentOnlinePayment')
        payment.p_id = 'p1234567890'
        payment.p_item = u'any item'
        payment.p_session = 2010
        payment.p_category = 'schoolfee'
        payment.amount_auth = 12345.678
        payment.p_state = 'paid'
        self.student['payments'][payment.p_id] = payment
        return

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(CatalogTestSetup, self).tearDown()
        return

class StudentCatalogTests(CatalogTestSetup):

    layer = FunctionalLayer

    def test_get_catalog(self):
        # We can get an students catalog if we wish
        cat = queryUtility(ICatalog, name='students_catalog')
        assert cat is not None

    def test_search_by_id(self):
        # We can find a certain student id
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(student_id=(self.student_id,
                                                self.student_id))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]

    def test_search_by_name(self):
        # We can find a certain name
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(fullname='Bob Tester')
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]

    def test_search_by_department(self):
        # We can find a student studying in a certain department
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(depcode=('dep1','dep1'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]

    def test_search_by_faculty(self):
        # We can find a student studying in a certain faculty
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(faccode=('fac1','fac1'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]

    def test_search_by_session(self):
        # We can find a student in a certain session
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(current_session=(2010,2010))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]

    def test_search_by_level(self):
        # We can find a student in a certain level
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(current_level=(100, 100))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]
        return

    def test_search_by_mode(self):
        # We can find a student in a certain mode
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(current_mode=('ug_ft', 'ug_ft'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]
        # Attention: A change of the certificate's study mode
        # is not reflected by the students catalog. The students_catalog
        # must be reindexed manually.
        self.certificate.study_mode = u'ug_pt'
        results = cat.searchResults(current_mode=('ug_ft', 'ug_ft'))
        assert len(results) == 1
        results = cat.searchResults(current_mode=('pg_ft', 'pg_ft'))
        assert len(results) == 0
        return


class CourseTicketCatalogTests(CatalogTestSetup):

    layer = FunctionalLayer

    def test_get_catalog(self):
        # We can get an students catalog if we wish
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        assert cat is not None

    def test_search_by_code(self):
        # We can find a certain course ticket by its code
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        results = cat.searchResults(code=('Course1', 'Course1'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'studycourse']['100']['Course1']

    def test_search_by_level(self):
        # We can find a certain course ticket by the level
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        results = cat.searchResults(level=(100, 100))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'studycourse']['100']['Course1']

    def test_search_by_session(self):
        # We can find a certain course ticket by the level session
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        results = cat.searchResults(session=(2010, 2010))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'studycourse']['100']['Course1']

class PaymentCatalogTests(CatalogTestSetup):

    layer = FunctionalLayer

    def test_get_catalog(self):
        # We can get a students catalog if we wish
        cat = queryUtility(ICatalog, name='payments_catalog')
        assert cat is not None

    def test_search_by_session(self):
        # We can find a payment ticket by the payment session
        cat = queryUtility(ICatalog, name='payments_catalog')
        results = cat.searchResults(p_session=(2010, 2010))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'payments']['p1234567890']

    def test_search_by_category(self):
        # We can find a payment ticket by the payment category
        cat = queryUtility(ICatalog, name='payments_catalog')
        results = cat.searchResults(p_category=('schoolfee','schoolfee'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'payments']['p1234567890']

    def test_search_by_item(self):
        # We can find a payment ticket by the payment item
        cat = queryUtility(ICatalog, name='payments_catalog')
        results = cat.searchResults(p_item=('any item','any item'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'payments']['p1234567890']

    def test_search_by_state(self):
        # We can find a payment ticket by the payment state
        cat = queryUtility(ICatalog, name='payments_catalog')
        results = cat.searchResults(p_state=('paid','paid'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'payments']['p1234567890']

    def test_reindex(self):
        # We can reindex any kind of catalog with the updateIndexes method.
        cat = queryUtility(ICatalog, name='payments_catalog')
        results = cat.searchResults(p_state=('failed','failed'))
        assert len(results) == 0
        results = cat.searchResults(p_state=('paid','paid'))
        assert len(results) == 1
        results = [x for x in results] # Turn results generator into list
        assert results[0] is self.app['students'][self.student_id][
            'payments']['p1234567890']
        results[0].p_state = 'failed'
        # Since we did not fire an ObjectModifiedEvent the catalog remained
        # unchanged
        results = cat.searchResults(p_state=('paid','paid'))
        assert len(results) == 1
        # Reindexing the catalog will lead to correct search results
        #reindexPayments()
        cat.clear() # The test works with and without clearing the catalog
        cat.updateIndexes()
        results = cat.searchResults(p_state=('paid','paid'))
        assert len(results) == 0
        results = cat.searchResults(p_state=('failed','failed'))
        assert len(results) == 1
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id][
            'payments']['p1234567890']
