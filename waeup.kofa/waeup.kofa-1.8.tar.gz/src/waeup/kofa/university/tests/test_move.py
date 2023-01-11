## $Id: test_move.py 12620 2015-02-16 11:27:24Z henrik $
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
Tests for moving objects in faculties.
"""
import os
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from waeup.kofa.university.faculty import Faculty
from waeup.kofa.university.department import Department
from waeup.kofa.students.tests.test_browser import StudentsFullSetup

class MoveObjectsInFaculties(StudentsFullSetup):

    def test_move_department(self):
        self.app['faculties']['fac2'] = Faculty(code=u'fac2')
        self.assertEqual(
            self.app['faculties']['fac1']['dep1'].certificates['CERT1'],
            self.certificate)
        department = self.app['faculties']['fac1']['dep1']
        faculty = self.app['faculties']['fac1']

        # We move the depart using the UtilityView
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/faculties/fac1/dep1/move_department?fac=fac2&dep=newdep')

        # New department is created and old department is removed
        self.assertEqual(
            [key for key in self.app['faculties']['fac2']], ['newdep'])

        # All subobjects have been moved too
        self.assertEqual(
            self.app['faculties']['fac2']['newdep'].courses['COURSE1'],
            self.course)
        self.assertEqual(
            self.app['faculties']['fac2']['newdep'].certificates['CERT1'],
            self.certificate)
        self.assertEqual(
            [key for key in self.app['faculties']['fac2'][
                'newdep'].certificates['CERT1'].keys()],
            [u'COURSE1_100'])

        # We can still find the certificate in the catalog
        cat = queryUtility(ICatalog, name='certificates_catalog')
        results = cat.searchResults(code=('CERT1','CERT1'))
        results = [x for x in results] 
        assert len(results) == 1
        assert results[0] is self.certificate

        # We can still find the course in the catalog
        cat = queryUtility(ICatalog, name='courses_catalog')
        results = cat.searchResults(code=('COURSE1','COURSE1'))
        results = [x for x in results] #
        assert len(results) == 1
        assert results[0] is self.course

        # We can still find the certificatecourse in the catalog
        cat = queryUtility(ICatalog, name='certcourses_catalog')
        results = cat.searchResults(course_code=('COURSE1','COURSE1'))
        results = [x for x in results] 
        assert len(results) == 1
        assert results[0] is self.app['faculties']['fac2'][
            'newdep'].certificates['CERT1']['COURSE1_100']

        # We can find the student studying in the new department
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(depcode=('newdep','newdep'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]

        # Messages are found in two log files
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue('INFO - zope.mgr - K1000000 - Department moved'
            in logcontent)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertTrue('INFO - zope.mgr - Department dep1 moved to fac2/newdep'
            in logcontent)


    def test_move_certificate(self):
        self.app['faculties']['fac2'] = Faculty(code=u'fac2')
        self.app['faculties']['fac2']['dep2'] = Department(code=u'dep2')
        self.assertEqual(
            self.app['faculties']['fac1']['dep1'].certificates['CERT1'],
            self.certificate)

        #self.certificate.moveCertificate('fac2', 'dep2', 'NEWCODE')

        # We move the depart using the UtilityView
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/faculties/fac1/dep1/certificates/CERT1/move_certificate?fac=fac2&dep=dep2&cert=NEWCODE')

        self.assertEqual(
            self.app['faculties']['fac2']['dep2'].certificates['NEWCODE'],
            self.certificate)
        self.assertEqual(
            [key for key in self.app['faculties']['fac2'][
                'dep2'].certificates['NEWCODE'].keys()], [u'COURSE1_100'])
        self.assertEqual(
            self.student['studycourse'].certificate,
            self.certificate)

        # We can find the moved certificate in the catalog
        cat = queryUtility(ICatalog, name='certificates_catalog')
        results = cat.searchResults(code=('NEWCODE','NEWCODE'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.certificate

        # Also certcourses_catalog has been updated
        cat = queryUtility(ICatalog, name='certcourses_catalog')
        results = cat.searchResults(course_code=('COURSE1','COURSE1'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['faculties']['fac2'][
                'dep2'].certificates['NEWCODE']['COURSE1_100']

        # We can find the student studying in the new department
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(depcode=('dep2','dep2'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]

        # We can find the student studying the new course ...
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(certcode=('NEWCODE','NEWCODE'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.app['students'][self.student_id]
        # ... but not the old course
        results = cat.searchResults(certcode=('CERT1','CERT1'))
        assert len(results) == 0

        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'students.log')
        logcontent = open(logfile).read()
        self.assertTrue('INFO - zope.mgr - K1000000 - Certificate moved'
            in logcontent)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertTrue('INFO - zope.mgr - Certificate CERT1 moved to fac2/dep2/NEWCODE'
            in logcontent)
