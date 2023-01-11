## $Id: test_dynamicroles.py 10639 2013-09-22 08:54:03Z henrik $
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
Tests for dynamic roles concerning students and related.
"""
from zope.interface import verify
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.settings import Allow
from zope.securitypolicy.tests.test_annotationprincipalrolemanager import (
    Test as APRMTest, Manageable)
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.app import University
from waeup.kofa.students.tests.test_browser import StudentsFullSetup
from waeup.kofa.students import Student, StudentPrincipalRoleManager

class StudentPrincipalRoleManagerTests(APRMTest):
    # Make sure our PRM behaves like a regular one for usual cases.
    # Usual cases are ones, that do not interact with external officers.
    # See next test case for functional tests including officer perms.

    def _make_roleManager(self, obj=None):
        # Overriding this method of original testcase we make sure
        # that really a Student PRM is tested.
        if obj is None:
            #obj = Manageable()
            obj = Student()
            obj['studycourse'] = Manageable()
        return StudentPrincipalRoleManager(obj)

class StudentPrincipalRoleManagerFunctionalTests(StudentsFullSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(StudentPrincipalRoleManagerFunctionalTests, self).setUp()
        # assign permissions for a virtual officers
        prm = IPrincipalRoleManager(self.app['faculties']['fac1']['dep1'])
        prm.assignRoleToPrincipal('waeup.local.ClearanceOfficer', 'alice')
        prm.assignRoleToPrincipal('waeup.local.PGClearanceOfficer', 'bob')
        prm.assignRoleToPrincipal('waeup.local.UGClearanceOfficer', 'anne')
        prm.assignRoleToPrincipal('waeup.local.LocalStudentsManager', 'benita')
        prm.assignRoleToPrincipal('waeup.local.LocalWorkflowManager', 'benita')
        return

    def test_iface(self):
        # make sure our StudentPRM really implements required ifaces.
        obj = StudentPrincipalRoleManager(self.student)
        verify.verifyClass(IPrincipalRoleManager,
                           StudentPrincipalRoleManager)
        verify.verifyObject(IPrincipalRoleManager, obj)
        return

    def test_get_as_adapter(self):
        # we can get an StudentPRM for Students by adapter lookup
        prm = IPrincipalRoleManager(self.student)
        self.assertTrue(
            isinstance(prm, StudentPrincipalRoleManager))
        return

    def test_no_officer_set(self):
        # if the faculty/dept. of the connected cert has no local
        # roles set, we won't get any additional roles for our
        # student
        prm = IPrincipalRoleManager(self.student)
        result = prm.getRolesForPrincipal('claus')
        self.assertEqual(result, [])
        return

    def test_valid_officer(self):
        # for an officer that has clearance role on the connected dept
        # we get the ClearanceOfficer role on our student
        prm = IPrincipalRoleManager(self.student)
        result = prm.getRolesForPrincipal('alice')
        self.assertEqual(result, [('waeup.StudentsClearanceOfficer', Allow)])
        # Student is a UG student
        self.assertFalse(self.student.is_postgrad)
        result = prm.getRolesForPrincipal('bob')
        self.assertEqual(result, [('waeup.StudentsOfficer', Allow)])
        result = prm.getRolesForPrincipal('anne')
        self.assertEqual(result, [('waeup.StudentsClearanceOfficer', Allow)])
        # Make student a PG student
        self.certificate.study_mode = u'pg_ft'
        self.assertTrue(self.student.is_postgrad)
        result = prm.getRolesForPrincipal('bob')
        # The dynamic roles changed
        self.assertEqual(result, [('waeup.StudentsClearanceOfficer', Allow)])
        result = prm.getRolesForPrincipal('anne')
        self.assertEqual(result, [('waeup.StudentsOfficer', Allow)])
        # Multiple roles can be assigned
        result = prm.getRolesForPrincipal('benita')
        self.assertEqual(result, [
            ('waeup.WorkflowManager', Allow),
            ('waeup.StudentsManager', Allow)
            ])
        return
