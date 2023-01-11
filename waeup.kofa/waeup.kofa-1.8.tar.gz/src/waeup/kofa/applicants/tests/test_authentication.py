## $Id: test_authentication.py 8983 2012-07-12 11:43:12Z henrik $
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
import unittest
from zope.authentication.interfaces import IAuthentication
from zope.component import provideUtility, queryUtility, getGlobalSiteManager
from zope.interface.verify import verifyClass, verifyObject
from zope.password.password import SSHAPasswordManager
from zope.password.interfaces import IPasswordManager
from zope.pluggableauth import PluggableAuthentication
from zope.securitypolicy.role import Role
from zope.securitypolicy.interfaces import IRole, Allow
from waeup.kofa.authentication import get_principal_role_manager
from waeup.kofa.interfaces import IAuthPluginUtility, IUserAccount
from waeup.kofa.applicants.authentication import (
    ApplicantsAuthenticatorSetup, ApplicantAccount)
from waeup.kofa.applicants.tests.test_browser import ApplicantsFullSetup
from waeup.kofa.testing import FunctionalLayer

class ApplicantsAuthenticatorSetupTests(unittest.TestCase):

    def test_iface(self):
        obj = ApplicantsAuthenticatorSetup()
        verifyClass(IAuthPluginUtility, ApplicantsAuthenticatorSetup)
        verifyObject(IAuthPluginUtility, obj)
        return

    def test_register(self):
        # Make sure registration works.
        setup = ApplicantsAuthenticatorSetup()
        pau = PluggableAuthentication()
        setup.register(pau)
        self.assertTrue('applicants' in pau.authenticatorPlugins)
        return

    def test_unregister(self):
        # Make sure deregistration works.
        setup = ApplicantsAuthenticatorSetup()
        pau = PluggableAuthentication()
        pau.authenticatorPlugins = ('applicants')
        setup.unregister(pau)
        self.assertTrue('applicants' not in pau.authenticatorPlugins)
        return


class FakeApplicant(object):
    applicant_id = 'test_appl'
    display_fullname = 'Tilman Gause'
    password = None
    email = None
    phone = None
    suspended = False


class MinimalPAU(PluggableAuthentication):
    def getPrincipal(self, id):
        return 'faked principal'

class ApplicantAccountTests(unittest.TestCase):

    def setUp(self):
        self.fake_stud = FakeApplicant()
        self.account = ApplicantAccount(self.fake_stud)

        # We provide a minimal PAU
        pau = MinimalPAU()
        provideUtility(pau, IAuthentication)

        # We register a role
        test_role = Role('waeup.test.Role', 'Testing Role')
        provideUtility(test_role, IRole, name='waeup.test.Role')

        # We have to setup a password manager utility manually as we
        # have no functional test. In functional tests this would
        # happen automatically, but it would take a lot more time to
        # run the tests.
        provideUtility(
            SSHAPasswordManager(), IPasswordManager, 'SSHA')
        return

    def tearDown(self):
        self.account.roles = [] # make sure roles are reset
        gsm = getGlobalSiteManager()
        to_clean = []
        # Clear up utilities registered in setUp
        to_clean.append(
            (IPasswordManager, queryUtility(
                    IPasswordManager, name='SSHA', default=None)))
        to_clean.append(
            (IAuthentication, queryUtility(IAuthentication, default=None)))
        to_clean.append(
            (IRole, queryUtility(IRole, name='test.Role', default=None)))
        for iface, elem in to_clean:
            if elem is not None:
                gsm.unregisterUtility(elem, iface)
        return

    def test_iface(self):
        verifyClass(IUserAccount, ApplicantAccount)
        verifyObject(IUserAccount, self.account)
        return

    def test_set_password(self):
        # make sure we can set a password.
        self.account.setPassword('secret')
        self.assertTrue(self.fake_stud.password is not None)
        # we do not store plaintext passwords
        self.assertTrue(self.fake_stud.password != 'secret')
        # passwords are stored as bytestream
        self.assertTrue(isinstance(self.fake_stud.password, basestring))
        self.assertFalse(isinstance(self.fake_stud.password, unicode))
        return

    def test_check_password(self):
        # make sure we can check a password.
        self.account.setPassword('secret')
        result1 = self.account.checkPassword(None)
        result2 = self.account.checkPassword('nonsense')
        result3 = self.account.checkPassword('secret')
        self.assertEqual(result1, False)
        self.assertEqual(result2, False)
        self.assertEqual(result3, True)
        return

    def test_check_unset_password(self):
        # empty and unset passwords do not match anything
        self.fake_stud.password = None
        result1 = self.account.checkPassword('')
        self.fake_stud.password = ''
        result2 = self.account.checkPassword('')
        self.assertEqual(result1, False)
        self.assertEqual(result2, False)
        return

    def test_check_password_no_string(self):
        # if passed in password is not a string, we gain no access
        self.fake_stud.password = 'secret'
        result1 = self.account.checkPassword(None)
        result2 = self.account.checkPassword(object())
        self.assertEqual(result1, False)
        self.assertEqual(result2, False)
        return

    def test_role_set(self):
        # make sure we can set roles for principals denoted by account
        prm = get_principal_role_manager()
        self.assertEqual(prm.getPrincipalsAndRoles(), [])
        self.account.roles = ['waeup.test.Role']
        self.assertEqual(
            prm.getPrincipalsAndRoles(),
            [('waeup.test.Role', 'test_appl', Allow)])
        return

    def test_role_get(self):
        # make sure we can get roles set for an account
        self.assertEqual(self.account.roles, [])
        self.account.roles = ['waeup.test.Role',] # set a role
        self.assertEqual(self.account.roles, ['waeup.test.Role'])
        return

class FunctionalApplicantAuthTests(ApplicantsFullSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(FunctionalApplicantAuthTests, self).setUp()
        return

    def tearDown(self):
        super(FunctionalApplicantAuthTests, self).tearDown()
        return
