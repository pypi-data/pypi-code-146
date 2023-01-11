## $Id: test_dynamicroles.py 10226 2013-05-24 17:54:10Z henrik $
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
Tests for dynamic roles concerning applicants and related.
"""
from zope.interface import verify
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.settings import Allow
from zope.securitypolicy.tests.test_annotationprincipalrolemanager import (
    Test as APRMTest, Manageable)
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.applicants.tests.test_browser import ApplicantsFullSetup
from waeup.kofa.applicants import ApplicantPrincipalRoleManager

class ApplicantPrincipalRoleManagerTests(APRMTest):
    # Make sure our PRM behaves like a regular one for usual cases.
    # Usual cases are ones, that do not interact with external officers.
    # See next test case for functional tests including officer perms.

    def _make_roleManager(self, obj=None):
        # Overriding this method of original testcase we make sure
        # that really an Applicant PRM is tested.
        if obj is None:
            obj = Manageable()
        return ApplicantPrincipalRoleManager(obj)

class ApplicantPrincipalRoleManagerFunctionalTests(ApplicantsFullSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantPrincipalRoleManagerFunctionalTests, self).setUp()
        self.applicant.course1 = self.certificate
        # assign application manage permissions for a virtual officer
        prm = IPrincipalRoleManager(self.department)
        prm.assignRoleToPrincipal('waeup.local.ApplicationsManager', 'alice')
        return

    def test_iface(self):
        # make sure out ApplicantPRM really implements required ifaces.
        obj = ApplicantPrincipalRoleManager(self.applicant)
        verify.verifyClass(IPrincipalRoleManager,
                           ApplicantPrincipalRoleManager)
        verify.verifyObject(IPrincipalRoleManager, obj)
        return

    def test_get_as_adapter(self):
        # we can get an ApplicantPRM for Applicants by adapter lookup
        prm = IPrincipalRoleManager(self.applicant)
        self.assertTrue(
            isinstance(prm, ApplicantPrincipalRoleManager))
        return

    def test_no_officer_set(self):
        # if the faculty/dept. of the connected cert has no local
        # roles set, we won't get any additional roles for our
        # applicant
        prm = IPrincipalRoleManager(self.applicant)
        result = prm.getRolesForPrincipal('bob')
        self.assertEqual(result, [])
        return

    def test_valid_officer(self):
        # for an officer that has application manage permissions
        # on the connected dept
        # we get the ApplicationsManager role on our applicant
        prm = IPrincipalRoleManager(self.applicant)
        result = prm.getRolesForPrincipal('alice')
        self.assertEqual(result, [('waeup.ApplicationsManager', Allow)])
        return
