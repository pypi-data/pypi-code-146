## $Id: test_authentication.py 15606 2019-09-24 17:21:28Z henrik $
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
from datetime import datetime, timedelta
from zope.authentication.interfaces import IAuthentication
from zope.component import provideUtility, queryUtility, getGlobalSiteManager
from zope.interface.verify import verifyClass, verifyObject
from zope.password.password import SSHAPasswordManager
from zope.password.interfaces import IPasswordManager
from zope.pluggableauth import PluggableAuthentication
from zope.security.interfaces import Unauthorized
from zope.securitypolicy.role import Role
from zope.securitypolicy.interfaces import IRole, Allow
from waeup.kofa.authentication import get_principal_role_manager
from waeup.kofa.interfaces import IAuthPluginUtility, IUserAccount
from waeup.kofa.students.authentication import (
    StudentsAuthenticatorSetup, StudentAccount)
from waeup.kofa.students.tests.test_browser import StudentsFullSetup
from waeup.kofa.testing import FunctionalLayer

class StudentsAuthenticatorSetupTests(unittest.TestCase):

    def test_iface(self):
        obj = StudentsAuthenticatorSetup()
        verifyClass(IAuthPluginUtility, StudentsAuthenticatorSetup)
        verifyObject(IAuthPluginUtility, obj)
        return

    def test_register(self):
        # Make sure registration works.
        setup = StudentsAuthenticatorSetup()
        pau = PluggableAuthentication()
        setup.register(pau)
        self.assertTrue('students' in pau.authenticatorPlugins)
        return

    def test_unregister(self):
        # Make sure deregistration works.
        setup = StudentsAuthenticatorSetup()
        pau = PluggableAuthentication()
        pau.authenticatorPlugins = ('students')
        setup.unregister(pau)
        self.assertTrue('students' not in pau.authenticatorPlugins)
        return


class FakeStudent(object):
    student_id = 'test_stud'
    display_fullname = 'Test User'
    password = None
    email = None
    phone = None
    suspended = False
    temp_password_minutes = 10

    def setTempPassword(self, user, password):
        passwordmanager = queryUtility(IPasswordManager, 'SSHA')
        self.temp_password = {}
        self.temp_password[
            'password'] = passwordmanager.encodePassword(password)
        self.temp_password['user'] = user
        self.temp_password['timestamp'] = datetime.utcnow()

    def getTempPassword(self):
        temp_password_dict = getattr(self, 'temp_password', None)
        if temp_password_dict is not None:
            delta = timedelta(minutes=self.temp_password_minutes)
            now = datetime.utcnow()
            if now < temp_password_dict.get('timestamp') + delta:
                return temp_password_dict.get('password')
            else:
                # Unset temporary password if expired
                self.temp_password = None
        return None

    def getParentsPassword(self):
        parents_password_dict = getattr(self, 'parents_password', None)
        if parents_password_dict is not None:
            delta = timedelta(minutes=self.temp_password_minutes)
            now = datetime.utcnow()
            if now < parents_password_dict.get('timestamp') + delta:
                return parents_password_dict.get('password')
            else:
                # Unset temporary password if expired
                self.parents_password = None
        return None



class MinimalPAU(PluggableAuthentication):
    def getPrincipal(self, id):
        return 'faked principal'

class StudentAccountTests(unittest.TestCase):

    def setUp(self):
        self.fake_stud = FakeStudent()
        self.account = StudentAccount(self.fake_stud)

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
        verifyClass(IUserAccount, StudentAccount)
        verifyObject(IUserAccount, self.account)
        return

    def test_set_password(self):
        # make sure we can set a password.
        self.account.setPassword('secret')
        self.assertTrue(self.fake_stud.password is not None)
        # we do not store plaintext passwords
        self.assertTrue(self.fake_stud.password != 'secret')
        # passwords are stored as bytestreams
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

    def test_check_temp_password(self):
        # make sure that, if a temp password is set,
        # this password is used for authentication
        self.account.setPassword('secret')
        self.fake_stud.setTempPassword(user='beate', password='temp_secret')
        result1 = self.account.checkPassword('secret')
        result2 = self.account.checkPassword(None)
        result3 = self.account.checkPassword('nonsense')
        result4 = self.account.checkPassword('temp_secret')
        self.assertEqual(result1, False)
        self.assertEqual(result2, False)
        self.assertEqual(result3, False)
        self.assertEqual(result4, True)
        # if the temp password is expired, the original password
        # is used again
        delta = timedelta(minutes=11)
        self.fake_stud.temp_password['timestamp'] = datetime.utcnow() - delta
        result5 = self.account.checkPassword('temp_secret')
        result6 = self.account.checkPassword('secret')
        self.assertEqual(result5, False)
        self.assertEqual(result6, True)
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
            [('waeup.test.Role', 'test_stud', Allow)])
        return

    def test_role_get(self):
        # make sure we can get roles set for an account
        self.assertEqual(self.account.roles, [])
        self.account.roles = ['waeup.test.Role',] # set a role
        self.assertEqual(self.account.roles, ['waeup.test.Role'])
        return



class FunctionalStudentAuthTests(StudentsFullSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(FunctionalStudentAuthTests, self).setUp()
        return

    def tearDown(self):
        super(FunctionalStudentAuthTests, self).tearDown()
        return

    def test_reset_protected_anonymous(self):
        # anonymous users cannot reset others passwords
        self.assertRaises(
            Unauthorized,
            self.browser.open, self.student_path + '/change_password')
        return
