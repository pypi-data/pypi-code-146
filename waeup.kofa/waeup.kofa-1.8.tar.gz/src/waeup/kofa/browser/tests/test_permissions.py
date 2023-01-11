## $Id: test_permissions.py 15287 2019-01-09 21:17:08Z henrik $
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
Permission tests.

Check accessibility of views, pages, viewlets.

"""
import shutil
import tempfile
from zc.async.testing import wait_for_result
from zope.app.testing.functional import HTTPCaller as http
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.component import createObject, getUtility
from zope.component.hooks import setSite, clearSite
from zope.security.interfaces import Unauthorized
from zope.testbrowser.testing import Browser
from waeup.kofa.interfaces import IJobManager
from waeup.kofa.app import University
from waeup.kofa.testing import (
    FunctionalLayer, FunctionalTestCase, get_all_loggers, remove_new_loggers,
    remove_logger)
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase
from waeup.kofa.tests.test_authentication import SECRET


manager_pages = [
    # The pages that should only be accessible by manager...
    '/@@manage', '/@@administration', '/faculties/@@search',
    '/users/@@index', '/users/@@add', '/users/alice/@@manage',
    '/datacenter/@@index', '/datacenter/@@upload', '/datacenter/@@import1',
    '/datacenter/@@import2', '/datacenter/@@import3', '/datacenter/@@import4',
    '/datacenter/@@logs', '/datacenter/@@show', '/datacenter/@@manage',
    '/faculties/@@index', '/faculties/@@add', '/faculties/@@manage',
    '/faculties/fac1/@@index', '/faculties/fac1/@@manage',
    '/faculties/fac1/@@add',
    '/faculties/fac1/dept1/@@index',
    '/faculties/fac1/dept1/@@manage',
    '/faculties/fac1/dept1/@@addcourse',
    '/faculties/fac1/dept1/@@addcertificate',
    '/faculties/fac1/dept1/courses/crs1/@@index',
    '/faculties/fac1/dept1/courses/crs1/@@manage',
    '/faculties/fac1/dept1/certificates/cert1/@@index',
    '/faculties/fac1/dept1/certificates/cert1/@@manage',
    '/faculties/fac1/dept1/certificates/cert1/@@addcertificatecourse',
    '/faculties/fac1/dept1/certificates/cert1/crs1_100/@@index',
    '/faculties/fac1/dept1/certificates/cert1/crs1_100/@@manage',
    ]
public_pages = [
    # Pages accessible also by the public...
    '/@@index', '/@@login', '/@@logout',
    ]

class PermissionTest(FunctionalAsyncTestCase, FunctionalTestCase):
    """Here we try to request all pages and check, whether they are
    accessible.
    """

    layer = FunctionalLayer

    def setUp(self):
        super(PermissionTest, self).setUp()
        # Set up a complete university to have every page available...
        app = University()
        self.getRootFolder()['app'] = app
        setSite(self.getRootFolder()['app'])
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)
        app['users'].addUser('alice', 'alice')
        fac1 = createObject('waeup.Faculty')
        fac1.code = "fac1"
        app['faculties'].addFaculty(fac1)
        dept = createObject('waeup.Department')
        dept.code = 'dept1'
        fac1.addDepartment(dept)
        course = createObject('waeup.Course')
        course.code = 'crs1'
        dept.courses.addCourse(course)
        cert = createObject('waeup.Certificate')
        cert.code = 'cert1'
        dept.certificates.addCertificate(cert)
        cert.addCertCourse(course)
        self.app = app

        self.browser = Browser()
        self.browser.handleErrors = False
        pass

    def tearDown(self):
        super(PermissionTest, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)
        return

    def isAccessible(self, path):
        path = 'http://localhost/app%s' % path
        try:
            self.browser.open(path)
            return True
        except Unauthorized:
            return False
        return

    def wait_for_report_job_completed(self, number):
        # helper function waiting until the current export job is completed
        manager = getUtility(IJobManager)
        job_id = self.app['reports'].running_report_jobs[number][0]
        job = manager.get(job_id)
        wait_for_result(job)
        return job_id

    def stored_in_reports(self, job_id):
        # tell whether job_id is stored in reports's running jobs list
        for entry in list(self.app['reports'].running_report_jobs):
            if entry[0] == job_id:
                return True
        return False

    def trigger_report_creation(self, session):
        self.browser.open('http://localhost/app/reports')
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.getLink("Create new report").click()
        self.browser.getControl(name="generator").value = ['student_stats']
        self.browser.getControl("Configure").click()
        self.browser.getControl(name="breakdown").value = ['depcode']
        self.browser.getControl(name="mode").value = ['All']
        self.browser.getControl(name="session").value = [session]
        self.browser.getControl("Create").click()
        return

    def testUnauthenticatedUser(self):
        for path in manager_pages:
            if not self.isAccessible(path):
                continue
            self.fail('Path %s can be accessed by anonymous.' % path)
        for path in public_pages:
            if self.isAccessible(path):
                continue
            self.fail('Path %s cannot be accessed by anonymous.' % path)
        return

    def testReportsPermissions(self):
        # Create reports officer
        self.app['users'].addUser('mrofficer', SECRET)
        self.app['users']['mrofficer'].email = 'mrofficer@foo.ng'
        self.app['users']['mrofficer'].title = 'Otto Report'
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.ReportsOfficer', 'mrofficer')
        # Create reports manager
        self.app['users'].addUser('mrmanager', SECRET)
        self.app['users']['mrmanager'].email = 'mrmanager@foo.ng'
        self.app['users']['mrmanager'].title = 'Manfred Report'
        prmglobal.assignRoleToPrincipal('waeup.ReportsManager', 'mrmanager')
        # The reports officer creates a report which the reports manager
        # can see.
        self.browser.open('http://localhost/app/login')
        self.browser.getControl(name="form.login").value = 'mrofficer'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.trigger_report_creation('2004')
        job_id = self.wait_for_report_job_completed(0)
        self.browser.open('http://localhost/app/reports')
        self.assertTrue(
            'Student Statistics (depcode, 0, All, 2004)'
            in self.browser.contents)
        self.browser.open('http://localhost/app/logout')
        # The reports manager creates a report which the reports officer
        # can't see.
        self.browser.open('http://localhost/app/login')
        self.browser.getControl(name="form.login").value = 'mrmanager'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.trigger_report_creation('2005')
        job_id = self.wait_for_report_job_completed(1)
        self.browser.open('http://localhost/app/reports')
        # Manager can see both reports.
        self.assertTrue(
            'Student Statistics (depcode, 0, All, 2004)'
            in self.browser.contents)
        self.assertTrue(
            'Student Statistics (depcode, 0, All, 2005)'
            in self.browser.contents)
        self.browser.open('http://localhost/app/logout')
        self.browser.open('http://localhost/app/login')
        self.browser.getControl(name="form.login").value = 'mrofficer'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()
        self.browser.open('http://localhost/app/reports')
        # Officer can only see his report.
        self.assertTrue(
            'Student Statistics (depcode, 0, All, 2004)'
            in self.browser.contents)
        self.assertFalse(
            'Student Statistics (depcode, 0, All, 2005)'
            in self.browser.contents)
        return
