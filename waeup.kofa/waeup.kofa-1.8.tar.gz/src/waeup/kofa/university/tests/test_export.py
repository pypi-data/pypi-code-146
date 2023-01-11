## $Id: test_export.py 16450 2021-04-11 10:17:28Z henrik $
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
import os
import shutil
import tempfile
import unittest
from zope.component import queryUtility
from zope.interface.verify import verifyObject, verifyClass
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.testing import KofaUnitTestLayer, FunctionalLayer
from waeup.kofa.university import (
    FacultiesContainer, Faculty, Department, Course, Certificate,
    )
from waeup.kofa.university.export import (
    FacultyExporter, DepartmentExporter, CourseExporter,
    CertificateExporter, CertificateCourseExporter,
    )

class FacultyExporterTest(unittest.TestCase):

    layer = FunctionalLayer

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = FacultyExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, FacultyExporter)
        return

    def test_get_as_utility(self):
        # we can get a faculty exporter as utility
        result = queryUtility(ICSVExporter, name="faculties")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can export a set of faculties
        fac = Faculty('Faculty of Cheese', 'faculty', 'F1')
        exporter = FacultyExporter()
        exporter.export([fac], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2\r\n'
            'F1,Faculty of Cheese,faculty,[],,\r\n'
            )
        return

    def test_export_to_string(self):
        # we can export a set of faculties to a string.
        fac = Faculty('Faculty of Cheese', 'faculty', 'F1')
        exporter = FacultyExporter()
        result = exporter.export([fac], filepath=None)
        self.assertEqual(
            result,
            'code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2\r\n'
            'F1,Faculty of Cheese,faculty,[],,\r\n'
            )
        return

    def test_export_all(self):
        # we can export all faculties in a site
        container = FacultiesContainer()
        site = {'faculties':container}
        fac1 = Faculty('Faculty of Cheese', 'faculty', 'F1')
        fac2 = Faculty('Centre of Onion', 'centre', 'F2')
        container.addFaculty(fac1)
        container.addFaculty(fac2)
        exporter = FacultyExporter()
        exporter.export_all(site, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2\r\n'
            'F1,Faculty of Cheese,faculty,[],,\r\n'
            'F2,Centre of Onion,centre,[],,\r\n'
            )
        return

    def test_export_all_to_string(self):
        # we can export all faculties in a site to a string
        container = FacultiesContainer()
        site = {'faculties':container}
        fac1 = Faculty('Faculty of Cheese', 'faculty', 'F1')
        fac2 = Faculty('Centre of Onion', 'centre', 'F2')
        container.addFaculty(fac1)
        container.addFaculty(fac2)
        exporter = FacultyExporter()
        result = exporter.export_all(site, filepath=None)
        self.assertEqual(
            result,
            'code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2\r\n'
            'F1,Faculty of Cheese,faculty,[],,\r\n'
            'F2,Centre of Onion,centre,[],,\r\n'
            )
        return

class DepartmentExporterTest(unittest.TestCase):
    # Tests for DepartmentExporter

    layer = FunctionalLayer

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        # create some departments in a fake site
        container = FacultiesContainer()
        self.site = {'faculties':container}
        self.fac1 = Faculty('Faculty of Cheese', 'faculty', 'F1')
        self.fac2 = Faculty('Centre of Onion', 'centre', 'F2')
        container.addFaculty(self.fac1)
        container.addFaculty(self.fac2)
        self.dept1 = Department(
            'Department of Cheddar', 'department', 'D1', 'HoCheese')
        self.dept2 = Department('Institue of Gouda', 'institute', 'D2')
        self.dept3 = Department('Department of Rings', 'department', 'D3')
        self.fac1.addDepartment(self.dept1)
        self.fac1.addDepartment(self.dept2)
        self.fac2.addDepartment(self.dept3)
        role_manager = IPrincipalRoleManager(self.dept1)
        role_manager.assignRoleToPrincipal(u'bobsrole', u'bob')
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = DepartmentExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, DepartmentExporter)
        return

    def test_get_as_utility(self):
        # we can get a department exporter as utility
        result = queryUtility(ICSVExporter, name="departments")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can export an iterable of departments
        exporter = DepartmentExporter()
        exporter.export([self.dept1], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,faculty_code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2,officer_3,officer_4\r\n'
            'D1,F1,Department of Cheddar,department,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]",'
            'HoCheese,,,\r\n'
            )
        return

    def test_export_to_string(self):
        # we can export an iterable of departments to a string.
        exporter = DepartmentExporter()
        result = exporter.export([self.dept1, self.dept2], filepath=None)
        self.assertEqual(
            result,
            'code,faculty_code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2,officer_3,officer_4\r\n'
            'D1,F1,Department of Cheddar,department,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]",'
            'HoCheese,,,\r\n'
            'D2,F1,Institue of Gouda,institute,[],,,,\r\n'
            )
        return

    def test_export_all(self):
        # we can export all depts in a site
        exporter = DepartmentExporter()
        exporter.export_all(self.site, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,faculty_code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2,officer_3,officer_4\r\n'
            'D1,F1,Department of Cheddar,department,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]",'
            'HoCheese,,,\r\n'
            'D2,F1,Institue of Gouda,institute,[],,,,\r\n'
            'D3,F2,Department of Rings,department,[],,,,\r\n'
            )
        return

    def test_export_all_to_string(self):
        # we can export all depts in a site to a string
        exporter = DepartmentExporter()
        result = exporter.export_all(self.site, filepath=None)
        self.assertEqual(
            result,
            'code,faculty_code,title,title_prefix,users_with_local_roles,'
            'officer_1,officer_2,officer_3,officer_4\r\n'
            'D1,F1,Department of Cheddar,department,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]",'
            'HoCheese,,,\r\n'
            'D2,F1,Institue of Gouda,institute,[],,,,\r\n'
            'D3,F2,Department of Rings,department,[],,,,\r\n'
            )
        return

class CourseExporterTest(unittest.TestCase):
    # Tests for CourseExporter

    layer = FunctionalLayer

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        # create some departments and courses in a fake site
        container = FacultiesContainer()
        self.site = {'faculties':container}
        self.fac = Faculty('Faculty of Cheese', 'faculty', 'F1')
        container.addFaculty(self.fac)
        self.dept1 = Department('Department of Cheddar', 'department', 'D1')
        self.dept2 = Department('Institue of Gouda', 'institute', 'D2')
        self.fac.addDepartment(self.dept1)
        self.fac.addDepartment(self.dept2)
        self.course1 = Course('Cheese Basics', 'C1')
        self.course2 = Course('Advanced Cheese Making', 'C2')
        self.course3 = Course('Selling Cheese', 'C3')
        self.dept1.courses.addCourse(self.course1)
        self.dept1.courses.addCourse(self.course2)
        self.dept2.courses.addCourse(self.course3)
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = CourseExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, CourseExporter)
        return

    def test_get_as_utility(self):
        # we can get a course exporter as utility
        result = queryUtility(ICSVExporter, name="courses")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can export an iterable of courses
        exporter = CourseExporter()
        exporter.export([self.course1], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,credits,'
            'passmark,semester,users_with_local_roles,former_course,'
            'results_validated_by,results_validation_date,'
            'results_validation_session\r\n'
            'C1,F1,D1,Cheese Basics,0,40,1,[],0,,,\r\n'
            )
        return

    def test_export_to_string(self):
        # we can export an iterable of courses to a string.
        exporter = CourseExporter()
        result = exporter.export([self.course1, self.course2], filepath=None)
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,credits,passmark,'
            'semester,users_with_local_roles,former_course,'
            'results_validated_by,results_validation_date,'
            'results_validation_session\r\n'
            'C1,F1,D1,Cheese Basics,0,40,1,[],0,,,\r\n'
            'C2,F1,D1,Advanced Cheese Making,0,40,1,[],0,,,\r\n'
            )
        return

    def test_export_all(self):
        # we can export all courses in a site
        exporter = CourseExporter()
        exporter.export_all(self.site, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,credits,passmark,'
            'semester,users_with_local_roles,former_course,'
            'results_validated_by,results_validation_date,'
            'results_validation_session\r\n'
            'C1,F1,D1,Cheese Basics,0,40,1,[],0,,,\r\n'
            'C2,F1,D1,Advanced Cheese Making,0,40,1,[],0,,,\r\n'
            'C3,F1,D2,Selling Cheese,0,40,1,[],0,,,\r\n'
            )
        return

    def test_export_all_to_string(self):
        # we can export all courses in a site to a string
        exporter = CourseExporter()
        result = exporter.export_all(self.site, filepath=None)
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,credits,passmark,'
            'semester,users_with_local_roles,former_course,'
            'results_validated_by,results_validation_date,'
            'results_validation_session\r\n'
            'C1,F1,D1,Cheese Basics,0,40,1,[],0,,,\r\n'
            'C2,F1,D1,Advanced Cheese Making,0,40,1,[],0,,,\r\n'
            'C3,F1,D2,Selling Cheese,0,40,1,[],0,,,\r\n'
            )
        return

class CertificateExporterTest(unittest.TestCase):
    # Tests for CertificateExporter

    layer = FunctionalLayer

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        # create some departments and courses in a fake site
        container = FacultiesContainer()
        self.site = {'faculties':container}
        self.fac = Faculty('Faculty of Cheese', 'faculty', 'F1')
        container.addFaculty(self.fac)
        self.dept1 = Department('Department of Cheddar', 'department', 'D1')
        self.dept2 = Department('Institue of Gouda', 'institute', 'D2')
        self.fac.addDepartment(self.dept1)
        self.fac.addDepartment(self.dept2)
        self.course1 = Course('Cheese Basics', 'C1')
        self.course2 = Course('Advanced Cheese Making', 'C2')
        self.course3 = Course('Selling Cheese', 'C3')
        self.dept1.courses.addCourse(self.course1)
        self.dept1.courses.addCourse(self.course2)
        self.dept2.courses.addCourse(self.course3)
        self.cert1 = Certificate(
            'CERT1', 'Master of Cheese', study_mode=u'ct_ft', start_level=100,
            end_level=300, application_category='basic')
        self.cert2 = Certificate(
            'CERT2', 'Master of Cheddar', study_mode='ct_ft', start_level=400,
            end_level=700, application_category='cest')
        self.cert3 = Certificate(
            'CERT3', 'Cert. of Rubbish', study_mode='dp_pt', start_level=100,
            end_level=200, application_category='no')
        self.dept1.certificates.addCertificate(self.cert1)
        self.dept1.certificates.addCertificate(self.cert2)
        self.dept2.certificates.addCertificate(self.cert3)
        role_manager = IPrincipalRoleManager(self.cert1)
        role_manager.assignRoleToPrincipal(u'bobsrole', u'bob')
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = CertificateExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, CertificateExporter)
        return

    def test_get_as_utility(self):
        # we can get a certificate exporter as utility
        result = queryUtility(ICSVExporter, name="certificates")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can export an iterable of certificates
        exporter = CertificateExporter()
        exporter.export([self.cert1], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,study_mode,'
            'degree,key,start_level,'
            'end_level,application_category,ratio,school_fee_1,'
            'school_fee_2,school_fee_3,school_fee_4,'
            'custom_textline_1,custom_textline_2,'
            'custom_float_1,custom_float_2,'
            'users_with_local_roles\r\n'
            'CERT1,F1,D1,Master of Cheese,ct_ft,,CERT1,100,300,basic,,,,,,,,,,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]"\r\n'
            )
        return

    def test_export_to_string(self):
        # we can export an iterable of certificates to a string.
        exporter = CertificateExporter()
        result = exporter.export([self.cert1, self.cert2], filepath=None)
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,study_mode,'
            'degree,key,start_level,'
            'end_level,application_category,ratio,school_fee_1,'
            'school_fee_2,school_fee_3,school_fee_4,'
            'custom_textline_1,custom_textline_2,'
            'custom_float_1,custom_float_2,'
            'users_with_local_roles\r\n'
            'CERT1,F1,D1,Master of Cheese,ct_ft,,CERT1,100,300,basic,,,,,,,,,,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]"\r\n'
            'CERT2,F1,D1,Master of Cheddar,ct_ft,,CERT2,400,700,cest,,,,,,,,,,[]\r\n'
            )
        return

    def test_export_all(self):
        # we can export all certificates in a site
        exporter = CertificateExporter()
        exporter.export_all(self.site, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,study_mode,'
            'degree,key,start_level,'
            'end_level,application_category,ratio,'
            'school_fee_1,school_fee_2,school_fee_3,school_fee_4,'
            'custom_textline_1,custom_textline_2,'
            'custom_float_1,custom_float_2,'
            'users_with_local_roles\r\n'
            'CERT1,F1,D1,Master of Cheese,ct_ft,,CERT1,100,300,basic,,,,,,,,,,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]"\r\n'
            'CERT2,F1,D1,Master of Cheddar,ct_ft,,CERT2,400,700,cest,,,,,,,,,,[]\r\n'
            'CERT3,F1,D2,Cert. of Rubbish,dp_pt,,CERT3,100,200,no,,,,,,,,,,[]\r\n'
            )
        return

    def test_export_all_to_string(self):
        # we can export all certificates in a site to a string
        exporter = CertificateExporter()
        result = exporter.export_all(self.site, filepath=None)
        self.assertEqual(
            result,
            'code,faculty_code,department_code,title,study_mode,'
            'degree,key,start_level,'
            'end_level,application_category,ratio,'
            'school_fee_1,school_fee_2,school_fee_3,school_fee_4,'
            'custom_textline_1,custom_textline_2,'
            'custom_float_1,custom_float_2,'
            'users_with_local_roles\r\n'
            'CERT1,F1,D1,Master of Cheese,ct_ft,,CERT1,100,300,basic,,,,,,,,,,'
            '"[{\'user_name\': u\'bob\', \'local_role\': u\'bobsrole\'}]"\r\n'
            'CERT2,F1,D1,Master of Cheddar,ct_ft,,CERT2,400,700,cest,,,,,,,,,,[]\r\n'
            'CERT3,F1,D2,Cert. of Rubbish,dp_pt,,CERT3,100,200,no,,,,,,,,,,[]\r\n'
            )
        return

class CertificateCourseExporterTest(unittest.TestCase):
    # Tests for CertificateCourseExporter

    layer = KofaUnitTestLayer

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        # create some departments and courses in a fake site
        container = FacultiesContainer()
        self.site = {'faculties':container}
        self.fac = Faculty('Faculty of Cheese', 'faculty', 'F1')
        container.addFaculty(self.fac)
        self.dept1 = Department('Department of Cheddar', 'department', 'D1')
        self.dept2 = Department('Institue of Gouda', 'institute', 'D2')
        self.fac.addDepartment(self.dept1)
        self.fac.addDepartment(self.dept2)
        self.course1 = Course('Cheese Basics', 'C1')
        self.course2 = Course('Advanced Cheese Making', 'C2')
        self.course3 = Course('Selling Cheese', 'C3')
        self.dept1.courses.addCourse(self.course1)
        self.dept1.courses.addCourse(self.course2)
        self.dept2.courses.addCourse(self.course3)
        self.cert1 = Certificate(
            'CERT1', 'Master of Cheese', study_mode=u'ct_ft', start_level=100,
            end_level=300, application_category='basic')
        self.cert2 = Certificate(
            'CERT2', 'Master of Cheddar', study_mode='ct_ft', start_level=400,
            end_level=700, application_category='cest')
        self.cert3 = Certificate(
            'CERT3', 'Cert. of Rubbish', study_mode='dp_pt', start_level=100,
            end_level=200, application_category='no')
        self.dept1.certificates.addCertificate(self.cert1)
        self.dept1.certificates.addCertificate(self.cert2)
        self.dept2.certificates.addCertificate(self.cert3)
        self.cert1.addCertCourse(self.course1, 100, True)
        self.cert1.addCertCourse(self.course2, 400, False)
        self.cert3.addCertCourse(self.course3, 100, False)
        self.certcourse1 = self.cert1['C1_100']
        self.certcourse2 = self.cert1['C2_400']
        self.certcourse3 = self.cert3['C3_100']
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = CertificateCourseExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, CertificateCourseExporter)
        return

    def test_get_as_utility(self):
        # we can get a certificate exporter as utility
        result = queryUtility(ICSVExporter, name="certificate_courses")
        self.assertTrue(result is not None)
        return

    def test_export(self):
        # we can export an iterable of certificates
        exporter = CertificateCourseExporter()
        exporter.export([self.certcourse1], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'course,faculty_code,department_code,certificate_code,'
            'level,mandatory,course_category\r\n'
            'C1,F1,D1,CERT1,100,1,\r\n'
            )
        return

    def test_export_to_string(self):
        # we can export an iterable of certificates to a string.
        exporter = CertificateCourseExporter()
        result = exporter.export(
            [self.certcourse1, self.certcourse2], filepath=None)
        self.assertEqual(
            result,
            'course,faculty_code,department_code,certificate_code,'
            'level,mandatory,course_category\r\n'
            'C1,F1,D1,CERT1,100,1,\r\n'
            'C2,F1,D1,CERT1,400,0,\r\n'
            )
        return

    def test_export_all(self):
        # we can export all certificates in a site
        exporter = CertificateCourseExporter()
        exporter.export_all(self.site, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'course,faculty_code,department_code,certificate_code,'
            'level,mandatory,course_category\r\n'
            'C1,F1,D1,CERT1,100,1,\r\n'
            'C2,F1,D1,CERT1,400,0,\r\n'
            'C3,F1,D2,CERT3,100,0,\r\n'
            )
        return

    def test_export_all_to_string(self):
        # we can export all certificates in a site to a string
        exporter = CertificateCourseExporter()
        result = exporter.export_all(self.site, filepath=None)
        self.assertEqual(
            result,
            'course,faculty_code,department_code,certificate_code,'
            'level,mandatory,course_category\r\n'
            'C1,F1,D1,CERT1,100,1,\r\n'
            'C2,F1,D1,CERT1,400,0,\r\n'
            'C3,F1,D2,CERT3,100,0,\r\n'
            )
        return
