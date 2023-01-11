## $Id: test_batching.py 13607 2016-01-13 06:34:05Z henrik $
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

# Tests for university related batching
import unittest
import tempfile
import shutil
import os
from zope.component.hooks import setSite, clearSite
from zope.component import createObject
from zope.securitypolicy.interfaces import (
    IPrincipalRoleMap, IPrincipalRoleManager)
from zope.testbrowser.testing import Browser
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.interfaces import IBatchProcessor
from waeup.kofa.testing import FunctionalTestCase, FunctionalLayer
from waeup.kofa.app import University
from waeup.kofa.university.batching import (
    FacultyProcessor, DepartmentProcessor, CourseProcessor,
    CertificateProcessor, CertificateCourseProcessor)
from waeup.kofa.university.certificate import Certificate, CertificateCourse
from waeup.kofa.university.course import Course
from waeup.kofa.university import Faculty, Department
from waeup.kofa.university.batching import FacultyProcessor

FACULTY_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_faculty_data.csv'),
    'rb').read()

FACULTY_HEADER_FIELDS = FACULTY_SAMPLE_DATA.split(
    '\n')[0].split(',')

FACULTY_SAMPLE_DATA_UPDATE = open(
    os.path.join(os.path.dirname(__file__), 'sample_faculty_data_update.csv'),
    'rb').read()

FACULTY_HEADER_FIELDS_UPDATE = FACULTY_SAMPLE_DATA_UPDATE.split(
    '\n')[0].split(',')

DEPARTMENT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_department_data.csv'),
    'rb').read()

DEPARTMENT_HEADER_FIELDS = DEPARTMENT_SAMPLE_DATA.split(
    '\n')[0].split(',')

CERTIFICATE_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_certificate_data.csv'),
    'rb').read()

CERTIFICATE_HEADER_FIELDS = CERTIFICATE_SAMPLE_DATA.split(
    '\n')[0].split(',')

COURSE_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_course_data.csv'),
    'rb').read()

COURSE_HEADER_FIELDS = COURSE_SAMPLE_DATA.split(
    '\n')[0].split(',')

COURSE_SAMPLE_DATA_UPDATE = open(
    os.path.join(os.path.dirname(__file__), 'sample_course_data_update.csv'),
    'rb').read()

COURSE_HEADER_FIELDS_UPDATE = COURSE_SAMPLE_DATA_UPDATE.split(
    '\n')[0].split(',')


CERTIFICATECOURSE_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_certificatecourse_data.csv'),
    'rb').read()

CERTIFICATECOURSE_HEADER_FIELDS = CERTIFICATECOURSE_SAMPLE_DATA.split(
    '\n')[0].split(',')

class UniversityProcessorSetup(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(UniversityProcessorSetup, self).setUp()
        self.dc_root = tempfile.mkdtemp()
        self.workdir = tempfile.mkdtemp()
        app = University()
        app['datacenter'].setStoragePath(self.dc_root)
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(app)

        self.app['users'].addUser('bob', 'bobssecret')
        self.app['users'].addUser('anne', 'annessecret')

        # Populate university
        self.certificate = createObject('waeup.Certificate')
        self.certificate.code = 'CRT1'
        self.app['faculties']['FAC1'] = Faculty(code='FAC1')
        self.app['faculties']['FAC1']['DEP1'] = Department(code='DEP1')
        self.app['faculties']['FAC1']['DEP1'].certificates.addCertificate(
            self.certificate)
        self.course = createObject('waeup.Course')
        self.course.code = 'CRS1'
        self.app['faculties']['FAC1']['DEP1'].courses.addCourse(
            self.course)
        #self.app['faculties']['fac1']['dep1'].certificates['CERT1'].addCertCourse(
        #    self.course, level=100)
        
        self.logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        return

    def tearDown(self):
        super(UniversityProcessorSetup, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

class TestFacultyProcessor(UniversityProcessorSetup):

    def setUp(self):
        super(TestFacultyProcessor, self).setUp()

        self.browser = Browser()
        self.browser.handleErrors = False
        self.datacenter_path = 'http://localhost/app/datacenter'
        self.app['datacenter'].setStoragePath(self.dc_root)

        self.proc = FacultyProcessor()
        self.site1 = dict(faculties=dict())
        self.site2 = dict(faculties=dict(FAC='pseudo faculty'))
        self.row = dict(code='FAC')

        self.csv_file_faculty = os.path.join(self.workdir, 'sample_faculty_data.csv')
        open(self.csv_file_faculty, 'wb').write(FACULTY_SAMPLE_DATA)
        self.csv_file_faculty_update = os.path.join(self.workdir, 'sample_faculty_data_update.csv')
        open(self.csv_file_faculty_update, 'wb').write(FACULTY_SAMPLE_DATA_UPDATE)
        return

    def test_ifaces(self):
        # Make sure we fullfill all interface contracts
        verifyClass(IBatchProcessor, FacultyProcessor)
        verifyObject(IBatchProcessor, self.proc)
        return

    def test_get_entry(self):
        # if a faculty exists already, we will get it
        result1 = self.proc.getEntry(self.row, self.site1)
        result2 = self.proc.getEntry(self.row, self.site2)
        self.assertTrue(result1 is None)
        self.assertEqual(result2, 'pseudo faculty')
        return

    def test_del_entry(self):
        # make sure we can del entries.
        self.proc.delEntry(self.row, self.site2)
        self.assertTrue('FAC' not in self.site2.keys())
        return

    def test_checkConversion(self):
        # Make sure we can check conversions.
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC', local_roles='[]'))
        self.assertEqual(len(errs),0)

        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC',
            local_roles="['nonsense'"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'Error')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC',
            local_roles="('abc')"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'no list')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC',
            local_roles="[('ABC')]"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'no dicts')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC',
            local_roles="('abc')"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'no list')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC', local_roles=
            "[{'name':'bob','local_role':'waeup.local.DepartmentManager'},]"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'user_name or local_role missing')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC', local_roles=
            "[{'user_name':'bob','localrole':'waeup.local.DepartmentManager'},]"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'user_name or local_role missing')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC', local_roles=
            "[{'user_name':'bob','local_role':'waeup.local.Boss'},]"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'waeup.local.Boss not allowed')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC', local_roles=
            "[{'user_name':'john','local_role':'waeup.local.DepartmentManager'},]"
            ))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs, [('local_roles', 'john does not exist')])
        errs, inv_errs, conv_dict = self.proc.checkConversion(
            dict(faculty_code='ABC', local_roles=
            "[{'user_name':'bob','local_role':'waeup.local.DepartmentManager'},]"
            ))
        self.assertEqual(len(errs),0)
        return

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_faculty, FACULTY_HEADER_FIELDS)
        content = open(fail_file).read()
        self.assertEqual(num_warns,5)
        self.assertEqual(
            content,
            'code,local_roles,--ERRORS--\r\n'
            'CDE,"[{\'user_name\':\'alice\',\'local_role\':\'waeup.local.DepartmentManager\'}]",'
            'local_roles: alice does not exist\r\n'
            'DEF,"[{\'user_name\':\'bob\',\'local_role\':\'waeup.local.Boss\'}]",'
            'local_roles: waeup.local.Boss not allowed\r\n'
            'EFG,[(\'anything\')],local_roles: no dicts\r\n'
            'FGH,[,local_roles: Error\r\n'
            'GHI,"[{\'user\':\'bob\',\'local\':\'waeup.local.DepartmentManager\'}]",'
            'local_roles: user_name or local_role missing\r\n'
            )
        # Bob got a local role in faculty ABC.
        abc = self.app['faculties']['ABC']
        role_map = IPrincipalRoleMap(abc)
        local_role, user_name, setting = role_map.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'bob')
        self.assertEqual(local_role, 'waeup.local.DepartmentManager')
        shutil.rmtree(os.path.dirname(fin_file))
        return

    def test_import_update(self):
        self.app['faculties']['FAC2'] = Faculty(code='FAC2')
        self.app['faculties']['FAC3'] = Faculty(code='FAC3')
        self.app['faculties']['FAC4'] = Faculty(code='FAC4')

        role_manager1 = IPrincipalRoleManager(self.app['faculties']['FAC1'])
        role_manager1.assignRoleToPrincipal('alfonsrole', 'alfons')
        role_map1 = IPrincipalRoleMap(self.app['faculties']['FAC1'])
        self.assertEqual(len(role_map1.getPrincipalsAndRoles()), 1)

        role_manager2 = IPrincipalRoleManager(self.app['faculties']['FAC2'])
        role_manager2.assignRoleToPrincipal('alfonsrole', 'alfons')
        role_map2 = IPrincipalRoleMap(self.app['faculties']['FAC2'])
        self.assertEqual(len(role_map2.getPrincipalsAndRoles()), 1)

        role_manager3 = IPrincipalRoleManager(self.app['faculties']['FAC3'])
        role_manager3.assignRoleToPrincipal('alfonsrole', 'alfons')
        role_map3 = IPrincipalRoleMap(self.app['faculties']['FAC3'])
        self.assertEqual(len(role_map3.getPrincipalsAndRoles()), 1)

        role_manager4 = IPrincipalRoleManager(self.app['faculties']['FAC4'])
        role_manager4.assignRoleToPrincipal('alfonsrole', 'alfons')
        role_map4 = IPrincipalRoleMap(self.app['faculties']['FAC4'])
        self.assertEqual(len(role_map4.getPrincipalsAndRoles()), 1)

        local_role, user_name, setting = role_map2.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'alfons')
        self.assertEqual(local_role, 'alfonsrole')

        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_faculty_update, FACULTY_HEADER_FIELDS_UPDATE, 'update')
        self.assertEqual(num_warns,0)
        # Local roles have been removed in FAC1 due to deletion marker.
        self.assertEqual(len(role_map1.getPrincipalsAndRoles()), 0)
        # Old local roles have been removed and new roles have been added in FAC2.
        self.assertEqual(len(role_map2.getPrincipalsAndRoles()), 1)
        local_role, user_name, setting = role_map2.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'bob')
        self.assertEqual(local_role, 'waeup.local.DepartmentManager')
        # Local roles are not touched in FAC3 due to ignore marker.
        self.assertEqual(len(role_map3.getPrincipalsAndRoles()), 1)
        local_role, user_name, setting = role_map3.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'alfons')
        self.assertEqual(local_role, 'alfonsrole')
        # Local roles are not touched in FAC4 due to empty cell.
        self.assertEqual(len(role_map4.getPrincipalsAndRoles()), 1)
        local_role, user_name, setting = role_map4.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'alfons')
        self.assertEqual(local_role, 'alfonsrole')
        shutil.rmtree(os.path.dirname(fin_file))
        return
        
    def test_import_update_logging(self):
        self.app['faculties']['FAC2'] = Faculty(code='FAC2')
        self.app['faculties']['FAC3'] = Faculty(code='FAC3')
        self.app['faculties']['FAC4'] = Faculty(code='FAC4')
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_faculty_update, FACULTY_HEADER_FIELDS_UPDATE, 'update')
        self.assertEqual(num_warns,0)
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry
        self.assertTrue(
            'INFO - system - Faculty Processor - sample_faculty_data_update - '
            'FAC1 - updated: code=FAC1'
            in logcontent)
        self.assertTrue(
            'INFO - system - Faculty Processor - sample_faculty_data_update - '
            'FAC2 - updated: local_roles=bob|waeup.local.DepartmentManager, '
            'code=FAC2'
            in logcontent)
        self.assertTrue(
            'INFO - system - Faculty Processor - sample_faculty_data_update - '
            'FAC3 - updated: code=FAC3'
            in logcontent)
        self.assertTrue(
            'INFO - system - Faculty Processor - sample_faculty_data_update - '
            'FAC4 - updated: code=FAC4'
            in logcontent)
        shutil.rmtree(os.path.dirname(fin_file))

    def test_upload_import_reupload(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.datacenter_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.datacenter_path)
        self.browser.getLink("Upload data").click()
        file = open(self.csv_file_faculty)
        ctrl = self.browser.getControl(name='uploadfile:file')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file, filename='sample_faculty_data.csv')
        self.browser.getControl('Upload').click()
        self.browser.getLink('Process data').click()
        self.assertTrue('Portal must be in maintenance mode for data import.'
            in self.browser.contents)
        self.browser.getLink("Switch").click()
        self.assertTrue('Maintenance mode enabled' in self.browser.contents)
        # Maintenance mode is now set.
        self.assertEqual(
            self.app['configuration'].maintmode_enabled_by, 'zope.mgr')
        self.browser.getControl(name="select").click()
        importerselect = self.browser.getControl(name='importer')
        importerselect.getControl('Faculty Processor').selected = True
        modeselect = self.browser.getControl(name='mode')
        modeselect.getControl(value='create').selected = True
        self.browser.getControl('Proceed to step 3').click()
        self.assertTrue('Header fields OK' in self.browser.contents)
        self.browser.getControl('Perform import').click()
        self.assertTrue('Successfully processed 1 rows' in self.browser.contents)
        self.assertTrue('Maintenance mode disabled' in self.browser.contents)
        # Maintenance mode is really disabled.
        self.assertEqual(
            self.app['configuration'].maintmode_enabled_by, None)
        # We import the same file a second time.
        self.browser.open(self.datacenter_path)
        self.browser.getLink("Upload data").click()
        file = open(self.csv_file_faculty)
        ctrl = self.browser.getControl(name='uploadfile:file')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(file, filename='sample_faculty_data.csv')
        self.browser.getControl('Upload').click()
        self.assertTrue(
            'File with same name was uploaded earlier' in self.browser.contents)
        return

class TestDepartmentProcessor(UniversityProcessorSetup):

    def setUp(self):
        super(TestDepartmentProcessor, self).setUp()
        self.proc = DepartmentProcessor()
        self.site0 = dict()
        self.site1 = dict(faculties=dict())
        self.site2 = dict(faculties=dict(FAC=dict()))
        self.site3 = dict(faculties=dict(FAC=dict(DPT='pseudo department')))
        self.row = dict(code='DPT', faculty_code='FAC')

        self.csv_file_department = os.path.join(self.workdir, 'sample_department_data.csv')
        open(self.csv_file_department, 'wb').write(DEPARTMENT_SAMPLE_DATA)
        return

    def test_ifaces(self):
        # Make sure we fullfill all interface contracts
        verifyClass(IBatchProcessor, DepartmentProcessor)
        verifyObject(IBatchProcessor, self.proc)
        return

    def test_parents_exist(self):
        # make sure we lookup parents correctly.
        result0 = self.proc.parentsExist(self.row, self.site0)
        result1 = self.proc.parentsExist(self.row, self.site1)
        result2 = self.proc.parentsExist(self.row, self.site2)
        result3 = self.proc.parentsExist(self.row, self.site3)
        self.assertTrue(result0 is False)
        self.assertTrue(result1 is False)
        self.assertTrue(result2 is True)
        self.assertTrue(result3 is True)
        return

    def test_entry_exists(self):
        # make sure we lookup entries correctly.
        result0 = self.proc.entryExists(self.row, dict())
        result1 = self.proc.entryExists(self.row, self.site1)
        result2 = self.proc.entryExists(self.row, self.site2)
        result3 = self.proc.entryExists(self.row, self.site3)
        self.assertTrue(result0 is False)
        self.assertTrue(result1 is False)
        self.assertTrue(result2 is False)
        self.assertTrue(result3 is True)
        return

    def test_get_entry(self):
        # we can get a dept. if it exists
        result1 = self.proc.getEntry(self.row, self.site2)
        result2 = self.proc.getEntry(self.row, self.site3)
        self.assertTrue(result1 is None)
        self.assertEqual(result2, 'pseudo department')
        return

    def test_del_entry(self):
        # we can delete departments
        self.proc.delEntry(self.row, self.site3)
        self.assertTrue('DPT' not in self.site3['faculties']['FAC'].keys())
        return

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_department, DEPARTMENT_HEADER_FIELDS)
        content = open(fail_file).read()
        self.assertEqual(num_warns,6)
        self.assertEqual(
            content,
            'faculty_code,code,local_roles,--ERRORS--\r\n'
            'FAC1,DEP2,"[{\'user_name\':\'alice\',\'local_role\':\'waeup.local.DepartmentManager\'}]",'
            'local_roles: alice does not exist\r\n'
            'FAC1,DEP2,"[{\'user_name\':\'anne\',\'local_role\':\'waeup.local.Boss\'}]",'
            'local_roles: waeup.local.Boss not allowed\r\n'
            'FAC1,DEP2,[(\'anything\')],local_roles: no dicts\r\n'
            'FAC1,DEP2,[,local_roles: Error\r\n'
            'FAC1,DEP2,"[{\'user\':\'anne\',\'local\':\'waeup.local.DepartmentManager\'}]",'
            'local_roles: user_name or local_role missing\r\n'
            'FAC11,DEP2,"[{\'user_name\':\'anne\',\'local_role\':\'waeup.local.DepartmentManager\'}]",'
            'Not all parents do exist yet.\r\n'
            )
        # Anne got a local role in department DEP2.
        dep = self.app['faculties']['FAC1']['DEP2']
        role_map = IPrincipalRoleMap(dep)
        local_role, user_name, setting = role_map.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'anne')
        self.assertEqual(local_role, 'waeup.local.DepartmentManager')
        shutil.rmtree(os.path.dirname(fin_file))
        return

class CourseProcessorTests(UniversityProcessorSetup):

    def setUp(self):
        super(CourseProcessorTests, self).setUp()
        self.proc = CourseProcessor()
        self.row1 = dict(department_code='DEP2', faculty_code='FAC1', code="CRS1")
        self.row2 = dict(department_code='DEP1', faculty_code='FAC2', code="CRS1")
        self.row3 = dict(department_code='DEP1', faculty_code='FAC1', code="CRS2")
        self.row4 = dict(department_code='DEP1', faculty_code='FAC1', code="CRS1")

        self.csv_file_course = os.path.join(
            self.workdir, 'sample_course_data.csv')
        open(self.csv_file_course, 'wb').write(COURSE_SAMPLE_DATA)
        self.csv_file_course_update = os.path.join(
            self.workdir, 'sample_course_data_update.csv')
        open(self.csv_file_course_update, 'wb').write(COURSE_SAMPLE_DATA_UPDATE)
        return

    def test_ifaces(self):
        # Make sure we fullfill all interface contracts
        verifyClass(IBatchProcessor, CourseProcessor)
        verifyObject(IBatchProcessor, self.proc)
        return

    def test_parents_exist(self):
        # make sure we lookup parents correctly
        result1 = self.proc.parentsExist(self.row1, self.app)
        result2 = self.proc.parentsExist(self.row2, self.app)
        result3 = self.proc.parentsExist(self.row3, self.app)
        self.assertTrue(result1 is False)
        self.assertTrue(result2 is False)
        self.assertTrue(result3 is True)
        return

    def test_entry_exists(self):
        # make sure we find an entry if it exists
        result1 = self.proc.entryExists(self.row1, self.app)
        result2 = self.proc.entryExists(self.row2, self.app)
        result3 = self.proc.entryExists(self.row3, self.app)
        result4 = self.proc.entryExists(self.row4, self.app)
        self.assertTrue(result1 is False)
        self.assertTrue(result2 is False)
        self.assertTrue(result3 is False)
        self.assertTrue(result4 is True)
        return

    def test_get_entry(self):
        # make sure we can get an entry if it exists
        result1 = self.proc.getEntry(self.row1, self.app)
        result2 = self.proc.getEntry(self.row4, self.app)
        self.assertTrue(result1 is None)
        self.assertTrue(result2 is self.course)
        return

    def test_del_entry(self):
        # make sure we can delete entries
        self.assertTrue('CRS1' in self.app['faculties']['FAC1']['DEP1'].courses.keys())
        self.proc.delEntry(self.row4, self.app)
        self.assertTrue('CRS1' not in self.app['faculties']['FAC1']['DEP1'].courses.keys())
        return

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_course, COURSE_HEADER_FIELDS)
        content = open(fail_file).read()
        self.assertEqual(num_warns,6)
        self.assertEqual(
            content,
            'faculty_code,department_code,code,local_roles,--ERRORS--\r\n'
            'FAC1,DEP1,CRS2,"[{\'user_name\':\'alice\',\'local_role\':\'waeup.local.Lecturer\'}]",'
            'local_roles: alice does not exist\r\n'
            'FAC1,DEP1,CRS2,"[{\'user_name\':\'anne\',\'local_role\':\'waeup.local.Boss\'}]",'
            'local_roles: waeup.local.Boss not allowed\r\n'
            'FAC1,DEP1,CRS2,[(\'anything\')],local_roles: no dicts\r\n'
            'FAC1,DEP1,CRS2,[,local_roles: Error\r\n'
            'FAC1,DEP1,CRS2,"[{\'user\':\'anne\',\'local\':\'waeup.local.Lecturer\'}]",'
            'local_roles: user_name or local_role missing\r\n'
            'FAC11,DEP2,CRS2,"[{\'user_name\':\'anne\',\'local_role\':\'waeup.local.Lecturer\'}]",'
            'Not all parents do exist yet.\r\n'
            )
        # Anne got a local role in course CRS2.
        dep = self.app['faculties']['FAC1']['DEP1'].courses['CRS2']
        role_map = IPrincipalRoleMap(dep)
        local_role, user_name, setting = role_map.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'anne')
        self.assertEqual(local_role, 'waeup.local.Lecturer')
        shutil.rmtree(os.path.dirname(fin_file))
        return

    def test_import_update(self):
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_course, COURSE_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_course_update, COURSE_HEADER_FIELDS_UPDATE, 'update')
        self.assertEqual(num_warns,0)
        self.assertEqual(
            self.app['faculties']['FAC1']['DEP1'].courses['CRS2'].title,
            'New Title')
        shutil.rmtree(os.path.dirname(fin_file))
        return


class CertificateProcessorTests(UniversityProcessorSetup):

    def setUp(self):
        super(CertificateProcessorTests, self).setUp()
        self.proc = CertificateProcessor()
        self.row1 = dict(department_code='DEP2', faculty_code='FAC1', code="CRT1")
        self.row2 = dict(department_code='DEP1', faculty_code='FAC2', code="CRT1")
        self.row3 = dict(department_code='DEP1', faculty_code='FAC1', code="CRT2")
        self.row4 = dict(department_code='DEP1', faculty_code='FAC1', code="CRT1")

        self.csv_file_certificate = os.path.join(self.workdir, 'sample_certificate_data.csv')
        open(self.csv_file_certificate, 'wb').write(CERTIFICATE_SAMPLE_DATA)
        return

    def test_ifaces(self):
        # Make sure we fullfill all interface contracts
        verifyClass(IBatchProcessor, CourseProcessor)
        verifyObject(IBatchProcessor, self.proc)
        return

    def test_parents_exist(self):
        # make sure we lookup parents correctly
        result1 = self.proc.parentsExist(self.row1, self.app)
        result2 = self.proc.parentsExist(self.row2, self.app)
        result3 = self.proc.parentsExist(self.row3, self.app)
        self.assertTrue(result1 is False)
        self.assertTrue(result2 is False)
        self.assertTrue(result3 is True)
        return

    def test_entry_exists(self):
        # make sure we find an entry if it exists
        result1 = self.proc.entryExists(self.row1, self.app)
        result2 = self.proc.entryExists(self.row2, self.app)
        result3 = self.proc.entryExists(self.row3, self.app)
        result4 = self.proc.entryExists(self.row4, self.app)
        self.assertTrue(result1 is False)
        self.assertTrue(result2 is False)
        self.assertTrue(result3 is False)
        self.assertTrue(result4 is True)
        return

    def test_get_entry(self):
        # make sure we can get an entry if it exists
        result1 = self.proc.getEntry(self.row1, self.app)
        result2 = self.proc.getEntry(self.row4, self.app)
        self.assertTrue(result1 is None)
        self.assertTrue(result2 is self.certificate)
        return

    def test_del_entry(self):
        # make sure we can delete entries
        self.assertTrue('CRT1' in self.app['faculties']['FAC1']['DEP1'].certificates.keys())
        self.proc.delEntry(self.row4, self.app)
        self.assertTrue('CRT1' not in self.app['faculties']['FAC1']['DEP1'].certificates.keys())
        return

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_certificate, CERTIFICATE_HEADER_FIELDS)
        content = open(fail_file).read()
        self.assertEqual(num_warns,6)
        self.assertEqual(
            content,
            'faculty_code,department_code,code,local_roles,--ERRORS--\r\n'
            'FAC1,DEP1,CRT2,"[{\'user_name\':\'alice\',\'local_role\':\'waeup.local.CourseAdviser100\'}]",'
            'local_roles: alice does not exist\r\n'
            'FAC1,DEP1,CRT2,"[{\'user_name\':\'anne\',\'local_role\':\'waeup.local.Boss\'}]",'
            'local_roles: waeup.local.Boss not allowed\r\n'
            'FAC1,DEP1,CRT2,[(\'anything\')],local_roles: no dicts\r\n'
            'FAC1,DEP1,CRT2,[,local_roles: Error\r\n'
            'FAC1,DEP1,CRT2,"[{\'user\':\'anne\',\'local\':\'waeup.local.CourseAdviser100\'}]",'
            'local_roles: user_name or local_role missing\r\n'
            'FAC11,DEP2,CRT2,"[{\'user_name\':\'anne\',\'local_role\':\'waeup.local.CourseAdviser100\'}]",'
            'Not all parents do exist yet.\r\n'
            )
        # Anne got a local role in certificate CRT2.
        dep = self.app['faculties']['FAC1']['DEP1'].certificates['CRT2']
        role_map = IPrincipalRoleMap(dep)
        local_role, user_name, setting = role_map.getPrincipalsAndRoles()[0]
        self.assertEqual(user_name, 'anne')
        self.assertEqual(local_role, 'waeup.local.CourseAdviser100')
        shutil.rmtree(os.path.dirname(fin_file))
        
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry
        self.assertTrue(
            'INFO - system - Certificate Processor - '
            'sample_certificate_data - CRT2 - '
            'updated: local_roles=anne|waeup.local.CourseAdviser100, code=CRT2'
            in logcontent)        
        
        return


class CertCourseProcessorTests(UniversityProcessorSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(CertCourseProcessorTests, self).setUp()
        self.proc = CertificateCourseProcessor()
        self.certificate.addCertCourse(self.course)
        self.row1 = dict(
            department_code='DEP1',
            faculty_code='FAC1',
            certificate_code='CRT1',
            course=self.course, level='100')
        self.row2 = dict(
            department_code='DEP1',
            faculty_code='FAC1',
            certificate_code='CRT2',
            course=self.course, level='100')
        self.csv_file_certificatecourse = os.path.join(
            self.workdir, 'sample_certificatecourse_data.csv')
        open(self.csv_file_certificatecourse, 'wb').write(CERTIFICATECOURSE_SAMPLE_DATA)
        return

    def test_ifaces(self):
        # Make sure we fullfill all interface contracts
        verifyClass(IBatchProcessor, CertificateCourseProcessor)
        verifyObject(IBatchProcessor, self.proc)
        return

    def test_parents_exist(self):
        # make sure we can find all certificate parents
        result1 = self.proc.parentsExist(self.row1, self.app)
        self.assertTrue(result1)
        result2 = self.proc.parentsExist(self.row2, self.app)
        self.assertFalse(result2)
        return

    def test_entry_exists(self):
        # make sure we find an entry if it exists
        result1 = self.proc.entryExists(self.row1, self.app)
        self.assertTrue(result1)
        result2 = self.proc.entryExists(self.row2, self.app)
        self.assertFalse(result2)
        return

    def test_get_entry(self):
        # make sure we can get an entry if it exists
        result1 = self.proc.getEntry(self.row1, self.app)
        self.assertTrue(result1 is self.certificate['CRS1_100'])
        result2 = self.proc.getEntry(self.row2, self.app)
        self.assertFalse(result2 is self.certificate['CRS1_100'])
        return

    def test_del_entry(self):
        # make sure we can delete entries
        self.assertTrue('CRS1_100' in self.certificate.keys())
        self.proc.delEntry(self.row1, self.app)
        self.assertTrue('CRS1_100' not in self.certificate.keys())
        return

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.proc.doImport(
            self.csv_file_certificatecourse, CERTIFICATECOURSE_HEADER_FIELDS)
        content = open(fail_file).read()
        self.assertEqual(num_warns,2) # the last two
        self.assertEqual(
            content,
            'mandatory,level,faculty_code,course,department_code,'
            'certificate_code,--ERRORS--\r\n'
            '<IGNORE>,100,FAC1,CRS1,'
            'DEP1,CRT1,This object already exists.\r\n'
            '<IGNORE>,100,FAC1,CRS1,DEP1,CRT2,Not all parents do exist yet.\r\n'
            )
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry
        self.assertTrue(
            'INFO - system - CertificateCourse Processor - '
            'sample_certificatecourse_data - CRT1 - updated: '
            'mandatory=True, level=200, course=CRS1\n'
            in logcontent)
        return
